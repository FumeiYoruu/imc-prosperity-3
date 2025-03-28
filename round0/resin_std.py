from datamodel import OrderDepth, TradingState, Order
from typing import List
import statistics
import numpy as np

class Trader:
    
    def __init__(self):
        self.position_limit = 50  # Max position allowed
        self.current_position = 0  # Current holdings
        self.price_history = []  # Track past prices
        self.volatility = 0  # Standard deviation of prices
        self.mean_price = 0  # Mean price
        self.last_trade_price = None  # Last executed trade price
        
    def run(self, state: TradingState):
        result = {}
        
        # Only trade Rainforest Resin
        if "RAINFOREST_RESIN" not in state.order_depths:
            return result, 0, state.traderData
            
        order_depth = state.order_depths["RAINFOREST_RESIN"]
        orders: List[Order] = []
        
        # Update current position
        if "RAINFOREST_RESIN" in state.position:
            self.current_position = state.position["RAINFOREST_RESIN"]
        
        # Get best bid/ask prices
        best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
        best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
        
        if best_bid and best_ask:
            mid_price = (best_bid + best_ask) / 2
            self.price_history.append(mid_price)
            
            # Keep price history length reasonable (last 50 prices)
            if len(self.price_history) > 50:
                self.price_history = self.price_history[-50:]
            
            # Calculate statistical measures
            if len(self.price_history) >= 10:  # Need enough data points
                self.mean_price = statistics.mean(self.price_history)
                self.volatility = statistics.stdev(self.price_history)
                
                # Dynamic acceptable price range based on volatility
                lower_bound = self.mean_price - (0.5 * self.volatility)
                upper_bound = self.mean_price + (0.5 * self.volatility)
                
                # Buy when price drops below lower bound
                if best_ask < lower_bound:
                    buy_amount = min(
                        -order_depth.sell_orders[best_ask],  # Available quantity
                        self.position_limit - self.current_position,  # Position limit
                        10  # Don't buy too much at once
                    )
                    if buy_amount > 0:
                        orders.append(Order("RAINFOREST_RESIN", best_ask, buy_amount))
                        self.current_position += buy_amount
                
                # Sell when price rises above upper bound
                if best_bid > upper_bound:
                    sell_amount = min(
                        order_depth.buy_orders[best_bid],  # Available quantity
                        self.position_limit + self.current_position,  # Position limit
                        10  # Don't sell too much at once
                    )
                    if sell_amount > 0:
                        orders.append(Order("RAINFOREST_RESIN", best_bid, -sell_amount))
                        self.current_position -= sell_amount
                
                # Additional conservative mean-reversion when near boundaries
                elif best_ask < self.mean_price - (0.25 * self.volatility):
                    # Smaller buy when approaching lower bound
                    buy_amount = min(
                        -order_depth.sell_orders[best_ask],
                        self.position_limit - self.current_position,
                        5
                    )
                    if buy_amount > 0:
                        orders.append(Order("RAINFOREST_RESIN", best_ask, buy_amount))
                
                elif best_bid > self.mean_price + (0.25 * self.volatility):
                    # Smaller sell when approaching upper bound
                    sell_amount = min(
                        order_depth.buy_orders[best_bid],
                        self.position_limit + self.current_position,
                        5
                    )
                    if sell_amount > 0:
                        orders.append(Order("RAINFOREST_RESIN", best_bid, -sell_amount))
        
        result["RAINFOREST_RESIN"] = orders
        return result, 0, state.traderData