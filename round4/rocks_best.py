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
        self.product = "VOLCANIC_ROCK"
        self.position_limit = 400
        self.volume = 10

        # EMA
        self.ema = None
        self.window = 50
        self.spread = 2
        self.alpha = 2 / (self.window + 1)

        # record
        self.history: List[float] = []
        self.timestamps: List[int] = []

        # slope, calculated based on some past data
        # maybe can still be tuned
        self.slope_window = 80
        self.slope_threshold = 3.0
        self.tick_interval = 100

    def run(self, state: TradingState):
        product = self.product
        orders = []

        if product not in state.order_depths:
            return {}, 0, ""

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return {}, 0, ""

        best_bid = max(order_depth.buy_orders)
        best_ask = min(order_depth.sell_orders)
        mid_price = (best_bid + best_ask) / 2
        timestamp = state.timestamp
        pos = state.position.get(product, 0)

        self.history.append(mid_price)
        self.timestamps.append(timestamp)
        if len(self.history) > 200:
            self.history = self.history[-200:]
            self.timestamps = self.timestamps[-200:]

        # EMA
        if self.ema is None:
            self.ema = mid_price
        else:
            self.ema = self.alpha * mid_price + (1 - self.alpha) * self.ema

        # slope
        slope = 0.0
        for j in range(len(self.timestamps) - 2, -1, -1):
            tick_diff = (timestamp - self.timestamps[j]) / self.tick_interval
            if tick_diff >= self.slope_window:
                slope = (mid_price - self.history[j]) / tick_diff
                break

        # extreme slope strategy
        if slope > self.slope_threshold and pos > -self.position_limit:
            orders.append(Order(product, best_bid, -self.volume))
        elif slope < -self.slope_threshold and pos < self.position_limit:
            orders.append(Order(product, best_ask, self.volume))
        
        # market making
        else:
            fair_value = int(self.ema)
            buy_price = fair_value - self.spread
            sell_price = fair_value + self.spread

            if pos < self.position_limit:
                buy_vol = min(self.volume, self.position_limit - pos)
                orders.append(Order(product, buy_price, buy_vol))
            if pos > -self.position_limit:
                sell_vol = min(self.volume, pos + self.position_limit)
                orders.append(Order(product, sell_price, -sell_vol))

        result = {product: orders}
        logger.flush(state, result, 0, "")
        return result, 0, ""
