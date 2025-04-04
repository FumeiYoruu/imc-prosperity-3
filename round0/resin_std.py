from datamodel import OrderDepth, TradingState, Order
from typing import List
import statistics
import numpy as np
import json
from typing import List, Any
import string

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
        self.position_limit = 50
        self.current_position = 0 
        self.price_history = []  
        self.volatility = 0  
        self.mean_price = 0  
        self.last_trade_price = None  
        
        
    def run(self, state: TradingState):
        result = {}

        if "RAINFOREST_RESIN" not in state.order_depths:
            return result, 0, state.traderData
            
        order_depth = state.order_depths["RAINFOREST_RESIN"]
        order_dict = {}
        orders: List[Order] = []
        
        if "RAINFOREST_RESIN" in state.position:
            self.current_position = state.position["RAINFOREST_RESIN"]
        
        best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
        best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
        bids = list(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
        asks = list(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
        
        if best_bid and best_ask:
            mid_price = (best_bid * order_depth.buy_orders[best_bid] + best_ask * (-order_depth.sell_orders[best_ask]))/ (order_depth.buy_orders[best_bid] - order_depth.sell_orders[best_ask]);
            self.price_history.append(mid_price)
            
            # if len(self.price_history) > 100:
            #     self.price_history = self.price_history[-100:]
            if len(self.price_history) >= 10:  
                self.mean_price = 10000
                self.volatility = statistics.stdev(self.price_history)
                
                
                lower_bound = self.mean_price - (0.1 * self.volatility)
                upper_bound = self.mean_price + (0.1 * self.volatility)
                if asks != None: 
                    for ask in asks:
                        if ask < lower_bound:
                            buy_amount = min(
                                -order_depth.sell_orders[ask],  
                                self.position_limit - self.current_position, 
                            )
                            if buy_amount > 0:
                                order_dict[ask] = order_dict.get(ask, 0) + buy_amount
                                self.current_position += buy_amount
                        elif ask < self.mean_price - (0.25 * self.volatility):
                            buy_amount = min(
                                -order_depth.sell_orders[ask],
                                self.position_limit - self.current_position,
                                5
                            )
                            if buy_amount > 0:   
                                order_dict[ask] = order_dict.get(ask, 0) + buy_amount
                                self.current_position += buy_amount
                if bids != None:
                    for bid in bids: 
                        if bid > upper_bound:
                            sell_amount = min(
                                order_depth.buy_orders[bid], 
                                self.position_limit + self.current_position,

                            )
                            if sell_amount > 0:
                                order_dict[bid] = order_dict.get(bid, 0) - sell_amount
                                self.current_position -= sell_amount
                        
                        
                        
                        elif bid > self.mean_price + (0.25 * self.volatility):
                            sell_amount = min(
                                order_depth.buy_orders[bid],
                                self.position_limit + self.current_position,
                                5
                            )
                            if sell_amount > 0:
                                order_dict[bid] = order_dict.get(bid, 0) - sell_amount
                                self.current_position -= sell_amount
                if asks != None: 
                    for ask in asks:
                        if ask < lower_bound:
                            buy_amount = min(
                                -order_depth.sell_orders[ask],  
                                self.position_limit - self.current_position, 
                            )
                            if buy_amount > 0:
                                order_dict[ask] = order_dict.get(ask, 0) + buy_amount
                                self.current_position += buy_amount
                        elif ask < self.mean_price - (0.25 * self.volatility):
                            buy_amount = min(
                                -order_depth.sell_orders[ask],
                                self.position_limit - self.current_position,
                                5
                            )
                            if buy_amount > 0:   
                                order_dict[ask] = order_dict.get(ask, 0) + buy_amount
                                self.current_position += buy_amount
                
                if self.current_position != 0:
                    if self.current_position > 0 and abs(best_bid - self.mean_price) < 0.1 * self.volatility:  
                        best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
                        if best_bid:
                            reduce_amount = min(
                                order_depth.buy_orders[best_bid],
                                abs(self.current_position) - 10
                            )
                            if reduce_amount > 0:
                                order_dict[best_bid] = order_dict.get(best_bid, 0) - reduce_amount
                                self.current_position -= reduce_amount
                    elif self.current_position < 0 and abs(best_ask -  self.mean_price) < 0.1 * self.volatility:
                        best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
                        if best_ask:
                            reduce_amount = min(
                                -order_depth.sell_orders[best_ask],
                                abs(self.current_position) - 10
                            )
                            if reduce_amount > 0:
                                order_dict[best_ask] = order_dict.get(best_ask, 0) + reduce_amount
                                self.current_position += reduce_amount
        
        # Convert order_dict to orders list
        for price, quantity in order_dict.items():
            orders.append(Order("RAINFOREST_RESIN", price, quantity))
        result["RAINFOREST_RESIN"] = orders
        traderData = "" 
        
        conversions = 0
        logger.flush(state, result, conversions, traderData)
        return result, 0, state.traderData
