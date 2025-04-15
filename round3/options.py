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
        self.voucher_limits = {
            "VOLCANIC_ROCK_VOUCHER_9500": 200,
            "VOLCANIC_ROCK_VOUCHER_9750": 200,
            "VOLCANIC_ROCK_VOUCHER_10000": 200,
            "VOLCANIC_ROCK_VOUCHER_10250": 200,
            "VOLCANIC_ROCK_VOUCHER_10500": 200,
        }
        # TODO: parameters not tuned
        self.window_size = 75
        self.threshold = 10
        self.volume = 40 # change to 40

    # estimate cdf of normal distribution
    def norm_cdf(self, x):
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    
    # calculate fair value using Black-Scholes
    def calculate_fair_value(self, rock_prices, strike, days_left):
        if len(rock_prices) < self.window_size:
            return max(0.0, rock_prices[-1] - strike)

        ma_rock = np.mean(rock_prices[-self.window_size:])
        log_returns = np.diff(np.log(rock_prices))
        sigma = np.std(log_returns)
        T = days_left

        if T == 0 or sigma == 0:
            return max(0.0, ma_rock - strike)

        d1 = (math.log(ma_rock / strike) + 0.5 * sigma ** 2 * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        return ma_rock * self.norm_cdf(d1) - strike * self.norm_cdf(d2)

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

        rock_pos = state.position.get(self.rock, 0)
        rock_limit = self.rock_limit
        rock_mid = (max(rock_depth.buy_orders) + min(rock_depth.sell_orders)) / 2
        rock_history.append(rock_mid)

        if len(rock_history) <= self.window_size:
            traderData = jsonpickle.encode({"rock_history": rock_history})
            logger.flush(state, result, conversions, traderData)
            return {}, conversions, traderData
        else:
            rock_history = rock_history[-self.window_size:]

        day = state.timestamp // 100000

        for voucher, strike in self.vouchers.items():
            voucher_orders = []

            if voucher not in state.order_depths:
                continue

            voucher_depth = state.order_depths[voucher]
            if not voucher_depth.buy_orders or not voucher_depth.sell_orders:
                continue
            
            best_bid = max(voucher_depth.buy_orders)
            best_ask = min(voucher_depth.sell_orders)
            voucher_mid = (best_bid + best_ask) / 2
            days_left = max(0, 6 - day)

            fair_value = self.calculate_fair_value(rock_history, strike, days_left)
            diff = voucher_mid - fair_value

            pos = state.position.get(voucher, 0)
            limit = self.voucher_limits[voucher]
            
            if diff < -self.threshold and pos < limit: # long vouchers
                ask_volume = -voucher_depth.sell_orders[best_ask]
                volume = min(self.volume, ask_volume, limit - pos)
                if volume > 0:
                    voucher_orders.append(Order(voucher, best_ask, volume))
            elif diff > self.threshold and pos > -limit: # short vouchers
                bid_volume = voucher_depth.buy_orders[best_bid]
                volume = min(self.volume, bid_volume, pos + limit)
                if volume > 0:
                    voucher_orders.append(Order(voucher, best_bid, -volume))

            if voucher_orders:
                result[voucher] = voucher_orders
        
        traderData = jsonpickle.encode({"rock_history": rock_history})
        logger.flush(state, result, conversions, traderData)
        return result, conversions, traderData
