import numpy

import ROOT
TMVA_tools = ROOT.TMVA.Tools.Instance()




training_vars = ['bdt_evt_leading_btag_pt', 'bdt_evt_leading_btag', 'bdt_evt_sleading_btag', 'bdt_tau_decaymode', 'bdt_stau_decaymode', 'bdt_evt_missing_et', 'bdt_evt_nvetobjet', 'bdt_evt_max_jet_eta30']#, 'bdt_evt_max_jet_eta', 'bdt_evt_njet_or', 'bdt_evt_njet', 'bdt_evt_centrality', 'bdt_evt_H', 'bdt_evt_HT', 'bdt_evt_sumjetpt', 'bdt_evt_Mmt', 'bdt_evt_sMmt',
    # 'bdt_evt_dphi_metmu',  'bdt_evt_dphi_mettau', 'bdt_evt_dphi_metstau', 'bdt_stau_MT', 'bdt_tau_MT', 'bdt_muon_MT']

# training_vars = ['bdt_evt_centrality', 'abs(bdt_evt_dphi_metmu)', 'bdt_evt_maxMT', 'bdt_evt_missing_et']
obs_vars = []


basic_selection = ''
signal_selection = '(bdt_evt_isSignal > 0.5 && bdt_evt_processid==13)*(bdt_evt_njet_or30>1)' #tH -1
# signal_selection = '(bdt_evt_processid==7)' #ttH
background_selection = '(bdt_evt_isSignal < 0.5 && bdt_evt_processid < 50 && (!{signal}))*(bdt_evt_njet_or30>1)'.format(signal=signal_selection) # no data!

if '7' in signal_selection:
    signal_selection += '*(bdt_evt_njet_or30>1)'
    background_selection += '*(bdt_evt_njet_or30>1)'

    




def train():
    tfile = ROOT.TFile('BDT_training.root')
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
    outFile = ROOT.TFile('TMVA_classification.root', 'RECREATE')

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
    factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=1000::BoostType=Grad:Shrinkage=0.5:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=2:MinNodeSize=1" )


    # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_TOP", "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.005:MaxDepth=5")
    # Optimizerd:
    factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_TOP", "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.2:MaxDepth=2:MinNodeSize=6")

    factory.BookMethod( ROOT.TMVA.Types.kFisher, "Fisher", "H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )

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
    train()
    # read()

