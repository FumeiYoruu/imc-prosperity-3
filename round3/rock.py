import json
from typing import List, Any
import jsonpickle
import numpy as np
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
        self.vouchers = {
            "VOLCANIC_ROCK_VOUCHER_9500": 9500,
            "VOLCANIC_ROCK_VOUCHER_9750": 9750,
            "VOLCANIC_ROCK_VOUCHER_10000": 10000,
            "VOLCANIC_ROCK_VOUCHER_10250": 10250,
            "VOLCANIC_ROCK_VOUCHER_10500": 10500,
        }
        self.threshold = 3
        self.volume_per_trade = 3
        self.position_limit = 100

    def calculate_fair_value(self, rock_prices: list[float], strike: float, days_left: int, lambda_decay=0.9) -> float:
        if not rock_prices:
            return 0.0
        weights = np.array([lambda_decay**i for i in reversed(range(len(rock_prices)))])
        ema_rock = np.dot(weights, rock_prices) / weights.sum()
        time_discount = 1 - np.exp(-days_left / 2.0)
        return (ema_rock - strike) * time_discount

    def run(self, state: TradingState):
        orders = {}
        conversions = 0
        day = state.timestamp // 100000
        rock_price_history = []
        if state.traderData:
            try:
                saved = jsonpickle.decode(state.traderData)
                rock_price_history = saved.get("rock_price_history", [])
            except:
                rock_price_history = []

        if self.rock not in state.order_depths:
            logger.flush(state, orders, conversions, jsonpickle.encode({"rock_price_history": rock_price_history}))
            return {}, conversions, jsonpickle.encode({"rock_price_history": rock_price_history})
        rock_depth = state.order_depths[self.rock]
        if not rock_depth.buy_orders or not rock_depth.sell_orders:
            logger.flush(state, orders, conversions, jsonpickle.encode({"rock_price_history": rock_price_history}))
            return {}, conversions, jsonpickle.encode({"rock_price_history": rock_price_history})

        rock_mid = (max(rock_depth.buy_orders) + min(rock_depth.sell_orders)) / 2
        rock_pos = state.position.get(self.rock, 0)
        rock_price_history.append(rock_mid)
        if len(rock_price_history) > 50:
            rock_price_history = rock_price_history[-50:]

        for voucher, strike in self.vouchers.items():
            if voucher not in state.order_depths:
                continue
            depth = state.order_depths[voucher]
            if not depth.buy_orders or not depth.sell_orders:
                continue

            bid = max(depth.buy_orders)
            ask = min(depth.sell_orders)
            vmid = (bid + ask) / 2
            pos = state.position.get(voucher, 0)
            voucher_orders = []

            days_left = max(0, 6 - day)
            fair_value = self.calculate_fair_value(rock_price_history, strike, days_left)
            diff = vmid - fair_value

            if diff > self.threshold:
                volume = min(self.volume_per_trade, pos + self.position_limit, self.position_limit - rock_pos)
                if volume > 0:
                    voucher_orders.append(Order(voucher, bid, -volume))
                    orders.setdefault(self.rock, []).append(Order(self.rock, max(rock_depth.buy_orders), volume))

            elif diff < -self.threshold:
                volume = min(self.volume_per_trade, self.position_limit - pos, rock_pos + self.position_limit)
                if volume > 0:
                    voucher_orders.append(Order(voucher, ask, volume))
                    orders.setdefault(self.rock, []).append(Order(self.rock, min(rock_depth.sell_orders), -volume))

            if voucher_orders:
                orders[voucher] = voucher_orders

        traderData = jsonpickle.encode({"rock_price_history": rock_price_history})
        logger.flush(state, orders, conversions, traderData)
        return orders, conversions, traderData
