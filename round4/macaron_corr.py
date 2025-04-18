import json
from typing import List, Any
import string
import statistics
import numpy as np

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
        self.goods = ["PICNIC_BASKET1", "PICNIC_BASKET2", "CROISSANTS", "JAMS", "DJEMBES", "KELP", 'RAINFOREST_RESIN', 'SQUID_INK', "VOLCANIC_ROCK",
                      "VOLCANIC_ROCK_VOUCHER_9500", "VOLCANIC_ROCK_VOUCHER_9750", "VOLCANIC_ROCK_VOUCHER_10000", "VOLCANIC_ROCK_VOUCHER_10250", "VOLCANIC_ROCK_VOUCHER_10500",
                      'MAGNIFICENT_MACARONS']
        self.product = "MAGNIFICENT_MACARONS"
        self.position_limit = 75
        self.conversion_limit = 10
        self.spread = 4.25
        self.conversion_pos = 0
        self.price_history = []
        self.bid_history = []
        self.ask_history = []
        self.obs_history = []
        self.sugar_history = []
        self.sunlight_history = []
        self.sugar_m = 3
        self.sunlight_m = -2
        self.window = 50
        self.volume = 75 
        self.ema = None
        self.foreign_ema = None
        self.alpha = 2 / (self.window + 1)
        self.csi = 52


    def run(self, state):
        orders = []
        buy_order_volume = {}
        sell_order_volume = {}
        product = self.product

        for p in self.goods:
            buy_order_volume[p] = 0
            sell_order_volume[p] = 0

        if product not in state.order_depths:
            return {}, 0, ""

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return {}, 0, ""
        

        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid_price = (best_bid + best_ask) / 2
        self.price_history.append(mid_price)
        if len(self.price_history) > 120:
            self.price_history = self.price_history[-120:]

        if self.ema is None:
            self.ema = mid_price
        else:
            self.ema = self.alpha * mid_price + (1 - self.alpha) * self.ema

        if len(self.price_history) < self.window:
            return {}, 0, ""

        observation = state.observations.conversionObservations.get(product, None)
        if not observation:
            return {}, 0, ""
        pos = state.position.get(product, 0)
        self.bid_history.append(observation.bidPrice)
        self.ask_history.append(observation.askPrice)
        implied_bid = observation.bidPrice - observation.exportTariff - observation.transportFees - 0.1
        implied_ask = observation.askPrice + abs(observation.importTariff) + observation.transportFees
        foreign_mid = (implied_bid + implied_ask) / 2
        if self.foreign_ema is None:
            self.foreign_ema = foreign_mid
        else:
            self.foreign_ema = self.alpha * foreign_mid + (1 - self.alpha) * self.ema
        self.obs_history.append(foreign_mid)
        if len(self.obs_history) > 120:
            self.obs_history = self.obs_history[-120:]

        export_t = observation.exportTariff + observation.transportFees + 0.1
        import_t = abs(observation.importTariff) + observation.transportFees
        sugarPrice = observation.sugarPrice
        sunlightIndex = observation.sunlightIndex
        self.sugar_history.append(sugarPrice)
        self.sunlight_history.append(sunlightIndex)
        
        
        
        # price_mean = np.mean(self.obs_history[-self.window:])
        # sugar_mean = np.mean(self.sugar_history[-self.window:])

        if observation.sunlightIndex < 52:
            if len(self.sugar_history) < self.window or len(self.sunlight_history) < self.window:
                return {}, 0, ""
            sugar_momentum = self.sugar_history[-1] - self.sugar_history[-self.window] 
            sunlight_momentum = self.sunlight_history[-1] - self.sunlight_history[-self.window]
            combined_momentum = sugar_momentum * np.mean(self.obs_history[-self.window]) / np.mean(self.sugar_history[-self.window])

            price_momentum = self.obs_history[-1] - self.obs_history[-self.window]
            fair_value = self.foreign_ema
            if  combined_momentum < price_momentum:
                ask = best_ask 
                volume = min(self.volume, self.position_limit + pos) # max amount to buy
                if volume > 0:
                    orders.append(Order(product, round(ask), -volume))
                    self.conversion_pos -= volume
                    sell_order_volume[product] += volume
            if combined_momentum > price_momentum:
                bid = best_bid 
                volume = min( self.volume, self.position_limit - pos) # max amount to buy
                if volume > 0:
                    orders.append(Order(product, round(bid), volume))
                    self.conversion_pos += volume
                    buy_order_volume[product] += volume
            conversion = -min(abs(pos), self.conversion_limit)
            if(pos < 0):
                if(combined_momentum < price_momentum):
                    if observation.askPrice < fair_value + 0.5:
                        conversion = -conversion
                    else:
                        conversion = 0
            else:
                if(combined_momentum > price_momentum):
                    if observation.bidPrice > fair_value - 0.5:
                        pass
                    else:
                        conversion = 0
        else:
            fair_value = self.foreign_ema
            ask = max(fair_value + 4.5, best_ask - 0.5)
            volume = min(self.volume, self.position_limit + pos) # max amount to buy
            if volume > 0:
                orders.append(Order(product, round(ask), -volume))
                self.conversion_pos -= volume
                sell_order_volume[product] += volume
            bid = min(fair_value - 4.5, best_bid + 0.5)
            volume = min( self.volume, self.position_limit - pos) # max amount to buy
            if volume > 0:
                orders.append(Order(product, round(bid), volume))
                self.conversion_pos += volume
                buy_order_volume[product] += volume
       
        
        self.conversion_pos += conversion
        result = {}
        for o in orders:
            result.setdefault(o.symbol, []).append(o)
        logger.flush(state, result, conversion, "")
        return result, conversion, ""
