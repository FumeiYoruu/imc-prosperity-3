import json
import numpy as np
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState
import statistics
from typing import List

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
        self.b1_weights = {
            'CROISSANTS' : 6,
            'JAMS' : 3,
            'DJEMBES' : 1,
        }
        self.spread_history = []
        self.time_frame = 100
        self.z_score_threshold = 0.5

    def take_best_orders(
        self,
        product: str,
        fair_value: int,
        take_width: float,
        orders: List[Order],
        order_depth: OrderDepth,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
        prevent_adverse: bool = False,
        adverse_volume: int = 0,
    ):
        position_limit = self.LIMIT[product]

        if len(order_depth.sell_orders) != 0:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_amount = -1 * order_depth.sell_orders[best_ask]

            if not prevent_adverse or abs(best_ask_amount) <= adverse_volume:
                if best_ask <= fair_value - take_width:
                    quantity = min(
                        best_ask_amount, position_limit - position
                    )  # max amt to buy
                    if quantity > 0:
                        orders.append(Order(product, best_ask, quantity))
                        buy_order_volume += quantity
                        order_depth.sell_orders[best_ask] += quantity
                        if order_depth.sell_orders[best_ask] == 0:
                            del order_depth.sell_orders[best_ask]

        if len(order_depth.buy_orders) != 0:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_amount = order_depth.buy_orders[best_bid]

            if not prevent_adverse or abs(best_bid_amount) <= adverse_volume:
                if best_bid >= fair_value + take_width:
                    quantity = min(
                        best_bid_amount, position_limit + position
                    )  # should be the max we can sell
                    if quantity > 0:
                        orders.append(Order(product, best_bid, -1 * quantity))
                        sell_order_volume += quantity
                        order_depth.buy_orders[best_bid] -= quantity
                        if order_depth.buy_orders[best_bid] == 0:
                            del order_depth.buy_orders[best_bid]

        return buy_order_volume, sell_order_volume

    def market_make(
            
        self,
        product: str,
        orders: List[Order],
        bid: int,
        ask: int,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ):
        buy_quantity = self.LIMIT[product] - (position + buy_order_volume)
        if buy_quantity > 0:
            orders.append(Order(product, round(bid), buy_quantity))  # Buy order

        sell_quantity = self.LIMIT[product] + (position - sell_order_volume)
        if sell_quantity > 0:
            orders.append(Order(product, round(ask), -sell_quantity))  # Sell order
        return buy_order_volume, sell_order_volume

    def take_orders(
        self,
        product: str,
        order_depth: OrderDepth,
        fair_value: float,
        take_width: float,
        position: int,
        
        prevent_adverse: bool = False,
        adverse_volume: int = 0,
    ) -> (List[Order], int, int):
        orders: List[Order] = []
        buy_order_volume = 0
        sell_order_volume = 0

        buy_order_volume, sell_order_volume = self.take_best_orders(
            product,
            fair_value,
            take_width,
            orders,
            order_depth,
            position,
            buy_order_volume,
            sell_order_volume,
            prevent_adverse,
            adverse_volume,
        )
        return orders, buy_order_volume, sell_order_volume
    
    def make_orders(
            

            
        self,
        product,
        order_depth: OrderDepth,
        fair_value: float,
        position: int,
        buy_order_volume,
        sell_order_volume,
        disregard_edge: float,  # disregard trades within this edge for pennying or joining
        join_edge: float,  # join trades within this edge
        default_edge: float,  # default edge to request if there are no levels to penny or join
        manage_position: bool = False,
        soft_position_limit: int = 0,
        # will penny all other levels with higher edge
    ):
        orders: List[Order] = []
        asks_above_fair = [
            price
            for price in order_depth.sell_orders.keys()
            if price > fair_value + disregard_edge
        ]
        bids_below_fair = [
            price
            for price in order_depth.buy_orders.keys()
            if price < fair_value - disregard_edge
        ]

        best_ask_above_fair = min(asks_above_fair) if len(asks_above_fair) > 0 else None
        best_bid_below_fair = max(bids_below_fair) if len(bids_below_fair) > 0 else None

        ask = round(fair_value + default_edge)
        if best_ask_above_fair != None:
            if abs(best_ask_above_fair - fair_value) <= join_edge:
                ask = best_ask_above_fair  # join
            else:
                ask = best_ask_above_fair - 1  # penny

        bid = round(fair_value - default_edge)
        if best_bid_below_fair != None:
            if abs(fair_value - best_bid_below_fair) <= join_edge:
                bid = best_bid_below_fair
            else:
                bid = best_bid_below_fair + 1

        if manage_position:
            if position > soft_position_limit:
                ask -= 1
            elif position < -1 * soft_position_limit:
                bid += 1

        buy_order_volume, sell_order_volume = self.market_make(
            product,
            orders,
            bid,
            ask,
            position,
            buy_order_volume,
            sell_order_volume,
        )

        return orders, buy_order_volume, sell_order_volume
    
    def implied_basket_volume(self, order_depths, pos, basket_weights, prods):
        depths = {p: order_depths[p] for p in prods}
        if not all(d.buy_orders and d.sell_orders for d in depths.values()):
            return {}, 0, ""

        bids = {p: max(depths[p].buy_orders) for p in prods}
        asks = {p: min(depths[p].sell_orders) for p in prods}
        mids = {p: (bids[p] + asks[p]) / 2 for p in prods}
        bid_vols = {p: depths[p].buy_orders[bids[p]] for p in prods}
        ask_vols = {p: depths[p].sell_orders[asks[p]] for p in prods}
        buy_volume = 10000
        for p in basket_weights.keys():
            

        return buy_volume, sell_volume

    def etf_b1(self, order_depths, pos, orders, buy_order_volume, sell_order_volume, prods):
        depths = {p: order_depths[p] for p in prods}
        if not all(d.buy_orders and d.sell_orders for d in depths.values()):
            return {}, 0, ""

        bids = {p: max(depths[p].buy_orders) for p in prods}
        asks = {p: min(depths[p].sell_orders) for p in prods}
        mids = {p: (bids[p] + asks[p]) / 2 for p in prods}
        bid_vols = {p: depths[p].buy_orders[bids[p]] for p in prods}
        ask_vols = {p: depths[p].sell_orders[asks[p]] for p in prods}

        # TODO: check whether to change the method for calculating nav
        nav = 6 * mids["CROISSANTS"] + 3 * mids["JAMS"] + mids["DJEMBES"]
        spread = mids["PICNIC_BASKET1"] - nav
        self.spread_history.append(abs(spread))
        if(len(self.spread_history) >= 50):
            spread_mean = statistics.mean(self.spread_history[-self.time_frame:])
            spread_vol = statistics.stdev(self.spread_history[-self.time_frame:])
            spread_z_score = (abs(spread) - spread_mean) / spread_vol
        else:
            spread_z_score = self.z_score_threshold + 1
        v = self.volume

        # TODO: tune self.volume & self.threshold
        if spread > 0 and spread_z_score > self.z_score_threshold:
            vol = min(v, bid_vols["PICNIC_BASKET1"], self.position_limit["PICNIC_BASKET1"] + pos.get("PICNIC_BASKET1", 0))
            if vol > 0:
                orders.append(Order("PICNIC_BASKET1", bids["PICNIC_BASKET1"], -vol))
                sell_order_volume['PICNIC_BASKET1'] += vol
            for prod, nums in [("CROISSANTS", 6), ("JAMS", 3), ("DJEMBES", 1)]:
                vol = min(nums * v, ask_vols[prod], self.position_limit[prod] - pos.get(prod, 0))
                if vol > 0:
                    orders.append(Order(prod, asks[prod], vol))
                    buy_order_volume[prod] += vol

        elif spread < 0 and spread_z_score > self.z_score_threshold:
            vol = min(v, ask_vols["PICNIC_BASKET1"], self.position_limit["PICNIC_BASKET1"] - pos.get("PICNIC_BASKET1", 0))
            if vol > 0:
                orders.append(Order("PICNIC_BASKET1", asks["PICNIC_BASKET1"], vol))
                buy_order_volume['PICNIC_BASKET1'] += vol
            for prod, nums in [("CROISSANTS", 6), ("JAMS", 3), ("DJEMBES", 1)]:
                vol = min(nums * v, bid_vols[prod], self.position_limit[prod] + pos.get(prod, 0))
                if vol > 0:
                    orders.append(Order(prod, bids[prod], -vol))
                    sell_order_volume[prod] += vol
        return orders, buy_order_volume, sell_order_volume

    def run(self, state: TradingState):
        orders = []
        buy_order_volume = {}
        sell_order_volume = {}
        prods = ["PICNIC_BASKET1", "CROISSANTS", "JAMS", "DJEMBES"]
        for p in prods:
            buy_order_volume[p] = 0
            sell_order_volume[p] = 0
        if not all(p in state.order_depths for p in prods):
            return {}, 0, ""
        orders, buy_order_volume, sell_order_volume = self.etf_b1(state.order_depths, state.position, orders, buy_order_volume, sell_order_volume, prods)
        
        result = {}
        for o in orders:
            result.setdefault(o.symbol, []).append(o)

        logger.flush(state, result, 0, "")
        return result, 0, ""
