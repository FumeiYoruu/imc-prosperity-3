import json
from typing import Any
import numpy as np
from datamodel import *

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
            "VOLCANIC_ROCK_VOUCHER_9500":  {"strike": 9500,  "volume": 30, "window": 50, "spread": 4},
            "VOLCANIC_ROCK_VOUCHER_9750":  {"strike": 9750,  "volume": 30, "window": 50, "spread": 4},
            "VOLCANIC_ROCK_VOUCHER_10000": {"strike": 10000, "volume": 30, "window": 50, "spread": 4},
            "VOLCANIC_ROCK_VOUCHER_10250": {"strike": 10250, "volume": 10, "window": 50, "spread": 4},
            "VOLCANIC_ROCK_VOUCHER_10500": {"strike": 10500, "volume": 10, "window": 20, "spread": 3},
        }

        self.limit = 200
        self.history = {k: [] for k in self.products}
        
        # TODO: whether use SMA instead of EMA
        self.ema = {k: None for k in self.products}
        self.alpha = {k: 2 / (cfg["window"] + 1) for k, cfg in self.products.items()}
        
        # TODO: tune this; should be able to calculate based on past data, but estimated value is 3 ~ 8
        self.z_threshold = 5.20

    def run(self, state: TradingState):
        result = {}

        for symbol, cfg in self.products.items():
            orders = []
            pos = state.position.get(symbol, 0)
            od = state.order_depths.get(symbol)
            if not od or not od.buy_orders or not od.sell_orders:
                continue

            vol = cfg["volume"]
            spread = cfg["spread"]
            
            best_bid = max(od.buy_orders)
            best_ask = min(od.sell_orders)
            mid = (best_bid + best_ask) / 2
            self.history[symbol].append(mid)
            if len(self.history[symbol]) > 200:
                self.history[symbol].pop(0)

            # EMA
            a = self.alpha[symbol]
            prev_ema = self.ema[symbol]
            ema = mid if prev_ema is None else (a * mid + (1 - a) * prev_ema)
            self.ema[symbol] = ema

            # Z-score
            hist_window = self.history[symbol][-cfg["window"]:]
            std = np.std(hist_window) if len(hist_window) >= 2 else 1e-6
            z = (mid - ema) / std if std > 1e-6 else 0

            # market making
            if abs(z) < self.z_threshold:
                fv = int(ema)
                if pos < self.limit:
                    orders.append(Order(symbol, fv - spread, min(vol, self.limit - pos)))
                if pos > -self.limit:
                    orders.append(Order(symbol, fv + spread, -min(vol, pos + self.limit)))

            # trend up, cover short & make long
            elif z >= self.z_threshold:
                if pos < 0:
                    # TODO: whether use best_ask instead for faster execution
                    orders.append(Order(symbol, best_bid, min(vol, -pos)))
                if pos < self.limit:
                    orders.append(Order(symbol, best_ask, min(vol, self.limit - pos)))

            # trend down, cover long & make short
            elif z <= -self.z_threshold:
                if pos > 0:
                    # TODO: whether use best_bid instead for faster execution
                    orders.append(Order(symbol, best_ask, -min(vol, pos)))
                if pos > -self.limit:
                    orders.append(Order(symbol, best_bid, -min(vol, pos + self.limit)))

            result[symbol] = orders

        logger.flush(state, result, 0, "")
        return result, 0, ""
