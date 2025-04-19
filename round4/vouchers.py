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
        self.products = {
            "VOLCANIC_ROCK_VOUCHER_9500":  {"strike": 9500,  "volume": 20, "window": 50, "spread": 10},
            "VOLCANIC_ROCK_VOUCHER_9750":  {"strike": 9750,  "volume": 20, "window": 50, "spread": 10},
            "VOLCANIC_ROCK_VOUCHER_10000": {"strike": 10000, "volume": 20, "window": 50, "spread": 10},
            "VOLCANIC_ROCK_VOUCHER_10250": {"strike": 10250, "volume": 20, "window": 50, "spread": 10},
            "VOLCANIC_ROCK_VOUCHER_10500": {"strike": 10500, "volume": 20, "window": 50, "spread": 5},
        }

        self.voucher_limit = 200
        self.histories = {k: [] for k in self.products}

    def run(self, state: TradingState):
        result = {k: [] for k in self.products}

        for voucher, config in self.products.items():
            if voucher not in state.order_depths:
                continue

            depth = state.order_depths[voucher]
            if not depth.buy_orders or not depth.sell_orders:
                continue

            best_bid = max(depth.buy_orders)
            best_ask = min(depth.sell_orders)
            mid = (best_bid + best_ask) / 2
            self.histories[voucher].append(mid)

            if len(self.histories[voucher]) > 120:
                self.histories[voucher] = self.histories[voucher][-120:]

            window = config["window"]
            fair_value = int(sum(self.histories[voucher][-window:]) / window)
            pos = state.position.get(voucher, 0)
            limit = self.voucher_limit

            # buy
            if pos < limit:
                buy_price = fair_value - config["spread"]
                volume = min(config["volume"], limit - pos)
                result[voucher].append(Order(voucher, buy_price, volume))

            # sell
            if pos > -limit:
                sell_price = fair_value + config["spread"]
                volume = min(config["volume"], pos + limit)
                result[voucher].append(Order(voucher, sell_price, -volume))

        logger.flush(state, result, 0, "")
        return result, 0, ""
