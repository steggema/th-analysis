import ROOT
# f = ROOT.TFile('BDT_training_ss_f12_mva.root')
f = ROOT.TFile('/afs/cern.ch/user/y/ytakahas/public/forJan/tH_BDTtraining_20140830/BDT_training_ss_f12.root')

tree = f.Get('Tree')
nEvts = tree.Draw("bdt_evt_run:bdt_evt_lum:bdt_evt_evt", "bdt_evt_processid==19")


run = tree.GetV1()
lumi = tree.GetV2()
evt = tree.GetV3()
evtList = []
for i in range(nEvts):
    print int(run[i]), int(lumi[i]), int(evt[i])

