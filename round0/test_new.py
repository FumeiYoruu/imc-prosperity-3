import json
from typing import List, Any
import string
import statistics

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
        self.threshold = 0.8
        self.quote_volume = 10
        self.sma_window = 25

        self.position_limit = 50
        self.price_history = []
        self.current_position = 0

    def run(self, state: TradingState):
        result = {}
        product = 'RAINFOREST_RESIN'
        orders: List[Order] = []

        order_depth = state.order_depths[product]
        if product in state.position:
            self.current_position = state.position[product]

        # acceptable price
        if order_depth.buy_orders and order_depth.sell_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_ask = min(order_depth.sell_orders.keys())
            mid_price = (best_bid + best_ask) / 2
            self.price_history.append(mid_price)
            acceptable_price = statistics.mean(self.price_history[-self.sma_window:])
        else:
            acceptable_price = self.price_history[-1] if self.price_history else 10

        # TAKER BUY
        if order_depth.sell_orders:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_volume = order_depth.sell_orders[best_ask]
            if best_ask < acceptable_price - self.threshold:
                buy_amount = min(-best_ask_volume, self.position_limit - self.current_position)
                if buy_amount > 0:
                    orders.append(Order(product, best_ask, buy_amount))
                    self.current_position += buy_amount

        # TAKER SELL
        if order_depth.buy_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_volume = order_depth.buy_orders[best_bid]
            if best_bid > acceptable_price + self.threshold:
                sell_amount = min(best_bid_volume, self.position_limit + self.current_position)
                if sell_amount > 0:
                    orders.append(Order(product, best_bid, -sell_amount))
                    self.current_position -= sell_amount

        # MAKER
        if not orders and order_depth.buy_orders and order_depth.sell_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_ask = min(order_depth.sell_orders.keys())

            if self.current_position < self.position_limit:
                buy_price = best_bid + 1
                buy_amount = min(self.quote_volume, self.position_limit - self.current_position)
                orders.append(Order(product, buy_price, buy_amount))

            if self.current_position > -self.position_limit:
                sell_price = best_ask - 1
                sell_amount = min(self.quote_volume, self.position_limit + self.current_position)
                orders.append(Order(product, sell_price, -sell_amount))

        result[product] = orders
        conversions = 0
        traderData = ""
        logger.flush(state, result, conversions, traderData)
        return result, conversions, traderData
