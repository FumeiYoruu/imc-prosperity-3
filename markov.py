from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict
import statistics
import numpy as np
from collections import defaultdict

class Trader:
    
    def __init__(self):
        self.position_limit = 50
        self.current_position = 0
        self.price_history = []
        self.volatility = 0
        self.mean_price = 0
        
        # Markov Chain components
        self.state_transitions = defaultdict(lambda: defaultdict(int))
        self.current_state = None
        self.previous_state = None
        self.state_bins = 5  # Number of discrete price states
        
    def run(self, state: TradingState):
        result = {}
        
        if "RAINFOREST_RESIN" not in state.order_depths:
            return result, 0, state.traderData
            
        order_depth = state.order_depths["RAINFOREST_RESIN"]
        orders: List[Order] = []
        
        # Update position
        if "RAINFOREST_RESIN" in state.position:
            self.current_position = state.position["RAINFOREST_RESIN"]
        
        # Process market data
        if order_depth.buy_orders and order_depth.sell_orders:
            best_bid = max(order_depth.buy_orders.keys())
            best_ask = min(order_depth.sell_orders.keys())
            mid_price = (best_bid + best_ask) / 2
            self.price_history.append(mid_price)
            
            # Maintain price history window
            if len(self.price_history) > 100:
                self.price_history = self.price_history[-50:]
            
            # Markov Chain Analysis
            if len(self.price_history) > 1:
                # Discretize price states
                price_min = min(self.price_history)
                price_max = max(self.price_history)
                bin_size = (price_max - price_min) / self.state_bins
                
                # Update current state
                self.previous_state = self.current_state
                self.current_state = int((mid_price - price_min) / bin_size) if bin_size > 0 else 0
                
                # Update transition matrix
                if self.previous_state is not None:
                    self.state_transitions[self.previous_state][self.current_state] += 1
            
            # Calculate statistical measures
            if len(self.price_history) >= 10:
                self.mean_price = statistics.mean(self.price_history)
                self.volatility = statistics.stdev(self.price_history) if len(self.price_history) > 1 else 0
                
                # Markov Chain Prediction
                next_state_probs = self.predict_next_state()
                predicted_direction = self.interpret_prediction(next_state_probs)
                
                # Enhanced trading logic combining stats and Markov
                self.generate_orders(orders, order_depth, predicted_direction)
        
        result["RAINFOREST_RESIN"] = orders
        return result, 0, state.traderData
    
    def predict_next_state(self):
        """Use Markov chain to predict probabilities of next states"""
        if self.current_state is None or self.current_state not in self.state_transitions:
            return None
            
        total_transitions = sum(self.state_transitions[self.current_state].values())
        return {state: count/total_transitions 
                for state, count in self.state_transitions[self.current_state].items()}
    
    def interpret_prediction(self, next_state_probs):
        """Interpret Markov chain prediction into market direction"""
        if not next_state_probs:
            return "neutral"
            
        # Calculate expected state change
        current = self.current_state
        expected_change = sum((state - current) * prob 
                         for state, prob in next_state_probs.items())
        
        if expected_change > 0.2:
            return "up"
        elif expected_change < -0.2:
            return "down"
        else:
            return "neutral"
    
    def generate_orders(self, orders: List[Order], order_depth: OrderDepth, predicted_direction: str):
        """Generate orders combining statistical and Markov analysis"""
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        
        # Base trading ranges using volatility
        lower_bound = self.mean_price - (0.5 * self.volatility) if self.volatility > 0 else self.mean_price * 0.995
        upper_bound = self.mean_price + (0.5 * self.volatility) if self.volatility > 0 else self.mean_price * 1.005
        
        # Adjust bounds based on Markov prediction
        if predicted_direction == "up":
            lower_bound *= 1.005  # Be more aggressive buying if expecting upward movement
        elif predicted_direction == "down":
            upper_bound *= 0.995  # Be more aggressive selling if expecting downward movement
        
        # Buy logic
        if best_ask < lower_bound:
            buy_amount = min(
                -order_depth.sell_orders[best_ask],
                self.position_limit - self.current_position,
                10  # Max units per trade
            )
            if buy_amount > 0:
                orders.append(Order("RAINFOREST_RESIN", best_ask, buy_amount))
        
        # Sell logic
        if best_bid > upper_bound:
            sell_amount = min(
                order_depth.buy_orders[best_bid],
                self.position_limit + self.current_position,
                10  # Max units per trade
            )
            if sell_amount > 0:
                orders.append(Order("RAINFOREST_RESIN", best_bid, -sell_amount))