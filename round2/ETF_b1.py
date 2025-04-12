import json
import numpy as np
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState

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
        self.volume = 10
        self.threshold = 1.0
        self.position_limit = {
            "PICNIC_BASKET1": 60,
            "CROISSANTS": 250,
            "JAMS": 350,
            "DJEMBES": 60
        }

    def run(self, state: TradingState):
        orders = []

        prods = ["PICNIC_BASKET1", "CROISSANTS", "JAMS", "DJEMBES"]
        if not all(p in state.order_depths for p in prods):
            return {}, 0, ""

        depths = {p: state.order_depths[p] for p in prods}
        if not all(d.buy_orders and d.sell_orders for d in depths.values()):
            return {}, 0, ""

        bids = {p: max(depths[p].buy_orders) for p in prods}
        asks = {p: min(depths[p].sell_orders) for p in prods}
        mids = {p: (bids[p] + asks[p]) / 2 for p in prods}
        bid_vols = {p: depths[p].buy_orders[bids[p]] for p in prods}
        ask_vols = {p: depths[p].sell_orders[asks[p]] for p in prods}
        pos = state.position

        # TODO: check whether to change the method for calculating nav
        nav = 6 * mids["CROISSANTS"] + 3 * mids["JAMS"] + mids["DJEMBES"]
        spread = mids["PICNIC_BASKET1"] - nav
        v = self.volume


        # TODO: tune self.volume & self.threshold
        if spread > self.threshold:
            vol = min(v, bid_vols["PICNIC_BASKET1"], self.position_limit["PICNIC_BASKET1"] + pos.get("PICNIC_BASKET1", 0))
            if vol > 0:
                orders.append(Order("PICNIC_BASKET1", bids["PICNIC_BASKET1"], -vol))
            for prod, nums in [("CROISSANTS", 6), ("JAMS", 3), ("DJEMBES", 1)]:
                vol = min(nums * v, abs(ask_vols[prod]), self.position_limit[prod] - pos.get(prod, 0))
                if vol > 0:
                    orders.append(Order(prod, asks[prod], vol))

        elif spread < -self.threshold:
            vol = min(v, abs(ask_vols["PICNIC_BASKET1"]), self.position_limit["PICNIC_BASKET1"] - pos.get("PICNIC_BASKET1", 0))
            if vol > 0:
                orders.append(Order("PICNIC_BASKET1", asks["PICNIC_BASKET1"], vol))
            for prod, nums in [("CROISSANTS", 6), ("JAMS", 3), ("DJEMBES", 1)]:
                vol = min(nums * v, bid_vols[prod], self.position_limit[prod] + pos.get(prod, 0))
                if vol > 0:
                    orders.append(Order(prod, bids[prod], -vol))

        result = {}
        for o in orders:
            result.setdefault(o.symbol, []).append(o)

        logger.flush(state, result, 0, "")
        return result, 0, ""
