import numpy as np

turtle1 = np.arange(160, 200.1, 0.1)
turtle2 = np.arange(250.0,320.1,0.1)
profitmax = -1
best_price = (0,0)

for price1 in np.arange(160,200):
    print(price1)
    for price2 in np.arange(250,320):
        profit = 0
        for turtle in turtle1:
            if price1 > turtle:
                profit += 320-price1
            elif price2 > turtle:
                profit += 320-price2
        for turtle in turtle2:
            if price1 > turtle:
                profit += 320-price1
            elif price2 > turtle:
                profit += 320-price2
        if profit>profitmax:
            profitmax = profit
            best_price = (price1, price2)

for price1 in np.arange(250,320):
    print(price1)
    for price2 in np.arange(price1,320):
        profit = 0
        for turtle in turtle1:
            if price1 > turtle:
                profit += 320-price1
            elif price2 > turtle:
                profit += 320-price2
        for turtle in turtle2:
            if price1 > turtle:
                profit += 320-price1
            elif price2 > turtle:
                profit += 320-price2
        if profit>profitmax:
            profitmax = profit
            best_price = (price1, price2)

print(best_price)
print(profitmax)

#best assuming average is below 284:(199, 284)