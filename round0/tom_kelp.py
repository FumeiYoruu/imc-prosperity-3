from datamodel import OrderDepth, TradingState, Order
from typing import List
import statistics
import numpy as np

class Trader:
    
    def __init__(self):
        self.position_limit = 50  # Max position allowed
        self.current_position = 0  # Current holdings
        self.price_history = []  # Track past prices
        self.last_trade_price = None  # Last executed trade price
        self.volatility = 0  # Measure of price fluctuations
        self.trend = "neutral"  # Current market trend
        
    def run(self, state: TradingState):
        result = {}
        
        # Only trade Kelp
        if "KELP" not in state.order_depths:
            return result, 0, state.traderData
            
        order_depth = state.order_depths["KELP"]
        orders: List[Order] = []
        
        # Update current position
        if "KELP" in state.position:
            self.current_position = state.position["KELP"]
        
        # Get best bid/ask prices
        best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
        best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
        
        if best_bid and best_ask:
            mid_price = (best_bid + best_ask) / 2
            self.price_history.append(mid_price)
            
            # Keep price history length reasonable
            if len(self.price_history) > 100:
                self.price_history = self.price_history[-50:]
            
            # Calculate volatility (standard deviation of recent prices)
            if len(self.price_history) >= 5:
                self.volatility = statistics.stdev(self.price_history[-5:])
            
            # Determine trend using moving averages
            if len(self.price_history) >= 10:
                short_ma = statistics.mean(self.price_history[-3:])
                long_ma = statistics.mean(self.price_history[-10:])
                self.trend = "up" if short_ma > long_ma * 1.01 else "down" if short_ma < long_ma * 0.99 else "neutral"
            
            # Trading Strategy
            if self.trend == "up":
                # Buy in uptrend (but don't chase prices too high)
                if best_ask < mid_price + self.volatility * 0.5:
                    buy_amount = min(
                        -order_depth.sell_orders[best_ask],  # Available quantity
                        self.position_limit - self.current_position,  # Position limit
                        10  # Don't buy too much at once
                    )
                    if buy_amount > 0:
                        orders.append(Order("KELP", best_ask, buy_amount))
                        self.current_position += buy_amount
            
            elif self.trend == "down":
                # Sell in downtrend (but don't sell too low)
                if best_bid > mid_price - self.volatility * 0.5:
                    sell_amount = min(
                        order_depth.buy_orders[best_bid],  # Available quantity
                        self.position_limit + self.current_position,  # Position limit
                        10  # Don't sell too much at once
                    )
                    if sell_amount > 0:
                        orders.append(Order("KELP", best_bid, -sell_amount))
                        self.current_position -= sell_amount
            
            else:  # Neutral market - mean reversion
                if best_ask < mid_price - self.volatility * 0.3:
                    # Buy if price drops below average
                    buy_amount = min(
                        -order_depth.sell_orders[best_ask],
                        self.position_limit - self.current_position,
                        5
                    )
                    if buy_amount > 0:
                        orders.append(Order("KELP", best_ask, buy_amount))
                
                elif best_bid > mid_price + self.volatility * 0.3:
                    # Sell if price rises above average
                    sell_amount = min(
                        order_depth.buy_orders[best_bid],
                        self.position_limit + self.current_position,
                        5
                    )
                    if sell_amount > 0:
                        orders.append(Order("KELP", best_bid, -sell_amount))
        
        result["KELP"] = orders
        return result, 0, state.traderData