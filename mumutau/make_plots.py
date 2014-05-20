import sys
sys.path.append("../Common")

from Plotter import Plotter
from samples import sampleDict

if __name__ == '__main__':
    variables = [
    {'var':'BDTG', 'varname':'BDTG', 'legend':'top left', 'logy':False, 'title':'BDT score', 'unit':'', 'nbinsx':10, 'xmin':-1., 'xmax':1.0001, 'save':True},
    {'var':'Fisher', 'varname':'Fisher', 'legend':'top left', 'logy':False, 'title':'Fisher score', 'unit':'', 'nbinsx':10, 'xmin':-1., 'xmax':1.0001, 'save':True},
    {'var':'bdt_evt_missing_et', 'varname':'bdt_evt_missing_et', 'legend':'top right', 'logy':False, 'title':'E_{T}^{miss}', 'unit':'GeV', 'nbinsx':20, 'xmin':0., 'xmax':300.},
    {'var':'bdt_evt_centrality', 'varname':'bdt_evt_centrality', 'legend':'top right', 'logy':False, 'title':'Centrality', 'unit':'', 'nbinsx':20, 'xmin':0., 'xmax':1.},
    # {'var':'bdt_evt_sphericity', 'varname':'bdt_evt_sphericity', 'legend':'top right', 'logy':False, 'title':'Sphericity', 'unit':'', 'nbinsx':12, 'xmin':0., 'xmax':1.},
    # {'var':'bdt_evt_aplanarity', 'varname':'bdt_evt_aplanarity', 'legend':'top right', 'logy':False, 'title':'Aplanarity', 'unit':'', 'nbinsx':12, 'xmin':0., 'xmax':0.4},
    {'var':'bdt_tau_decaymode', 'varname':'bdt_tau_decaymode', 'legend':'top right', 'logy':False, 'title':'#tau decay mode', 'unit':'', 'nbinsx':11, 'xmin':-0.5, 'xmax':10.5},
    {'var':'bdt_tau_mass', 'varname':'bdt_tau_mass', 'legend':'top right', 'logy':False, 'title':'#tau_{1} mass', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':3.5},
    {'var':'bdt_stau_mass', 'varname':'bdt_stau_mass', 'legend':'top right', 'logy':False, 'title':'#tau_{2} mass', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':3.5},
    {'var':'bdt_tau_isolation', 'varname':'bdt_tau_isolation', 'legend':'top right', 'logy':False, 'title':'#tau_{1} isolation (GeV)', 'unit':'GeV', 'nbinsx':11, 'xmin':0., 'xmax':2.2},
    {'var':'bdt_stau_isolation', 'varname':'bdt_stau_isolation', 'legend':'top right', 'logy':False, 'title':'#tau_{2} isolation (GeV)', 'unit':'GeV', 'nbinsx':11, 'xmin':0., 'xmax':2.2},
    {'var':'bdt_evt_leading_btag_pt', 'varname':'bdt_evt_leading_btag_pt', 'legend':'top right', 'logy':False, 'title':'p_{T} b jet_{1}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':200.},
    {'var':'bdt_evt_sleading_btag_pt', 'varname':'bdt_evt_sleading_btag_pt', 'legend':'top right', 'logy':False, 'title':'p_{T} b jet_{2}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':200.},
    {'var':'bdt_evt_leading_btag', 'varname':'bdt_evt_leading_btag', 'legend':'top right', 'logy':False, 'title':'CSV b jet_{1}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.},
    {'var':'bdt_evt_sleading_btag', 'varname':'bdt_evt_sleading_btag', 'legend':'top right', 'logy':False, 'title':'CSV b jet_{2}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.},
    # {'var':'bdt_evt_leading_nbtag', 'varname':'bdt_evt_leading_nbtag', 'legend':'top right', 'logy':False, 'title':'CSV l jet_{1}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.},
    # {'var':'bdt_evt_sleading_nbtag', 'varname':'bdt_evt_sleading_nbtag', 'legend':'top right', 'logy':False, 'title':'CSV l jet_{2}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.},
    {'var':'bdt_evt_max_jet_eta', 'varname':'bdt_evt_max_jet_eta', 'legend':'top right', 'logy':False, 'title':'max(jet |#eta|)', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':5.},
    {'var':'(bdt_evt_max_jet_eta30*(bdt_evt_max_jet_eta30>0.))', 'varname':'bdt_evt_max_jet_eta30', 'legend':'top right', 'logy':False, 'title':'max(jet |#eta|, 30 GeV)', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':5.},
    {'var':'bdt_evt_njet_or', 'varname':'bdt_evt_njet_or', 'legend':'top right', 'logy':False, 'title':'N_{jets} (20 GeV)', 'unit':'', 'nbinsx':10, 'xmin':-0.5, 'xmax':9.5},
    {'var':'bdt_evt_njet_or30', 'varname':'bdt_evt_njet_or30', 'legend':'top right', 'logy':False, 'title':'N_{jets} (30 GeV)', 'unit':'', 'nbinsx':10, 'xmin':-0.5, 'xmax':9.5},
    {'var':'bdt_evt_sumjetpt', 'varname':'bdt_evt_sumjetpt', 'legend':'top right', 'logy':False, 'title':'#Sigma jet p{T}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':500.},
    {'var':'bdt_evt_Mmt', 'varname':'bdt_evt_Mmt', 'legend':'top right', 'logy':False, 'title':'m(#mu, #tau)', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    # {'var':'bdt_evt_LT', 'varname':'bdt_evt_LT', 'legend':'top right', 'logy':False, 'title':'#Sigma lepton p_{T}', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':300.},
    # {'var':'bdt_evt_L2T', 'varname':'bdt_evt_L2T', 'legend':'top right', 'logy':False, 'title':'m_{vis}(#tau, l_{2})', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':200.},
    {'var':'bdt_evt_nbjet', 'varname':'bdt_evt_nbjet', 'legend':'top right', 'logy':False, 'title':'N_{b jet}', 'unit':'GeV', 'nbinsx':5, 'xmin':-0.5, 'xmax':4.5},
    {'var':'bdt_evt_HT', 'varname':'bdt_evt_HT', 'legend':'top right', 'logy':False, 'title':'#Sigma p_{T} (jets, leptons)', 'unit':'GeV', 'nbinsx':10, 'xmin':100., 'xmax':600.},
    {'var':'abs(bdt_evt_deltaeta)', 'varname':'abs_bdt_evt_deltaeta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(forward jet, muon)|', 'unit':'GeV', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'abs(bdt_muon_eta-bdt_tau_eta)', 'varname':'abs_bdt_muon_eta_MINUS_bdt_tau_eta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(#mu, #tau)|', 'unit':'GeV', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'bdt_evt_maxMT', 'varname':'bdt_evt_maxMT', 'legend':'top right', 'logy':False, 'title':'max(M_{T} #mu, e)', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_tau_MT', 'varname':'bdt_tau_MT', 'legend':'top right', 'logy':False, 'title':'M_{T} #tau', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_muon_MT', 'varname':'bdt_muon_MT', 'legend':'top right', 'logy':False, 'title':'M_{T} #mu', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    # {'var':'abs(bdt_evt_dphi_mete)', 'varname':'abs_bdt_evt_dphi_mete', 'legend':'top right', 'logy':False, 'title':'|#Delta #phi(E_{T}^{miss}, e)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':3.1415927},
    {'var':'abs(bdt_evt_dphi_metmu)', 'varname':'abs_bdt_evt_dphi_metmu', 'legend':'top right', 'logy':False, 'title':'|#Delta #phi(E_{T}^{miss}, #mu)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':3.1415927},
    {'var':'abs(bdt_evt_dphi_mettau)', 'varname':'abs_bdt_evt_dphi_mettau', 'legend':'top right', 'logy':False, 'title':'|#Delta #phi(E_{T}^{miss}, #tau)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':3.1415927},
    ]


    p = Plotter(variables, sampleDict, fileName="BDT_training_mva.root", signalsampleIds=[13], datasampleIds=[100])
    p.readTuples()
    p.makePlots(weight='bdt_evt_weight')
    