from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import statistics

class Trader:
    
    def __init__(self):
        # Initialize position limit for Rainforest Resin
        self.position_limit = 50
        # Track price history for better acceptable price calculation
        self.price_history = []
        # Track our current position
        self.current_position = 0
        
    def run(self, state: TradingState):
        result = {}
        
        # Only trade Rainforest Resin (ignore other products)
        if 'RAINFOREST_RESIN' not in state.order_depths:
            return result, 0, state.traderData
            
        product = 'RAINFOREST_RESIN'
        order_depth = state.order_depths[product]
        orders: List[Order] = []
        
        # Update our position from previous trades
        if product in state.position:
            self.current_position = state.position[product]
        
        # Calculate acceptable price based on market mid-price
        if order_depth.buy_orders and order_depth.sell_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_ask = min(order_depth.sell_orders.keys())
            mid_price = (best_bid + best_ask) / 2
            self.price_history.append(mid_price)
            
            # Use average of recent prices as acceptable price
            acceptable_price = statistics.mean(self.price_history[-10:]) if len(self.price_history) > 0 else mid_price
        else:
            # If no orders, use last acceptable price
            acceptable_price = self.price_history[-1] if self.price_history else 10
        
        print(f"Acceptable price for {product}: {acceptable_price}")
        print(f"Current position: {self.current_position}/{self.position_limit}")
        
        # Buy strategy - look for good prices below acceptable
        if order_depth.sell_orders:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_amount = order_depth.sell_orders[best_ask]
            
            if best_ask < acceptable_price:
                # Calculate max we can buy without exceeding position limit
                buy_amount = min(-best_ask_amount, self.position_limit - self.current_position)
                if buy_amount > 0:
                    print(f"BUY {product} {buy_amount}x {best_ask}")
                    orders.append(Order(product, best_ask, buy_amount))
                    self.current_position += buy_amount
        
        # Sell strategy - look for good prices above acceptable
        if order_depth.buy_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_amount = order_depth.buy_orders[best_bid]
            
            if best_bid > acceptable_price:
                # Calculate max we can sell without exceeding position limit
                sell_amount = min(best_bid_amount, self.position_limit + self.current_position)
                if sell_amount > 0:
                    print(f"SELL {product} {sell_amount}x {best_bid}")
                    orders.append(Order(product, best_bid, -sell_amount))
                    self.current_position -= sell_amount
        
        result[product] = orders
        
        # No conversions needed for this product
        return result, 0, state.traderData