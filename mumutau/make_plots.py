import sys
sys.path.append("../Common")

import ROOT

from Plotter import Plotter

if __name__ == '__main__':
    variables = [
    {'var':'BDTG', 'varname':'BDTG', 'legend':'top left', 'logy':False, 'title':'BDT score', 'unit':'', 'nbinsx':5, 'xmin':-0.8, 'xmax':0.8, 'save':True},
    {'var':'Fisher', 'varname':'Fisher', 'legend':'top left', 'logy':False, 'title':'Fisher score', 'unit':'', 'nbinsx':5, 'xmin':-0.6, 'xmax':0.6, 'save':True},
    {'var':'bdt_evt_missing_et', 'varname':'bdt_evt_missing_et', 'legend':'top right', 'logy':False, 'title':'E_{T}^{miss}', 'unit':'GeV', 'nbinsx':20, 'xmin':0., 'xmax':300.},
    {'var':'bdt_evt_centrality', 'varname':'bdt_evt_centrality', 'legend':'top right', 'logy':False, 'title':'Centrality', 'unit':'', 'nbinsx':20, 'xmin':0., 'xmax':1.},
    {'var':'bdt_evt_sphericity', 'varname':'bdt_evt_sphericity', 'legend':'top right', 'logy':False, 'title':'Sphericity', 'unit':'', 'nbinsx':12, 'xmin':0., 'xmax':1.},
    {'var':'bdt_evt_aplanarity', 'varname':'bdt_evt_aplanarity', 'legend':'top right', 'logy':False, 'title':'Aplanarity', 'unit':'', 'nbinsx':12, 'xmin':0., 'xmax':0.4},
    {'var':'bdt_tau_decaymode', 'varname':'bdt_tau_decaymode', 'legend':'top right', 'logy':False, 'title':'#tau decay mode', 'unit':'', 'nbinsx':11, 'xmin':-0.5, 'xmax':10.5},
    {'var':'bdt_tau_mass', 'varname':'bdt_tau_mass', 'legend':'top right', 'logy':False, 'title':'#tau mass', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':3.5},
    {'var':'bdt_evt_leading_btag_pt', 'varname':'bdt_evt_leading_btag_pt', 'legend':'top right', 'logy':False, 'title':'p_{T} b jet_{1}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':200.},
    {'var':'bdt_evt_sleading_btag_pt', 'varname':'bdt_evt_sleading_btag_pt', 'legend':'top right', 'logy':False, 'title':'p_{T} b jet_{2}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':200.},
    {'var':'bdt_evt_leading_btag', 'varname':'bdt_evt_leading_btag', 'legend':'top right', 'logy':False, 'title':'CSV b jet_{1}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.},
    {'var':'bdt_evt_sleading_btag', 'varname':'bdt_evt_sleading_btag', 'legend':'top right', 'logy':False, 'title':'CSV b jet_{2}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.},
    {'var':'bdt_evt_leading_nbtag', 'varname':'bdt_evt_leading_nbtag', 'legend':'top right', 'logy':False, 'title':'CSV l jet_{1}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.},
    {'var':'bdt_evt_sleading_nbtag', 'varname':'bdt_evt_sleading_nbtag', 'legend':'top right', 'logy':False, 'title':'CSV l jet_{2}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.},
    {'var':'bdt_evt_max_jet_eta', 'varname':'bdt_evt_max_jet_eta', 'legend':'top right', 'logy':False, 'title':'max(jet |#eta|)', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':5.},
    {'var':'(bdt_evt_max_jet_eta30*(bdt_evt_max_jet_eta30>0.))', 'varname':'bdt_evt_max_jet_eta30', 'legend':'top right', 'logy':False, 'title':'max(jet |#eta|, 30 GeV)', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':5.},
    {'var':'bdt_evt_njet_or', 'varname':'bdt_evt_njet_or', 'legend':'top right', 'logy':False, 'title':'N_{jets} (20 GeV)', 'unit':'', 'nbinsx':10, 'xmin':-0.5, 'xmax':9.5},
    {'var':'bdt_evt_njet_or30', 'varname':'bdt_evt_njet_or30', 'legend':'top right', 'logy':False, 'title':'N_{jets} (30 GeV)', 'unit':'', 'nbinsx':10, 'xmin':-0.5, 'xmax':9.5},
    {'var':'bdt_evt_sumjetpt', 'varname':'bdt_evt_sumjetpt', 'legend':'top right', 'logy':False, 'title':'#Sigma jet p{T}', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':500.},
    {'var':'bdt_evt_Met', 'varname':'bdt_evt_Met', 'legend':'top right', 'logy':False, 'title':'m(e, #tau)', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_evt_Mmt', 'varname':'bdt_evt_Mmt', 'legend':'top right', 'logy':False, 'title':'m(#mu, #tau)', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_evt_Mem', 'varname':'bdt_evt_Mem', 'legend':'top right', 'logy':False, 'title':'m(e, #mu)', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_evt_LT', 'varname':'bdt_evt_LT', 'legend':'top right', 'logy':False, 'title':'#Sigma lepton p_{T}', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':300.},
    {'var':'bdt_evt_L2T', 'varname':'bdt_evt_L2T', 'legend':'top right', 'logy':False, 'title':'m_{vis}(#tau, l_{2})', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':200.},
    {'var':'bdt_evt_nbjet', 'varname':'bdt_evt_nbjet', 'legend':'top right', 'logy':False, 'title':'N_{b jet}', 'unit':'GeV', 'nbinsx':5, 'xmin':-0.5, 'xmax':4.5},
    {'var':'bdt_evt_nbjet10', 'varname':'bdt_evt_nbjet10', 'legend':'top right', 'logy':False, 'title':'N_{b jet} (10 GeV)', 'unit':'GeV', 'nbinsx':5, 'xmin':-0.5, 'xmax':4.5},
    {'var':'bdt_evt_HT', 'varname':'bdt_evt_HT', 'legend':'top right', 'logy':False, 'title':'#Sigma p_{T} (jets, leptons)', 'unit':'GeV', 'nbinsx':10, 'xmin':100., 'xmax':600.},
    {'var':'abs(bdt_evt_deltaeta)', 'varname':'abs_bdt_evt_deltaeta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(forward jet, muon)|', 'unit':'GeV', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'abs(bdt_muon_eta-bdt_tau_eta)', 'varname':'abs_bdt_muon_eta_MINUS_bdt_tau_eta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(#mu, #tau)|', 'unit':'GeV', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'abs(bdt_muon_eta-bdt_smuon_eta)', 'varname':'abs_bdt_muon_eta_MINUS_bdt_smuon_eta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(#mu, e)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'abs(bdt_muon_eta-bdt_tau_eta)', 'varname':'abs_bdt_muon_eta_MINUS_bdt_tau_eta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(#mu, #tau)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'abs(bdt_smuon_eta-bdt_tau_eta)', 'varname':'bdt_smuon_eta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(e, #tau)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'bdt_evt_maxMT', 'varname':'bdt_evt_maxMT', 'legend':'top right', 'logy':False, 'title':'max(M_{T} #mu, e)', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_tau_MT', 'varname':'bdt_tau_MT', 'legend':'top right', 'logy':False, 'title':'M_{T} #tau', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_smuon_MT', 'varname':'bdt_smuon_MT', 'legend':'top right', 'logy':False, 'title':'M_{T} e', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_muon_MT', 'varname':'bdt_muon_MT', 'legend':'top right', 'logy':False, 'title':'M_{T} #mu', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'abs(bdt_evt_dphi_mete)', 'varname':'abs_bdt_evt_dphi_mete', 'legend':'top right', 'logy':False, 'title':'|#Delta #phi(E_{T}^{miss}, e)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':3.1415927},
    {'var':'abs(bdt_evt_dphi_metmu)', 'varname':'abs_bdt_evt_dphi_metmu', 'legend':'top right', 'logy':False, 'title':'|#Delta #phi(E_{T}^{miss}, #mu)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':3.1415927},
    {'var':'abs(bdt_evt_dphi_mettau)', 'varname':'abs_bdt_evt_dphi_mettau', 'legend':'top right', 'logy':False, 'title':'|#Delta #phi(E_{T}^{miss}, #tau)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':3.1415927},
    {'var':'bdt_muon_jet_csv', 'varname':'bdt_muon_jet_csv_10', 'legend':'top right', 'logy':False, 'title':'CSV #mu jet (10 GeV)', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.00001},
    {'var':'bdt_muon_jet_csv_10', 'varname':'bdt_muon_jet_csv', 'legend':'top right', 'logy':False, 'title':'CSV #mu jet', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.00001},
    {'var':'bdt_tau_jet_csv', 'varname':'bdt_tau_jet_csv', 'legend':'top right', 'logy':False, 'title':'CSV #tau jet', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.00001},
    {'var':'bdt_smuon_jet_csv', 'varname':'bdt_smuon_jet_csv', 'legend':'top right', 'logy':False, 'title':'CSV e jet', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.00001},
    {'var':'bdt_smuon_jet_csv', 'varname':'bdt_smuon_jet_csv_10', 'legend':'top right', 'logy':False, 'title':'CSV e jet (10 GeV)', 'unit':'', 'nbinsx':10, 'xmin':0., 'xmax':1.00001},
    {'var':'abs(bdt_muon_pdg)', 'varname':'bdt_muon_pdg', 'legend':'top right', 'logy':False, 'title':'PDG muon match', 'unit':'', 'nbinsx':16, 'xmin':-0.5, 'xmax':15.5},
    {'var':'abs(bdt_smuon_pdg)', 'varname':'bdt_smuon_pdg', 'legend':'top right', 'logy':False, 'title':'PDG smuon match', 'unit':'', 'nbinsx':16, 'xmin':-0.5, 'xmax':15.5},
    {'var':'abs(bdt_tau_pdg)', 'varname':'bdt_tau_pdg', 'legend':'top right', 'logy':False, 'title':'PDG tau match', 'unit':'', 'nbinsx':16, 'xmin':-0.5, 'xmax':15.5},
    {'var':'abs(bdt_evt_dr_mujet)', 'varname':'bdt_evt_dr_mujet', 'legend':'top right', 'logy':False, 'title':'#Delta R(#mu, jet)', 'unit':'', 'nbinsx':15, 'xmin':0., 'xmax':6.},
    {'var':'abs(bdt_evt_dr_taujet)', 'varname':'bdt_evt_dr_taujet', 'legend':'top right', 'logy':False, 'title':'#Delta R(#tau, jet)', 'unit':'', 'nbinsx':15, 'xmin':0., 'xmax':6.},
    {'var':'abs(bdt_evt_dr_ejet)', 'varname':'bdt_evt_dr_ejet', 'legend':'top right', 'logy':False, 'title':'#Delta R(e, jet)', 'unit':'', 'nbinsx':15, 'xmin':0., 'xmax':6.},
    {'var':'bdt_evt_dr_mujet_csv', 'varname':'bdt_evt_dr_mujet_csv', 'legend':'top right', 'logy':False, 'title':'CSV jet near #mu', 'unit':'', 'nbinsx':15, 'xmin':0., 'xmax':1.0001},
    {'var':'bdt_evt_dr_ejet_csv', 'varname':'bdt_evt_dr_ejet_csv', 'legend':'top right', 'logy':False, 'title':'CSV jet near e', 'unit':'', 'nbinsx':15, 'xmin':0., 'xmax':1.0001},
    {'var':'bdt_evt_dr_taujet_csv', 'varname':'bdt_evt_dr_taujet_csv', 'legend':'top right', 'logy':False, 'title':'CSV jet near #tau', 'unit':'', 'nbinsx':15, 'xmin':0., 'xmax':1.0001},
    {'var':'log(abs(bdt_muon_dB3D))', 'varname':'bdt_muon_dB3D', 'legend':'top right', 'logy':False, 'title':'#mu log(|dB_{3D}|)', 'unit':'log(cm)', 'nbinsx':15, 'xmin':-10., 'xmax':0.},
    {'var':'log(abs(bdt_muon_dz))', 'varname':'bdt_muon_dz', 'legend':'top right', 'logy':False, 'title':'#mu log(|d_{z}|)', 'unit':'log(cm)', 'nbinsx':15, 'xmin':-10., 'xmax':0.},
    {'var':'log(abs(bdt_muon_dxy))', 'varname':'bdt_muon_dxy', 'legend':'top right', 'logy':False, 'title':'#mu log(|d_{xy}|)', 'unit':'log(cm)', 'nbinsx':15, 'xmin':-10., 'xmax':0.},
    {'var':'log(abs(bdt_smuon_dB3D))', 'varname':'bdt_smuon_dB3D', 'legend':'top right', 'logy':False, 'title':'e log(|dB_{3D}|)', 'unit':'log(cm)', 'nbinsx':15, 'xmin':-10., 'xmax':0.},
    {'var':'log(abs(bdt_smuon_dz))', 'varname':'bdt_smuon_dz', 'legend':'top right', 'logy':False, 'title':'e log(|d_{z}|)', 'unit':'log(cm)', 'nbinsx':15, 'xmin':-10., 'xmax':0.},
    {'var':'log(abs(bdt_smuon_dxy))', 'varname':'bdt_smuon_dxy', 'legend':'top right', 'logy':False, 'title':'e log(|d_{xy}|)', 'unit':'log(cm)', 'nbinsx':15, 'xmin':-10., 'xmax':0.},
    {'var':'log(abs(bdt_tau_dB3D))', 'varname':'bdt_tau_dB3D', 'legend':'top right', 'logy':False, 'title':'tau log(|dB_{3D}|)', 'unit':'log(cm)', 'nbinsx':15, 'xmin':-10., 'xmax':0.},
    {'var':'log(abs(bdt_tau_dz))', 'varname':'bdt_tau_dz', 'legend':'top right', 'logy':False, 'title':'tau log(|d_{z}|)', 'unit':'log(cm)', 'nbinsx':15, 'xmin':-10., 'xmax':0.},
    {'var':'log(abs(bdt_tau_dxy))', 'varname':'bdt_tau_dxy', 'legend':'top right', 'logy':False, 'title':'tau log(|d_{xy}|)', 'unit':'log(cm)', 'nbinsx':15, 'xmin':-10., 'xmax':0.},

    ]

    sampleDict = {
        1:{'name':'WW', 'colour':ROOT.TColor.GetColor(222,90,106), 'label':'Diboson'},
        1:{'name':'WZ', 'colour':ROOT.TColor.GetColor(222,90,106), 'label':'Diboson'},
        2:{'name':'ZZ', 'colour':ROOT.TColor.GetColor(222,90,106), 'label':'Diboson'},
        3:{'name':'tt0l', 'colour':ROOT.TColor.GetColor(155,133,296), 'label':'t#bar{t}'},
        4:{'name':'tt1l', 'colour':ROOT.TColor.GetColor(155,152,296), 'label':'t#bar{t}'},
        5:{'name':'tt2l', 'colour':ROOT.TColor.GetColor(155,152,296), 'label':'t#bar{t}'},
        # 4:{'name':'tt1l', 'colour':ROOT.TColor.GetColor(155,152,250), 'label':'t#bar{t}'},
        # 5:{'name':'tt2l', 'colour':ROOT.TColor.GetColor(155,152,204), 'label':'t#bar{t}'},

        # # 6:{'name':'DY', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'DY'},
        # 7:{'name':'DY1', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'DY'},
        # 8:{'name':'DY2', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'DY'},
        # 9:{'name':'DY3', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'DY'},
        # 10:{'name':'DY4', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'DY'},

        # # 11:{'name':'Wjet', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'W'},
        # 12:{'name':'W1jet', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'W'},
        # 13:{'name':'W2jet', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'W'},
        # 14:{'name':'W3jet', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'W'},
        # 15:{'name':'W4jet', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'W'},
        17:{'name':'ttW', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':'t#bar{t}W/Z'},
        18:{'name':'ttZ', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':'t#bar{t}W/Z'}, #'label':'t#bar{t}Z'
        16:{'name':'tH_YtMinus', 'colour':ROOT.TColor.kRed + 3, 'label':'tH (y_{t}=-1)'},
        19:{'name':'ttH', 'colour':ROOT.TColor.GetColor(100,182,232), 'label':'t#bar{t}H'},
        20:{'name':'reducible', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'Reducible'},
        # 100:{'name':'data', 'colour':1, 'label':'Data'}, # FIXME: 100?
    }
    p = Plotter(variables, sampleDict, fileName="BDT_training_ss_f12_nottbar_mva.root", directory='plots',
        signalsampleIds=[16], datasampleIds=[100])
    p.readTuples()
    p.makePlots(weight='bdt_evt_weight')
    