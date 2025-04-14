**Rocks & Vouchers: `optionsBLKSCH.py`**\
Website Simulation: 30,049\
BT match worse trades: 212,328\
BT normal: 167,330\
Note: calculation of fair price is important, if it is underestimated, then the PNL will increase much more but that is due to bias of the current data (i.e., short only again)


### TODO: robustness test (positive pnl on backtester for r1(or r2)~r3 using `--match-trades worse` and on web simulation):

PICNIC_BASKET1: ❌ **no trades dealed on website simulation**\
PICNIC_BASKET2: ❌ **negative pnl on website simulation**\
SQUID_INK: ✅ tests all passed, unchanged from round2, `squidMarketMaking.py` \
DJEMBES: ❌ **negative pnl on website simulation** \
CROISSANTS: ❌ even **not passing backtester** \
JAMS: ❌ all short strategy\
KELP & RESIN: ✅
