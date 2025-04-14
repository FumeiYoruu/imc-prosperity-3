import numpy as np

turtle1 = np.arange(160, 200.1, 0.1)
turtle2 = np.arange(250.0,320.1,0.1)


for average in range(250,320):
    profitmax = -1
    best_price = (0,0)
    for price1 in np.arange(160,200):
        for price2 in np.arange(250,320):
            profit = 0
            for turtle in turtle1:
                if price1 > turtle:
                    profit += 320-price1
                elif price2 > turtle and price2 < average:
                    profit += (320-price2)*(((320-average)/(320-price2))**3)
                elif price2 > turtle and price2 >= average:
                    profit += (320-price2)
            for turtle in turtle2:
                if price1 > turtle:
                    profit += 320-price1
                elif price2 > turtle and price2 < average:
                    profit += (320-price2)*(((320-average)/(320-price2))**3)
                elif price2 > turtle and price2 >= average:
                    profit += (320-price2)
            if profit>profitmax:
                profitmax = profit
                best_price = (price1, price2)

    for price1 in np.arange(250,320):
        for price2 in np.arange(price1,320):
            profit = 0
            for turtle in turtle1:
                if price1 > turtle:
                    profit += 320-price1
                elif price2 > turtle and price2 < average:
                    profit += (320-price2)*(((320-average)/(320-price2))**3)
                elif price2 > turtle and price2 >= average:
                    profit += (320-price2)
            for turtle in turtle2:
                if price1 > turtle:
                    profit += 320-price1
                elif price2 > turtle and price2 < average:
                    profit += (320-price2)*(((320-average)/(320-price2))**3)
                elif price2 > turtle and price2 >= average:
                    profit += (320-price2)
            if profit>profitmax:
                profitmax = profit
                best_price = (price1, price2)

    print("Average: ", average, " Best: ", best_price, " Profit: ", profitmax)


"""
Output: (just so you don't have to run it again)
Average:  250  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  251  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  252  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  253  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  254  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  255  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  256  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  257  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  258  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  259  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  260  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  261  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  262  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  263  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  264  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  265  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  266  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  267  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  268  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  269  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  270  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  271  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  272  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  273  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  274  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  275  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  276  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  277  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  278  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  279  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  280  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  281  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  282  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  283  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  284  Best:  (np.int64(199), np.int64(284))  Profit:  59947
Average:  285  Best:  (np.int64(199), np.int64(285))  Profit:  59946
Average:  286  Best:  (np.int64(199), np.int64(286))  Profit:  59925
Average:  287  Best:  (np.int64(199), np.int64(287))  Profit:  59884
Average:  288  Best:  (np.int64(199), np.int64(288))  Profit:  59823
Average:  289  Best:  (np.int64(199), np.int64(289))  Profit:  59742
Average:  290  Best:  (np.int64(199), np.int64(290))  Profit:  59641
Average:  291  Best:  (np.int64(199), np.int64(291))  Profit:  59520
Average:  292  Best:  (np.int64(199), np.int64(292))  Profit:  59379
Average:  293  Best:  (np.int64(199), np.int64(293))  Profit:  59218
Average:  294  Best:  (np.int64(199), np.int64(294))  Profit:  59037
Average:  295  Best:  (np.int64(199), np.int64(295))  Profit:  58836
Average:  296  Best:  (np.int64(199), np.int64(296))  Profit:  58615
Average:  297  Best:  (np.int64(199), np.int64(297))  Profit:  58374
Average:  298  Best:  (np.int64(199), np.int64(298))  Profit:  58113
Average:  299  Best:  (np.int64(199), np.int64(299))  Profit:  57832
Average:  300  Best:  (np.int64(199), np.int64(300))  Profit:  57531
Average:  301  Best:  (np.int64(199), np.int64(301))  Profit:  57210
Average:  302  Best:  (np.int64(199), np.int64(302))  Profit:  56869
Average:  303  Best:  (np.int64(199), np.int64(303))  Profit:  56508
Average:  304  Best:  (np.int64(199), np.int64(304))  Profit:  56127
Average:  305  Best:  (np.int64(199), np.int64(305))  Profit:  55726
Average:  306  Best:  (np.int64(199), np.int64(306))  Profit:  55305
Average:  307  Best:  (np.int64(199), np.int64(307))  Profit:  54864
Average:  308  Best:  (np.int64(199), np.int64(308))  Profit:  54403
Average:  309  Best:  (np.int64(199), np.int64(309))  Profit:  53922
Average:  310  Best:  (np.int64(199), np.int64(310))  Profit:  53421
Average:  311  Best:  (np.int64(199), np.int64(311))  Profit:  52900
Average:  312  Best:  (np.int64(199), np.int64(312))  Profit:  52359
Average:  313  Best:  (np.int64(199), np.int64(313))  Profit:  51798
Average:  314  Best:  (np.int64(199), np.int64(314))  Profit:  51217
Average:  315  Best:  (np.int64(199), np.int64(315))  Profit:  50616
Average:  316  Best:  (np.int64(199), np.int64(316))  Profit:  49995
Average:  317  Best:  (np.int64(199), np.int64(317))  Profit:  49354
Average:  318  Best:  (np.int64(199), np.int64(318))  Profit:  48693
Average:  319  Best:  (np.int64(199), np.int64(319))  Profit:  48012
"""
