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
        self.position_limit = 60
        self.volume = 10
        self.threshold = 1.0

    def run(self, state: TradingState):
        orders = []

        # very stupid implementation because i love shit block
        if "PICNIC_BASKET1" in state.order_depths and \
           "CROISSANTS" in state.order_depths and \
           "JAMS" in state.order_depths and \
           "DJEMBES" in state.order_depths:

            pb1_depth = state.order_depths["PICNIC_BASKET1"]
            cro_depth = state.order_depths["CROISSANTS"]
            jam_depth = state.order_depths["JAMS"]
            djembe_depth = state.order_depths["DJEMBES"]

            if pb1_depth.buy_orders and pb1_depth.sell_orders and \
               cro_depth.buy_orders and cro_depth.sell_orders and \
               jam_depth.buy_orders and jam_depth.sell_orders and \
               djembe_depth.buy_orders and djembe_depth.sell_orders:

                pb1_bid = max(pb1_depth.buy_orders)
                pb1_ask = min(pb1_depth.sell_orders)
                pb1_mid = (pb1_bid + pb1_ask) / 2

                cro_bid = max(cro_depth.buy_orders)
                cro_ask = min(cro_depth.sell_orders)
                cro_mid = (cro_bid + cro_ask) / 2

                jam_bid = max(jam_depth.buy_orders)
                jam_ask = min(jam_depth.sell_orders)
                jam_mid = (jam_bid + jam_ask) / 2

                djembe_bid = max(djembe_depth.buy_orders)
                djembe_ask = min(djembe_depth.sell_orders)
                djembe_mid = (djembe_bid + djembe_ask) / 2

                nav = 6 * cro_mid + 3 * jam_mid + 1 * djembe_mid
                spread = pb1_mid - nav
                
                pos_pb1 = state.position.get("PICNIC_BASKET1", 0)
                pos_cro = state.position.get("CROISSANTS", 0)
                pos_jam = state.position.get("JAMS", 0)
                pos_dje = state.position.get("DJEMBES", 0)

                pb1_bid_vol = pb1_depth.buy_orders[pb1_bid]
                pb1_ask_vol = pb1_depth.sell_orders[pb1_ask]

                cro_bid_vol = cro_depth.buy_orders[cro_bid]
                cro_ask_vol = cro_depth.sell_orders[cro_ask]

                jam_bid_vol = jam_depth.buy_orders[jam_bid]
                jam_ask_vol = jam_depth.sell_orders[jam_ask]

                dje_bid_vol = djembe_depth.buy_orders[djembe_bid]
                dje_ask_vol = djembe_depth.sell_orders[djembe_ask]

                if spread > self.threshold:
                    volume = min(self.volume, pb1_bid_vol, self.position_limit + pos_pb1)
                    if volume > 0:
                        orders.append(Order("PICNIC_BASKET1", pb1_bid, -volume))

                    cro_vol = min(6 * self.volume, cro_ask_vol, self.position_limit - pos_cro)
                    if cro_vol > 0:
                        orders.append(Order("CROISSANTS", cro_ask, cro_vol))

                    jam_vol = min(3 * self.volume, jam_ask_vol, self.position_limit - pos_jam)
                    if jam_vol > 0:
                        orders.append(Order("JAMS", jam_ask, jam_vol))

                    dje_vol = min(1 * self.volume, dje_ask_vol, self.position_limit - pos_dje)
                    if dje_vol > 0:
                        orders.append(Order("DJEMBES", djembe_ask, dje_vol))

                elif spread < -self.threshold:
                    volume = min(self.volume, pb1_ask_vol, self.position_limit - pos_pb1)
                    if volume > 0:
                        orders.append(Order("PICNIC_BASKET1", pb1_ask, volume))

                    cro_vol = min(6 * self.volume, cro_bid_vol, self.position_limit + pos_cro)
                    if cro_vol > 0:
                        orders.append(Order("CROISSANTS", cro_bid, -cro_vol))

                    jam_vol = min(3 * self.volume, jam_bid_vol, self.position_limit + pos_jam)
                    if jam_vol > 0:
                        orders.append(Order("JAMS", jam_bid, -jam_vol))

                    dje_vol = min(1 * self.volume, dje_bid_vol, self.position_limit + pos_dje)
                    if dje_vol > 0:
                        orders.append(Order("DJEMBES", djembe_bid, -dje_vol))
                        
        result = {}
        for order in orders:
            if order.symbol not in result:
                result[order.symbol] = []
            result[order.symbol].append(order)

        conversions = 0
        traderData = ""
        logger.flush(state, result, conversions, traderData)
        return result, conversions, traderData
