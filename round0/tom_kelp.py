from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Dict
import statistics
import numpy as np

class Trader:
    
    def __init__(self):
        # Position limits for each product
        self.position_limits = {
            'RAINFOREST_RESIN': 50,
            'KELP': 50
        }
        
        # Track price history and positions
        self.price_history = {
            'RAINFOREST_RESIN': [],
            'KELP': []
        }
        self.positions = {
            'RAINFOREST_RESIN': 0,
            'KELP': 0
        }
        
        # Kelp-specific tracking
        self.kelp_trend = 'neutral'
        self.kelp_std_dev = 0
        self.kelp_mean = 0

    def run(self, state: TradingState):
        result = {}
        
        # Update positions from state
        for product in self.position_limits:
            if product in state.position:
                self.positions[product] = state.position[product]
        
        # Trade each product
        for product in state.order_depths:
            if product not in self.position_limits:
                continue  # Skip products we don't trade
                
            order_depth = state.order_depths[product]
            orders: List[Order] = []
            
            # Calculate market metrics
            if order_depth.buy_orders and order_depth.sell_orders:
                best_bid = max(order_depth.buy_orders.keys())
                best_ask = min(order_depth.sell_orders.keys())
                mid_price = (best_bid + best_ask) / 2
                self.price_history[product].append(mid_price)
                
                # Keep only recent history to adapt to changing markets
                if len(self.price_history[product]) > 100:
                    self.price_history[product] = self.price_history[product][-50:]
            
            # Product-specific trading strategies
            if product == 'RAINFOREST_RESIN':
                orders = self.trade_resin(order_depth)
            elif product == 'KELP':
                orders = self.trade_kelp(order_depth)
            
            result[product] = orders
        
        return result, 0, state.traderData

    def trade_resin(self, order_depth: OrderDepth) -> List[Order]:
        """Stable value mean-reversion strategy"""
        orders = []
        
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return orders
            
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid_price = (best_bid + best_ask) / 2
        
        # Calculate fair value as median of recent prices
        fair_price = statistics.median(self.price_history['RAINFOREST_RESIN'][-10:]) if self.price_history['RAINFOREST_RESIN'] else mid_price
        
        # Buy if price is significantly below fair value
        if best_ask < fair_price * 0.995:
            buy_amount = min(
                -order_depth.sell_orders[best_ask],
                self.position_limits['RAINFOREST_RESIN'] - self.positions['RAINFOREST_RESIN']
            )
            if buy_amount > 0:
                orders.append(Order('RAINFOREST_RESIN', best_ask, buy_amount))
                self.positions['RAINFOREST_RESIN'] += buy_amount
        
        # Sell if price is significantly above fair value
        if best_bid > fair_price * 1.005:
            sell_amount = min(
                order_depth.buy_orders[best_bid],
                self.position_limits['RAINFOREST_RESIN'] + self.positions['RAINFOREST_RESIN']
            )
            if sell_amount > 0:
                orders.append(Order('RAINFOREST_RESIN', best_bid, -sell_amount))
                self.positions['RAINFOREST_RESIN'] -= sell_amount
                
        return orders

    def trade_kelp(self, order_depth: OrderDepth) -> List[Order]:
        """Volatile asset momentum strategy"""
        orders = []
        
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return orders
            
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid_price = (best_bid + best_ask) / 2
        
        # Update Kelp statistics
        if len(self.price_history['KELP']) >= 5:
            recent_prices = self.price_history['KELP'][-5:]
            self.kelp_mean = statistics.mean(recent_prices)
            self.kelp_std_dev = statistics.stdev(recent_prices) if len(recent_prices) > 1 else 0
            
            # Determine trend based on moving averages
            short_ma = statistics.mean(recent_prices[-3:])
            long_ma = self.kelp_mean
            self.kelp_trend = 'up' if short_ma > long_ma * 1.01 else 'down' if short_ma < long_ma * 0.99 else 'neutral'
        
        # Momentum-based trading
        if self.kelp_trend == 'up':
            # Buy with trend, more aggressive if strong momentum
            buy_amount = min(
                -order_depth.sell_orders[best_ask],
                self.position_limits['KELP'] - self.positions['KELP'],
                int(self.position_limits['KELP'] * 0.2)  # Don't go all in at once
            )
            if buy_amount > 0 and best_ask < mid_price + self.kelp_std_dev * 0.5:
                orders.append(Order('KELP', best_ask, buy_amount))
                self.positions['KELP'] += buy_amount
                
        elif self.kelp_trend == 'down':
            # Sell with trend
            sell_amount = min(
                order_depth.buy_orders[best_bid],
                self.position_limits['KELP'] + self.positions['KELP'],
                int(self.position_limits['KELP'] * 0.2)
            )
            if sell_amount > 0 and best_bid > mid_price - self.kelp_std_dev * 0.5:
                orders.append(Order('KELP', best_bid, -sell_amount))
                self.positions['KELP'] -= sell_amount
                
        return orders