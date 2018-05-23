import matplotlib.pyplot as plt
import numpy as np


# first attempt without the correct buckets and decision to buy
# wins = [-0.000548741085857627  ,
#  -0.000223161851068725  ,
#  0.001876172607879801    ,
#  -0.0011625975751536391  ,
#  0.0    ,
#  -0.0011641443539000696  ,
#  0.0030968468468467692    ,
#  -0.003432494279176201  ,
#  -0.0007086669973779852  ,
#  0.005413675414852369    ,
#  -0.003343093764428718  ,
#  5.988023952101797e-05,
#  -0.0022211830722468928  ,
#  0.0006197706848464958    ,
#  0.0016393442622950265    ,
#  -0.0008941116362240807  ,
#  0.0016548360405870006    ,
#  -0.001455967386330559  ,
#  0.0005816731412427083    ,
#  0.001966085033177666    ,
#  -0.007001166861143457  ,
#  -0.006427032704872845  ,
#  -0.0027649769585253127  ,
#  0.002134044681560572    ,
#  0.006896551724137777    ,
#  0.0012048192771084631    ,
#  0.004249291784702508    ,
#  0.006526064464783027    ,
#  -0.0030642434488588506  ,
#  -0.004432249894470348  ,
#  0.0023213825122517977    ,
#  -0.004904306220095748  ,
#  -0.0010043875878839098  ,
#  0.0053794363433365845    ,
#  -0.0022000586682311904  ,
#  0.008166713601802203    ,
#  0.000339558573853929    ,
#  0.0011195718904525587    ,
#  0.000535000951112677    ,
#  0.0009518143961927333    ,
#  0.0022259973053716737    ,
#  -0.00035934599029760207  ,
#  0.001875000000000088    ,
#  -0.0014028524666821612  ,
#  -0.0037582995782352614  ,
#  -0.0030030651975809647  ,
#  0.000740009866798175    ,
#  0.001744921033420448    ,
#  0.0    ,
#  -0.0018126888217522444  ,
#  -0.0014005602240896224  ,
#  0.00455126157777066    ,
#  -0.0021213406873144343  ,
#  -0.0008591065292096429  ,
#  0.0028585040495473437    ,
#  -0.00791097515953802  ,
#  -8.837617613953565e-05,
#  -0.0019248043115615795  ,
#  -0.001087902523933882  ,
#  -0.00354191263282169  ,
#  0.0    ,
#  0.0014028993252721547    ,
#  -0.001835290977042277  ,
#  0.0005207655253222363    ,
#  -0.0008807985907222444  ,
#  -0.000280112044817934  ,
#  -0.0053944706675658075  ,
#  0.0015184912491485014    ,
#  -0.0013063202147115286  ,
#  -0.0038970240906942817  ,
#  -0.0007792363483785364  ,
#  -0.001110981171792768  ,
#  -0.00031055900621101935  ,
#  -4.1918175720889114e-05,
#  -0.0020392874979191125  ,
#  -0.002819548872180424  ,
#  0.0004920049200492792    ,
#  -0.004407859798194487  ,
#  -0.0019743336623889917  ,
#  -0.003621001810500993  ,
#  -0.006944444444444378  ,
#  -7.984031936114954e-05,
#  0.008085687283419116    ,
#  0.0034697296003827565    ,
#  -0.0017338534893801896  ,
#  -0.004290708761521366  ,
#  -0.001407729715894513  ,
#  -0.0005112925122093345  ,
#  0.0019457776624724821    ,
#  -0.0009212344541687081  ,
#  0.0023640661938534053    ,
#  0.0    ,
#  0.0020943452677770207    ,
#  0.0014239482200648298    ,
#  -0.0013192612137203645  ,
#  -0.005574136008918602  ,
#  0.0003387533875339295    ,
#  0.0017790811339197684    ,
#  -0.0018289569007494135  ,
#  -0.004486422668240767  ,
#  -0.00012004801920780313  ,
#  -0.0046612802983218415  ,
#  -0.0016412661195779046  ,
#  0.0009555463232238769    ,
#  -0.004088273330274117  ,
#  0.001069442463995463    ,
#  -0.003990024937655741  ,
#  -0.0048543689320388215  ,
#  -0.0069417054508164365  ,
#  -0.003985317252228614  ,
#  0.001188354129530629    ,
#  0.0018602179112410476    ,
#  -0.002378107145617349  ,
#  0.0014269036191465292    ,
#  0.0013745293730950826    ,
#  -0.010386336969275604  ,
#  -0.0014742014742015433  ,
#  -0.009422850412249615  ,
#  -0.004187994416007396  ,
#  -0.0032422417786011756  ,
#  -0.005625879043600509  ,
#  -0.0024059492563430155  ,
#  -0.009525052192066825  ,
#  -0.003836505828537698  ,
#  3.352329869262488e-05 ,
#  0.022415242364808005    ,
#  -0.0010319917440660957  ,
#  0.002712067307525119    ,
#  0.0061244019138757474    ,
#  0.0029829375969455444    ,
#  -0.0010264460813911155  ,
#  0.0028391167192429287    ,
#  0.0007100591715977467    ,
#  0.0032333921222810398    ,
#  -0.0017186452045606711  ,
#  0.00042970708300525066    ,
#  0.006609049313675643    ,
#  0.003687768899815568    ,
#  -0.00463511911178188  ,
#  0.0033157022183626698    ,
#  0.004000000000000031    ,
#  -0.003787059078121652  ,
#  0.002202380952380909    ,
#  -0.006285739229123865  ,
#  0.004668304668304748    ,
#  -0.0064965197215775825  ,
#  0.0011834319526627104    ,
#  -0.0024503311258279098  ,
#  0.0    ,
#  0.0002185792349726829    ,
#  0.0010724938834333472    ,
#  -0.0083857442348009  ,
#  0.004609778933369885    ,
#  -0.00012961762799731244  ,
#  -0.002379889930090662  ,
#  0.01035834266517352    ,
#  0.0010295126973233152    ,
#  0.001144353503717427    ,
#  0.0012730063174425182    ,
#  -0.0011916110581506488  ,
#  0.0007885956930542386    ,
#  -0.0028453999367689165  ,
#  -0.0004756242568370136  ,
#  -0.0021328203412512114  ,
#  0.0016753615812019286    ,
#  0.0005068423720223684    ,
#  0.001841620626150991    ,
#  -0.0025801407349491145  ,
#  0.003838771593090189    ,
#  -0.002531340405014461  ,
#  0.0006239415277655582    ,
#  0.0    ,
#  -0.002918577640121611  ,
#  -1.1940298507474628e-05,
#  0.0    ,
#  -0.004649530660584232  ,
#  0.0024384296513044537    ,
#  -0.0047449584816134415  ,
#  -0.003254300325430061  ,
#  0.0014144271570014008    ,
#  0.00013294336612610562    ,
#  -0.003900325027085568  ,
#  -0.0027961191214122  ,
#  -0.00013234515616735923  ,
#  0.0014947683109118775    ,
#  -0.0025046218298174143  ,
#  -0.0007728434694726309  ,
#  0.0021469465648855162    ,
#  0.0017532192733209146    ,
#  -0.002215891104779919  ,
#  0.0    ,
#  -2.1175673386434866e-05,
#  -0.0015949632738719766  ,
#  -0.003521126760563411  ,
#  -0.001226241569589239  ,
#  -0.0018891687657431188  ,
#  -0.0074517212426532435  ,
#  -0.0016731734523145973  ,
#  -0.003966822935449004  ,
#  -0.003090659340659253  ,
#  -0.0005434782608696373  ,
#  -0.004045950437107205  ,
#  0.002972940177162939    ,
#  0.005504587155963352    ,
#  0.006398862424457813    ,
#  0.0036900369003690934    ,
#  0.004701457451810074    ,
#  0.0006687621213135376    ,
#  0.0    ,
#  -0.002195871761089206  ,
#  0.004029550033579536    ,
#  0.0013601329907813704    ,
#  -0.0020608980871382543  ,
#  0.0027160257484027494    ,
#  -0.0010766838138534227  ,
#  0.0018862563253067084    ,
#  -0.0011529825838947543  ,
#  0.004176035978156134    ,
#  0.0031257513825438915    ,
#  -0.001346687989226383  ,
#  0.0015268146828679224    ,
#  -0.0012048192771084221  ,
#  -0.0010265319014530051  ,
#  -0.005076142131979709  ,
#  -0.0013850415512465161  ,
#  0.012594727292133708    ,
#  -0.008422234699606863  ,
#  0.002777777777777869    ,
#  -0.00012239902080790285  ,
#  -0.006836544437538808  ,
#  0.007622544928503842    ,
#  0.0014526064172105735    ,
#  0.0025178902729923033    ,
#  -0.005312328265250009  ,
#  -0.0032138442521631753  ,
#  0.00047281323877054326    ,
#  -0.010486558542546091  ,
#  -0.0022181891510384606  ,
#  0.0    ,
#  -0.007107952021323788  ,
#  -0.001081373344147093  ,
#  0.0023794183882119425    ,
#  0.00409614529904256    ,
#  0.011333494092114796    ,
#  0.008269264879477862    ,
#  0.008134556574923619    ,
#  0.009261515963928827    ,
#  0.002415252425939426    ,
#  0.0031582936792015274    ,
#  0.0072992700729928375    ,
#  0.006195147134744489    ,
#  0.008109794135995003    ,
#  -0.001440345682964033  ,
#  0.016908476055416163    ,
#  0.003195816385822116    ,
#  0.002101879327398599    ,
#  0.0006441223832527027    ,
#  0.0004071108698602793    ,
#  0.0043972706595905246    ,
#  0.004955752212389453    ,
#  -0.0005179526073363611  ,
#  0.008072201356578358    ,
#  -0.0018833535844470259  ,
#  0.0005308560053085154    ,
#  -0.003496190049305256  ,
#  -0.003015833123900449  ,
#  -0.003322259136212654  ,
#  -0.00762502803319124  ,
#  0.0006061422413792155    ,
#  -0.002591380250954708  ,
#  0.002902757619738724    ,
#  0.0013010344839968929    ,
#  0.0008274869580859821    ,
#  0.0007192519779428919    ,
#  0.0021797045289416524    ,
#  0.0019489048002372964    ,
#  0.0033431198165569383    ,
#  0.012048192771084222    ,
#  0.002065049044914867    ,
#  0.0024953212726137744    ,
#  0.0037812681791738723    ,
#  0.0015283842794759012    ,
#  -0.0003698680803847386  ,
#  -0.0053314235696664825  ,
#  0.0021402800709350157    ,
#  -0.006406149903907907  ,
#  0.0020982971511582372    ,
#  0.0019062531912721005    ,
#  -0.0027186225645672536  ,
#  -0.0024691358024691717  ,
#  0.0030415867866095685    ,
#  0.00024350155232240198    ,
#  0.0003930302633303286    ,
#  -0.0016599371915657162  ,
#  -0.0003368137420005723  ,
#  0.007497273718647724    ,
#  -0.0002511931675458829  ,
#  -0.0004739336492889569  ,
#  0.0    ,
#  0.0    ,
#  -0.0015562472209870227  ,
#  -0.00045292777773804676  ,
#  -0.00025149700598810925  ,
#  0.0010751403655478151    ,
#  0.0021587910769969017    ,
#  0.0019420754876298618    ,
#  0.0007935656836461621    ,
#  0.0035842293906809693    ,
#  -0.0005125576627371259  ,
#  0.002501563477173294    ,
#  0.004309416074121945    ,
#  -0.004355400696864217  ,
#  -0.00012327416173563637  ,
#  0.0    ,
#  0.0004015419209766033    ,
#  0.00030125018828140764    ,
#  0.0009232473687448546    ,
#  0.00013598966478549436    ,
#  0.0007052186177715024    ,
#  0.007673336833237746    ,
#  -0.00021948676677710437  ,
#  -0.00036359229184348746  ,
#  -0.0024784763892512288  ,
#  0.0029007163890475253    ,
#  -0.002475860361475505  ,
#  0.0014177693761814579    ,
#  0.0006052454606589504    ,
#  -0.0032152588555858794  ,
#  0.00013513513513521168    ,
#  0.0005111906561990629    ,
#  -0.0004997501249375356  ,
#  -0.00541941564561741  ,
#  0.0011981787682722553    ,
#  0.00025151959756860453    ,
#  -0.0020916483469575237  ,
#  0.0    ,
#  -0.0015290519877677869  ,
#  0.006218905472636832    ,
#  -0.0008613264427218125  ,
#  0.00199291408325945    ,
#  0.02633101851851853    ,
#  0.0019438707325963296  ]


# second with default value
# wins = [0.0016704450542894078  ,
# 0.00326797385620923  ,
# 0.00023975065931435143  ,
# 0.0  ,
# -0.0024390243902438795  ,
# 0.0  ,
# -0.0013836042891732833  ,
# -0.000476701227505737  ,
# 0.00554468362687541  ,
# 0.00529482551143204  ,
# 0.004273504273504152  ,
# 0.006150061500614947  ,
# 0.004385964912280784  ,
# -0.001549833094897478  ,
# -0.005849853753656213  ,
# -0.00504080652904464  ,
# 0.0  ,
# -0.0031098825155494413  ,
# 0.0  ,
# 0.0029282576866763994]



# 3rd wth 0.70
# wins = [0.0 ,
#  0.0012991230919129463 ,
#  0.007904191616766433 ,
#  0.0007249879168680043 ,
#  0.0003334444814938846 ,
#  0.0 ,
#  -0.0014577259475219754,
#  -0.0022816166883962725,
#  0.00072568940493464 ,
#  0.0012360939431396668 ,
#  0.0014771048744460715 ,
#  -0.00033579583613157186,
#  0.0016766467065869321 ,
#  -0.00032647730982701917,
#  0.002659574468085204 ,
#  -0.002438429651304619,
#  0.009852216748768378 ,
#  0.0014792899408285136]

# 3rd with 0.90
# wins = [0.0014727540500736236  ,
# 0.002484472049689628  ,
# -0.0026945099360053634  ,
# 0.00023866348448674991  ,
# 0.0  ,
# 0.0014499758337361724  ,
# 0.004628501827040109  ,
# -0.0001196315348726926  ,
# -0.00032647730982701917  ,
# 0.0009671179883945749  ,
# -0.002438429651304619  ,
# 0.007389162561576284  ,
# 0.0014792899408285136 ]


# 4th_bot_results_buy_0.90.txt
# wins = [-0.0007237635705669004 ,
# -0.0010060362173037565 ,
# 0.0010065425264217315 , 
# 0.008578431372549145 , 
# 0.004573170731707273 , 
# 0.005768578215134036 , 
# -0.0010169491525423057 ,
# 0.003717472118959072 , 
# 0.0061633281972265745 , 
# -0.00034083162917524195 ,
# -0.000724900326205099 ,
# 0.004864311315924129 , 
# 0.0020512820512820318 ]


# 5th_bot_resultst_buy_0.90.txt
# wins = [0.0003345600535295487  ,
# 0.0  ,
# 0.0010392309690828688  ,
# 0.0011820330969267026  ,
# 0.0  ,
# -0.0016784155756965832  ,
# 0.0014393666786614565  ,
# 0.0002400096003840537  ,
# 0.000667556742323091  ,
# -0.0015056461731493805  ,
# 0.001296008294453116  ,
# 0.0  ,
# -0.0030165912518853406  ,
# -0.0016447368421053032]


# log_tuesday_start_0.6.txt not finished
wins = [-0.0017307026652821466  ,
-0.0040246847330293435  ,
0.0024483133841131893  ,
-0.0020855057351407517  ,
-0.0015723270440251421  ,
0.003714961161769694  ,
-0.00024734108335381706  ,
-0.0008628127696290449  ,
0.002431399791594339  ,
0.0010905125408942097  ,
0.0010460251046025004  ,
0.002118083134763019  ,
-0.0015822784810126432  ,
-0.003062266076896932  ,
0.004082642583199373  ,
0.0017458100558659642  ,
0.0019225487503434335  ,
0.003154574132492083  ,
0.0030927835051546677  ,
0.000800000000000128  ,
-0.003210272873194191  ,
-0.00012348728081001262  ,
0.0  ,
0.0  ,
-0.0003418803418802807  ,
-0.0021668472372697515  ,
-0.005561735261401504  ,
-0.004343105320303976  ,
0.001706484641638209  ,
0.0006257822277847461  ,
-0.001420959147424498  ,
-0.00720720720720726  ,
-0.008565310492505453  ,
-0.003859081289680096  ,
-0.0007528230865746052  ,
0.0014630577907827219  ,
0.001083423618634876  ,
0.003878702397743323  ,
0.005235602094240788  ,
0.0  ,
0.0025062656641604243  ,
-0.002162799842705412  ,
0.0010873504893077713  ,
0.006437768240343286  ,
0.0017519271198317388  ,
0.0017301038062283573  ,
0.0016982734220208331  ,
0.0019433647973349365  ,
-0.006821282401091403  ,
-0.010649627263045691  ,
0.002433936022253165  ,
-0.005468465184105004  ,
-0.005145797598627738  ,
-0.0002506579771899943  ,
0.0003669724770641545  ,
-0.003028634361233405  ,
0.0017452006980802626  ,
0.0  ,
0.0010706638115631588  ,
0.0024734982332155838  ,
0.00019689884321932754  ,
-0.00512820512820508  ,
0.00027578599007156154  ,
0.0002499062851429419  ,
-0.0014662756598240328  ,
0.004918653045781326  ,
-0.0033149171270717916  ,
0.008354522339266236  ,
-0.0020384391380313814  ,
0.005910498170560081  ,
0.005366726296958955  ,
-0.006493506493506582  ,
0.0007538635506974444  ,
0.001403705783267861  ,
-0.00029036004645765384  ,
0.0044792833146698  ,
-0.004494382022471867  ,
0.0025273799494524244  ,
0.009275362318840687  ,
-0.0022421524663676917  ,
-0.00534759358288765  ,
-0.0021969974368363024  ,
-0.000897435897435954  ,
0.00486891385767792  ,
0.0002797985450476105  ,
0.0022246941045606016  ,
0.008912655971479567  ,
-0.0035277877192085236  ,
-0.0002556890820762362  ,
-0.0017021276595745479  ,
0.003965392934390795  ,
-0.007864878803506909  ,
-0.011796042617960379  ,
-0.008424599831508018  ,
-0.012429378531073518  ,
-0.008393632416787233  ,
-0.0055762081784387655  ,
-0.013529184383455807  ,
-0.005651846269781472  ,
0.0033821871476888065  ,
-0.003696857670979632  ,
-0.0007791195948578032  ,
0.0017472335468841822  ,
0.0012755102040816638  ,
-0.0036697247706423217  ,
-0.007717750826901801  ,
0.0019462826002336012  ,
-0.005959031657355623  ,
0.0005768676088838534  ,
-0.0010946907498631533  ,
-0.0002542911633821131  ,
0.0  ,
0.005535055350553609  ,
0.000287686996547802  ,
-0.002696456086286504  ,
-0.0033271719038817315]


wins = np.array(wins, dtype='float32')

print(len(wins))


def display_histogram_wins(wins):
	plt.title('Histogram of wins')
	plt.xlabel('Value')
	plt.ylabel('Number of wins')
	plt.hist(wins, bins=20, range=(-0.01, 0.01))
	plt.show()


print(np.mean(wins))


print(np.sum(wins))
display_histogram_wins(wins)



