import json
import numpy as np
from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState
import statistics
from typing import List
import math
import jsonpickle

class Logger:
    def __init__(self) -> None:
        self.logs = ""
        self.max_log_length = 3750

    def print(self, *objects, sep=" ", end="\n") -> None:
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

    def compress_state(self, state: TradingState, trader_data: str) -> list:
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

    def compress_listings(self, listings: dict) -> list:
        compressed = []
        for listing in listings.values():
            compressed.append([listing.symbol, listing.product, listing.denomination])
        return compressed

    def compress_order_depths(self, order_depths: dict) -> dict:
        compressed = {}
        for symbol, order_depth in order_depths.items():
            compressed[symbol] = [order_depth.buy_orders, order_depth.sell_orders]
        return compressed

    def compress_trades(self, trades: dict) -> list:
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

    def compress_observations(self, observations: Observation) -> list:
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

    def compress_orders(self, orders: dict) -> list:
        compressed = []
        for arr in orders.values():
            for order in arr:
                compressed.append([order.symbol, order.price, order.quantity])
        return compressed

    def to_json(self, value) -> str:
        return json.dumps(value, cls=ProsperityEncoder, separators=(",", ":"))

    def truncate(self, value: str, max_length: int) -> str:
        if len(value) <= max_length:
            return value
        return value[: max_length - 3] + "..."


logger = Logger()


class Trader:
    def __init__(self):
        self.goods = ["PICNIC_BASKET1", "PICNIC_BASKET2", "CROISSANTS", "JAMS", "DJEMBES", "KELP", 'RAINFOREST_RESIN', 'SQUID_INK', "VOLCANIC_ROCK",
                      "VOLCANIC_ROCK_VOUCHER_9500", "VOLCANIC_ROCK_VOUCHER_9750", "VOLCANIC_ROCK_VOUCHER_10000", "VOLCANIC_ROCK_VOUCHER_10250", "VOLCANIC_ROCK_VOUCHER_10500"]
        self.rock = "VOLCANIC_ROCK"
        self.rock_limit = 400
        self.vouchers = {
            "VOLCANIC_ROCK_VOUCHER_9500": 9500,
            "VOLCANIC_ROCK_VOUCHER_9750": 9750,
            "VOLCANIC_ROCK_VOUCHER_10000": 10000,
            "VOLCANIC_ROCK_VOUCHER_10250": 10250,
            "VOLCANIC_ROCK_VOUCHER_10500": 10500,
        }
        self.voucher_limits = {k: 200 for k in self.vouchers}
        self.voucher_window_size = 75
        # Volatility smile fit parameters
        self.vm_a = 4.393540
        self.vm_b = 0.004045
        self.vm_c = 0.008134
        
        # TODO: tune following params
        self.voucher_threshold = 0.003
        self.voucher_volume = 30
        # Per-voucher smile bias correction
        self.v_bias = {
            "VOLCANIC_ROCK_VOUCHER_9500":  0.0000,
            "VOLCANIC_ROCK_VOUCHER_9750":  0.0000,
            "VOLCANIC_ROCK_VOUCHER_10000": -0.005,
            "VOLCANIC_ROCK_VOUCHER_10250": -0.004,
            "VOLCANIC_ROCK_VOUCHER_10500": -0.004,
        }
        self.volume = 30 #etf
        self.squidvolume = 5
        self.threshold = 1.0
        self.position_limit = {
            "PICNIC_BASKET1": 60,
            "CROISSANTS": 250,
            "JAMS": 350,
            "DJEMBES": 60,
            "PICNIC_BASKET2": 100,
            'KELP' : 50,
            'RAINFOREST_RESIN' : 50,
            'SQUID_INK' : 50,
            "VOLCANIC_ROCK_VOUCHER_9500": 200,
            "VOLCANIC_ROCK_VOUCHER_9750": 200,
            "VOLCANIC_ROCK_VOUCHER_10000": 200,
            "VOLCANIC_ROCK_VOUCHER_10250": 200,
            "VOLCANIC_ROCK_VOUCHER_10500": 200,
            "VOLCANIC_ROCK" : 400,
        }
        self.b1_weights = {
            'CROISSANTS' : 6,
            'JAMS' : 3,
            'DJEMBES' : 1,
        }

        self.b2_weights = {
            'CROISSANTS' : 4,
            'JAMS' : 2,
        }
        self.spread_history = []
        self.price_history = {}
        self.time_frame = 100
        self.spread_mean_lookback = 100
        self.z_score_threshold = 3
        self.z_score_threshold_etf2 = 2
        self.z_upper_threshold = 2
        self.z_lower_threshold = -2
        self.spread_history2 = []
        self.djembes_reversion_param = -0.2
        self.djembes_adverse_volume = 30
        self.kelp_reversion_param = -0.229
        self.kelp_adverse_volume = 20
        self.squid_window = 30
        self.squid_momentum_threshold = 0.5
        self.std_threshold = 3.3 #squid
        self.croissant_volume = 10
        self.croissant_window = 100
        self.croissant_spread = 3
        self.pred_threshold = 2.2 #kuasong
        self.time_remaining = 0
        self.time_remaining_etf1 = 0
        self.rock_volume = 10
        self.rock_window = 50
        self.rock_spread = 2
        self.rock_ema = None
        self.rock_alpha = 2 / (self.rock_window + 1)
        self.jam_volume = 25
        self.jam_window = 30
        self.jam_spread = 2
        self.djembes_window_size = 20
        self.djembes_threshold = 9.5
        self.djembes_volume = 20

    def norm_cdf(self, x):
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    
    def bs_price(self, sigma, S, K, T):
        # B-S price, assume r = 0
        if T <= 0 or sigma <= 0:
            return max(S - K, 0)
            
        d1 = (math.log(S / K) + 0.5 * sigma**2 * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        return S * self.norm_cdf(d1) - K * self.norm_cdf(d2)

    def implied_volatility(self, C, S, K, T, eps=1e-6, max_iter=100):
        # binary answer for implied volatility
        low = 1e-4
        high = 5.0
        for _ in range(max_iter):
            mid = (low + high) / 2
            price = self.bs_price(mid, S, K, T)
            if abs(price - C) < eps:
                return mid
            if price > C:
                high = mid
            else:
                low = mid
        return None

    def voucher_trade(self, state, orders, traderObject):
        result = {}
        rock_history = []

        if traderObject:
            try:
                rock_history = traderObject.get("rock_history", [])
            except:
                rock_history = []

        if self.rock not in state.order_depths:
            traderObject['rock_history'] = rock_history
            return orders, result

        rock_depth = state.order_depths[self.rock]
        if not rock_depth.buy_orders or not rock_depth.sell_orders:
            traderObject['rock_history'] = rock_history
            return orders, result

        rock_mid = (max(rock_depth.buy_orders) + min(rock_depth.sell_orders)) / 2
        rock_history.append(rock_mid)

        if len(rock_history) <= self.voucher_window_size:
            traderObject['rock_history'] = rock_history
            return orders, result
        else:
            rock_history = rock_history[-self.voucher_window_size:]

        ### main loop here ###
        orders = []
        for voucher, strike in self.vouchers.items():
            if voucher not in state.order_depths:
                continue

            depth = state.order_depths[voucher]
            if not depth.buy_orders or not depth.sell_orders:
                continue
            
            pos = state.position.get(voucher, 0)
            limit = self.voucher_limits[voucher]


            best_bid = max(depth.buy_orders)
            best_ask = min(depth.sell_orders)
            voucher_mid = (best_bid + best_ask) / 2

            S = sum(rock_history) / len(rock_history)
            K = strike
            T = 5

            m_t = math.log(K / S) / math.sqrt(T)
            v_fit = self.vm_a * m_t**2 + self.vm_b * m_t + self.vm_c
            v_fit += self.v_bias.get(voucher, 0.0)
            iv = self.implied_volatility(voucher_mid, S, K, T)
            if iv is None:
                continue
            
            # difference between implied volatility and fitted volatility
            diff = iv - v_fit
            # voucher overestimate
            if diff > self.voucher_threshold and pos > -limit:
                volume = min(self.voucher_volume, depth.buy_orders[best_bid], pos + limit)
                if volume > 0:
                    orders.append(Order(voucher, best_bid, -volume))
            # voucher underestimate
            elif diff < -self.voucher_threshold and pos < limit:
                volume = min(self.voucher_volume, -depth.sell_orders[best_ask], limit - pos)
                if volume > 0:
                    orders.append(Order(voucher, best_ask, volume))

            if orders:
                result[voucher] = orders

        traderObject['rock_history'] = rock_history
        return orders, result
    
    def squid(self, state, orders, buy_order_volume, sell_order_volume, product = 'SQUID_INK'):

        if product not in state.order_depths:
            return orders, buy_order_volume, sell_order_volume

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return orders, buy_order_volume, sell_order_volume

        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        pos = state.position.get(product, 0)

        if pos < self.position_limit["SQUID_INK"]:
            buy_volume = min(self.squidvolume, self.position_limit["SQUID_INK"] - pos)
            orders.append(Order(product, best_bid, buy_volume))
            
        if pos > -self.position_limit["SQUID_INK"]:
            sell_volume = min(self.squidvolume, pos + self.position_limit["SQUID_INK"])
            orders.append(Order(product, best_ask, -sell_volume))

        return orders, buy_order_volume, sell_order_volume

    def croissant(self, state, orders, buy_order_volume, sell_order_volume, product = 'CROISSANTS'):

        if product not in state.order_depths:
            return orders, buy_order_volume, sell_order_volume

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return orders, buy_order_volume, sell_order_volume

        best_bid = max(order_depth.buy_orders)
        best_ask = min(order_depth.sell_orders)
        mid_price = (best_bid + best_ask) / 2

        if len(self.price_history[product]) > 120:
            self.price_history[product] = self.price_history[product][-120:]

        if len(self.price_history[product]) < self.croissant_window:
            return orders, buy_order_volume, sell_order_volume

        # using SMA
        fair_value = int(sum(self.price_history[product][-self.croissant_window:]) / self.croissant_window)
        pos = state.position.get(product, 0)

        # try to buy
        buy_price = fair_value - self.croissant_spread
        if pos < self.position_limit[product]:
            volume = min(self.croissant_volume, self.position_limit[product] - pos)
            orders.append(Order(product, buy_price, volume))

        # try to sell
        sell_price = fair_value + self.croissant_spread
        if pos > -self.position_limit[product]:
            volume = min(self.croissant_volume, pos + self.position_limit[product])
            orders.append(Order(product, sell_price, -volume))
        return orders, buy_order_volume, sell_order_volume

    
    def take_best_orders(
        self,
        product: str,
        fair_value: int,
        take_width: float,
        orders: List[Order],
        order_depth: OrderDepth,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
        prevent_adverse: bool = False,
        adverse_volume: int = 0,
    ) -> (int, int):
        position_limit = self.position_limit[product]

        if len(order_depth.sell_orders) != 0:
            best_ask = min(order_depth.sell_orders.keys())
            best_ask_amount = -1 * order_depth.sell_orders[best_ask]

            if not prevent_adverse or abs(best_ask_amount) <= adverse_volume:
                if best_ask <= fair_value - take_width:
                    quantity = min(
                        best_ask_amount, position_limit - position
                    )  # max amt to buy
                    if quantity > 0:
                        orders.append(Order(product, best_ask, quantity))
                        buy_order_volume += quantity
                        order_depth.sell_orders[best_ask] += quantity
                        if order_depth.sell_orders[best_ask] == 0:
                            del order_depth.sell_orders[best_ask]

        if len(order_depth.buy_orders) != 0:
            best_bid = max(order_depth.buy_orders.keys())
            best_bid_amount = order_depth.buy_orders[best_bid]

            if not prevent_adverse or abs(best_bid_amount) <= adverse_volume:
                if best_bid >= fair_value + take_width:
                    quantity = min(
                        best_bid_amount, position_limit + position
                    )  # should be the max we can sell
                    if quantity > 0:
                        orders.append(Order(product, best_bid, -1 * quantity))
                        sell_order_volume += quantity
                        order_depth.buy_orders[best_bid] -= quantity
                        if order_depth.buy_orders[best_bid] == 0:
                            del order_depth.buy_orders[best_bid]

        return buy_order_volume, sell_order_volume

    def rocks(self, state, product, orders, buy_order_volume, sell_order_volume):
        if product not in state.order_depths:
            return orders, buy_order_volume, sell_order_volume

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return orders, buy_order_volume, sell_order_volume

        best_bid = max(order_depth.buy_orders)
        best_ask = min(order_depth.sell_orders)
        mid_price = (best_bid + best_ask) / 2

        if len(self.price_history) > 120:
            self.price_history[product] = self.price_history[product][-120:]

        if self.rock_ema is None:
            self.rock_ema = mid_price
        else:
            self.rock_ema = self.rock_alpha * mid_price + (1 - self.rock_alpha) * self.rock_ema

        if len(self.price_history[product]) < self.rock_window:
            return orders, buy_order_volume, sell_order_volume

        fair_value = int(self.rock_ema)
        pos = state.position.get(product, 0)

        # try to buy
        buy_price = fair_value - self.rock_spread
        if pos < self.position_limit[product]:
            volume = min(self.rock_volume, self.position_limit[product] - pos)
            orders.append(Order(product, buy_price, volume))

        # try to sell
        sell_price = fair_value + self.rock_spread
        if pos > -self.position_limit[product]:
            volume = min(self.rock_volume, pos + self.position_limit[product])
            orders.append(Order(product, sell_price, -volume))
        return orders, buy_order_volume, sell_order_volume

    def market_make(
            
        self,
        product: str,
        orders: List[Order],
        bid: int,
        ask: int,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ):
        buy_quantity = self.position_limit[product] - (position + buy_order_volume)
        if buy_quantity > 0:
            orders.append(Order(product, round(bid), buy_quantity))  # Buy order

        sell_quantity = self.position_limit[product] + (position - sell_order_volume)
        if sell_quantity > 0:
            orders.append(Order(product, round(ask), -sell_quantity))  # Sell order
        return buy_order_volume, sell_order_volume

    def take_orders(
        self,
        orders,
        product: str,
        order_depth: OrderDepth,
        fair_value: float,
        take_width: float,
        position: int,
        buy_order_volume,
        sell_order_volume,
        prevent_adverse: bool = False,
        adverse_volume: int = 0,
    ):

        buy_order_volume[product], sell_order_volume[product] = self.take_best_orders(
            product,
            fair_value,
            take_width,
            orders,
            order_depth,
            position,
            buy_order_volume[product],
            sell_order_volume[product],
            prevent_adverse,
            adverse_volume
        )
        return orders, buy_order_volume, sell_order_volume
    

    def make_orders(
            

            
        self,
        orders,
        product,
        order_depth: OrderDepth,
        fair_value: float,
        position: int,
        buy_order_volume,
        sell_order_volume,
        disregard_edge: float,  # disregard trades within this edge for pennying or joining
        join_edge: float,  # join trades within this edge
        default_edge: float,  # default edge to request if there are no levels to penny or join
        manage_position: bool = False,
        soft_position_limit: int = 0,
        # will penny all other levels with higher edge
    ):
        asks_above_fair = [
            price
            for price in order_depth.sell_orders.keys()
            if price > fair_value + disregard_edge
        ]
        bids_below_fair = [
            price
            for price in order_depth.buy_orders.keys()
            if price < fair_value - disregard_edge
        ]

        best_ask_above_fair = min(asks_above_fair) if len(asks_above_fair) > 0 else None
        best_bid_below_fair = max(bids_below_fair) if len(bids_below_fair) > 0 else None

        ask = round(fair_value + default_edge)
        if best_ask_above_fair != None:
            if abs(best_ask_above_fair - fair_value) <= join_edge:
                ask = best_ask_above_fair  # join
            else:
                ask = best_ask_above_fair - 1  # penny

        bid = round(fair_value - default_edge)
        if best_bid_below_fair != None:
            if abs(fair_value - best_bid_below_fair) <= join_edge:
                bid = best_bid_below_fair
            else:
                bid = best_bid_below_fair + 1

        if manage_position:
            if position > soft_position_limit:
                ask -= 1
            elif position < -1 * soft_position_limit:
                bid += 1

        buy_order_volume, sell_order_volume = self.market_make(
            product,
            orders,
            bid,
            ask,
            position,
            buy_order_volume,
            sell_order_volume,
        )

        return orders, buy_order_volume, sell_order_volume
    
    def clear_position_order(
        self,
        product: str,
        fair_value: float,
        width: int,
        orders: List[Order],
        order_depth: OrderDepth,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) -> List[Order]:
        position_after_take = position + buy_order_volume - sell_order_volume
        fair_for_bid = round(fair_value - width)
        fair_for_ask = round(fair_value + width)

        buy_quantity = self.position_limit[product] - (position + buy_order_volume)
        sell_quantity = self.position_limit[product] + (position - sell_order_volume)

        if position_after_take > 0:
            # Aggregate volume from all buy orders with price greater than fair_for_ask
            clear_quantity = sum(
                volume
                for price, volume in order_depth.buy_orders.items()
                if price >= fair_for_ask
            )
            clear_quantity = min(clear_quantity, position_after_take)
            sent_quantity = min(sell_quantity, clear_quantity)
            if sent_quantity > 0:
                orders.append(Order(product, fair_for_ask, -abs(sent_quantity)))
                sell_order_volume += abs(sent_quantity)

        if position_after_take < 0:
            # Aggregate volume from all sell orders with price lower than fair_for_bid
            clear_quantity = sum(
                abs(volume)
                for price, volume in order_depth.sell_orders.items()
                if price <= fair_for_bid
            )
            clear_quantity = min(clear_quantity, abs(position_after_take))
            sent_quantity = min(buy_quantity, clear_quantity)
            if sent_quantity > 0:
                orders.append(Order(product, fair_for_bid, abs(sent_quantity)))
                buy_order_volume += abs(sent_quantity)

        return orders, buy_order_volume, sell_order_volume
    def clear_orders(
        self,
        orders,
        product: str,
        order_depth: OrderDepth,
        fair_value: float,
        clear_width: int,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
    ) :
        orders, buy_order_volume[product], sell_order_volume[product] = self.clear_position_order(
            product,
            fair_value,
            clear_width,
            orders,
            order_depth,
            position,
            buy_order_volume[product],
            sell_order_volume[product],
        )
        return orders, buy_order_volume, sell_order_volume

    def wmid(self, order_depths, product):
        order_depth = order_depths[product]
        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        best_bid_vol = abs(order_depth.buy_orders[best_bid])
        best_ask_vol = abs(order_depth.sell_orders[best_ask])
        if(product in []):
            return (best_bid * best_ask_vol + best_ask * best_bid_vol) / (best_bid_vol + best_ask_vol)
        else:
            return (best_bid + best_ask) /2
    
    def implied_basket_volume(self, order_depths, pos, basket_weights, prods):
        depths = {p: order_depths[p] for p in prods}

        bids = {p: max(depths[p].buy_orders) for p in prods}
        asks = {p: min(depths[p].sell_orders) for p in prods}
        mids = {p: self.wmid(order_depths, p) for p in prods}
        bid_vols = {p: depths[p].buy_orders[bids[p]] for p in prods}
        ask_vols = {p: depths[p].sell_orders[asks[p]] for p in prods}
        buy_volume = 10000
        for p in basket_weights.keys():
            ask_volume = abs(ask_vols.get(p, 0))
            buy_volume = min(buy_volume, math.floor(ask_volume / basket_weights[p]), (self.position_limit[p] - pos.get(p, 0)) // basket_weights[p])
        sell_volume = 1000
        for p in basket_weights.keys():
            bid_volume = bid_vols.get(p, 0)
            sell_volume = min(sell_volume, math.floor(bid_volume / basket_weights[p]), (self.position_limit[p] + pos.get(p, 0)) // basket_weights[p])

        return buy_volume, sell_volume

    def update_price_history(self, order_depths, prods):
        depths = {p: order_depths[p] for p in prods}
        if not all(d.buy_orders and d.sell_orders for d in depths.values()):
            return None
        mids = {p: self.wmid(order_depths, p) for p in prods}
        for p in prods:
            if p not in self.price_history.keys():
               self.price_history[p] = []
            else:
                self.price_history[p].append(mids[p])
    def etf_b1(self, order_depths, pos, orders, buy_order_volume, sell_order_volume, prods):
        self.time_remaining_etf1 = max(self.time_remaining_etf1 - 1, 0)
        if not all(p in order_depths for p in prods):
            return orders, buy_order_volume, sell_order_volume
    
        depths = {p: order_depths[p] for p in prods}
        if not all(d.buy_orders and d.sell_orders for d in depths.values()):
            return {}, 0, ""

        bids = {p: max(depths[p].buy_orders) for p in prods}
        asks = {p: min(depths[p].sell_orders) for p in prods}
        mids = {p: self.wmid(order_depths, p) for p in prods}
        bid_vols = {p: depths[p].buy_orders[bids[p]] for p in prods}
        ask_vols = {p: depths[p].sell_orders[asks[p]] for p in prods}
        # TODO: check whether to change the method for calculating nav
        nav = 6 * mids["CROISSANTS"] + 3 * mids["JAMS"] + mids["DJEMBES"]
        spread = mids["PICNIC_BASKET1"] - nav
        
        implied_buy_volume, implied_sell_volume = self.implied_basket_volume(order_depths=order_depths, pos=pos, basket_weights=self.b1_weights, prods=prods)
        if(len(self.spread_history) >= 100):
            spread_mean = statistics.mean(self.spread_history[-self.time_frame:])
            spread_vol = statistics.stdev(self.spread_history[-self.time_frame:])
            spread_z_score = (spread - spread_mean) / spread_vol
        elif len(self.spread_history) >= 2:
            spread_vol = 80
            spread_mean = statistics.mean(self.spread_history[-self.time_frame:])
            spread_z_score = (spread - spread_mean) / spread_vol
        else:
            spread_z_score = 0
            
        self.spread_history.append(spread)
        v = self.volume

        # TODO: tune self.volume & self.threshold
        if abs(spread_z_score) > self.z_score_threshold:
            if  spread > 0 and spread_z_score > self.z_score_threshold:
                vol = min(v, bid_vols["PICNIC_BASKET1"], self.position_limit["PICNIC_BASKET1"] + pos.get("PICNIC_BASKET1", 0))
                if vol > 0:
                    self.time_remaining_etf1 = 100
                    orders.append(Order("PICNIC_BASKET1", bids["PICNIC_BASKET1"], -vol))
                    sell_order_volume['PICNIC_BASKET1'] += vol
                # for prod, nums in [("CROISSANTS", 6), ("JAMS", 3), ("DJEMBES", 1)]:
                #     vol = min(nums * vol, -ask_vols[prod], self.position_limit[prod] - pos.get(prod, 0))
                #     if vol > 0:
                #         orders.append(Order(prod, asks[prod], vol))
                #         buy_order_volume[prod] += vol

            elif  spread  < 0 and spread_z_score < -self.z_score_threshold:
                vol = min(v, -ask_vols["PICNIC_BASKET1"], self.position_limit["PICNIC_BASKET1"] - pos.get("PICNIC_BASKET1", 0))
                if vol > 0:
                    self.time_remaining_etf1 = 100
                    orders.append(Order("PICNIC_BASKET1", asks["PICNIC_BASKET1"], vol))
                    buy_order_volume['PICNIC_BASKET1'] += vol
                # for prod, nums in [("CROISSANTS", 6), ("JAMS", 3), ("DJEMBES", 1)]:
                #     vol = min(nums * vol, bid_vols[prod], self.position_limit[prod] + pos.get(prod, 0))
                #     if vol > 0:
                #         orders.append(Order(prod, bids[prod], -vol))
                #         sell_order_volume[prod] += vol
            # elif abs(spread_z_score) < 0.5 * self.z_score_threshold:
            #     for p in [prods[0]]:
            #         fair_value = nav
            #         orders, buy_order_volume, sell_order_volume = self.clear_orders(orders, p, order_depths[p], fair_value, 1, pos.get(p, 0), buy_order_volume, sell_order_volume)

        return orders, buy_order_volume, sell_order_volume
    
    def etf_b2(self, order_depths, pos, orders, buy_order_volume, sell_order_volume, prods):
        self.time_remaining = max(self.time_remaining - 1, 0)
    
        depths = {p: order_depths[p] for p in prods}
        if not all(d.buy_orders and d.sell_orders for d in depths.values()):
            return orders, buy_order_volume, sell_order_volume

        bids = {p: max(depths[p].buy_orders.keys()) for p in prods}
        asks = {p: min(depths[p].sell_orders.keys()) for p in prods}
        mids = {p: self.wmid(order_depths, p) for p in prods}
        bid_vols = {p: depths[p].buy_orders[bids[p]] for p in prods}
        ask_vols = {p: depths[p].sell_orders[asks[p]] for p in prods}
        for p in prods:
            if p not in self.price_history.keys():
               self.price_history[p] = []
            else:
                self.price_history[p].append(mids[p])
        # TODO: check whether to change the method for calculating nav
        nav = 4 * mids["CROISSANTS"] + 2 * mids["JAMS"] 
        spread = mids["PICNIC_BASKET2"] - nav
        
        implied_buy_volume, implied_sell_volume = self.implied_basket_volume(order_depths=order_depths, pos=pos, basket_weights=self.b1_weights, prods=prods)
        if(len(self.spread_history2) >= 100):
            spread_mean = statistics.mean(self.spread_history2[-self.time_frame:])
            spread_vol = statistics.stdev(self.spread_history2[-self.time_frame:])
            spread_z_score = (spread - spread_mean) / spread_vol
        elif len(self.spread_history2) >= 2:
            spread_vol = 50
            spread_mean = statistics.mean(self.spread_history2[-self.time_frame:]) 
            spread_z_score = (spread - spread_mean) / spread_vol
        else:
            spread_z_score = 0
        self.spread_history2.append(spread)
        v = self.volume

        # TODO: tune self.volume & self.threshold
        if abs(spread_z_score) > self.z_score_threshold_etf2:
            if  spread > 0 and spread_z_score > self.z_score_threshold_etf2:
                vol = min(v, bid_vols["PICNIC_BASKET2"], self.position_limit["PICNIC_BASKET2"] + pos.get("PICNIC_BASKET2", 0))
                
                if vol > 0:
                    orders.append(Order("PICNIC_BASKET2", bids["PICNIC_BASKET2"], -vol))
                    self.time_remaining = 100
                    sell_order_volume['PICNIC_BASKET2'] += vol
                # for prod, nums in [("CROISSANTS", 6), ("JAMS", 3), ("DJEMBES", 1)]:
                #     vol = min(nums * vol, -ask_vols[prod], self.position_limit[prod] - pos.get(prod, 0))
                #     if vol > 0:
                #         orders.append(Order(prod, asks[prod], vol))
                #         buy_order_volume[prod] += vol

            elif  spread  < 0 and spread_z_score < -self.z_score_threshold_etf2:
                vol = min(v, -ask_vols["PICNIC_BASKET2"], self.position_limit["PICNIC_BASKET2"] - pos.get("PICNIC_BASKET2", 0))
                if vol > 0:
                    orders.append(Order("PICNIC_BASKET2", asks["PICNIC_BASKET2"], vol))
                    self.time_remaining = 100
                    buy_order_volume['PICNIC_BASKET2'] += vol
                # for prod, nums in [("CROISSANTS", 6), ("JAMS", 3), ("DJEMBES", 1)]:
                #     vol = min(nums * vol, bid_vols[prod], self.position_limit[prod] + pos.get(prod, 0))
                #     if vol > 0:
                #         orders.append(Order(prod, bids[prod], -vol))
                #         sell_order_volume[prod] += vol
        # elif abs(spread_z_score) < 0.25 * self.z_score_threshold:
        #     for p in [prods[0]]:
        #         fair_value = nav
        #         orders, buy_order_volume, sell_order_volume = self.clear_orders(orders, p, order_depths[p], fair_value, 2, pos.get(p, 0), buy_order_volume, sell_order_volume)

        return orders, buy_order_volume, sell_order_volume
    
    def jams(self, orders, state, buy_order_volume, sell_order_volume, product = "JAMS"):
        if product not in state.order_depths:
            return orders, buy_order_volume, sell_order_volume

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return orders, buy_order_volume, sell_order_volume

        best_bid = max(order_depth.buy_orders)
        best_ask = min(order_depth.sell_orders)
        mid_price = (best_bid + best_ask) / 2

        if len(self.price_history[product]) > 120:
            self.price_history[product] = self.price_history[product][-120:]

        if len(self.price_history[product]) < self.jam_window:
            return orders, buy_order_volume, sell_order_volume

        # using SMA
        fair_value = int(sum(self.price_history[product][-self.jam_window:]) / self.jam_window)
        pos = state.position.get(product, 0)

        # try to buy
        buy_price = fair_value - self.jam_spread
        if pos < self.position_limit[product]:
            volume = min(self.jam_volume, self.position_limit[product] - pos)
            orders.append(Order(product, buy_price, volume))

        # try to sell
        sell_price = fair_value + self.jam_spread
        if pos > -self.position_limit[product]:
            volume = min(self.jam_volume, pos + self.position_limit[product])
            orders.append(Order(product, sell_price, -volume))

        return orders, buy_order_volume, sell_order_volume


    
    
    def KELP_fair_value(self, order_depths: OrderDepth, product, traderObject) -> float:
        order_depth = order_depths[product]
        if len(order_depth.sell_orders) != 0 and len(order_depth.buy_orders) != 0:
            best_ask = min(order_depth.sell_orders.keys())
            best_bid = max(order_depth.buy_orders.keys())
            filtered_ask = [
                price
                for price in order_depth.sell_orders.keys()
                if abs(order_depth.sell_orders[price])
                >= self.kelp_adverse_volume
            ]
            filtered_bid = [
                price
                for price in order_depth.buy_orders.keys()
                if abs(order_depth.buy_orders[price])
                >= self.kelp_adverse_volume
            ]
            mm_ask = min(filtered_ask) if len(filtered_ask) > 0 else None
            mm_bid = max(filtered_bid) if len(filtered_bid) > 0 else None
            if mm_ask == None or mm_bid == None:
                if traderObject.get("KELP_last_price", None) == None:
                    mmmid_price = (best_ask + best_bid) / 2
                else:
                    mmmid_price = traderObject["KELP_last_price"]
            else:
                mmmid_price = (mm_ask + mm_bid) / 2

            if traderObject.get("KELP_last_price", None) != None:
                last_price = traderObject["KELP_last_price"]
                last_returns = (mmmid_price - last_price) / last_price
                pred_returns = (
                    last_returns * self.kelp_reversion_param
                )
                fair = mmmid_price + (mmmid_price * pred_returns)
            else:
                fair = mmmid_price
            traderObject["KELP_last_price"] = mmmid_price
            return fair
        return None
    
    def make_djembes_orders(
        self,
        orders,
        order_depth: OrderDepth,
        fair_value: float,
        join_edge: float,
        default_edge, 
        position: int,
        buy_order_volume,
        sell_order_volume,
        product,
        disregard_edge = 15,
        manage_position = False,
        soft_position_limit: int = 0,
    ):
        
        asks_above_fair = [
            price
            for price in order_depth.sell_orders.keys()
            if price > fair_value + disregard_edge
        ]
        bids_below_fair = [
            price
            for price in order_depth.buy_orders.keys()
            if price < fair_value - disregard_edge
        ]

        best_ask_above_fair = min(asks_above_fair) if len(asks_above_fair) > 0 else None
        best_bid_below_fair = max(bids_below_fair) if len(bids_below_fair) > 0 else None

        ask = round(fair_value + default_edge)
        if best_ask_above_fair != None:
            if abs(best_ask_above_fair - fair_value) <= join_edge:
                ask = best_ask_above_fair  # join
            else:
                ask = best_ask_above_fair - 1  # penny

        bid = round(fair_value - default_edge)
        if best_bid_below_fair != None:
            if abs(fair_value - best_bid_below_fair) <= join_edge:
                bid = best_bid_below_fair
            else:
                bid = best_bid_below_fair + 1

        if manage_position:
            if position > soft_position_limit:
                ask -= 1
            elif position < -1 * soft_position_limit:
                bid += 1
        buy_order_volume[product], sell_order_volume[product] = self.market_make(
            product,
            orders,
            bid,
            ask,
            position,
            buy_order_volume[product],
            sell_order_volume[product],
        )

        return orders, buy_order_volume, sell_order_volume
    
    def djembes(self, state, product, orders, buy_order_volume, sell_order_volume, traderObject):
        djembes_history = []

        if traderObject:
            try:
                djembes_history = traderObject.get("djembes_history", [])
            except:
                djembes_history = []
        
        if product not in state.order_depths:
            traderObject['djembes_history'] = djembes_history
            return orders, buy_order_volume, sell_order_volume

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            traderObject['djembes_history'] = djembes_history
            return orders, buy_order_volume, sell_order_volume

        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid_price = (best_bid + best_ask) / 2
        djembes_history.append(mid_price)

        if len(djembes_history) <= self.djembes_window_size:
            traderObject['djembes_history'] = djembes_history
            return orders, buy_order_volume, sell_order_volume
        else:
            djembes_history = djembes_history[-self.djembes_window_size:]

        momentum = djembes_history[-1] - djembes_history[-self.djembes_window_size]
        pos = state.position.get(product, 0)

        if momentum > self.djembes_threshold and pos < self.position_limit[product]:
            ask_volume = -order_depth.sell_orders[best_ask]
            volume = min(self.djembes_volume, ask_volume, self.position_limit[product] - pos)
            if volume > 0:
                orders.append(Order(product, best_ask, volume))
        elif momentum < -self.djembes_threshold and pos > -self.position_limit[product]:
            bid_volume = order_depth.buy_orders[best_bid]
            volume = min(self.djembes_volume, bid_volume, pos + self.position_limit[product])
            if volume > 0:
                orders.append(Order(product, best_bid, -volume))
        
        traderObject['djembes_history'] = djembes_history
        return orders, buy_order_volume, sell_order_volume

    
    def kelp(self, state, product, orders, buy_order_volume, sell_order_volume, traderObject):
        if product in state.order_depths:
            position = ( state.position[product] if product in state.position else 0)
            djembes_fair_value = self.KELP_fair_value(state.order_depths, product, traderObject)
            self.take_orders(
                orders,
                product,
                state.order_depths[product],
                djembes_fair_value,
                1,
                position,
                buy_order_volume,
                sell_order_volume,
                True,
                self.djembes_adverse_volume
            )
            self.clear_orders(
                orders,
                product,
                state.order_depths[product],
                djembes_fair_value,
                0,
                position,
                buy_order_volume,
                sell_order_volume,
            )
        
            self.make_orders(
                orders,
                product,
                state.order_depths[product],
                djembes_fair_value,
                position,
                buy_order_volume[product],
                sell_order_volume[product],
                1,
                0,
                1
            )
        return orders, buy_order_volume, sell_order_volume

    def make_rainforest_resin_orders(
        self,
        order_depth: OrderDepth,
        fair_value: int,
        position: int,
        buy_order_volume: int,
        sell_order_volume: int,
        volume_limit: int,
        product,
        orders
    ) :
        if(len(order_depth.sell_orders.keys()) == 0):
            return orders, buy_order_volume, sell_order_volume
        baaf = [price for price in order_depth.sell_orders.keys() if price > fair_value + 1]
        baaf = min(baaf) if len(baaf) > 0 else 1e6
        bbbf = [price for price in order_depth.buy_orders.keys() if price < fair_value - 1]
        bbbf = max(bbbf) if len(bbbf) > 0 else 0

        if baaf <= fair_value + 2:
            if position <= volume_limit:
                baaf = fair_value + 3  # still want edge 2 if position is not a concern

        if bbbf >= fair_value - 2:
            if position >= -volume_limit:
                bbbf = fair_value - 3  # still want edge 2 if position is not a concern

        buy_order_volume[product], sell_order_volume[product] = self.market_make(
            product,
            orders,
            bbbf + 1,
            baaf - 1,
            position,
            buy_order_volume[product],
            sell_order_volume[product],
        )
        return orders, buy_order_volume, sell_order_volume
    def rainforest_resin(self, state, product, orders, buy_order_volume, sell_order_volume):
        if product in state.order_depths:
            position = (
                state.position[product]
                if product in state.position
                else 0
            )
            orders, buy_order_volume, sell_order_volume = (
                self.take_orders(
                    orders,
                    product,
                    state.order_depths[product],
                    10000,
                    1,
                    position,
                    buy_order_volume,
                    sell_order_volume
                )
            )
            orders, buy_order_volume, sell_order_volume = self.make_rainforest_resin_orders(
                state.order_depths[product],
                10000,
                position,
                buy_order_volume,
                sell_order_volume,
                50,
                product,
                orders
            )
        return orders, buy_order_volume, sell_order_volume
    
    def run(self, state: TradingState):
        traderObject = {}
        if state.traderData != None and state.traderData != "":
            traderObject = jsonpickle.decode(state.traderData)
        orders = []
        buy_order_volume = {}
        sell_order_volume = {}
        prods = ["PICNIC_BASKET1", "CROISSANTS", "JAMS", "DJEMBES"]
        prods2 = ["PICNIC_BASKET2", "CROISSANTS", "JAMS"]
        for p in self.goods:
            buy_order_volume[p] = 0
            sell_order_volume[p] = 0
        
        self.update_price_history(state.order_depths, self.goods)
        orders, result = self.voucher_trade(state, orders, traderObject)
        orders, buy_order_volume, sell_order_volume = self.etf_b1(state.order_depths, state.position, orders, buy_order_volume, sell_order_volume, prods)
        orders, buy_order_volume, sell_order_volume = self.etf_b2(state.order_depths, state.position, orders, buy_order_volume, sell_order_volume, prods2)
        orders, buy_order_volume, sell_order_volume = self.jams(orders, state, buy_order_volume, sell_order_volume, 'JAMS')
        orders, buy_order_volume, sell_order_volume = self.djembes(state, 'DJEMBES', orders, buy_order_volume, sell_order_volume, traderObject)
        orders, buy_order_volume, sell_order_volume = self.kelp(state, 'KELP', orders, buy_order_volume, sell_order_volume, traderObject)
        orders, buy_order_volume, sell_order_volume = self.rainforest_resin(state, 'RAINFOREST_RESIN', orders, buy_order_volume, sell_order_volume)
        orders, buy_order_volume, sell_order_volume = self.squid(state, orders, buy_order_volume, sell_order_volume, 'SQUID_INK')
        orders, buy_order_volume, sell_order_volume = self.croissant(state, orders, buy_order_volume, sell_order_volume, 'CROISSANTS')
        orders, buy_order_volume, sell_order_volume = self.rocks(state, "VOLCANIC_ROCK", orders, buy_order_volume, sell_order_volume)
        result = {}
        for o in orders:
            result.setdefault(o.symbol, []).append(o)
        traderData = jsonpickle.encode(traderObject)
        logger.flush(state, result, 0, traderData)
        return result, 0, traderData
