import json
import jsonpickle
from typing import List, Any
import numpy as np
import math
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState

class Logger:
    def __init__(self) -> None:
        self.logs = ""
        self.max_log_length = 3750

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]], conversions: int, trader_data: str) -> None:
        base_length = len(
            self.to_json(
                [
                    self.compress_state(state, ""),
                    self.compress_orders(orders),
                    conversions,
                    "",
                    "",
                ]
            )
        )

        # We truncate state.traderData, trader_data, and self.logs to the same max. length to fit the log limit
        max_item_length = (self.max_log_length - base_length) // 3

        print(
            self.to_json(
                [
                    self.compress_state(state, self.truncate(state.traderData, max_item_length)),
                    self.compress_orders(orders),
                    conversions,
                    self.truncate(trader_data, max_item_length),
                    self.truncate(self.logs, max_item_length),
                ]
            )
        )

        self.logs = ""

    def compress_state(self, state: TradingState, trader_data: str) -> list[Any]:
        return [
            state.timestamp,
            trader_data,
            self.compress_listings(state.listings),
            self.compress_order_depths(state.order_depths),
            self.compress_trades(state.own_trades),
            self.compress_trades(state.market_trades),
            state.position,
            self.compress_observations(state.observations),
        ]

    def compress_listings(self, listings: dict[Symbol, Listing]) -> list[list[Any]]:
        compressed = []
        for listing in listings.values():
            compressed.append([listing.symbol, listing.product, listing.denomination])

        return compressed

    def compress_order_depths(self, order_depths: dict[Symbol, OrderDepth]) -> dict[Symbol, list[Any]]:
        compressed = {}
        for symbol, order_depth in order_depths.items():
            compressed[symbol] = [order_depth.buy_orders, order_depth.sell_orders]

        return compressed

    def compress_trades(self, trades: dict[Symbol, list[Trade]]) -> list[list[Any]]:
        compressed = []
        for arr in trades.values():
            for trade in arr:
                compressed.append(
                    [
                        trade.symbol,
                        trade.price,
                        trade.quantity,
                        trade.buyer,
                        trade.seller,
                        trade.timestamp,
                    ]
                )

        return compressed

    def compress_observations(self, observations: Observation) -> list[Any]:
        conversion_observations = {}
        for product, observation in observations.conversionObservations.items():
            conversion_observations[product] = [
                observation.bidPrice,
                observation.askPrice,
                observation.transportFees,
                observation.exportTariff,
                observation.importTariff,
                observation.sugarPrice,
                observation.sunlightIndex,
            ]

        return [observations.plainValueObservations, conversion_observations]

    def compress_orders(self, orders: dict[Symbol, list[Order]]) -> list[list[Any]]:
        compressed = []
        for arr in orders.values():
            for order in arr:
                compressed.append([order.symbol, order.price, order.quantity])

        return compressed

    def to_json(self, value: Any) -> str:
        return json.dumps(value, cls=ProsperityEncoder, separators=(",", ":"))

    def truncate(self, value: str, max_length: int) -> str:
        if len(value) <= max_length:
            return value

        return value[: max_length - 3] + "..."

logger = Logger()

class Trader:
    def __init__(self):
        self.rock = "VOLCANIC_ROCK"
        self.rock_limit = 400
        self.vouchers = {
            "VOLCANIC_ROCK_VOUCHER_9500": 9500,
            "VOLCANIC_ROCK_VOUCHER_9750": 9750,
            "VOLCANIC_ROCK_VOUCHER_10000": 10000,
            "VOLCANIC_ROCK_VOUCHER_10250": 10250,
            "VOLCANIC_ROCK_VOUCHER_10500": 10500,
        }
        self.voucher_limits = {k: 200 for k in self.vouchers}
        self.window_size = 75
        # Volatility smile fit parameters
        self.vm_a = 4.393540
        self.vm_b = 0.004045
        self.vm_c = 0.008134
        
        # TODO: tune following params
        self.threshold = 0.003
        self.volume = 30
        # Per-voucher smile bias correction
        self.v_bias = {
            "VOLCANIC_ROCK_VOUCHER_9500":  0.0000,
            "VOLCANIC_ROCK_VOUCHER_9750":  0.0000,
            "VOLCANIC_ROCK_VOUCHER_10000": -0.005,
            "VOLCANIC_ROCK_VOUCHER_10250": -0.004,
            "VOLCANIC_ROCK_VOUCHER_10500": -0.004,
        }

    def norm_cdf(self, x):
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    
    def bs_price(self, sigma, S, K, T):
        # B-S price, assume r = 0
        if T <= 0 or sigma <= 0:
            return max(S - K, 0)
            
        d1 = (math.log(S / K) + 0.5 * sigma**2 * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        return S * self.norm_cdf(d1) - K * self.norm_cdf(d2)

    def implied_volatility(self, C, S, K, T, eps=1e-6, max_iter=100):
        # binary search for implied volatility
        low = 1e-4
        high = 5.0
        for _ in range(max_iter):
            mid = (low + high) / 2
            price = self.bs_price(mid, S, K, T)
            if abs(price - C) < eps:
                return mid
            if price > C:
                high = mid
            else:
                low = mid
        return None

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        rock_history = []

        if state.traderData:
            try:
                saved = jsonpickle.decode(state.traderData)
                rock_history = saved.get("rock_history", [])
            except:
                rock_history = []

        if self.rock not in state.order_depths:
            traderData = jsonpickle.encode({"rock_history": rock_history})
            logger.flush(state, result, conversions, traderData)
            return {}, conversions, traderData

        rock_depth = state.order_depths[self.rock]
        if not rock_depth.buy_orders or not rock_depth.sell_orders:
            traderData = jsonpickle.encode({"rock_history": rock_history})
            logger.flush(state, result, conversions, traderData)
            return {}, conversions, traderData

        rock_mid = (max(rock_depth.buy_orders) + min(rock_depth.sell_orders)) / 2
        rock_history.append(rock_mid)

        if len(rock_history) <= self.window_size:
            traderData = jsonpickle.encode({"rock_history": rock_history})
            logger.flush(state, result, conversions, traderData)
            return {}, conversions, traderData
        else:
            rock_history = rock_history[-self.window_size:]

        # day = state.timestamp // 100000

        ### main loop here ###
        for voucher, strike in self.vouchers.items():
            if voucher not in state.order_depths:
                continue

            depth = state.order_depths[voucher]
            if not depth.buy_orders or not depth.sell_orders:
                continue
            
            pos = state.position.get(voucher, 0)
            limit = self.voucher_limits[voucher]
            orders = []

            best_bid = max(depth.buy_orders)
            best_ask = min(depth.sell_orders)
            voucher_mid = (best_bid + best_ask) / 2
            days_left = max(0.5, 6 - day)

            S = sum(rock_history) / len(rock_history)
            K = strike
            # T = days_left
            T = 5

            m_t = math.log(K / S) / math.sqrt(T)
            v_fit = self.vm_a * m_t**2 + self.vm_b * m_t + self.vm_c
            v_fit += self.v_bias.get(voucher, 0.0)
            iv = self.implied_volatility(voucher_mid, S, K, T)
            if iv is None:
                continue
            
            # difference between implied volatility and fitted volatility
            diff = iv - v_fit
            # voucher overvalued
            if diff > self.threshold and pos > -limit:
                volume = min(self.volume, depth.buy_orders[best_bid], pos + limit)
                if volume > 0:
                    orders.append(Order(voucher, best_bid, -volume))
            # voucher undervalued
            elif diff < -self.threshold and pos < limit:
                volume = min(self.volume, -depth.sell_orders[best_ask], limit - pos)
                if volume > 0:
                    orders.append(Order(voucher, best_ask, volume))

            if orders:
                result[voucher] = orders

        traderData = jsonpickle.encode({"rock_history": rock_history})
        logger.flush(state, result, conversions, traderData)
        return result, conversions, traderData
