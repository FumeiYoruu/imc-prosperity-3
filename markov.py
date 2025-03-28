class Trader:
    
    def __init__(self):
        self.position_limit = 50
        self.current_position = 0
        self.price_history = []
        self.volatility = 0
        self.mean_price = 0
        self.last_trade_price = None
        self.consecutive_losses = 0  # Track losing streaks
        
        # Simplified Markov components
        self.state_transitions = {'up': 0, 'down': 0, 'neutral': 0}
        self.last_direction = None

    def run(self, state: TradingState):
        result = {}
        
        if "RAINFOREST_RESIN" not in state.order_depths:
            return result, 0, state.traderData
            
        order_depth = state.order_depths["RAINFOREST_RESIN"]
        orders: List[Order] = []
        
        # Update position and track P&L
        if "RAINFOREST_RESIN" in state.position:
            self.current_position = state.position["RAINFOREST_RESIN"]
        
        # Process market data
        if order_depth.buy_orders and order_depth.sell_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_ask = min(order_depth.sell_orders.keys())
            mid_price = (best_bid + best_ask) / 2
            
            # Track price history (limited to recent data)
            self.price_history.append(mid_price)
            if len(self.price_history) > 100:
                self.price_history = self.price_history[-50:]
            
            # Calculate basic statistics
            if len(self.price_history) >= 20:  # Require more data points
                self.mean_price = statistics.mean(self.price_history)
                self.volatility = statistics.stdev(self.price_history) if len(self.price_history) > 1 else 0
                
                # Simplified direction detection (no Markov states)
                current_direction = self.detect_direction()
                
                # More conservative trading ranges
                lower_bound = self.mean_price - (0.7 * self.volatility)  # Wider bands
                upper_bound = self.mean_price + (0.7 * self.volatility)
                
                # Add liquidity instead of taking it
                self.make_market(orders, order_depth, lower_bound, upper_bound)
        
        result["RAINFOREST_RESIN"] = orders
        return result, 0, state.traderData
    
    def detect_direction(self):
        """Simplified trend detection without Markov chains"""
        if len(self.price_history) < 5:
            return "neutral"
            
        short_term = statistics.mean(self.price_history[-3:])
        long_term = statistics.mean(self.price_history[-10:])
        
        if short_term > long_term * 1.005:
            return "up"
        elif short_term < long_term * 0.995:
            return "down"
        return "neutral"
    
    def make_market(self, orders: List[Order], order_depth: OrderDepth, lower: float, upper: float):
        """Post limit orders instead of market orders"""
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        
        # More conservative position sizing
        max_trade_size = max(5, int(self.position_limit * 0.1))  # Smaller trades
        
        # Post bids (buy orders)
        bid_price = min(best_bid + 1, lower)  # Don't chase prices
        bid_size = min(max_trade_size, self.position_limit - self.current_position)
        if bid_size > 0 and bid_price < upper:
            orders.append(Order("RAINFOREST_RESIN", bid_price, bid_size))
        
        # Post asks (sell orders)
        ask_price = max(best_ask - 1, upper)  # Don't give away edge
        ask_size = min(max_trade_size, self.position_limit + self.current_position)
        if ask_size > 0 and ask_price > lower:
            orders.append(Order("RAINFOREST_RESIN", ask_price, -ask_size))