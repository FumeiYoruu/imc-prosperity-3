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
    price1 = 199
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

    print("Average: ", average, " Best Price2: ", best_price[1], " Profit: ", profitmax)

for price2 in range(284, 319, 2):
    price1 = 199
    print("-------------------", price2, "-------------------")
    for average in range(price2,320):
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
        print("Average: ", average, " Profit: ", profit)
    print()


'''Output: (just so you don't have to run it again)





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





Average:  284  Best Price2:  284  Profit:  12636
Average:  285  Best Price2:  285  Profit:  12635
Average:  286  Best Price2:  286  Profit:  12614
Average:  287  Best Price2:  287  Profit:  12573
Average:  288  Best Price2:  288  Profit:  12512
Average:  289  Best Price2:  289  Profit:  12431
Average:  290  Best Price2:  290  Profit:  12330
Average:  291  Best Price2:  291  Profit:  12209
Average:  292  Best Price2:  292  Profit:  12068
Average:  293  Best Price2:  293  Profit:  11907
Average:  294  Best Price2:  294  Profit:  11726
Average:  295  Best Price2:  295  Profit:  11525
Average:  296  Best Price2:  296  Profit:  11304
Average:  297  Best Price2:  297  Profit:  11063
Average:  298  Best Price2:  298  Profit:  10802
Average:  299  Best Price2:  299  Profit:  10521
Average:  300  Best Price2:  300  Profit:  10220
Average:  301  Best Price2:  301  Profit:  9899
Average:  302  Best Price2:  302  Profit:  9558
Average:  303  Best Price2:  303  Profit:  9197
Average:  304  Best Price2:  304  Profit:  8816
Average:  305  Best Price2:  305  Profit:  8415
Average:  306  Best Price2:  306  Profit:  7994
Average:  307  Best Price2:  307  Profit:  7553
Average:  308  Best Price2:  308  Profit:  7092
Average:  309  Best Price2:  309  Profit:  6611
Average:  310  Best Price2:  310  Profit:  6110
Average:  311  Best Price2:  311  Profit:  5589
Average:  312  Best Price2:  312  Profit:  5048
Average:  313  Best Price2:  313  Profit:  4487
Average:  314  Best Price2:  314  Profit:  3906
Average:  315  Best Price2:  315  Profit:  3305
Average:  316  Best Price2:  316  Profit:  2684
Average:  317  Best Price2:  317  Profit:  2043
Average:  318  Best Price2:  318  Profit:  1382
Average:  319  Best Price2:  319  Profit:  701





------------------- 284 -------------------
Average:  284  Profit:  12636
Average:  285  Profit:  11611.979166666732
Average:  286  Profit:  10644.833333333361
Average:  287  Profit:  9732.937500000002
Average:  288  Profit:  8874.666666666692
Average:  289  Profit:  8068.395833333268
Average:  290  Profit:  7312.499999999965
Average:  291  Profit:  6605.354166666622
Average:  292  Profit:  5945.3333333333485
Average:  293  Profit:  5330.8125
Average:  294  Profit:  4760.166666666674
Average:  295  Profit:  4231.770833333324
Average:  296  Profit:  3743.9999999999814
Average:  297  Profit:  3295.2291666666556
Average:  298  Profit:  2883.833333333308
Average:  299  Profit:  2508.187500000001
Average:  300  Profit:  2166.666666666653
Average:  301  Profit:  1857.6458333333235
Average:  302  Profit:  1579.5
Average:  303  Profit:  1330.6041666666702
Average:  304  Profit:  1109.3333333333364
Average:  305  Profit:  914.0624999999957
Average:  306  Profit:  743.1666666666686
Average:  307  Profit:  595.0208333333343
Average:  308  Profit:  467.99999999999767
Average:  309  Profit:  360.4791666666635
Average:  310  Profit:  270.8333333333316
Average:  311  Profit:  197.4375
Average:  312  Profit:  138.66666666666706
Average:  313  Profit:  92.89583333333357
Average:  314  Profit:  58.49999999999971
Average:  315  Profit:  33.85416666666645
Average:  316  Profit:  17.333333333333382
Average:  317  Profit:  7.312499999999964
Average:  318  Profit:  2.1666666666666727
Average:  319  Profit:  0.2708333333333341

------------------- 286 -------------------
Average:  286  Profit:  12614
Average:  287  Profit:  11533.414359861488
Average:  288  Profit:  10516.373702422241
Average:  289  Profit:  9560.952422145236
Average:  290  Profit:  8665.224913494849
Average:  291  Profit:  7827.265570934281
Average:  292  Profit:  7045.148788927394
Average:  293  Profit:  6316.94896193767
Average:  294  Profit:  5640.7404844290195
Average:  295  Profit:  5014.59775086506
Average:  296  Profit:  4436.595155709338
Average:  297  Profit:  3904.8070934256025
Average:  298  Profit:  3417.307958477526
Average:  299  Profit:  2972.172145328726
Average:  300  Profit:  2567.4740484429194
Average:  301  Profit:  2201.288062283735
Average:  302  Profit:  1871.6885813148917
Average:  303  Profit:  1576.75
Average:  304  Profit:  1314.5467128027801
Average:  305  Profit:  1083.153114186856
Average:  306  Profit:  880.6435986159242
Average:  307  Profit:  705.0925605536274
Average:  308  Profit:  554.5743944636672
Average:  309  Profit:  427.16349480969075
Average:  310  Profit:  320.9342560553649
Average:  311  Profit:  233.96107266436147
Average:  312  Profit:  164.31833910034752
Average:  313  Profit:  110.08044982699053
Average:  314  Profit:  69.3217993079584
Average:  315  Profit:  40.116782006920616
Average:  316  Profit:  20.53979238754344
Average:  317  Profit:  8.6652249134948
Average:  318  Profit:  2.56747404844293
Average:  319  Profit:  0.32093425605536624

------------------- 288 -------------------
Average:  288  Profit:  12512
Average:  289  Profit:  11375.2744140625
Average:  290  Profit:  10309.5703125
Average:  291  Profit:  9312.5966796875
Average:  292  Profit:  8382.0625
Average:  293  Profit:  7515.6767578125
Average:  294  Profit:  6711.1484375
Average:  295  Profit:  5966.1865234375
Average:  296  Profit:  5278.5
Average:  297  Profit:  4645.7978515625
Average:  298  Profit:  4065.7890625
Average:  299  Profit:  3536.1826171875
Average:  300  Profit:  3054.6875
Average:  301  Profit:  2619.0126953125
Average:  302  Profit:  2226.8671875
Average:  303  Profit:  1875.9599609375
Average:  304  Profit:  1564.0
Average:  305  Profit:  1288.6962890625
Average:  306  Profit:  1047.7578125
Average:  307  Profit:  838.8935546875
Average:  308  Profit:  659.8125
Average:  309  Profit:  508.2236328125
Average:  310  Profit:  381.8359375
Average:  311  Profit:  278.3583984375
Average:  312  Profit:  195.5
Average:  313  Profit:  130.9697265625
Average:  314  Profit:  82.4765625
Average:  315  Profit:  47.7294921875
Average:  316  Profit:  24.4375
Average:  317  Profit:  10.3095703125
Average:  318  Profit:  3.0546875
Average:  319  Profit:  0.3818359375

------------------- 290 -------------------
Average:  290  Profit:  12330
Average:  291  Profit:  11137.643333333379
Average:  292  Profit:  10024.746666666715
Average:  293  Profit:  8988.569999999994
Average:  294  Profit:  8026.373333333367
Average:  295  Profit:  7135.416666666723
Average:  296  Profit:  6312.959999999964
Average:  297  Profit:  5556.263333333303
Average:  298  Profit:  4862.586666666638
Average:  299  Profit:  4229.189999999988
Average:  300  Profit:  3653.3333333333017
Average:  301  Profit:  3132.2766666666557
Average:  302  Profit:  2663.2800000000066
Average:  303  Profit:  2243.603333333322
Average:  304  Profit:  1870.506666666674
Average:  305  Profit:  1541.25
Average:  306  Profit:  1253.0933333333394
Average:  307  Profit:  1003.2966666666708
Average:  308  Profit:  789.1199999999955
Average:  309  Profit:  607.8233333333297
Average:  310  Profit:  456.6666666666627
Average:  311  Profit:  332.9100000000008
Average:  312  Profit:  233.81333333333424
Average:  313  Profit:  156.63666666666742
Average:  314  Profit:  98.63999999999943
Average:  315  Profit:  57.08333333333284
Average:  316  Profit:  29.22666666666678
Average:  317  Profit:  12.329999999999929
Average:  318  Profit:  3.6533333333333475
Average:  319  Profit:  0.45666666666666844

------------------- 292 -------------------
Average:  292  Profit:  12068
Average:  293  Profit:  10820.628826530525
Average:  294  Profit:  9662.31632653056
Average:  295  Profit:  8589.764030612316
Average:  296  Profit:  7599.673469387694
Average:  297  Profit:  6688.746173469381
Average:  298  Profit:  5853.683673469381
Average:  299  Profit:  5091.1875
Average:  300  Profit:  4397.959183673465
Average:  301  Profit:  3770.7002551020796
Average:  302  Profit:  3206.1122448979295
Average:  303  Profit:  2700.896683673454
Average:  304  Profit:  2251.7551020408087
Average:  305  Profit:  1855.3890306122307
Average:  306  Profit:  1508.5
Average:  307  Profit:  1207.78954081632
Average:  308  Profit:  949.9591836734618
Average:  309  Profit:  731.7104591836726
Average:  310  Profit:  549.7448979591832
Average:  311  Profit:  400.7640306122412
Average:  312  Profit:  281.4693877551011
Average:  313  Profit:  188.5625
Average:  314  Profit:  118.74489795918272
Average:  315  Profit:  68.7181122448979
Average:  316  Profit:  35.183673469387635
Average:  317  Profit:  14.84311224489784
Average:  318  Profit:  4.397959183673454
Average:  319  Profit:  0.5497448979591818

------------------- 294 -------------------
Average:  294  Profit:  11726
Average:  295  Profit:  10424.371301775216
Average:  296  Profit:  9222.816568047368
Average:  297  Profit:  8117.332840236626
Average:  298  Profit:  7103.91715976337
Average:  299  Profit:  6178.566568047322
Average:  300  Profit:  5337.278106508833
Average:  301  Profit:  4576.048816568026
Average:  302  Profit:  3890.875739644943
Average:  303  Profit:  3277.7559171597577
Average:  304  Profit:  2732.686390532529
Average:  305  Profit:  2251.664201183422
Average:  306  Profit:  1830.6863905325529
Average:  307  Profit:  1465.75
Average:  308  Profit:  1152.852071005921
Average:  309  Profit:  887.9896449704213
Average:  310  Profit:  667.1597633136041
Average:  311  Profit:  486.3594674556179
Average:  312  Profit:  341.5857988165661
Average:  313  Profit:  228.8357988165691
Average:  314  Profit:  144.10650887574013
Average:  315  Profit:  83.39497041420051
Average:  316  Profit:  42.698224852070766
Average:  317  Profit:  18.013313609467517
Average:  318  Profit:  5.337278106508846
Average:  319  Profit:  0.6671597633136057

------------------- 296 -------------------
Average:  296  Profit:  11304
Average:  297  Profit:  9949.057291666593
Average:  298  Profit:  8706.958333333403
Average:  299  Profit:  7572.796875
Average:  300  Profit:  6541.666666666604
Average:  301  Profit:  5608.66145833339
Average:  302  Profit:  4768.875
Average:  303  Profit:  4017.401041666625
Average:  304  Profit:  3349.333333333364
Average:  305  Profit:  2759.765625
Average:  306  Profit:  2243.7916666666674
Average:  307  Profit:  1796.5052083333233
Average:  308  Profit:  1413.0
Average:  309  Profit:  1088.3697916666754
Average:  310  Profit:  817.7083333333255
Average:  311  Profit:  596.109375
Average:  312  Profit:  418.6666666666705
Average:  313  Profit:  280.4739583333334
Average:  314  Profit:  176.625
Average:  315  Profit:  102.21354166666569
Average:  316  Profit:  52.33333333333381
Average:  317  Profit:  22.078125
Average:  318  Profit:  6.5416666666667265
Average:  319  Profit:  0.8177083333333408

------------------- 298 -------------------
Average:  298  Profit:  10802
Average:  299  Profit:  9394.940082644529
Average:  300  Profit:  8115.702479338884
Average:  301  Profit:  6958.2004132230995
Average:  302  Profit:  5916.347107438033
Average:  303  Profit:  4984.055785123939
Average:  304  Profit:  4155.239669421528
Average:  305  Profit:  3423.811983471095
Average:  306  Profit:  2783.6859504132435
Average:  307  Profit:  2228.7747933884434
Average:  308  Profit:  1752.991735537181
Average:  309  Profit:  1350.25
Average:  310  Profit:  1014.4628099173605
Average:  311  Profit:  739.5433884297541
Average:  312  Profit:  519.404958677691
Average:  313  Profit:  347.96074380165544
Average:  314  Profit:  219.12396694214763
Average:  315  Profit:  126.80785123967006
Average:  316  Profit:  64.92561983471137
Average:  317  Profit:  27.390495867768454
Average:  318  Profit:  8.115702479338921
Average:  319  Profit:  1.0144628099173651

------------------- 300 -------------------
Average:  300  Profit:  10220
Average:  301  Profit:  8762.372499999987
Average:  302  Profit:  7450.379999999969
Average:  303  Profit:  6276.3575000000155
Average:  304  Profit:  5232.639999999934
Average:  305  Profit:  4311.5625
Average:  306  Profit:  3505.460000000013
Average:  307  Profit:  2806.667499999985
Average:  308  Profit:  2207.5199999999963
Average:  309  Profit:  1700.352500000018
Average:  310  Profit:  1277.5
Average:  311  Profit:  931.2974999999961
Average:  312  Profit:  654.0799999999917
Average:  313  Profit:  438.18250000000165
Average:  314  Profit:  275.93999999999954
Average:  315  Profit:  159.6875
Average:  316  Profit:  81.75999999999897
Average:  317  Profit:  34.49249999999994
Average:  318  Profit:  10.219999999999871
Average:  319  Profit:  1.2774999999999839

------------------- 302 -------------------
Average:  302  Profit:  9558
Average:  303  Profit:  8051.861111111133
Average:  304  Profit:  6712.888888888911
Average:  305  Profit:  5531.250000000018
Average:  306  Profit:  4497.111111111145
Average:  307  Profit:  3600.6388888888664
Average:  308  Profit:  2832.0000000000105
Average:  309  Profit:  2181.3611111110886
Average:  310  Profit:  1638.888888888874
Average:  311  Profit:  1194.75
Average:  312  Profit:  839.1111111111139
Average:  313  Profit:  562.1388888888931
Average:  314  Profit:  354.0000000000013
Average:  315  Profit:  204.86111111110924
Average:  316  Profit:  104.88888888888924
Average:  317  Profit:  44.25000000000016
Average:  318  Profit:  13.111111111111155
Average:  319  Profit:  1.6388888888888944

------------------- 304 -------------------
Average:  304  Profit:  8816
Average:  305  Profit:  7264.16015625
Average:  306  Profit:  5906.03125
Average:  307  Profit:  4728.69921875
Average:  308  Profit:  3719.25
Average:  309  Profit:  2864.76953125
Average:  310  Profit:  2152.34375
Average:  311  Profit:  1569.05859375
Average:  312  Profit:  1102.0
Average:  313  Profit:  738.25390625
Average:  314  Profit:  464.90625
Average:  315  Profit:  269.04296875
Average:  316  Profit:  137.75
Average:  317  Profit:  58.11328125
Average:  318  Profit:  17.21875
Average:  319  Profit:  2.15234375

------------------- 306 -------------------
Average:  306  Profit:  7994
Average:  307  Profit:  6400.443877550932
Average:  308  Profit:  5034.122448979536
Average:  309  Profit:  3877.5561224489747
Average:  310  Profit:  2913.2653061224755
Average:  311  Profit:  2123.77040816324
Average:  312  Profit:  1491.5918367347024
Average:  313  Profit:  999.25
Average:  314  Profit:  629.265306122442
Average:  315  Profit:  364.15816326530944
Average:  316  Profit:  186.4489795918378
Average:  317  Profit:  78.65816326530525
Average:  318  Profit:  23.306122448979725
Average:  319  Profit:  2.9132653061224656

------------------- 308 -------------------
Average:  308  Profit:  7092
Average:  309  Profit:  5462.64583333338
Average:  310  Profit:  4104.166666666623
Average:  311  Profit:  2991.9375
Average:  312  Profit:  2101.3333333333608
Average:  313  Profit:  1407.729166666655
Average:  314  Profit:  886.5
Average:  315  Profit:  513.0208333333279
Average:  316  Profit:  262.6666666666701
Average:  317  Profit:  110.8125
Average:  318  Profit:  32.83333333333376
Average:  319  Profit:  4.10416666666672

------------------- 310 -------------------
Average:  310  Profit:  6110
Average:  311  Profit:  4454.189999999981
Average:  312  Profit:  3128.319999999956
Average:  313  Profit:  2095.73000000001
Average:  314  Profit:  1319.7600000000064
Average:  315  Profit:  763.75
Average:  316  Profit:  391.0399999999945
Average:  317  Profit:  164.9700000000008
Average:  318  Profit:  48.87999999999931
Average:  319  Profit:  6.109999999999914

------------------- 312 -------------------
Average:  312  Profit:  5048
Average:  313  Profit:  3381.765625
Average:  314  Profit:  2129.625
Average:  315  Profit:  1232.421875
Average:  316  Profit:  631.0
Average:  317  Profit:  266.203125
Average:  318  Profit:  78.875
Average:  319  Profit:  9.859375

------------------- 314 -------------------
Average:  314  Profit:  3906
Average:  315  Profit:  2260.416666666642
Average:  316  Profit:  1157.33333333335
Average:  317  Profit:  488.25
Average:  318  Profit:  144.66666666666876
Average:  319  Profit:  18.083333333333595

------------------- 316 -------------------
Average:  316  Profit:  2684
Average:  317  Profit:  1132.3125
Average:  318  Profit:  335.5
Average:  319  Profit:  41.9375

------------------- 318 -------------------
Average:  318  Profit:  1382
Average:  319  Profit:  172.75
'''
