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
                      "VOLCANIC_ROCK_VOUCHER_9500", "VOLCANIC_ROCK_VOUCHER_9750", "VOLCANIC_ROCK_VOUCHER_10000", "VOLCANIC_ROCK_VOUCHER_10250", "VOLCANIC_ROCK_VOUCHER_10500", 'MAGNIFICENT_MACARONS']
        self.vouchers_settings = {
            "VOLCANIC_ROCK_VOUCHER_9500":  {"strike": 9500,  "volume": 30, "window": 50, "spread": 4},
            "VOLCANIC_ROCK_VOUCHER_9750":  {"strike": 9750,  "volume": 30, "window": 50, "spread": 4},
            "VOLCANIC_ROCK_VOUCHER_10000": {"strike": 10000, "volume": 30, "window": 50, "spread": 4},
            "VOLCANIC_ROCK_VOUCHER_10250": {"strike": 10250, "volume": 10, "window": 50, "spread": 4},
            "VOLCANIC_ROCK_VOUCHER_10500": {"strike": 10500, "volume": 10, "window": 20, "spread": 3},
        }
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
            "MAGNIFICENT_MACARONS" : 75,
        }
        self.etf_components1 = {
            "CROISSANTS": 6,
            "JAMS": 3,
            "DJEMBES": 1,
        }
        self.etf_components2 = {
            "CROISSANTS": 4,
            "JAMS": 2,
        }
        self.price_history = {}
        self.kelp_reversion_param = -0.229
        self.kelp_adverse_volume = 20
        self.djembes_window_size = 20
        self.djembes_threshold = 9.5
        self.djembes_volume = 20
        self.rock_volume = 25
        self.vouchers_limit = 200
        self.vouchers_history = {k: [] for k in self.vouchers_settings}
        
        self.vouchers_ema = {k: None for k in self.vouchers_settings}
        self.vouchers_alpha = {k: 2 / (cfg["window"] + 1) for k, cfg in self.vouchers_settings.items()}
        
        self.voucher_z_threshold = 5.20

        self.rock_window = 120
        self.rock_spread = 3
        self.rock_alpha = 2 / (self.rock_window + 1)
        self.b1_time_frame = 100
        self.b1_volume = 30
        self.b1_z_score_threshold = 1
        self.b1_warm_up_threshold = 2
        self.b2_time_frame = 150
        self.b2_volume = 50
        self.b2_z_score_threshold = 1.5
        self.b2_warm_up_threshold = 2
        self.b2_momentum_window = 30



    
    def voucher_trade(self, state, orders, traderObject):
        voucher_history = {}

        if traderObject:
            try:
                voucher_history = traderObject.get("voucher_history", {})
            except:
                voucher_history = {}

        if voucher_history == {}:
            voucher_history = {k: [] for k in self.vouchers_settings}

        for symbol, cfg in self.vouchers_settings.items():
            pos = state.position.get(symbol, 0)
            od = state.order_depths.get(symbol)
            if not od or not od.buy_orders or not od.sell_orders:
                continue

            vol = cfg["volume"]
            spread = cfg["spread"]
            
            best_bid = max(od.buy_orders)
            best_ask = min(od.sell_orders)
            mid = (best_bid + best_ask) / 2
            voucher_history[symbol].append(mid)
            if len(voucher_history[symbol]) > cfg["window"]:
                voucher_history[symbol].pop(0)

            # EMA
            a = self.vouchers_alpha[symbol]
            prev_ema = self.vouchers_ema[symbol]
            ema = mid if prev_ema is None else (a * mid + (1 - a) * prev_ema)
            self.vouchers_ema[symbol] = ema

            # Z-score
            hist_window = voucher_history[symbol][-cfg["window"]:]
            std = np.std(hist_window) if len(hist_window) >= 2 else 1e-6
            z = (mid - ema) / std if std > 1e-6 else 0

            # market making
            if abs(z) < self.voucher_z_threshold:
                fv = int(ema)
                if pos < self.vouchers_limit:
                    orders.append(Order(symbol, fv - spread, min(vol, self.vouchers_limit - pos)))
                if pos > -self.vouchers_limit:
                    orders.append(Order(symbol, fv + spread, -min(vol, pos + self.vouchers_limit)))

            # trend up, cover short & make long
            elif z >= self.voucher_z_threshold:
                if pos < 0:
                    # TODO: whether use best_ask instead for faster execution
                    orders.append(Order(symbol, best_bid, min(vol, -pos)))
                if pos < self.vouchers_limit:
                    orders.append(Order(symbol, best_ask, min(vol, self.vouchers_limit - pos)))

            # trend down, cover long & make short
            elif z <= -self.voucher_z_threshold:
                if pos > 0:
                    # TODO: whether use best_bid instead for faster execution
                    orders.append(Order(symbol, best_ask, -min(vol, pos)))
                if pos > -self.vouchers_limit:
                    orders.append(Order(symbol, best_bid, -min(vol, pos + self.vouchers_limit)))\
        
        traderObject['voucher_history'] = voucher_history
        return orders, traderObject


    
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

    def rocks(self, state, product, orders, traderObject):
        rock_ema = None
        if traderObject:
            try:
                rock_ema = traderObject.get("rock_ema", None)
            except:
                rock_ema = None
        if product not in state.order_depths:
            return orders

        order_depth = state.order_depths[product]
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return orders
        
        best_bid = max(order_depth.buy_orders)
        best_ask = min(order_depth.sell_orders)
        mid_price = (best_bid + best_ask) / 2
        pos = state.position.get(product, 0)


        if rock_ema is None:
            rock_ema = mid_price
        else:
            rock_ema = self.rock_alpha * mid_price + (1 - self.rock_alpha) * rock_ema
        traderObject['rock_ema'] = rock_ema
        # market making
        fair_value = int(rock_ema)
        buy_price = fair_value - self.rock_spread
        sell_price = fair_value + self.rock_spread

        if pos < self.position_limit[product]:
            buy_vol = min(self.rock_volume, self.position_limit[product] - pos)
            orders.append(Order(product, buy_price, buy_vol))
        if pos > -self.position_limit[product]:
            sell_vol = min(self.rock_volume, pos + self.position_limit[product])
            orders.append(Order(product, sell_price, -sell_vol))
        return orders, traderObject

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
        return (best_bid + best_ask) /2
    

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
                self.kelp_adverse_volume
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
    
    def calculate_z_score(self, spread, spread_history, warm_up_threshold, time_frame):
        if len(spread_history) < warm_up_threshold:
            return 0.0

        spread_history = spread_history[-time_frame:]

        mean = statistics.mean(spread_history)
        stdev = statistics.stdev(spread_history) if len(spread_history) >= 2 else 0.0

        return 0.0 if stdev == 0 else (spread - mean) / stdev

    def etf_b1(self, order_depths, pos, orders, buy_order_volume, sell_order_volume, prods, traderObject):
        b1_spread_history = []

        if traderObject:
            try:
                b1_spread_history = traderObject.get("b1_spread_history", [])
            except:
                b1_spread_history = []

        if not all(p in order_depths for p in prods):
            return orders, buy_order_volume, sell_order_volume, traderObject

        depths = {p: order_depths[p] for p in prods}

        if not all(d.buy_orders and d.sell_orders for d in depths.values()):
            return orders, buy_order_volume, sell_order_volume, traderObject

        etf_name = "PICNIC_BASKET1"

        bids = {p: max(depths[p].buy_orders) for p in prods}
        asks = {p: min(depths[p].sell_orders) for p in prods}
        mids = {p: self.wmid(order_depths, p) for p in prods}
        bid_vols = {p: depths[p].buy_orders[bids[p]] for p in prods}
        ask_vols = {p: depths[p].sell_orders[asks[p]] for p in prods}

        nav = sum(weight * mids[p] for p, weight in self.etf_components1.items())
        buy_nav = sum(weight * asks[p] for p, weight in self.etf_components1.items())
        sell_nav = sum(weight * bids[p] for p, weight in self.etf_components1.items())

        spread = mids[etf_name] - nav
        sell_spread = bids[etf_name] - buy_nav
        buy_spread = asks[etf_name] - sell_nav

        spread_z_score = self.calculate_z_score(spread, b1_spread_history, self.b1_warm_up_threshold, self.b1_time_frame)

        b1_spread_history.append(spread)
        b1_spread_history = b1_spread_history[-self.b1_time_frame:]
        traderObject['b1_spread_history'] = b1_spread_history

        if sell_spread > 0 and spread_z_score > self.b1_z_score_threshold:
            vol = min(self.b1_volume, bid_vols[etf_name], self.position_limit[etf_name] + pos.get(etf_name, 0))

            if vol > 0:
                orders.append(Order(etf_name, bids[etf_name], -vol))
                sell_order_volume[etf_name] += vol

        elif buy_spread < 0 and spread_z_score < -self.b1_z_score_threshold:
            vol = min(self.b1_volume, -ask_vols[etf_name], self.position_limit[etf_name] - pos.get(etf_name, 0))

            if vol > 0:
                orders.append(Order(etf_name, asks[etf_name], vol))
                buy_order_volume[etf_name] += vol

        return orders, buy_order_volume, sell_order_volume, traderObject

    def calculate_momentum(self, product):
        if len(self.price_history[product]) < self.b2_momentum_window:
            return 0.0
            
        recent_prices = self.price_history[product][-self.b2_momentum_window:]
        return recent_prices[-1] - recent_prices[-self.b2_momentum_window]


    def etf_b2(self, order_depths, pos, orders, buy_order_volume, sell_order_volume, prods, traderObject):
        b2_spread_history = []

        if traderObject:
            try:
                b2_spread_history = traderObject.get("b2_spread_history", [])
            except:
                b2_spread_history = []

        if not all(p in order_depths for p in prods):
            return orders, buy_order_volume, sell_order_volume, traderObject

        depths = {p: order_depths[p] for p in prods}

        if not all(d.buy_orders and d.sell_orders for d in depths.values()):
            return orders, buy_order_volume, sell_order_volume, traderObject

        etf_name = "PICNIC_BASKET2"


        bids = {p: max(depths[p].buy_orders) for p in prods}
        asks = {p: min(depths[p].sell_orders) for p in prods}
        mids = {p: self.wmid(order_depths, p) for p in prods}
        bid_vols = {p: depths[p].buy_orders[bids[p]] for p in prods}
        ask_vols = {p: depths[p].sell_orders[asks[p]] for p in prods}

        nav = sum(weight * mids[p] for p, weight in self.etf_components2.items())
        buy_nav = sum(weight * asks[p] for p, weight in self.etf_components2.items())
        sell_nav = sum(weight * bids[p] for p, weight in self.etf_components2.items())

        spread = mids[etf_name] - nav
        sell_spread = bids[etf_name] - buy_nav
        buy_spread = asks[etf_name] - sell_nav

        spread_z_score = self.calculate_z_score(spread, b2_spread_history, self.b2_warm_up_threshold, self.b2_time_frame)

        b2_spread_history.append(spread)
        b2_spread_history = b2_spread_history[-self.b2_time_frame:]
        traderObject['b2_spread_history'] = b2_spread_history


        component_momentum = {
            p: self.calculate_momentum(p) 
            for p in self.etf_components2.keys()
        }
        avg_momentum = 0
        for p, m in component_momentum.items():
            avg_momentum += self.etf_components2[p] * m
        
        momentum_threshold = 10
        if avg_momentum > momentum_threshold:
            # Positive momentum - buy basket
            vol = min(self.b2_volume, -ask_vols[etf_name], self.position_limit[etf_name] - pos.get(etf_name, 0))
            if vol > 0:
                orders.append(Order(etf_name, round(buy_nav) - 1, vol))
                buy_order_volume[etf_name] += vol
        elif avg_momentum < -momentum_threshold:
            # Negative momentum - sell basket
            vol = min(self.b2_volume, bid_vols[etf_name], self.position_limit[etf_name] + pos.get(etf_name, 0))
            if vol > 0:
                orders.append(Order(etf_name, round(sell_nav) + 1, -vol))
                sell_order_volume[etf_name] += vol

        # Statistical arbitrage as fallback when momentum is weak
        if abs(avg_momentum) < momentum_threshold/2:
            if sell_spread > 0 and spread_z_score > self.b2_z_score_threshold:
                vol = min(self.b2_volume, bid_vols[etf_name], self.position_limit[etf_name] + pos.get(etf_name, 0))
                if vol > 0:
                    orders.append(Order(etf_name, bids[etf_name], -vol))
                    sell_order_volume[etf_name] += vol

            elif buy_spread < 0 and spread_z_score < -self.b2_z_score_threshold:
                vol = min(self.b2_volume, -ask_vols[etf_name], self.position_limit[etf_name] - pos.get(etf_name, 0))
                if vol > 0:
                    orders.append(Order(etf_name, asks[etf_name], vol))
                    buy_order_volume[etf_name] += vol

        return orders, buy_order_volume, sell_order_volume, traderObject





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
        orders, buy_order_volume, sell_order_volume = self.kelp(state, 'KELP', orders, buy_order_volume, sell_order_volume, traderObject)
        orders, buy_order_volume, sell_order_volume = self.rainforest_resin(state, 'RAINFOREST_RESIN', orders, buy_order_volume, sell_order_volume)
        orders, buy_order_volume, sell_order_volume = self.djembes(state, 'DJEMBES', orders, buy_order_volume, sell_order_volume, traderObject)
        orders, buy_order_volume, sell_order_volume, traderObject = self.etf_b1(state.order_depths, state.position, orders,
                                                                  buy_order_volume, sell_order_volume, prods, traderObject)
        orders, buy_order_volume, sell_order_volume, traderObject = self.etf_b2(state.order_depths, state.position, orders,
                                                                   buy_order_volume, sell_order_volume, prods2, traderObject)
        orders, traderObject =  self.rocks(state, 'VOLCANIC_ROCK', orders, traderObject)
        orders, traderObject = self.voucher_trade(state, orders, traderObject)
        
        result = {}
        for o in orders:
            result.setdefault(o.symbol, []).append(o)
        traderData = jsonpickle.encode(traderObject)
        logger.flush(state, result, 0, "")
        return result, 0, traderData
