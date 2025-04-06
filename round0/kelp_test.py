import json
import statistics
from typing import List, Any
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState
import math


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
        self.remaining_time = 0

        # parameters
        self.position_limit = 50
        self.time_frame = 500
        self.alpha = 0.5
        self.beta = 1 - self.alpha
        self.momentum_threshold = 1
        self.time_threshold = 5

    def run(self, state: TradingState):
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
        else:
            # TODO: Decide what to do here
            assert False, "price calculation failed"

        if self.price_history:
            t_price_change = t_price - self.price_history[-1]
            t_mean_price = statistics.mean(self.price_history[-self.time_frame:])
        else:
            t_price_change = 0
            t_mean_price = 0
            # TODO: Decide what to do here
            # assert False, "no price history"

        momentum = self.alpha * (t_price - t_mean_price) + self.beta * t_price_change

        average_gain, average_loss = 0, 0
        gain_count, loss_count = 0, 0

        for i in range(max(0, len(self.price_history) - self.time_frame), len(self.price_history) - 1):
            price_change = self.price_history[i + 1] - self.price_history[i]

            if(price_change > 0):
                average_gain += price_change
                gain_count += 1
            elif(price_change < 0):
                average_loss += abs(price_change)
                loss_count += 1

        if gain_count:
            average_gain /= gain_count
        if loss_count:
            average_loss /= loss_count

        # TODO: what if average_loss = 0?
        # relative_strength = average_gain / average_loss
        if(average_loss == 0):
            relative_strength = math.inf
        else:
            relative_strength = average_gain / average_loss

        relative_strength_index = 100 - 100 / (1 + relative_strength)

        if self.current_position != 0:
            self.remaining_time -= 1

            if self.current_position > 0 and (momentum <= 0 or relative_strength_index < 50 or self.remaining_time <= 0):
                orders.append(Order(product, best_ask, -self.current_position))
            elif self.current_position < 0 and (momentum >= 0 or relative_strength_index > 50 or self.remaining_time <= 0):
                orders.append(Order(product, best_bid, -self.current_position))
        else:
            if momentum > 0 and relative_strength_index < 70:
                count = self.position_limit * min(1, abs(momentum // self.momentum_threshold))
                if count > 0:
                    orders.append(Order(product, best_bid, count))

                    self.remaining_time = self.time_threshold
            elif momentum < 0 and relative_strength_index > 30:
                count = self.position_limit * min(1, abs(momentum // self.momentum_threshold))
                if count > 0:
                    orders.append(Order(product, best_ask, -count))

                    self.remaining_time = self.time_threshold

        self.price_history.append(t_price)

        result[product] = orders
        conversions = 0
        trader_data = ""
        logger.flush(state, result, conversions, trader_data)
        return result, conversions, trader_data