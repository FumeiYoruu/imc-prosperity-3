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
        orders: List[Order] = []
        
        if "RAINFOREST_RESIN" in state.position:
            self.current_position = state.position["RAINFOREST_RESIN"]
        
        best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
        best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
        bids = list(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
        asks = list(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
        if best_bid and best_ask:
            mid_price = (best_bid + best_ask) / 2
            self.price_history.append(mid_price)
            
            if len(self.price_history) > 100:
                self.price_history = self.price_history[-100:]
            if len(self.price_history) >= 10:  
                self.mean_price = statistics.mean(self.price_history)
                self.volatility = statistics.stdev(self.price_history)
                order_rank = {}
                for bid in bids:
                    order_rank[bid] = bid - self.mean_price
                for ask in asks:
                    order_rank[ask] = -ask + self.mean_price
                order_rank = dict(sorted(order_rank.items(), key=lambda item: item[1], reverse=True))
                
                bound = 0.5 * self.volatility
                min_bound = 0.25 * self.volatility
                if len(order_rank.keys()): 
                    for price, diff in order_rank.items():
                        if(price > mid_price):
                            ask = price
                            if diff > bound:
                                buy_amount = min(
                                    -order_depth.sell_orders[ask],  
                                    self.position_limit - self.current_position,   
                                )
                                if buy_amount > 0:
                                    orders.append(Order("RAINFOREST_RESIN", ask, buy_amount))
                                    self.current_position += buy_amount
                            elif diff > min_bound:
                                buy_amount = min(
                                    -order_depth.sell_orders[ask],
                                    self.position_limit - self.current_position,
                                    5
                                )
                                if buy_amount > 0:   
                                    orders.append(Order("RAINFOREST_RESIN", ask, buy_amount))
                                    self.current_position += buy_amount
            
                        elif(price < mid_price): 
                            bid = price
                            if diff > bound:
                                sell_amount = min(
                                    order_depth.buy_orders[bid], 
                                    self.position_limit + self.current_position,  
                                )
                                if sell_amount > 0:
                                    orders.append(Order("RAINFOREST_RESIN", bid, -sell_amount))
                                    self.current_position -= sell_amount
                            
                            
                            
                            elif diff > min_bound:
                                sell_amount = min(
                                    order_depth.buy_orders[bid],
                                    self.position_limit + self.current_position,
                                    5
                                )
                                if sell_amount > 0:
                                    orders.append(Order("RAINFOREST_RESIN", bid, -sell_amount))
                                    self.current_position -= sell_amount
        
        if best_bid and best_ask:
            mid_price = (best_bid * order_depth.buy_orders[best_bid] + best_ask * (-order_depth.sell_orders[best_ask]))/ (order_depth.buy_orders[best_bid] - order_depth.sell_orders[best_ask]);
            self.price_history.append(mid_price)
            
            if len(self.price_history) > 100:
                self.price_history = self.price_history[-100:]
            if len(self.price_history) >= 10:  
                self.mean_price = statistics.mean(self.price_history)
                self.volatility = statistics.stdev(self.price_history)
                
                lower_bound = self.mean_price - (0.5 * self.volatility)
                upper_bound = self.mean_price + (0.5 * self.volatility)
                if asks != None: 
                    for ask in asks:
                        if ask < lower_bound:
                            buy_amount = min(
                                -order_depth.sell_orders[ask],  
                                self.position_limit - self.current_position,   
                            )
                            if buy_amount > 0:
                                orders.append(Order("RAINFOREST_RESIN", ask, buy_amount))
                                self.current_position += buy_amount
                        elif ask < self.mean_price - (0.25 * self.volatility):
                            buy_amount = min(
                                -order_depth.sell_orders[ask],
                                self.position_limit - self.current_position,
                                5
                            )
                            if buy_amount > 0:   
                                orders.append(Order("RAINFOREST_RESIN", ask, buy_amount))
                                self.current_position += buy_amount
                if bids != None:
                    for bid in bids: 
                        if bid > upper_bound:
                            sell_amount = min(
                                order_depth.buy_orders[bid], 
                                self.position_limit + self.current_position,  
                            )
                            if sell_amount > 0:
                                orders.append(Order("RAINFOREST_RESIN", bid, -sell_amount))
                                self.current_position -= sell_amount
                        
                        
                        
                        elif bid > self.mean_price + (0.25 * self.volatility):
                            sell_amount = min(
                                order_depth.buy_orders[bid],
                                self.position_limit + self.current_position,
                                5
                            )
                            if sell_amount > 0:
                                orders.append(Order("RAINFOREST_RESIN", bid, -sell_amount))
                                self.current_position -= sell_amount
                if asks != None: 
                    for ask in asks:
                        if ask < lower_bound:
                            buy_amount = min(
                                -order_depth.sell_orders[ask],  
                                self.position_limit - self.current_position,   
                            )
                            if buy_amount > 0:
                                orders.append(Order("RAINFOREST_RESIN", ask, buy_amount))
                                self.current_position += buy_amount
                        elif ask < self.mean_price - (0.25 * self.volatility):
                            buy_amount = min(
                                -order_depth.sell_orders[ask],
                                self.position_limit - self.current_position,
                                5
                            )
                            if buy_amount > 0:   
                                orders.append(Order("RAINFOREST_RESIN", ask, buy_amount))
                                self.current_position += buy_amount
        
        result["RAINFOREST_RESIN"] = orders
        traderData = "" 
        
        conversions = 0
        logger.flush(state, result, conversions, traderData)
        return result, 0, state.traderData