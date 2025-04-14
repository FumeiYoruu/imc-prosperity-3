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



for price2 in range(284, 319, 2):
    price1 = 199
    print("-------------------", price2, "-------------------")
    for average in range(price2,320):
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






------------------- 284 -------------------
Average:  284  Profit:  59947
Average:  285  Profit:  58922.9791666655
Average:  286  Profit:  57955.833333333365
Average:  287  Profit:  57043.93749999915
Average:  288  Profit:  56185.66666666607
Average:  289  Profit:  55379.39583333223
Average:  290  Profit:  54623.50000000085
Average:  291  Profit:  53916.35416666749
Average:  292  Profit:  53256.3333333328
Average:  293  Profit:  52641.8125
Average:  294  Profit:  52071.1666666672
Average:  295  Profit:  51542.77083333251
Average:  296  Profit:  51054.99999999915
Average:  297  Profit:  50606.22916666777
Average:  298  Profit:  50194.83333333393
Average:  299  Profit:  49819.18750000085
Average:  300  Profit:  49477.666666666635
Average:  301  Profit:  49168.6458333345
Average:  302  Profit:  48890.5
Average:  303  Profit:  48641.60416666635
Average:  304  Profit:  48420.333333334216
Average:  305  Profit:  48225.06249999915
Average:  306  Profit:  48054.16666666692
Average:  307  Profit:  47906.02083333308
Average:  308  Profit:  47779.00000000085
Average:  309  Profit:  47671.479166665784
Average:  310  Profit:  47581.83333333365
Average:  311  Profit:  47508.4375
Average:  312  Profit:  47449.6666666655
Average:  313  Profit:  47403.895833333365
Average:  314  Profit:  47369.49999999915
Average:  315  Profit:  47344.85416666607
Average:  316  Profit:  47328.33333333223
Average:  317  Profit:  47318.31250000085
Average:  318  Profit:  47313.16666666749
Average:  319  Profit:  47311.2708333328

------------------- 286 -------------------
Average:  286  Profit:  59925
Average:  287  Profit:  58844.41435986278
Average:  288  Profit:  57827.37370242163
Average:  289  Profit:  56871.95242214449
Average:  290  Profit:  55976.224913493876
Average:  291  Profit:  55138.26557093502
Average:  292  Profit:  54356.148788927756
Average:  293  Profit:  53627.948961937305
Average:  294  Profit:  52951.7404844289
Average:  295  Profit:  52325.59775086506
Average:  296  Profit:  51747.595155708324
Average:  297  Profit:  51215.807093426614
Average:  298  Profit:  50728.30795847706
Average:  299  Profit:  50283.17214532759
Average:  300  Profit:  49878.47404844343
Average:  301  Profit:  49512.28806228441
Average:  302  Profit:  49182.68858131576
Average:  303  Profit:  48887.75
Average:  304  Profit:  48625.54671280237
Average:  305  Profit:  48394.153114188084
Average:  306  Profit:  48191.64359861698
Average:  307  Profit:  48016.09256055429
Average:  308  Profit:  47865.57439446253
Average:  309  Profit:  47738.16349480963
Average:  310  Profit:  47631.93425605543
Average:  311  Profit:  47544.961072665144
Average:  312  Profit:  47475.31833910131
Average:  313  Profit:  47421.08044982645
Average:  314  Profit:  47380.32179930849
Average:  315  Profit:  47351.116782007266
Average:  316  Profit:  47331.539792388
Average:  317  Profit:  47319.665224913224
Average:  318  Profit:  47313.56747404816
Average:  319  Profit:  47311.320934255345

------------------- 288 -------------------
Average:  288  Profit:  59823
Average:  289  Profit:  58686.2744140625
Average:  290  Profit:  57620.5703125
Average:  291  Profit:  56623.5966796875
Average:  292  Profit:  55693.0625
Average:  293  Profit:  54826.6767578125
Average:  294  Profit:  54022.1484375
Average:  295  Profit:  53277.1865234375
Average:  296  Profit:  52589.5
Average:  297  Profit:  51956.7978515625
Average:  298  Profit:  51376.7890625
Average:  299  Profit:  50847.1826171875
Average:  300  Profit:  50365.6875
Average:  301  Profit:  49930.0126953125
Average:  302  Profit:  49537.8671875
Average:  303  Profit:  49186.9599609375
Average:  304  Profit:  48875.0
Average:  305  Profit:  48599.6962890625
Average:  306  Profit:  48358.7578125
Average:  307  Profit:  48149.8935546875
Average:  308  Profit:  47970.8125
Average:  309  Profit:  47819.2236328125
Average:  310  Profit:  47692.8359375
Average:  311  Profit:  47589.3583984375
Average:  312  Profit:  47506.5
Average:  313  Profit:  47441.9697265625
Average:  314  Profit:  47393.4765625
Average:  315  Profit:  47358.7294921875
Average:  316  Profit:  47335.4375
Average:  317  Profit:  47321.3095703125
Average:  318  Profit:  47314.0546875
Average:  319  Profit:  47311.3818359375

------------------- 290 -------------------
Average:  290  Profit:  59641
Average:  291  Profit:  58448.64333333364
Average:  292  Profit:  57335.746666665524
Average:  293  Profit:  56299.57000000108
Average:  294  Profit:  55337.37333333376
Average:  295  Profit:  54446.416666666
Average:  296  Profit:  53623.96000000024
Average:  297  Profit:  52867.26333333292
Average:  298  Profit:  52173.58666666648
Average:  299  Profit:  51540.19000000036
Average:  300  Profit:  50964.333333334
Average:  301  Profit:  50443.27666666684
Average:  302  Profit:  49974.280000001316
Average:  303  Profit:  49554.60333333388
Average:  304  Profit:  49181.50666666696
Average:  305  Profit:  48852.25
Average:  306  Profit:  48564.09333333244
Average:  307  Profit:  48314.29666666672
Average:  308  Profit:  48100.11999999928
Average:  309  Profit:  47918.82333333256
Average:  310  Profit:  47767.666666666
Average:  311  Profit:  47643.90999999904
Average:  312  Profit:  47544.81333333412
Average:  313  Profit:  47467.63666666768
Average:  314  Profit:  47409.63999999916
Average:  315  Profit:  47368.083333334
Average:  316  Profit:  47340.22666666564
Average:  317  Profit:  47323.32999999952
Average:  318  Profit:  47314.653333332084
Average:  319  Profit:  47311.45666666576

------------------- 292 -------------------
Average:  292  Profit:  59379
Average:  293  Profit:  58131.62882653023
Average:  294  Profit:  56973.31632653023
Average:  295  Profit:  55900.76403061084
Average:  296  Profit:  54910.67346938916
Average:  297  Profit:  53999.74617346977
Average:  298  Profit:  53164.68367346977
Average:  299  Profit:  52402.1875
Average:  300  Profit:  51708.95918367443
Average:  301  Profit:  51081.70025510076
Average:  302  Profit:  50517.11224489924
Average:  303  Profit:  50011.89668367443
Average:  304  Profit:  49562.755102040304
Average:  305  Profit:  49166.38903061084
Average:  306  Profit:  48819.5
Average:  307  Profit:  48518.789540815495
Average:  308  Profit:  48260.95918367443
Average:  309  Profit:  48042.710459184505
Average:  310  Profit:  47860.744897959696
Average:  311  Profit:  47711.76403061084
Average:  312  Profit:  47592.46938775504
Average:  313  Profit:  47499.5625
Average:  314  Profit:  47429.744897959696
Average:  315  Profit:  47379.71811224496
Average:  316  Profit:  47346.18367346977
Average:  317  Profit:  47325.84311224496
Average:  318  Profit:  47315.397959184505
Average:  319  Profit:  47311.54974489924

------------------- 294 -------------------
Average:  294  Profit:  59037
Average:  295  Profit:  57735.371301775536
Average:  296  Profit:  56533.81656804691
Average:  297  Profit:  55428.33284023783
Average:  298  Profit:  54414.91715976217
Average:  299  Profit:  53489.56656804691
Average:  300  Profit:  52648.278106509206
Average:  301  Profit:  51887.048816569484
Average:  302  Profit:  51201.87573964489
Average:  303  Profit:  50588.75591715914
Average:  304  Profit:  50043.68639053266
Average:  305  Profit:  49562.6642011826
Average:  306  Profit:  49141.68639053266
Average:  307  Profit:  48776.75
Average:  308  Profit:  48463.85207100504
Average:  309  Profit:  48198.9896449715
Average:  310  Profit:  47978.15976331324
Average:  311  Profit:  47797.35946745725
Average:  312  Profit:  47652.5857988174
Average:  313  Profit:  47539.8357988174
Average:  314  Profit:  47455.1065088744
Average:  315  Profit:  47394.394970415386
Average:  316  Profit:  47353.698224850945
Average:  317  Profit:  47329.01331360807
Average:  318  Profit:  47316.33727810719
Average:  319  Profit:  47311.66715976217

------------------- 296 -------------------
Average:  296  Profit:  58615
Average:  297  Profit:  57260.05729166743
Average:  298  Profit:  56017.95833333257
Average:  299  Profit:  54883.796875
Average:  300  Profit:  53852.66666666743
Average:  301  Profit:  52919.66145833257
Average:  302  Profit:  52079.875
Average:  303  Profit:  51328.40104166743
Average:  304  Profit:  50660.33333333257
Average:  305  Profit:  50070.765625
Average:  306  Profit:  49554.79166666743
Average:  307  Profit:  49107.50520833257
Average:  308  Profit:  48724.0
Average:  309  Profit:  48399.36979166743
Average:  310  Profit:  48128.70833333257
Average:  311  Profit:  47907.109375
Average:  312  Profit:  47729.66666666743
Average:  313  Profit:  47591.47395833257
Average:  314  Profit:  47487.625
Average:  315  Profit:  47413.21354166743
Average:  316  Profit:  47363.33333333257
Average:  317  Profit:  47333.078125
Average:  318  Profit:  47317.54166666743
Average:  319  Profit:  47311.81770833257

------------------- 298 -------------------
Average:  298  Profit:  58113
Average:  299  Profit:  56705.94008264622
Average:  300  Profit:  55426.70247934023
Average:  301  Profit:  54269.20041322397
Average:  302  Profit:  53227.347107439375
Average:  303  Profit:  52295.05578512482
Average:  304  Profit:  51466.239669422255
Average:  305  Profit:  50734.81198347004
Average:  306  Profit:  50094.685950413696
Average:  307  Profit:  49539.77479338802
Average:  308  Profit:  49063.99173553852
Average:  309  Profit:  48661.25
Average:  310  Profit:  48325.462809917975
Average:  311  Profit:  48050.543388430815
Average:  312  Profit:  47830.40495867689
Average:  313  Profit:  47658.96074380171
Average:  314  Profit:  47530.123966943655
Average:  315  Profit:  47437.80785124109
Average:  316  Profit:  47375.92561983595
Average:  317  Profit:  47338.39049586662
Average:  318  Profit:  47319.1157024786
Average:  319  Profit:  47312.01446281027

------------------- 300 -------------------
Average:  300  Profit:  57531
Average:  301  Profit:  56073.372499999554
Average:  302  Profit:  54761.38000000089
Average:  303  Profit:  53587.357500000595
Average:  304  Profit:  52543.63999999896
Average:  305  Profit:  51622.5625
Average:  306  Profit:  50816.4600000003
Average:  307  Profit:  50117.66750000015
Average:  308  Profit:  49518.51999999985
Average:  309  Profit:  49011.3524999997
Average:  310  Profit:  48588.5
Average:  311  Profit:  48242.29750000104
Average:  312  Profit:  47965.079999999405
Average:  313  Profit:  47749.18249999911
Average:  314  Profit:  47586.940000000446
Average:  315  Profit:  47470.6875
Average:  316  Profit:  47392.760000001785
Average:  317  Profit:  47345.49249999866
Average:  318  Profit:  47321.219999998364
Average:  319  Profit:  47312.27750000119

------------------- 302 -------------------
Average:  302  Profit:  56869
Average:  303  Profit:  55362.8611111092
Average:  304  Profit:  54023.88888889037
Average:  305  Profit:  52842.24999999871
Average:  306  Profit:  51808.11111111264
Average:  307  Profit:  50911.63888888736
Average:  308  Profit:  50143.00000000129
Average:  309  Profit:  49492.36111110963
Average:  310  Profit:  48949.8888888908
Average:  311  Profit:  48505.75
Average:  312  Profit:  48150.11111111178
Average:  313  Profit:  47873.13888888908
Average:  314  Profit:  47664.99999999871
Average:  315  Profit:  47515.86111111135
Average:  316  Profit:  47415.88888888994
Average:  317  Profit:  47355.25000000129
Average:  318  Profit:  47324.11111111221
Average:  319  Profit:  47312.63888888951

------------------- 304 -------------------
Average:  304  Profit:  56127
Average:  305  Profit:  54575.16015625
Average:  306  Profit:  53217.03125
Average:  307  Profit:  52039.69921875
Average:  308  Profit:  51030.25
Average:  309  Profit:  50175.76953125
Average:  310  Profit:  49463.34375
Average:  311  Profit:  48880.05859375
Average:  312  Profit:  48413.0
Average:  313  Profit:  48049.25390625
Average:  314  Profit:  47775.90625
Average:  315  Profit:  47580.04296875
Average:  316  Profit:  47448.75
Average:  317  Profit:  47369.11328125
Average:  318  Profit:  47328.21875
Average:  319  Profit:  47313.15234375

------------------- 306 -------------------
Average:  306  Profit:  55305
Average:  307  Profit:  53711.443877550766
Average:  308  Profit:  52345.122448980524
Average:  309  Profit:  51188.556122449234
Average:  310  Profit:  50224.26530612101
Average:  311  Profit:  49434.77040816411
Average:  312  Profit:  48802.591836734355
Average:  313  Profit:  48310.25
Average:  314  Profit:  47940.26530612101
Average:  315  Profit:  47675.158163265645
Average:  316  Profit:  47497.44897959387
Average:  317  Profit:  47389.658163265645
Average:  318  Profit:  47334.306122449234
Average:  319  Profit:  47313.913265304596

------------------- 308 -------------------
Average:  308  Profit:  54403
Average:  309  Profit:  52773.645833332856
Average:  310  Profit:  51415.166666667144
Average:  311  Profit:  50302.9375
Average:  312  Profit:  49412.333333332856
Average:  313  Profit:  48718.729166667144
Average:  314  Profit:  48197.5
Average:  315  Profit:  47824.020833332856
Average:  316  Profit:  47573.666666667144
Average:  317  Profit:  47421.8125
Average:  318  Profit:  47343.833333332856
Average:  319  Profit:  47315.104166667144

------------------- 310 -------------------
Average:  310  Profit:  53421
Average:  311  Profit:  51765.19000000053
Average:  312  Profit:  50439.3200000016
Average:  313  Profit:  49406.73000000018
Average:  314  Profit:  48630.760000002134
Average:  315  Profit:  48074.75
Average:  316  Profit:  47702.039999999644
Average:  317  Profit:  47475.969999998044
Average:  318  Profit:  47359.88000000107
Average:  319  Profit:  47317.110000001245

------------------- 312 -------------------
Average:  312  Profit:  52359
Average:  313  Profit:  50692.765625
Average:  314  Profit:  49440.625
Average:  315  Profit:  48543.421875
Average:  316  Profit:  47942.0
Average:  317  Profit:  47577.203125
Average:  318  Profit:  47389.875
Average:  319  Profit:  47320.859375

------------------- 314 -------------------
Average:  314  Profit:  51217
Average:  315  Profit:  49571.41666666456
Average:  316  Profit:  48468.33333333544
Average:  317  Profit:  47799.25
Average:  318  Profit:  47455.66666666456
Average:  319  Profit:  47329.08333333544

------------------- 316 -------------------
Average:  316  Profit:  49995
Average:  317  Profit:  48443.3125
Average:  318  Profit:  47646.5
Average:  319  Profit:  47352.9375

------------------- 318 -------------------
Average:  318  Profit:  48693
Average:  319  Profit:  47483.75
"""
