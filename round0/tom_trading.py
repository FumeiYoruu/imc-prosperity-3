
import statistics
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
        
        
        # Buy strategy - look for good prices below acceptable
        if order_depth.sell_orders:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_amount = order_depth.sell_orders[best_ask]
            
            if best_ask < acceptable_price:
                # Calculate max we can buy without exceeding position limit
                buy_amount = min(-best_ask_amount, self.position_limit - self.current_position)
                if buy_amount > 0:
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
                    orders.append(Order(product, best_bid, -sell_amount))
                    self.current_position -= sell_amount
        
        result[product] = orders
        traderData = "" 
        
        conversions = 0
        logger.flush(state, result, conversions, traderData)
        # No conversions needed for this product
        return result, 0, state.traderData