import json
import statistics
from typing import List, Any
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState
import math
import jsonpickle


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
        self.current_position = 0
        self.price_history = []
        self.return_history = []
        self.remaining_time = 0
        self.position_wanted = 0
        self.spread_history = []

        # parameters
        self.position_limit = 50
        self.time_frame = 200
        self.z_score_threshold = 0.5
        self.time_threshold = 100

    def encode_trader_data(self):
        data_dict = {
            'price_history': self.price_history,
            'return_history': self.return_history,
            'remaining_time': self.remaining_time,
            'position_wanted': self.position_wanted
        }
        return jsonpickle.encode(data_dict)

    def decode_trader_data(self, data):
        if not data:
            return
        data_dict = jsonpickle.decode(data)
        self.price_history = data_dict['price_history']
        self.return_history = data_dict['return_history']
        self.remaining_time = data_dict['remaining_time']
        self.position_wanted = data_dict['position_wanted']

    def run(self, state: TradingState):
        #self.decode_trader_data(state.traderData)
        result = {}
        product = "KELP"
        orders: List[Order] = []

        order_depth = state.order_depths[product]

        if product in state.position:
            self.current_position = state.position[product]

        if order_depth.buy_orders and order_depth.sell_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_ask = min(order_depth.sell_orders.keys())
            t_price = (best_bid + best_ask) / 2
            spread = abs(best_ask - best_bid)
        else:
            return {}, 0, ""  # Exit early if no data to trade on

        if self.price_history:
            t_return = (t_price - self.price_history[-1]) * 1000 / self.price_history[-1]
            self.return_history.append(t_return)
        else:
            t_return = 0
            self.return_history.append(0)

        if len(self.return_history) >= self.time_frame:
            mean_return = statistics.mean(self.return_history[-self.time_frame:])
            std_return = statistics.stdev(self.return_history[-self.time_frame:])
            z_score = (t_return - mean_return) / std_return if std_return != 0 else 0
        else:
            mean_return = 0
            std_return = 1
            z_score = 0

        if self.spread_history:
            t_mean_spread = statistics.mean(self.spread_history[-self.time_frame:])
        else:
            t_mean_spread = spread

        logger.print(f"Return: {t_return:.4f}, Z-Score: {z_score:.2f}, Mean Return: {mean_return:.4f}, Std Return: {std_return:.4f}")

        self.remaining_time -= 1

        if self.current_position > 0 and (z_score >= 0.5):
            self.position_wanted = 0
        elif self.current_position < 0 and (z_score <= -0.5 ):
            self.position_wanted = 0
        if z_score < -self.z_score_threshold:
            self.position_wanted = self.position_limit
            self.remaining_time = self.time_threshold
        elif z_score > self.z_score_threshold:
            self.position_wanted = -self.position_limit
            self.remaining_time = self.time_threshold

        position_diff = self.position_wanted - self.current_position

        if position_diff > 0:
            #if self.position_wanted == 0:
                #orders.append(Order(product, round(best_ask - t_mean_spread), position_diff))
            #else:
                orders.append(Order(product, best_bid + 1, position_diff))
        elif position_diff < 0:
            #if self.position_wanted == 0:
                #orders.append(Order(product, round(best_bid + t_mean_spread), position_diff))
            #else:
                orders.append(Order(product, best_ask - 1, position_diff))

        #self.current_position = self.position_wanted
        self.price_history.append(t_price)
        self.spread_history.append(spread)
        #trader_data = self.encode_trader_data()
        result[product] = orders
        conversions = 0
        trader_data = ""
        logger.flush(state, result, conversions, trader_data)
        return result, conversions, trader_data

