import json
from typing import List, Any
import jsonpickle
import statistics
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
        self.product = "DJEMBES"
        self.position_limit = 60
        
        self.window_size = 20
        self.threshold = 9.5
        self.volume = 20

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        price_history = []
        orders = []

        if state.traderData:
            try:
                saved = jsonpickle.decode(state.traderData)
                price_history = saved.get("price_history", [])
            except:
                price_history = []
        
        if self.product not in state.order_depths:
            traderData = jsonpickle.encode({"price_history": price_history})
            logger.flush(state, result, conversions, traderData)
            return {}, conversions, traderData

        order_depth = state.order_depths[self.product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            traderData = jsonpickle.encode({"price_history": price_history})
            logger.flush(state, result, conversions, traderData)
            return {}, conversions, traderData

        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid_price = (best_bid + best_ask) / 2
        price_history.append(mid_price)

        if len(price_history) <= self.window_size:
            traderData = jsonpickle.encode({"price_history": price_history})
            logger.flush(state, result, conversions, traderData)
            return {}, conversions, traderData
        else:
            price_history = price_history[-self.window_size:]

        momentum = price_history[-1] - price_history[-self.window_size]
        pos = state.position.get(self.product, 0)

        if momentum > self.threshold and pos < self.position_limit:
            ask_volume = -order_depth.sell_orders[best_ask]
            volume = min(self.volume, ask_volume, self.position_limit - pos)
            if volume > 0:
                orders.append(Order(self.product, best_ask, volume))
        elif momentum < -self.threshold and pos > -self.position_limit:
            bid_volume = order_depth.buy_orders[best_bid]
            volume = min(self.volume, bid_volume, pos + self.position_limit)
            if volume > 0:
                orders.append(Order(self.product, best_bid, -volume))

        if orders:
            result[self.product] = orders
        
        traderData = jsonpickle.encode({"price_history": price_history})
        logger.flush(state, result, conversions, traderData)
        return result, conversions, traderData
