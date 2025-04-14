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

for price2 in range(284, 319):
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

------------------- 285 -------------------
Average:  285  Profit:  12635
Average:  286  Profit:  11582.64816326524
Average:  287  Profit:  10590.413877551062
Average:  288  Profit:  9656.528979591896
Average:  289  Profit:  8779.225306122484
Average:  290  Profit:  7956.734693877628
Average:  291  Profit:  7187.288979591878
Average:  292  Profit:  6469.120000000021
Average:  293  Profit:  5800.459591836727
Average:  294  Profit:  5179.539591836733
Average:  295  Profit:  4604.591836734711
Average:  296  Profit:  4073.848163265283
Average:  297  Profit:  3585.5404081632732
Average:  298  Profit:  3137.9004081632415
Average:  299  Profit:  2729.1599999999844
Average:  300  Profit:  2357.5510204081734
Average:  301  Profit:  2021.3053061224678
Average:  302  Profit:  1718.6546938775562
Average:  303  Profit:  1447.831020408155
Average:  304  Profit:  1207.066122448987
Average:  305  Profit:  994.5918367347035
Average:  306  Profit:  808.6400000000026
Average:  307  Profit:  647.4424489795916
Average:  308  Profit:  509.23102040816036
Average:  309  Profit:  392.2375510204052
Average:  310  Profit:  294.69387755102167
Average:  311  Profit:  214.83183673469452
Average:  312  Profit:  150.88326530612338
Average:  313  Profit:  101.08000000000033
Average:  314  Profit:  63.653877551020045
Average:  315  Profit:  36.83673469387771
Average:  316  Profit:  18.860408163265422
Average:  317  Profit:  7.956734693877506
Average:  318  Profit:  2.3575510204081778
Average:  319  Profit:  0.2946938775510222

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

------------------- 287 -------------------
Average:  287  Profit:  12573
Average:  288  Profit:  11464.286501377346
Average:  289  Profit:  10422.74655647378
Average:  290  Profit:  9446.280991735526
Average:  291  Profit:  8532.790633608827
Average:  292  Profit:  7680.176308539876
Average:  293  Profit:  6886.338842975156
Average:  294  Profit:  6149.179063360869
Average:  295  Profit:  5466.597796143217
Average:  296  Profit:  4836.495867768588
Average:  297  Profit:  4256.774104683179
Average:  298  Profit:  3725.3333333333494
Average:  299  Profit:  3240.074380165308
Average:  300  Profit:  2798.8980716253573
Average:  301  Profit:  2399.7052341597764
Average:  302  Profit:  2040.3966942148672
Average:  303  Profit:  1718.8732782369198
Average:  304  Profit:  1433.0358126721683
Average:  305  Profit:  1180.7851239669408
Average:  306  Profit:  960.0220385674845
Average:  307  Profit:  768.6473829201086
Average:  308  Profit:  604.5619834710735
Average:  309  Profit:  465.6666666666687
Average:  310  Profit:  349.86225895316966
Average:  311  Profit:  255.0495867768584
Average:  312  Profit:  179.12947658402103
Average:  313  Profit:  120.00275482093556
Average:  314  Profit:  75.57024793388419
Average:  315  Profit:  43.73278236914621
Average:  316  Profit:  22.39118457300263
Average:  317  Profit:  9.446280991735524
Average:  318  Profit:  2.7988980716253287
Average:  319  Profit:  0.3498622589531661

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

------------------- 289 -------------------
Average:  289  Profit:  12431
Average:  290  Profit:  11266.38917793969
Average:  291  Profit:  10176.887617065498
Average:  292  Profit:  9159.991675338219
Average:  293  Profit:  8213.197710718012
Average:  294  Profit:  7334.002081165443
Average:  295  Profit:  6519.901144641061
Average:  296  Profit:  5768.391259105122
Average:  297  Profit:  5076.9687825182355
Average:  298  Profit:  4443.130072840806
Average:  299  Profit:  3864.3714880332814
Average:  300  Profit:  3338.189386056205
Average:  301  Profit:  2862.080124869915
Average:  302  Profit:  2433.540062434945
Average:  303  Profit:  2050.0655567117633
Average:  304  Profit:  1709.1529656607595
Average:  305  Profit:  1408.2986472424614
Average:  306  Profit:  1144.9989594172773
Average:  307  Profit:  916.7502601456804
Average:  308  Profit:  721.0489073881403
Average:  309  Profit:  555.3912591051007
Average:  310  Profit:  417.2736732570256
Average:  311  Profit:  304.1925078043681
Average:  312  Profit:  213.64412070759494
Average:  313  Profit:  143.12486992715966
Average:  314  Profit:  90.13111342351753
Average:  315  Profit:  52.1592091571282
Average:  316  Profit:  26.705515088449367
Average:  317  Profit:  11.266389177939692
Average:  318  Profit:  3.338189386056171
Average:  319  Profit:  0.41727367325702136

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

------------------- 291 -------------------
Average:  291  Profit:  12209
Average:  292  Profit:  10989.051129607691
Average:  293  Profit:  9853.202140309155
Average:  294  Profit:  8798.449464922609
Average:  295  Profit:  7821.789536266279
Average:  296  Profit:  6920.218787158116
Average:  297  Profit:  6090.733650416193
Average:  298  Profit:  5330.330558858474
Average:  299  Profit:  4636.005945303176
Average:  300  Profit:  4004.756242568344
Average:  301  Profit:  3433.577883472046
Average:  302  Profit:  2919.4673008323475
Average:  303  Profit:  2459.4209274673094
Average:  304  Profit:  2050.4351961949983
Average:  305  Profit:  1689.506539833538
Average:  306  Profit:  1373.6313912009614
Average:  307  Profit:  1099.8061831153261
Average:  308  Profit:  865.0273483947645
Average:  309  Profit:  666.2913198573093
Average:  310  Profit:  500.594530321043
Average:  311  Profit:  364.93341260404344
Average:  312  Profit:  256.3043995243748
Average:  313  Profit:  171.70392390012017
Average:  314  Profit:  108.12841854934557
Average:  315  Profit:  62.574316290130376
Average:  316  Profit:  32.03804994054685
Average:  317  Profit:  13.516052318668196
Average:  318  Profit:  4.004756242568356
Average:  319  Profit:  0.5005945303210445

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

------------------- 293 -------------------
Average:  293  Profit:  11907
Average:  294  Profit:  10632.395061728368
Average:  295  Profit:  9452.160493827143
Average:  296  Profit:  8362.666666666602
Average:  297  Profit:  7360.283950617225
Average:  298  Profit:  6441.382716049352
Average:  299  Profit:  5602.333333333339
Average:  300  Profit:  4839.50617283952
Average:  301  Profit:  4149.271604938273
Average:  302  Profit:  3527.9999999999995
Average:  303  Profit:  2972.0617283950633
Average:  304  Profit:  2477.827160493827
Average:  305  Profit:  2041.6666666666563
Average:  306  Profit:  1659.9506172839415
Average:  307  Profit:  1329.049382716046
Average:  308  Profit:  1045.3333333333253
Average:  309  Profit:  805.172839506169
Average:  310  Profit:  604.93827160494
Average:  311  Profit:  440.99999999999994
Average:  312  Profit:  309.72839506172835
Average:  313  Profit:  207.49382716049269
Average:  314  Profit:  130.66666666666566
Average:  315  Profit:  75.6172839506175
Average:  316  Profit:  38.716049382716044
Average:  317  Profit:  16.333333333333208
Average:  318  Profit:  4.8395061728395055
Average:  319  Profit:  0.6049382716049382

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

------------------- 295 -------------------
Average:  295  Profit:  11525
Average:  296  Profit:  10196.582399999985
Average:  297  Profit:  8974.379199999983
Average:  298  Profit:  7853.964799999955
Average:  299  Profit:  6830.913600000042
Average:  300  Profit:  5900.800000000049
Average:  301  Profit:  5059.198400000019
Average:  302  Profit:  4301.683200000017
Average:  303  Profit:  3623.828799999978
Average:  304  Profit:  3021.2096000000192
Average:  305  Profit:  2489.4000000000215
Average:  306  Profit:  2023.9744
Average:  307  Profit:  1620.5072000000148
Average:  308  Profit:  1274.572799999998
Average:  309  Profit:  981.7455999999944
Average:  310  Profit:  737.6000000000062
Average:  311  Profit:  537.7104000000021
Average:  312  Profit:  377.6512000000024
Average:  313  Profit:  252.9968
Average:  314  Profit:  159.32159999999976
Average:  315  Profit:  92.20000000000077
Average:  316  Profit:  47.2064000000003
Average:  317  Profit:  19.91519999999997
Average:  318  Profit:  5.900800000000038
Average:  319  Profit:  0.7376000000000047

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

------------------- 297 -------------------
Average:  297  Profit:  11063
Average:  298  Profit:  9681.8298676749
Average:  299  Profit:  8420.68241965983
Average:  300  Profit:  7274.102079395058
Average:  301  Profit:  6236.633270321304
Average:  302  Profit:  5302.820415879011
Average:  303  Profit:  4467.207939508501
Average:  304  Profit:  3724.340264650307
Average:  305  Profit:  3068.761814744791
Average:  306  Profit:  2495.017013232513
Average:  307  Profit:  1997.650283553858
Average:  308  Profit:  1571.2060491493257
Average:  309  Profit:  1210.2287334593625
Average:  310  Profit:  909.2627599243823
Average:  311  Profit:  662.8525519848764
Average:  312  Profit:  465.54253308128835
Average:  313  Profit:  311.8771266540641
Average:  314  Profit:  196.40075614366572
Average:  315  Profit:  113.65784499054779
Average:  316  Profit:  58.192816635161044
Average:  317  Profit:  24.550094517958215
Average:  318  Profit:  7.2741020793951305
Average:  319  Profit:  0.9092627599243913

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

------------------- 299 -------------------
Average:  299  Profit:  10521
Average:  300  Profit:  9088.435374149725
Average:  301  Profit:  7792.197278911524
Average:  302  Profit:  6625.469387755071
Average:  303  Profit:  5581.435374149707
Average:  304  Profit:  4653.278911564639
Average:  305  Profit:  3834.183673469362
Average:  306  Profit:  3117.3333333333126
Average:  307  Profit:  2495.911564625852
Average:  308  Profit:  1963.1020408163342
Average:  309  Profit:  1512.0884353741478
Average:  310  Profit:  1136.0544217687157
Average:  311  Profit:  828.1836734693838
Average:  312  Profit:  581.6598639455799
Average:  313  Profit:  389.66666666666407
Average:  314  Profit:  245.38775510204178
Average:  315  Profit:  142.00680272108946
Average:  316  Profit:  72.70748299319749
Average:  317  Profit:  30.673469387755222
Average:  318  Profit:  9.088435374149686
Average:  319  Profit:  1.1360544217687107

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

------------------- 301 -------------------
Average:  301  Profit:  9899
Average:  302  Profit:  8416.819944598257
Average:  303  Profit:  7090.506925207709
Average:  304  Profit:  5911.401662049816
Average:  305  Profit:  4870.844875346205
Average:  306  Profit:  3960.1772853185444
Average:  307  Profit:  3170.7396121883635
Average:  308  Profit:  2493.8725761772735
Average:  309  Profit:  1920.9168975069106
Average:  310  Profit:  1443.2132963989045
Average:  311  Profit:  1052.1024930747822
Average:  312  Profit:  738.925207756227
Average:  313  Profit:  495.02216066481805
Average:  314  Profit:  311.7340720221592
Average:  315  Profit:  180.40166204986306
Average:  316  Profit:  92.36565096952837
Average:  317  Profit:  38.9667590027699
Average:  318  Profit:  11.545706371191047
Average:  319  Profit:  1.4432132963988809

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

------------------- 303 -------------------
Average:  303  Profit:  9197
Average:  304  Profit:  7667.59861591704
Average:  305  Profit:  6317.906574394424
Average:  306  Profit:  5136.6920415224895
Average:  307  Profit:  4112.723183390942
Average:  308  Profit:  3234.7681660899616
Average:  309  Profit:  2491.5951557093426
Average:  310  Profit:  1871.9723183391106
Average:  311  Profit:  1364.6678200692184
Average:  312  Profit:  958.44982698963
Average:  313  Profit:  642.0865051903112
Average:  314  Profit:  404.3460207612452
Average:  315  Profit:  233.99653979238883
Average:  316  Profit:  119.80622837370375
Average:  317  Profit:  50.54325259515565
Average:  318  Profit:  14.975778546712968
Average:  319  Profit:  1.871972318339121

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

------------------- 305 -------------------
Average:  305  Profit:  8415
Average:  306  Profit:  6841.706666666755
Average:  307  Profit:  5477.853333333295
Average:  308  Profit:  4308.47999999997
Average:  309  Profit:  3318.6266666666183
Average:  310  Profit:  2493.3333333333026
Average:  311  Profit:  1817.6400000000046
Average:  312  Profit:  1276.5866666666598
Average:  313  Profit:  855.2133333333444
Average:  314  Profit:  538.5599999999962
Average:  315  Profit:  311.6666666666628
Average:  316  Profit:  159.57333333333247
Average:  317  Profit:  67.31999999999952
Average:  318  Profit:  19.94666666666656
Average:  319  Profit:  2.49333333333332

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

------------------- 307 -------------------
Average:  307  Profit:  7553
Average:  308  Profit:  5940.63905325451
Average:  309  Profit:  4575.804733727824
Average:  310  Profit:  3437.869822485174
Average:  311  Profit:  2506.2071005916914
Average:  312  Profit:  1760.1893491124056
Average:  313  Profit:  1179.1893491124235
Average:  314  Profit:  742.5798816568138
Average:  315  Profit:  429.73372781064677
Average:  316  Profit:  220.0236686390507
Average:  317  Profit:  92.82248520710172
Average:  318  Profit:  27.502958579881337
Average:  319  Profit:  3.437869822485167

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

------------------- 309 -------------------
Average:  309  Profit:  6611
Average:  310  Profit:  4966.942148760309
Average:  311  Profit:  3620.9008264462914
Average:  312  Profit:  2543.074380165295
Average:  313  Profit:  1703.6611570248065
Average:  314  Profit:  1072.8595041322258
Average:  315  Profit:  620.8677685950386
Average:  316  Profit:  317.8842975206619
Average:  317  Profit:  134.10743801652822
Average:  318  Profit:  39.73553719008274
Average:  319  Profit:  4.966942148760342

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

------------------- 311 -------------------
Average:  311  Profit:  5589
Average:  312  Profit:  3925.333333333347
Average:  313  Profit:  2629.66666666669
Average:  314  Profit:  1656.000000000012
Average:  315  Profit:  958.3333333333238
Average:  316  Profit:  490.6666666666684
Average:  317  Profit:  207.0000000000015
Average:  318  Profit:  61.33333333333355
Average:  319  Profit:  7.666666666666694

------------------- 312 -------------------
Average:  312  Profit:  5048
Average:  313  Profit:  3381.765625
Average:  314  Profit:  2129.625
Average:  315  Profit:  1232.421875
Average:  316  Profit:  631.0
Average:  317  Profit:  266.203125
Average:  318  Profit:  78.875
Average:  319  Profit:  9.859375

------------------- 313 -------------------
Average:  313  Profit:  4487
Average:  314  Profit:  2825.63265306119
Average:  315  Profit:  1635.2040816326735
Average:  316  Profit:  837.2244897959257
Average:  317  Profit:  353.20408163264875
Average:  318  Profit:  104.65306122449071
Average:  319  Profit:  13.08163265306134

------------------- 314 -------------------
Average:  314  Profit:  3906
Average:  315  Profit:  2260.416666666642
Average:  316  Profit:  1157.33333333335
Average:  317  Profit:  488.25
Average:  318  Profit:  144.66666666666876
Average:  319  Profit:  18.083333333333595

------------------- 315 -------------------
Average:  315  Profit:  3305
Average:  316  Profit:  1692.1599999999753
Average:  317  Profit:  713.8800000000052
Average:  318  Profit:  211.5199999999969
Average:  319  Profit:  26.439999999999614

------------------- 316 -------------------
Average:  316  Profit:  2684
Average:  317  Profit:  1132.3125
Average:  318  Profit:  335.5
Average:  319  Profit:  41.9375

------------------- 317 -------------------
Average:  317  Profit:  2043
Average:  318  Profit:  605.3333333333425
Average:  319  Profit:  75.66666666666781

------------------- 318 -------------------
Average:  318  Profit:  1382
Average:  319  Profit:  172.75
'''
