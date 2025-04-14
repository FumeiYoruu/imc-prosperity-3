import json
import jsonpickle
import numpy as np
from typing import List, Any
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState

class Logger:
    def __init__(self) -> None:
        self.logs = ""
        self.max_log_length = 3750

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]], conversions: int, trader_data: str) -> None:
        base_length = len(
            self.to_json([self.compress_state(state, ""), self.compress_orders(orders), conversions, "", ""])
        )
        max_item_length = (self.max_log_length - base_length) // 3
        print(self.to_json([
            self.compress_state(state, self.truncate(state.traderData, max_item_length)),
            self.compress_orders(orders),
            conversions,
            self.truncate(trader_data, max_item_length),
            self.truncate(self.logs, max_item_length),
        ]))
        self.logs = ""

    def compress_state(self, state: TradingState, trader_data: str) -> list[Any]:
        return [
            state.timestamp, trader_data,
            [[l.symbol, l.product, l.denomination] for l in state.listings.values()],
            {s: [d.buy_orders, d.sell_orders] for s, d in state.order_depths.items()},
            [[t.symbol, t.price, t.quantity, t.buyer, t.seller, t.timestamp] for trades in state.own_trades.values() for t in trades],
            [[t.symbol, t.price, t.quantity, t.buyer, t.seller, t.timestamp] for trades in state.market_trades.values() for t in trades],
            state.position,
            [state.observations.plainValueObservations, {
                p: [o.bidPrice, o.askPrice, o.transportFees, o.exportTariff, o.importTariff, o.sugarPrice, o.sunlightIndex]
                for p, o in state.observations.conversionObservations.items()
            }]
        ]

    def compress_orders(self, orders: dict[Symbol, list[Order]]) -> list[list[Any]]:
        return [[o.symbol, o.price, o.quantity] for ol in orders.values() for o in ol]

    def to_json(self, value: Any) -> str:
        return json.dumps(value, cls=ProsperityEncoder, separators=(",", ":"))

    def truncate(self, value: str, max_length: int) -> str:
        return value if len(value) <= max_length else value[:max_length - 3] + "..."

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
        self.position_limits = {
            "VOLCANIC_ROCK": 400,
            "VOLCANIC_ROCK_VOUCHER_9500": 200,
            "VOLCANIC_ROCK_VOUCHER_9750": 200,
            "VOLCANIC_ROCK_VOUCHER_10000": 200,
            "VOLCANIC_ROCK_VOUCHER_10250": 200,
            "VOLCANIC_ROCK_VOUCHER_10500": 200,
        }

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
            traderData = jsonpickle.encode({"rock_price_history": rock_price_history})
            logger.flush(state, orders, conversions, traderData)
            return {}, conversions, traderData

        rock_depth = state.order_depths[self.rock]
        if not rock_depth.buy_orders or not rock_depth.sell_orders:
            traderData = jsonpickle.encode({"rock_price_history": rock_price_history})
            logger.flush(state, orders, conversions, traderData)
            return {}, conversions, traderData

        rock_mid = (max(rock_depth.buy_orders) + min(rock_depth.sell_orders)) / 2
        rock_pos = state.position.get(self.rock, 0)
        rock_limit = self.position_limits[self.rock]
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
            limit = self.position_limits[voucher]
            voucher_orders = []

            days_left = max(0, 6 - day)
            fair_value = self.calculate_fair_value(rock_price_history, strike, days_left)
            diff = vmid - fair_value
            if diff > self.threshold:
                volume = min(self.volume_per_trade, pos + limit, rock_limit - rock_pos)
                if volume > 0:
                    voucher_orders.append(Order(voucher, bid, -volume))
                    orders.setdefault(self.rock, []).append(Order(self.rock, max(rock_depth.buy_orders), volume))
            elif diff < -self.threshold:
                volume = min(self.volume_per_trade, limit - pos, rock_pos + rock_limit)
                if volume > 0:
                    voucher_orders.append(Order(voucher, ask, volume))
                    orders.setdefault(self.rock, []).append(Order(self.rock, min(rock_depth.sell_orders), -volume))

            if voucher_orders:
                orders[voucher] = voucher_orders

        traderData = jsonpickle.encode({"rock_price_history": rock_price_history})
        logger.flush(state, orders, conversions, traderData)
        return orders, conversions, traderData
