import ROOT

sampleDict = {
    0:{'name':'WW', 'colour':ROOT.TColor.GetColor(222,90,106), 'label':'WZ/WW'},
    1:{'name':'WZ', 'colour':ROOT.TColor.GetColor(222,90,106), 'label':''},
    2:{'name':'ZZ', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':'ZZ'},
    3:{'name':'tt1l', 'colour':ROOT.TColor.GetColor(155,152,204), 'label':'t#bar{t} (1l)'},
    4:{'name':'tt2l', 'colour':ROOT.TColor.GetColor(160,160,220), 'label':'t#bar{t} (2l)'},

    5:{'name':'W1Jet', 'colour':ROOT.TColor.kGreen + 2, 'label':'W + jets'},
    6:{'name':'W2Jet', 'colour':ROOT.TColor.kGreen + 2, 'label':''},
    7:{'name':'W3Jet', 'colour':ROOT.TColor.kGreen + 2, 'label':''},
    8:{'name':'W4Jet', 'colour':ROOT.TColor.kGreen + 2, 'label':''},

    9:{'name':'DY1Jet', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':'DY + jets'},
    10:{'name':'DY2Jet', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':''},
    11:{'name':'DY3Jet', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':''},
    12:{'name':'DY4Jet', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':''},

    # 4:{'name':'ttW', 'colour':ROOT.TColor.kGreen + 2, 'label':'t#bar{t}W'},
    # 5:{'name':'ttZ', 'colour':ROOT.TColor.kGreen + 3, 'label':'t#bar{t}Z'},
    13:{'name':'tH_YtMinus', 'colour':ROOT.TColor.kRed + 3, 'label':'tH (y_{t}=-1)'},
    # 7:{'name':'ttH', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':'t#bar{t}H'},

    # 8:{'name':'reducible', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'Reducible'},
    # 100:{'name':'data', 'colour':1, 'label':'Data'}, # FIXME: 100?
}
