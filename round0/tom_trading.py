class ResinTrader:
    def __init__(self):
        self.position_limit = 50  # Max position allowed
        self.current_position = 0  # Current holdings (positive = long, negative = short)
        
    def handle_market_update(self, resin_price):
        """Process new market price and make trading decisions"""
        if resin_price is None:
            return []  # No price data, no orders
        
        orders = []
        
        # Simple mean-reversion strategy for stable asset
        target_position = 0  # Aim for neutral position with stable asset
        
        if self.current_position < target_position:
            # Need to buy to reach target
            buy_amount = min(target_position - self.current_position, 
                           self.position_limit - self.current_position)
            if buy_amount > 0:
                orders.append(('BUY', 'RAINFOREST_RESIN', resin_price, buy_amount))
                self.current_position += buy_amount
                
        elif self.current_position > target_position:
            # Need to sell to reach target
            sell_amount = min(self.current_position - target_position,
                            self.position_limit + self.current_position)
            if sell_amount > 0:
                orders.append(('SELL', 'RAINFOREST_RESIN', resin_price, sell_amount))
                self.current_position -= sell_amount
                
        return orders


# Example usage
if __name__ == "__main__":
    trader = ResinTrader()
    
    # Simulate market updates
    market_prices = [100, 101, 100, 99, 100, 102]
    
    for price in market_prices:
        orders = trader.handle_market_update(price)
        print(f"Market price: {price}")
        print(f"Generated orders: {orders}")
        print(f"Current position: {trader.current_position}\n")