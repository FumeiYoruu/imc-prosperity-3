import json
from typing import List, Any
import string
import statistics
import numpy as np
import jsonpickle

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
        self.goods = ["PICNIC_BASKET1", "PICNIC_BASKET2", "CROISSANTS", "JAMS", "DJEMBES", "KELP", 'RAINFOREST_RESIN', 'SQUID_INK', "VOLCANIC_ROCK",
                      "VOLCANIC_ROCK_VOUCHER_9500", "VOLCANIC_ROCK_VOUCHER_9750", "VOLCANIC_ROCK_VOUCHER_10000", "VOLCANIC_ROCK_VOUCHER_10250", "VOLCANIC_ROCK_VOUCHER_10500",
                      'MAGNIFICENT_MACARONS']
        self.product = "MAGNIFICENT_MACARONS"
        self.position_limit = 75
        self.conversion_limit = 10

        self.sunlight_history = []
        self.csi_window = 200
        self.csi = 52
        self.csi_flag = False
    def record_trades(self, state, traderObject):
        buy_trades = []

        if traderObject:
            try:
                buy_trades = traderObject.get("buy_trades", [])
            except:
                buy_trades = []
        sell_trades = []

        if traderObject:
            try:
                sell_trades = traderObject.get("sell_trades", [])
            except:
                sell_trades = []
        trades = state.own_trades.get(self.product, [])
        for trade in trades:
            if trade.buyer == 'SUBMISSION':
                buy_trades.append((trade.price, trade.quantity))
            else:
                sell_trades.append((trade.price, trade.quantity))
        traderObject['buy_trades'] = buy_trades[-100:]
        traderObject['sell_trades'] = sell_trades[-100:]
        return traderObject

    def clear_position(self, state, orders, product, thres, traderObject):
        buy_trades = []

        if traderObject:
            try:
                buy_trades = traderObject.get("buy_trades", [])
            except:
                buy_trades = []
        sell_trades = []

        if traderObject:
            try:
                sell_trades = traderObject.get("sell_trades", [])
            except:
                sell_trades = []
        
        # Get current position and order book
        pos = state.position.get(self.product, 0)
        order_depth = state.order_depths.get(self.product, None)
        if not order_depth:
            return orders
            
        best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
        best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
        
        if pos > 0:
            total_quantity = 0
            vol = 0
            better_sells = [t for t in buy_trades if abs(t[0]) < best_bid - thres]
            for t  in better_sells:
                # Calculate total quantity available at better prices
                total_quantity += abs(t[1])
                if(total_quantity <= abs(order_depth.buy_orders[best_bid])):
                    vol = total_quantity
                    buy_trades.remove(t)
                else:
                    break
            orders.append(Order(product, best_bid, -vol))
            pos -= vol
                
        elif pos < 0:  
            total_quantity = 0
            vol  = 0
            better_buys = [t for t in sell_trades if abs(t[0]) > best_ask + thres]
            for t  in better_buys:
                # Calculate total quantity available at better prices
                total_quantity += abs(t[1])
                if(total_quantity <= abs(order_depth.sell_orders[best_ask])):
                    vol = total_quantity
                    sell_trades.remove(t)
                else:
                    break
            orders.append(Order(product, best_ask, +vol))
            pos += vol
            traderObject['buy_trades'] = buy_trades
            traderObject['sell_trades'] = sell_trades
        return orders, pos, traderObject
        
    def run(self, state):
        traderObject = {}
        if state.traderData != None and state.traderData != "":
            traderObject = jsonpickle.decode(state.traderData)
        traderObject = self.record_trades(state, traderObject)
        orders = []
        buy_order_volume = {}
        sell_order_volume = {}
        product = self.product

        for p in self.goods:
            buy_order_volume[p] = 0
            sell_order_volume[p] = 0

        if product not in state.order_depths:
            return {}, 0, ""

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return {}, 0, ""
        

        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid_price = (best_bid + best_ask) / 2


        observation = state.observations.conversionObservations.get(product, None)
        if not observation:
            return {}, 0, ""
        pos = state.position.get(product, 0)


        if len(self.sunlight_history) > 500:
            self.sunlight_history = self.sunlight_history[-500:]
        implied_bid = observation.bidPrice - observation.exportTariff - observation.transportFees - 0.1
        implied_ask = observation.askPrice + abs(observation.importTariff) + observation.transportFees
        
        
        conversion = 0
        if(len(self.sunlight_history) > self.csi_window):
            self.csi = np.mean(self.sunlight_history[-self.csi_window:])
        if observation.sunlightIndex < self.csi:
            #net long
            bid = best_ask
            volume = self.position_limit - pos
            if volume > 0:
                orders.append(Order(product, round(bid), volume))
                buy_order_volume[product] += volume
                self.csi_flag = True
            
            
        else:
            if (self.csi_flag):
                if pos <= 0:
                    self.csi_flag = False
                else:
                    orders, pos, traderObject= self.clear_position(state, orders, self.product, 0, traderObject)
            else:
                bid_price = int(mid_price) - 4
                ask_price = int(mid_price) + 4
                volume = 7
                if pos < self.position_limit:
                    buy_volume = min(volume, self.position_limit - pos)
                    orders.append(Order(self.product, bid_price, buy_volume))
                if pos > -self.position_limit:
                    sell_volume = min(volume, pos + self.position_limit)
                    orders.append(Order(self.product, ask_price, -sell_volume))

                


        result = {}
        for o in orders:
            result.setdefault(o.symbol, []).append(o)
        logger.flush(state, result, conversion, "")
        traderData = jsonpickle.encode(traderObject)
        return result, conversion, traderData
