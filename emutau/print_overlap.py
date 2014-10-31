import ROOT
# f = ROOT.TFile('BDT_training_ss_f12_mva.root')
f = ROOT.TFile('/afs/cern.ch/user/y/ytakahas/public/forJan/tH_BDTtraining_20140830/BDT_training_ss_f12.root')

tree = f.Get('Tree')
nEvts = tree.Draw("bdt_evt_evt", "bdt_evt_isSignal")
signalEvts = tree.GetV1()
evtList = []
for i in range(nEvts):
    evtList.append(int(signalEvts[i]))

fBen = open('/afs/cern.ch/user/s/stiegerb/public/forYuta/eventlist_thq_2lss_em.txt', 'rb')
evtsBen = []
for line in fBen:
    try:
        evtsBen.append(int(line))
    except:
        pass

overlap = [evt for evt in evtsBen if evt in evtList]

print overlap
print 'Overlap', len(overlap)
print 'N us', len(evtList)
print 'N them', len(evtsBen)
