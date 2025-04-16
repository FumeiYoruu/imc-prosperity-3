`kuasong.py` 1,728 on website\
`jams.py` 4,123 on website\
`djembes.py` 2,881 on website\
`rocks.py` ~20k on website\
`options.py` 36,169 on website\
`options_best.py`: 48,131 on website



**Rocks & Vouchers: `optionsBLKSCH.py`**\
Website Simulation: 30,049\
BT match worse trades: 212,328\
BT normal: 167,330\
**Note1**: calculation of fair price is important, if it is underestimated, then the PNL will increase much more but that is due to bias of the current data (i.e., short only again)\
**Note2**: rocks seem difficult to take orders in web simulation, so we might can use current file to do vouchers but another strategy for rocks (i have not found yet, all losing money)

file: options.py\
BT: 447k\
website: 36,169\
**Note**: overall pnl is similar but pnl curve is more stable/less dips

### TODO: robustness test (positive pnl on backtester for r1(or r2)~r3 using `--match-trades worse` and on web simulation):

PICNIC_BASKET1: ☑️ Unchanged from round2 \
PICNIC_BASKET2: ☑️ Fixed \
SQUID_INK: ✅ tests all passed, unchanged from round2, `squidMarketMaking.py` \
DJEMBES: ☑️ Fixed using momentum \
CROISSANTS: ☑️ Fixed using market making \
JAMS: ☑️ Fixed using market making \
KELP & RESIN: ✅
