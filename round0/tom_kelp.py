<<<<<<< Updated upstream
from datamodel import OrderDepth, TradingState, Order
from typing import List
=======

from typing import List, Dict, Any
>>>>>>> Stashed changes
import statistics
import numpy as np

import json
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
                
<<<<<<< Updated upstream
                elif best_bid > mid_price + self.volatility * 0.3:
                    # Sell if price rises above average
                    sell_amount = min(
                        order_depth.buy_orders[best_bid],
                        self.position_limit + self.current_position,
                        5
                    )
                    if sell_amount > 0:
                        orders.append(Order("KELP", best_bid, -sell_amount))
=======
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
            traderData = "" 
        
        conversions = 0
        logger.flush(state, result, conversions, traderData)
>>>>>>> Stashed changes
        
        result["KELP"] = orders
        return result, 0, state.traderData