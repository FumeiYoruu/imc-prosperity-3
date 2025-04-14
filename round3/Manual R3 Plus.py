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

for average in range(284,320):
    profitmax = -1
    best_price = (0,0)
    for price1 in np.arange(160,200):
        for price2 in np.arange(250,320):
            profit = 0
            for turtle in turtle1:
                if price1 > turtle:
                    profit += 0
                elif price2 > turtle and price2 < average:
                    profit += (320-price2)*(((320-average)/(320-price2))**3)
                elif price2 > turtle and price2 >= average:
                    profit += (320-price2)
            for turtle in turtle2:
                if price1 > turtle:
                    profit += 0
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
                    profit += 0
                elif price2 > turtle and price2 < average:
                    profit += (320-price2)*(((320-average)/(320-price2))**3)
                elif price2 > turtle and price2 >= average:
                    profit += (320-price2)
            for turtle in turtle2:
                if price1 > turtle:
                    profit += 0
                elif price2 > turtle and price2 < average:
                    profit += (320-price2)*(((320-average)/(320-price2))**3)
                elif price2 > turtle and price2 >= average:
                    profit += (320-price2)
            if profit>profitmax:
                profitmax = profit
                best_price = (price1, price2)

    print("Average: ", average, " Best Price2: ", best_price[1], " Profit: ", profitmax)

for price2 in range(284, 319, 2):
    price1 = 199
    print("-------------------", price2, "-------------------")
    for average in range(price2,320):
        profit = 0
        for turtle in turtle2:
            if price1 > turtle:
                profit += 0
            elif price2 > turtle and price2 < average:
                profit += (320-price2)*(((320-average)/(320-price2))**3)
            elif price2 > turtle and price2 >= average:
                profit += (320-price2)
        print("Average: ", average, " Profit: ", profit)
    print()

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





Average:  284  Best Price2:  284  Profit:  26712
Average:  285  Best Price2:  285  Profit:  26320
Average:  286  Best Price2:  286  Profit:  25908
Average:  287  Best Price2:  287  Profit:  25476
Average:  288  Best Price2:  288  Profit:  25024
Average:  289  Best Price2:  289  Profit:  24552
Average:  290  Best Price2:  290  Profit:  24060
Average:  291  Best Price2:  291  Profit:  23548
Average:  292  Best Price2:  292  Profit:  23016
Average:  293  Best Price2:  293  Profit:  22464
Average:  294  Best Price2:  294  Profit:  21892
Average:  295  Best Price2:  295  Profit:  21300
Average:  296  Best Price2:  296  Profit:  20688
Average:  297  Best Price2:  297  Profit:  20056
Average:  298  Best Price2:  298  Profit:  19404
Average:  299  Best Price2:  299  Profit:  18732
Average:  300  Best Price2:  300  Profit:  18040
Average:  301  Best Price2:  301  Profit:  17328
Average:  302  Best Price2:  302  Profit:  16596
Average:  303  Best Price2:  303  Profit:  15844
Average:  304  Best Price2:  304  Profit:  15072
Average:  305  Best Price2:  305  Profit:  14280
Average:  306  Best Price2:  306  Profit:  13468
Average:  307  Best Price2:  307  Profit:  12636
Average:  308  Best Price2:  308  Profit:  11784
Average:  309  Best Price2:  309  Profit:  10912
Average:  310  Best Price2:  310  Profit:  10020
Average:  311  Best Price2:  311  Profit:  9108
Average:  312  Best Price2:  312  Profit:  8176
Average:  313  Best Price2:  313  Profit:  7224
Average:  314  Best Price2:  314  Profit:  6252
Average:  315  Best Price2:  315  Profit:  5260
Average:  316  Best Price2:  316  Profit:  4248
Average:  317  Best Price2:  317  Profit:  3216
Average:  318  Best Price2:  318  Profit:  2164
Average:  319  Best Price2:  319  Profit:  1092





------------------- 284 -------------------
Average:  284  Profit:  12276
Average:  285  Profit:  11281.153549382778
Average:  286  Profit:  10341.561728395089
Average:  287  Profit:  9455.645833333341
Average:  288  Profit:  8621.82716049385
Average:  289  Profit:  7838.527006172778
Average:  290  Profit:  7104.166666666635
Average:  291  Profit:  6417.167438271565
Average:  292  Profit:  5775.950617283963
Average:  293  Profit:  5178.9375
Average:  294  Profit:  4624.54938271606
Average:  295  Profit:  4111.207561728382
Average:  296  Profit:  3637.333333333316
Average:  297  Profit:  3201.34799382715
Average:  298  Profit:  2801.6728395061486
Average:  299  Profit:  2436.729166666666
Average:  300  Profit:  2104.9382716049254
Average:  301  Profit:  1804.721450617275
Average:  302  Profit:  1534.5
Average:  303  Profit:  1292.695216049386
Average:  304  Profit:  1077.7283950617314
Average:  305  Profit:  888.0208333333294
Average:  306  Profit:  721.9938271604954
Average:  307  Profit:  578.0686728395075
Average:  308  Profit:  454.6666666666645
Average:  309  Profit:  350.2091049382686
Average:  310  Profit:  263.1172839506157
Average:  311  Profit:  191.8125
Average:  312  Profit:  134.71604938271642
Average:  313  Profit:  90.24922839506192
Average:  314  Profit:  56.833333333333066
Average:  315  Profit:  32.88966049382696
Average:  316  Profit:  16.839506172839553
Average:  317  Profit:  7.104166666666633
Average:  318  Profit:  2.104938271604944
Average:  319  Profit:  0.263117283950618

------------------- 286 -------------------
Average:  286  Profit:  12274
Average:  287  Profit:  11222.540657439347
Average:  288  Profit:  10232.91349480978
Average:  289  Profit:  9303.244809688493
Average:  290  Profit:  8431.660899654025
Average:  291  Profit:  7616.288062283759
Average:  292  Profit:  6855.252595155765
Average:  293  Profit:  6146.680795847707
Average:  294  Profit:  5488.6989619376745
Average:  295  Profit:  4879.433391003468
Average:  296  Profit:  4317.010380622833
Average:  297  Profit:  3799.5562283736995
Average:  298  Profit:  3325.197231833926
Average:  299  Profit:  2892.0596885813197
Average:  300  Profit:  2498.269896193784
Average:  301  Profit:  2141.954152249133
Average:  302  Profit:  1821.2387543252714
Average:  303  Profit:  1534.25
Average:  304  Profit:  1279.1141868512225
Average:  305  Profit:  1053.9576124567532
Average:  306  Profit:  856.9065743944707
Average:  307  Profit:  686.0873702422093
Average:  308  Profit:  539.6262975778541
Average:  309  Profit:  415.6496539792407
Average:  310  Profit:  312.283737024223
Average:  311  Profit:  227.65484429065893
Average:  312  Profit:  159.8892733564028
Average:  313  Profit:  107.11332179930884
Average:  314  Profit:  67.45328719723176
Average:  315  Profit:  39.035467128027875
Average:  316  Profit:  19.98615916955035
Average:  317  Profit:  8.43166089965397
Average:  318  Profit:  2.498269896193794
Average:  319  Profit:  0.31228373702422424

------------------- 288 -------------------
Average:  288  Profit:  12192
Average:  289  Profit:  11084.3466796875
Average:  290  Profit:  10045.8984375
Average:  291  Profit:  9074.4228515625
Average:  292  Profit:  8167.6875
Average:  293  Profit:  7323.4599609375
Average:  294  Profit:  6539.5078125
Average:  295  Profit:  5813.5986328125
Average:  296  Profit:  5143.5
Average:  297  Profit:  4526.9794921875
Average:  298  Profit:  3961.8046875
Average:  299  Profit:  3445.7431640625
Average:  300  Profit:  2976.5625
Average:  301  Profit:  2552.0302734375
Average:  302  Profit:  2169.9140625
Average:  303  Profit:  1827.9814453125
Average:  304  Profit:  1524.0
Average:  305  Profit:  1255.7373046875
Average:  306  Profit:  1020.9609375
Average:  307  Profit:  817.4384765625
Average:  308  Profit:  642.9375
Average:  309  Profit:  495.2255859375
Average:  310  Profit:  372.0703125
Average:  311  Profit:  271.2392578125
Average:  312  Profit:  190.5
Average:  313  Profit:  127.6201171875
Average:  314  Profit:  80.3671875
Average:  315  Profit:  46.5087890625
Average:  316  Profit:  23.8125
Average:  317  Profit:  10.0458984375
Average:  318  Profit:  2.9765625
Average:  319  Profit:  0.3720703125

------------------- 290 -------------------
Average:  290  Profit:  12030
Average:  291  Profit:  10866.654444444483
Average:  292  Profit:  9780.835555555595
Average:  293  Profit:  8769.869999999986
Average:  294  Profit:  7831.0844444444765
Average:  295  Profit:  6961.80555555561
Average:  296  Profit:  6159.359999999967
Average:  297  Profit:  5421.074444444415
Average:  298  Profit:  4744.275555555531
Average:  299  Profit:  4126.289999999988
Average:  300  Profit:  3564.444444444415
Average:  301  Profit:  3056.065555555545
Average:  302  Profit:  2598.4800000000064
Average:  303  Profit:  2189.0144444444336
Average:  304  Profit:  1824.9955555555625
Average:  305  Profit:  1503.75
Average:  306  Profit:  1222.6044444444494
Average:  307  Profit:  978.8855555555596
Average:  308  Profit:  769.9199999999959
Average:  309  Profit:  593.0344444444414
Average:  310  Profit:  445.55555555555185
Average:  311  Profit:  324.8100000000008
Average:  312  Profit:  228.12444444444532
Average:  313  Profit:  152.82555555555618
Average:  314  Profit:  96.23999999999948
Average:  315  Profit:  55.69444444444398
Average:  316  Profit:  28.515555555555665
Average:  317  Profit:  12.029999999999935
Average:  318  Profit:  3.564444444444458
Average:  319  Profit:  0.44555555555555726

------------------- 292 -------------------
Average:  292  Profit:  11788
Average:  293  Profit:  10569.570153061146
Average:  294  Profit:  9438.13265306118
Average:  295  Profit:  8390.465561224557
Average:  296  Profit:  7423.346938775453
Average:  297  Profit:  6533.554846938769
Average:  298  Profit:  5717.867346938769
Average:  299  Profit:  4973.0625
Average:  300  Profit:  4295.918367346931
Average:  301  Profit:  3683.2130102041183
Average:  302  Profit:  3131.724489795891
Average:  303  Profit:  2638.230867346924
Average:  304  Profit:  2199.510204081623
Average:  305  Profit:  1812.3405612244765
Average:  306  Profit:  1473.5
Average:  307  Profit:  1179.7665816326476
Average:  308  Profit:  927.9183673469316
Average:  309  Profit:  714.7334183673461
Average:  310  Profit:  536.9897959183663
Average:  311  Profit:  391.46556122448635
Average:  312  Profit:  274.9387755102029
Average:  313  Profit:  184.1875
Average:  314  Profit:  115.98979591836645
Average:  315  Profit:  67.12372448979579
Average:  316  Profit:  34.36734693877536
Average:  317  Profit:  14.498724489795807
Average:  318  Profit:  4.29591836734692
Average:  319  Profit:  0.536989795918365

------------------- 294 -------------------
Average:  294  Profit:  11466
Average:  295  Profit:  10193.23224852077
Average:  296  Profit:  9018.319526627241
Average:  297  Profit:  7937.347633136036
Average:  298  Profit:  6946.40236686396
Average:  299  Profit:  6041.569526627204
Average:  300  Profit:  5218.9349112425625
Average:  301  Profit:  4474.584319526611
Average:  302  Profit:  3804.6035502958325
Average:  303  Profit:  3205.0784023668584
Average:  304  Profit:  2672.0946745561996
Average:  305  Profit:  2201.7381656804637
Average:  306  Profit:  1790.0946745562212
Average:  307  Profit:  1433.25
Average:  308  Profit:  1127.2899408284052
Average:  309  Profit:  868.300295857995
Average:  310  Profit:  652.3668639053203
Average:  311  Profit:  475.57544378697906
Average:  312  Profit:  334.01183431952495
Average:  313  Profit:  223.76183431952765
Average:  314  Profit:  140.91124260355065
Average:  315  Profit:  81.54585798816504
Average:  316  Profit:  41.75147928994062
Average:  317  Profit:  17.61390532544383
Average:  318  Profit:  5.218934911242577
Average:  319  Profit:  0.6523668639053222

------------------- 296 -------------------
Average:  296  Profit:  11064
Average:  297  Profit:  9737.824652777706
Average:  298  Profit:  8522.09722222229
Average:  299  Profit:  7412.015625
Average:  300  Profit:  6402.777777777717
Average:  301  Profit:  5489.581597222277
Average:  302  Profit:  4667.625
Average:  303  Profit:  3932.1059027777383
Average:  304  Profit:  3278.222222222251
Average:  305  Profit:  2701.171875
Average:  306  Profit:  2196.1527777777806
Average:  307  Profit:  1758.3628472222124
Average:  308  Profit:  1383.0
Average:  309  Profit:  1065.2621527777862
Average:  310  Profit:  800.3472222222147
Average:  311  Profit:  583.453125
Average:  312  Profit:  409.77777777778135
Average:  313  Profit:  274.51909722222257
Average:  314  Profit:  172.875
Average:  315  Profit:  100.04340277777683
Average:  316  Profit:  51.22222222222267
Average:  317  Profit:  21.609375
Average:  318  Profit:  6.402777777777834
Average:  319  Profit:  0.8003472222222292

------------------- 298 -------------------
Average:  298  Profit:  10582
Average:  299  Profit:  9203.597107437921
Average:  300  Profit:  7950.413223140536
Average:  301  Profit:  6816.485537190043
Average:  302  Profit:  5795.851239669438
Average:  303  Profit:  4882.54752066113
Average:  304  Profit:  4070.6115702479756
Average:  305  Profit:  3354.0805785124157
Average:  306  Profit:  2726.99173553721
Average:  307  Profit:  2183.3822314049717
Average:  308  Profit:  1717.2892561983383
Average:  309  Profit:  1322.75
Average:  310  Profit:  993.801652892567
Average:  311  Profit:  724.4814049586797
Average:  312  Profit:  508.82644628099695
Average:  313  Profit:  340.87396694215124
Average:  314  Profit:  214.6611570247923
Average:  315  Profit:  124.22520661157087
Average:  316  Profit:  63.60330578512462
Average:  317  Profit:  26.832644628099036
Average:  318  Profit:  7.950413223140577
Average:  319  Profit:  0.9938016528925722

------------------- 300 -------------------
Average:  300  Profit:  10020
Average:  301  Profit:  8590.897499999995
Average:  302  Profit:  7304.57999999997
Average:  303  Profit:  6153.532500000013
Average:  304  Profit:  5130.239999999936
Average:  305  Profit:  4227.1875
Average:  306  Profit:  3436.860000000012
Average:  307  Profit:  2751.7424999999866
Average:  308  Profit:  2164.3199999999947
Average:  309  Profit:  1667.077500000017
Average:  310  Profit:  1252.5
Average:  311  Profit:  913.0724999999962
Average:  312  Profit:  641.279999999992
Average:  313  Profit:  429.6075000000015
Average:  314  Profit:  270.53999999999934
Average:  315  Profit:  156.5625
Average:  316  Profit:  80.159999999999
Average:  317  Profit:  33.81749999999992
Average:  318  Profit:  10.019999999999875
Average:  319  Profit:  1.2524999999999844

------------------- 302 -------------------
Average:  302  Profit:  9378
Average:  303  Profit:  7900.225308641997
Average:  304  Profit:  6586.469135802491
Average:  305  Profit:  5427.0833333333485
Average:  306  Profit:  4412.419753086452
Average:  307  Profit:  3532.830246913559
Average:  308  Profit:  2778.6666666666756
Average:  309  Profit:  2140.280864197509
Average:  310  Profit:  1608.0246913580102
Average:  311  Profit:  1172.25
Average:  312  Profit:  823.3086419753114
Average:  313  Profit:  551.5524691358065
Average:  314  Profit:  347.33333333333445
Average:  315  Profit:  201.00308641975127
Average:  316  Profit:  102.91358024691392
Average:  317  Profit:  43.416666666666806
Average:  318  Profit:  12.86419753086424
Average:  319  Profit:  1.60802469135803

------------------- 304 -------------------
Average:  304  Profit:  8656
Average:  305  Profit:  7132.32421875
Average:  306  Profit:  5798.84375
Average:  307  Profit:  4642.87890625
Average:  308  Profit:  3651.75
Average:  309  Profit:  2812.77734375
Average:  310  Profit:  2113.28125
Average:  311  Profit:  1540.58203125
Average:  312  Profit:  1082.0
Average:  313  Profit:  724.85546875
Average:  314  Profit:  456.46875
Average:  315  Profit:  264.16015625
Average:  316  Profit:  135.25
Average:  317  Profit:  57.05859375
Average:  318  Profit:  16.90625
Average:  319  Profit:  2.11328125

------------------- 306 -------------------
Average:  306  Profit:  7854
Average:  307  Profit:  6288.352040816242
Average:  308  Profit:  4945.959183673415
Average:  309  Profit:  3809.6479591836687
Average:  310  Profit:  2862.244897959208
Average:  311  Profit:  2086.5765306122184
Average:  312  Profit:  1465.4693877551097
Average:  313  Profit:  981.75
Average:  314  Profit:  618.2448979591769
Average:  315  Profit:  357.780612244901
Average:  316  Profit:  183.1836734693887
Average:  317  Profit:  77.28061224489711
Average:  318  Profit:  22.89795918367359
Average:  319  Profit:  2.8622448979591986

------------------- 308 -------------------
Average:  308  Profit:  6972
Average:  309  Profit:  5370.215277777824
Average:  310  Profit:  4034.72222222218
Average:  311  Profit:  2941.3125
Average:  312  Profit:  2065.777777777804
Average:  313  Profit:  1383.9097222222115
Average:  314  Profit:  871.5
Average:  315  Profit:  504.3402777777725
Average:  316  Profit:  258.2222222222255
Average:  317  Profit:  108.9375
Average:  318  Profit:  32.27777777777819
Average:  319  Profit:  4.034722222222274

------------------- 310 -------------------
Average:  310  Profit:  6010
Average:  311  Profit:  4381.289999999982
Average:  312  Profit:  3077.119999999957
Average:  313  Profit:  2061.4300000000117
Average:  314  Profit:  1298.1600000000055
Average:  315  Profit:  751.25
Average:  316  Profit:  384.63999999999464
Average:  317  Profit:  162.2700000000007
Average:  318  Profit:  48.07999999999933
Average:  319  Profit:  6.009999999999916

------------------- 312 -------------------
Average:  312  Profit:  4968
Average:  313  Profit:  3328.171875
Average:  314  Profit:  2095.875
Average:  315  Profit:  1212.890625
Average:  316  Profit:  621.0
Average:  317  Profit:  261.984375
Average:  318  Profit:  77.625
Average:  319  Profit:  9.703125

------------------- 314 -------------------
Average:  314  Profit:  3846
Average:  315  Profit:  2225.6944444444202
Average:  316  Profit:  1139.5555555555718
Average:  317  Profit:  480.75
Average:  318  Profit:  142.44444444444648
Average:  319  Profit:  17.80555555555581

------------------- 316 -------------------
Average:  316  Profit:  2644
Average:  317  Profit:  1115.4375
Average:  318  Profit:  330.5
Average:  319  Profit:  41.3125

------------------- 318 -------------------
Average:  318  Profit:  1362
Average:  319  Profit:  170.25
"""
