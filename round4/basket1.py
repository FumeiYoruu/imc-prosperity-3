import json
import numpy as np
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState
import statistics
from typing import List
import math
import jsonpickle


class Logger:
    def __init__(self) -> None:
        self.logs = ""
        self.max_log_length = 3750

    def print(self, *objects, sep=" ", end="\n") -> None:
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

    def compress_state(self, state: TradingState, trader_data: str) -> list:
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

    def compress_listings(self, listings: dict) -> list:
        compressed = []
        for listing in listings.values():
            compressed.append([listing.symbol, listing.product, listing.denomination])
        return compressed

    def compress_order_depths(self, order_depths: dict) -> dict:
        compressed = {}
        for symbol, order_depth in order_depths.items():
            compressed[symbol] = [order_depth.buy_orders, order_depth.sell_orders]
        return compressed

    def compress_trades(self, trades: dict) -> list:
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

    def compress_observations(self, observations: Observation) -> list:
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

    def compress_orders(self, orders: dict) -> list:
        compressed = []
        for arr in orders.values():
            for order in arr:
                compressed.append([order.symbol, order.price, order.quantity])
        return compressed

    def to_json(self, value) -> str:
        return json.dumps(value, cls=ProsperityEncoder, separators=(",", ":"))

    def truncate(self, value: str, max_length: int) -> str:
        if len(value) <= max_length:
            return value
        return value[: max_length - 3] + "..."


logger = Logger()


class Trader:
    def __init__(self):
        self.goods = ["PICNIC_BASKET1", "CROISSANTS", "JAMS", "DJEMBES"]

        self.volume = 30  # etf
        self.position_limit = {
            "PICNIC_BASKET1": 60,
            "CROISSANTS": 250,
            "JAMS": 350,
            "DJEMBES": 60,
        }
        self.spread_history = []
        self.time_frame = 100
        self.z_score_threshold = 1

    def wmid(self, order_depths, product):
        order_depth = order_depths[product]
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())

        return (best_bid + best_ask) / 2

    def calculate_z_score(self, spread):
        if len(self.spread_history) < 2:
            return 0.0

        self.spread_history = self.spread_history[-self.time_frame:]

        mean = statistics.mean(self.spread_history)
        stdev = statistics.stdev(self.spread_history) if len(self.spread_history) >= 2 else 0.0

        return 0.0 if stdev == 0 else (spread - mean) / stdev

    def etf_b1(self, order_depths, pos, orders, buy_order_volume, sell_order_volume, prods):
        if not all(p in order_depths for p in prods):
            return orders, buy_order_volume, sell_order_volume

        depths = {p: order_depths[p] for p in prods}

        if not all(d.buy_orders and d.sell_orders for d in depths.values()):
            return {}, 0, ""

        etf_name = "PICNIC_BASKET1"

        bids = {p: max(depths[p].buy_orders) for p in prods}
        asks = {p: min(depths[p].sell_orders) for p in prods}
        mids = {p: self.wmid(order_depths, p) for p in prods}
        bid_vols = {p: depths[p].buy_orders[bids[p]] for p in prods}
        ask_vols = {p: depths[p].sell_orders[asks[p]] for p in prods}

        nav = 6 * mids["CROISSANTS"] + 3 * mids["JAMS"] + mids["DJEMBES"]
        spread = mids[etf_name] - nav
        spread_z_score = self.calculate_z_score(spread)

        self.spread_history.append(spread)

        logger.print(spread, spread_z_score, self.position_limit[etf_name])
        logger.print(bid_vols)
        logger.print(ask_vols)

        if spread > 0 and spread_z_score > self.z_score_threshold:
            vol = min(self.volume, bid_vols[etf_name], self.position_limit[etf_name] + pos.get(etf_name, 0))

            if vol > 0:
                orders.append(Order(etf_name, bids[etf_name], -vol))
                sell_order_volume[etf_name] += vol

        elif spread < 0 and spread_z_score < -self.z_score_threshold:
            vol = min(self.volume, -ask_vols[etf_name], self.position_limit[etf_name] - pos.get(etf_name, 0))

            if vol > 0:
                orders.append(Order(etf_name, asks[etf_name], vol))
                buy_order_volume[etf_name] += vol

        return orders, buy_order_volume, sell_order_volume

    def run(self, state: TradingState):
        traderObject = {}
        if state.traderData is not None and state.traderData != "":
            traderObject = jsonpickle.decode(state.traderData)

        orders = []
        buy_order_volume = {}
        sell_order_volume = {}
        prods = ["PICNIC_BASKET1", "CROISSANTS", "JAMS", "DJEMBES"]

        for p in self.goods:
            buy_order_volume[p] = 0
            sell_order_volume[p] = 0

        orders, buy_order_volume, sell_order_volume = self.etf_b1(state.order_depths, state.position, orders,
                                                                  buy_order_volume, sell_order_volume, prods)
        result = {}
        for o in orders:
            result.setdefault(o.symbol, []).append(o)
        traderData = jsonpickle.encode(traderObject)
        logger.flush(state, result, 0, traderData)
        return result, 0, traderData
