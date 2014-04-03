import numpy

import ROOT
TMVA_tools = ROOT.TMVA.Tools.Instance()

tfile = ROOT.TFile('BDT_training.root')
tree = tfile.Get('Tree')


# training_vars = ['bdt_evt_leading_btag_pt','bdt_evt_leading_btag', 'bdt_evt_max_jet_eta', '(bdt_evt_max_jet_eta30*(bdt_evt_max_jet_eta30>0.))', 'bdt_evt_njet_or30', 'bdt_evt_Met', 'bdt_evt_Mmt', 'bdt_evt_Mem', 'bdt_evt_LT',  'bdt_evt_missing_et', 'bdt_evt_nbjet', 'bdt_evt_centrality', 
# 'bdt_evt_HT', 'abs(bdt_evt_deltaeta)', 'abs(bdt_muon_eta-bdt_tau_eta)', 'abs(bdt_muon_eta-bdt_electron_eta)', 'abs(bdt_electron_eta-bdt_tau_eta)', 'bdt_evt_maxMT', 'abs(bdt_evt_dphi_mete)', 'abs(bdt_evt_dphi_metmu)', 'abs(bdt_evt_dphi_mettau)']#, 'bdt_tau_decaymode', 'bdt_muon_charge',

training_vars = ['bdt_evt_max_jet_eta','bdt_evt_njet_or30', 'bdt_evt_sphericity', 'bdt_evt_aplanarity']
# training_vars = ['bdt_evt_nbjet', 'bdt_evt_centrality', 'bdt_muon_charge', 'bdt_evt_HT']

# training_vars = ['bdt_evt_centrality', 'abs(bdt_evt_dphi_metmu)', 'bdt_evt_maxMT', 'bdt_evt_missing_et']
obs_vars = []


basic_selection = ''
signal_selection = '(bdt_evt_isSignal > 0.5 && bdt_evt_processid==6)' #tH -1
# signal_selection = '(bdt_evt_processid==7)' #ttH
background_selection = '(bdt_evt_isSignal < 0.5 && bdt_evt_processid < 50 && (!{signal}))'.format(signal=signal_selection) # no data!

if '7' in signal_selection:
    signal_selection += '*(bdt_evt_njet_or30>1)'
    background_selection += '*(bdt_evt_njet_or30>1)'

num_pass = tree.GetEntries(signal_selection)
num_fail = tree.GetEntries(background_selection)

h = ROOT.TH1F('int', 'int', 1, -0.5, 1.5)

tree.Project('int', '1.', '{sel}*bdt_evt_weight'.format(sel=signal_selection))

print 'Integral signal', h.Integral()

tree.Project('int', '1.', '{sel}*bdt_evt_weight'.format(sel=background_selection))

print 'Background signal', h.Integral()

print 'N events signal', num_pass
print 'N events background', num_fail


def train():
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
    # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=1000::BoostType=Grad:Shrinkage=0.5:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=2:MinNodeSize=1" )
    factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=500::BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.9:nCuts=500:MaxDepth=4:MinNodeSize=10" )


    # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_TOP", "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.005:MaxDepth=5")
    # Optimizerd:
    factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_TOP", "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.2:MaxDepth=2:MinNodeSize=6")

    factory.BookMethod( ROOT.TMVA.Types.kFisher, "Fisher", "H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )
    factory.BookMethod( ROOT.TMVA.Types.kFisher, "Fisher2", "H:!V:Mahalanobis" )

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



def read():
    import array

    reader = ROOT.TMVA.Reader('TMVAClassification_BDTG')

    varDict = {}
    for var in training_vars:
        varDict[var] = array.array('f',[0])
        reader.AddVariable(var, varDict[var])

    reader.BookMVA("BDTG","weights/TMVAClassification_BDTG.weights.xml")

    cut = 0.8
    ngood = 0
    nbad = 0

    ASSUMEDLOSS = 8.62
    deviation = 0.

    sumLoss = 0.
    nLoss = 0.

    sumDeltaLoss = 0.

    bdtOuts = []
    losses = []

    for jentry in xrange(tree.GetEntries()):

        ientry = tree.LoadTree(jentry)
        nb = tree.GetEntry(jentry)

        for var in varDict:
            varDict[var][0] = getattr(tree, var)

        bdtOutput = reader.EvaluateMVA("BDTG")

        loss = tree.loss
        bdtOuts.append(bdtOutput)
        losses.append(loss)

        if jentry%1000 == 0:
            print jentry, varDict['f1'], bdtOutput, loss
        if loss:
            sumLoss += loss
            nLoss += 1.

        if bdtOutput > cut:
            sumDeltaLoss += abs(ASSUMEDLOSS - loss)
            if not loss:
                nbad += 1
            else:
                ngood += 1
        else:
            sumDeltaLoss += abs(loss)
            if loss:
                nbad += 1
            else:
                ngood += 1
    
    print 'ngood', ngood
    print 'nbad', nbad

    totalSum = float(tree.GetEntries())

    print 'DeltaLoss', sumDeltaLoss/totalSum
    print 'Average Loss:', sumLoss/nLoss

    cuts = [0., 0.1, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8]
    # Also minimise assumed loss
    for cut in cuts:
        sumDeltaLoss = 0.
        for i, bdtOut in enumerate(bdtOuts):
            loss = losses[i]
            if bdtOut > cut:
                 sumDeltaLoss += abs(ASSUMEDLOSS - loss)
            else:
                 sumDeltaLoss += abs(loss)
        print 'Cut', cut, 'DeltaLoss', sumDeltaLoss/totalSum

    # BETTER EVEN: find optimal assumed loss for each bin in output BDT

    BDTG = numpy.zeros(1, dtype=float)
    loss = numpy.zeros(1, dtype=float)

    fout = ROOT.TFile('trainPlusBDTG.root', 'RECREATE')
    treeout = ROOT.TTree()
    treeout.Branch('BDTG', BDTG, 'BDTG/D')
    treeout.Branch('loss', loss, 'loss/D')


    for i, bdtOut in enumerate(bdtOuts):
        BDTG[0] = bdtOut
        loss[0] = losses[i]
        if i%1000==0:
            print i, BDTG[0], loss[0]
        treeout.Fill()
    treeout.Write()
    fout.Write()
    fout.Close()


if __name__ == '__main__':
    train()
    # read()

