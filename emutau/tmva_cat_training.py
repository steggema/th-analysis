import optparse

import ROOT


training_vars = ['bdt_evt_leading_btag_pt', 'abs(bdt_evt_max_jet_eta)', '(bdt_evt_max_jet_eta30*(bdt_evt_max_jet_eta30>0.))', 'bdt_evt_njet_or30', 'bdt_evt_Met', 'bdt_evt_Mmt', 'bdt_evt_Mem',  'bdt_evt_missing_et', 'bdt_evt_nbjet', 'bdt_evt_centrality']#'bdt_evt_LT', , 
# 'bdt_evt_HT', 'abs(bdt_evt_deltaeta)', 'abs(bdt_muon_eta-bdt_tau_eta)', 'abs(bdt_muon_eta-bdt_electron_eta)', 'abs(bdt_electron_eta-bdt_tau_eta)', 'bdt_evt_maxMT', 'abs(bdt_evt_dphi_mete)', 'abs(bdt_evt_dphi_metmu)', 'abs(bdt_evt_dphi_mettau)']#, 'bdt_tau_decaymode', 'bdt_muon_charge',

# training_vars = ['bdt_evt_max_jet_eta','bdt_evt_njet_or30', 'bdt_evt_sphericity', 'bdt_evt_aplanarity']
# training_vars = ['bdt_evt_max_jet_eta','bdt_evt_njet_or30', 'bdt_evt_sphericity', 'bdt_evt_aplanarity', 'log(abs(bdt_muon_dz))', 'bdt_evt_sleading_btag_pt', 'bdt_muon_jet_csv']

# training_vars = ['bdt_evt_nbjet', 'bdt_evt_centrality', 'bdt_muon_charge', 'bdt_evt_HT']

# training_vars = ['bdt_evt_centrality', 'abs(bdt_evt_dphi_metmu)', 'bdt_evt_maxMT', 'bdt_evt_missing_et']

obs_vars = []

basic_selection = ''
signal_selection = '(bdt_evt_isSignal > 0.5 && bdt_evt_processid==16)' #tH -1
# signal_selection = '(bdt_evt_processid==7)' #ttH
# background_selection = '(bdt_evt_isSignal < 0.5 && bdt_evt_processid != 20 && bdt_evt_processid < 50 && (!{signal}))'.format(signal=signal_selection) # no data!
background_selection = '(bdt_evt_isSignal < 0.5 && bdt_evt_processid < 50 && (!{signal}))'.format(signal=signal_selection)

if '7' in signal_selection:
    signal_selection += '*(bdt_evt_njet_or30>1)'
    background_selection += '*(bdt_evt_njet_or30>1)'

def parse_options():
    usage = '''
%prog [options]
'''
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--input', dest='input_file', help='input file name', default='/afs/cern.ch/user/y/ytakahas/public/forJan/tH_BDTtraining_20140917/BDT_training_ss_f3.root', type='string')
    parser.add_option('-o', '--out_postfix', dest='out_postfix', help='output file postfix', default='', type='string')
    opts, args = parser.parse_args()
    return opts, args

def train(fileName, postfix):
    TMVA_tools = ROOT.TMVA.Tools.Instance()

    tfile = ROOT.TFile(fileName, postfix)

    tree = tfile.Get('Tree')

    num_pass = tree.GetEntries(signal_selection)
    num_fail = tree.GetEntries(background_selection)

    h = ROOT.TH1F('int', 'int', 1, -0.5, 1.5)

    tree.Project('int', '1.', '{sel}*bdt_evt_weight'.format(sel=signal_selection))

    print 'Integral signal', h.Integral()

    tree.Project('int', '1.', '{sel}*bdt_evt_weight'.format(sel=background_selection))

    print 'Background signal', h.Integral()

    print 'N events signal', num_pass
    print 'N events background', num_fail


    outFile = ROOT.TFile('TMVA_classification{postfix}.root'.format(postfix=postfix), 'RECREATE')

    factory    = ROOT.TMVA.Factory(
        "TMVAClassification", 
        outFile, 
        "!V:!Silent:Color:DrawProgressBar:Transformations=I" ) 

    for var in training_vars:
        factory.AddVariable(var, 'F') # add float variable

    factory.SetWeightExpression('bdt_evt_weight')

    factory.AddSignalTree(tree, 1.)
    factory.AddBackgroundTree(tree, 1.)

    # import pdb; pdb.set_trace()

    factory.PrepareTrainingAndTestTree( ROOT.TCut(signal_selection), ROOT.TCut(background_selection),
                                        "nTrain_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

    # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=250::BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=4:MinNodeSize=5" )

    # Optimized:
    # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=250::BoostType=Grad:Shrinkage=0.275:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=2:MinNodeSize=15" )
    # Re-Optimized:
    # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=1000::BoostType=Grad:Shrinkage=0.5:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=2:MinNodeSize=1" )
    factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG"+postfix, "!H:!V:NTrees=500::BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=4:MinNodeSize=10" )


    # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_TOP", "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.005:MaxDepth=5")
    # Optimizerd:
    factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_TOP"+postfix, "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.2:MaxDepth=2:MinNodeSize=6")

    factory.BookMethod( ROOT.TMVA.Types.kFisher, "Fisher"+postfix, "H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )
    # factory.BookMethod( ROOT.TMVA.Types.kFisher, "Fisher2"+postfix, "H:!V:Mahalanobis" )

    # factory.BookMethod( ROOT.TMVA.Types.kSVM, "SVM", "Gamma=0.25:Tol=0.001:VarTransform=Norm" )
# --- OptimizeConfigParamete...: For BDT_TOP the optimized Parameters are: 
# --- OptimizeConfigParamete...: AdaBoostBeta = 0.2
# --- OptimizeConfigParamete...: MaxDepth = 2
# --- OptimizeConfigParamete...: MinNodeSize = 8
# --- OptimizeConfigParamete...: NTrees = 10

# --- OptimizeConfigParamete...: MaxDepth = 4
# --- OptimizeConfigParamete...: MinNodeSize = 1
# --- OptimizeConfigParamete...: NTrees = 1000
# --- OptimizeConfigParamete...: Shrinkage = 0.5

# --- OptimizeConfigParamete...: For BDTG the optimized Parameters are: 
# --- OptimizeConfigParamete...: MaxDepth = 4
# --- OptimizeConfigParamete...: MinNodeSize = 10
# --- OptimizeConfigParamete...: NTrees = 505
# --- OptimizeConfigParamete...: Shrinkage = 0.05

# --- <WARNING> BDT_TOP                  : AdaBoostBeta = 0.2
# --- <WARNING> BDT_TOP                  : MaxDepth = 2
# --- <WARNING> BDT_TOP                  : MinNodeSize = 6
# --- <WARNING> BDT_TOP                  : NTrees = 257.5

    factory.TrainAllMethods()

    # factory.OptimizeAllMethods()

    factory.TestAllMethods()

    factory.EvaluateAllMethods()

    outFile.Close()

    # ROOT.TMVARegGui('TMVA.root')


if __name__ == '__main__':
    opts, args = parse_options()

    input_file = opts.input_file
    postfix = opts.out_postfix
    train(input_file, postfix)
