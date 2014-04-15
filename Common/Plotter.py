import os
import math

import ROOT

from PlotStyle import PlotStyle

class Plotter(object):
    def __init__(self, configurations, sampleDict, signalsampleIds=[6], datasampleIds=[9], scaleSignal="integral", drawRatios=False, pullRange=0.8, fileName="BDT_training_mva.root", sysName="", endings=["pdf"], directory="plots", overFlowLastBin=True, underFlowFirstBin=False, calculateSeparation=True, verbose=False, treeName='Tree'):
        
        self._sampleDict = sampleDict

        
        # List of signal sample names; if set, will be drawn as separate line
        self._signalsampleIds = signalsampleIds
        
        # That's fixed for now
        self._datasampleIds = datasampleIds
        
        # Scale signal to "integral" or "luminosity" (i.e. cross section)
        self._scaleSignal = scaleSignal
        
        
        """ a configuration is a list of dicts that contain the following information
            "var": variable name (string)
            "legend": "none", "top left", "top right"
            "logy": True/False
        """
        self._configurations = configurations
        
        # In which formats the plots are given out
        self._endings = endings
        self._directory = directory
        
        # Whether the ratio below the plot shall be drawn
        self._drawRatios = drawRatios
        self._pullRange = 0.8
        self._errorBandFillColor = 14
        self._errorBandStyle = 3354

        # Pattern for file name: {0}: sample name, {1}: lepton name, {2}: sys addendum
        self._fileName = fileName
        self._treeName = treeName
        self._tree = 0
        
        # For a shape systematic based on up/down files:
        #   Legend entry - if this is present, the systematic uncertainty will be drawn
        self._sysName = sysName
        
        # Whether to calculate and print separation measures
        self._calculateSeparation = calculateSeparation
        
        # Be verbose or not
        self._verbose = verbose
        
        # Whether to put the overflow into the last bin
        self._overFlowLastBin = overFlowLastBin
        
        # Whether to put the underflow into the first bin
        self._underFlowFirstBin = underFlowFirstBin
        
        # List of open root files
        self._rootFiles = {}
        
        PlotStyle.initStyle()

    # Reads all tuples
    def readTuples(self):
        
        if self._tree:
            print "Tree already read"
            return
        if os.path.isfile(self._fileName):
            if self._fileName not in self._rootFiles:
                rootFile = ROOT.TFile(self._fileName)
                self._rootFiles[self._fileName] = rootFile
                self._tree = rootFile.Get(self._treeName)
                if not self._tree:
                    print 'ERROR, tree', self._tree, 'not found'
        else:
            print 'ERROR, file', self._fileName, 'not found'
            


    """ Method to produce plots for all variables,
        given the passed weight (+ cut) expression.
        'title' is a name for the weight expression that
        is added to the output plot names.
        'inset' is a TLatex description that is added within
        the plot.
    """
    def makePlots(self, weight="weight", title="default", inset=""):
        multicv = ROOT.TCanvas(title, title, 10, 10, 700, 500)
        multicv.Print(self._directory+"/summary_"+title+".ps[", "PORTRAIT")
        
        separationList = []
        rocList = []
        
        for varDict in self._configurations:
            if self._verbose:
                print varDict
              
            # put all information about the observable into local variables
            varProjName = varDict['var']
            varName = varDict['varname']
            varTitle = varDict['title']
            varUnit = varDict['unit']
            nbinsx = varDict['nbinsx']
            xmin = varDict['xmin']
            xmax = varDict['xmax']
            
            labelx = varTitle
            if varUnit != "":
                labelx += " (" + varUnit + ")"
            
            labely = "Events"
            
            legendPos = "top"
            if "legend" in varDict:
                legendPos = varDict["legend"]
            
            logy = False
            if "logy" in varDict:
                logy = varDict["logy"]
                if self._verbose:
                    print "Using LOG y"
            
            plotName = varName
            if title != "":
                plotName = plotName + "_" + title
            
            if not self._drawRatios:
                cv = ROOT.TCanvas(plotName, plotName, 10, 10, 700, 500) # top default ratio, adding some space below for pull distributions:
                if logy:
                    cv.SetLogy(1)
            else:
                cv = self.createPullCanvas(plotName, logy)
            
            if legendPos != "none":
                #legend = ROOT.TLegend(0.55, 0.29, 0.92, 0.92, "", "NDC") #FIXME: More legend positions for the future!
                
                if legendPos == "top left":
                    legend = ROOT.TLegend(0.19, 0.32, 0.45, 0.92, "", "NDC") #FIXME: More legend positions for the future!
                else:
                    legend = ROOT.TLegend(0.66, 0.32, 0.92, 0.92, "", "NDC") #FIXME: More legend positions for the future!
                    
                legendEntries = {}
            
            stack = ROOT.THStack()
            
            histName = plotName+"sumMC"
            if logy:
                histName += "logy"
            histSumMC = ROOT.TH1F(histName, "", nbinsx, xmin, xmax)
            
            histSumMCup = 0
            histSumMCdown = 0
            
            
            modes = [""]
            # if self._sysName:
            #     if len(self._tuplesUp) != 0:
            #         histSumMCup = ROOT.TH1F(histName+"up", "", nbinsx, xmin, xmax)
            #         modes.append("up")
            #     if len(self._tuplesDown) != 0:
            #         histSumMCdown = ROOT.TH1F(histName+"down", "", nbinsx, xmin, xmax)
            #         modes.append("down")
            
            
            histData = 0
            
            histograms = []
            stackHistograms = []
            separateHistograms = {}
            
            for mode in modes:
                # tuples = self._tuples
                # if mode == "up":
                #     tuples = self._tuplesUp
                # elif mode == "down":
                #     tuples = self._tuplesDown
                 
                for sampleId in self._sampleDict:
                    # for iTuple, ntuple in enumerate(tuples[sampleId]):
                    histName = plotName+str(sampleId)+mode
                    if logy:
                        histName += "logy"

                    hist = ROOT.TH1F(histName, "", nbinsx, xmin, xmax)
                    hist.Sumw2()
                    
                    # Do fancy formatting etc only for nominal hist
                    if mode == "":
                        histograms.append(hist)
                        if sampleId not in self._signalsampleIds and sampleId not in self._datasampleIds:
                            print 'Appending non-data histogram', sampleId
                            stackHistograms.append(hist)
                            hist.SetFillStyle(1001)
                        else:
                            if sampleId not in separateHistograms:
                                separateHistograms[sampleId] = hist
                            hist.SetFillStyle(0)
                            hist.SetLineWidth(2)
                            print 'Appending data or signal histogram', sampleId
                        
                        hist.SetLineColor(self._sampleDict[sampleId]["colour"])
                        hist.SetFillColor(self._sampleDict[sampleId]["colour"])
                        hist.SetMarkerColor(self._sampleDict[sampleId]["colour"])
                    
                    plotWeight = '{weight} * (bdt_evt_processid == {id})'.format(weight=weight, id=sampleId)
                    self._tree.Project(histName, varProjName, plotWeight)
                    
                    if self._overFlowLastBin:
                        overflow = hist.GetBinContent(hist.GetNbinsX()+1)
                        hist.SetBinContent(hist.GetNbinsX(), hist.GetBinContent(hist.GetNbinsX()) + overflow)
                    if self._underFlowFirstBin:
                        underflow = hist.GetBinContent(0)
                        hist.SetBinContent(1, hist.GetBinContent(1) + underflow)
                    
                    if sampleId in separateHistograms:
                        #print "Before:", separateHistograms[sampleId].Integral()
                        separateHistograms[sampleId].Add(hist)
                        #print sampleId
                        #print "Adding to existing hist"
                        #print "After:", separateHistograms[sampleId].Integral()
                    
                    if sampleId not in self._signalsampleIds:
                        if mode == "up":
                            histSumMCup.Add(hist)
                        elif mode == "down":
                            histSumMCdown.Add(hist)
                    
                    # Legend entries only for nominal hist
                    if mode == "" and legendPos != "none":
                        label = self._sampleDict[sampleId]["label"]
                        if label not in legendEntries:
                            if sampleId in self._signalsampleIds:
                                #legend.AddEntry(hist, label, "F")
                                legendEntries[label] = {"hist":hist, "style":"L", "label":label}
                            elif sampleId == "Data":
                                legendEntries[label] = {"hist":hist, "style":"PL", "label":label}
                            else:
                                #legend.AddEntry(hist, label, "LP")
                                legendEntries[label] = {"hist":hist, "style":"F", "label":label}
            
            for stackHist in stackHistograms:
                stackHist.SetLineWidth(0)
                stack.Add(stackHist)
                histSumMC.Add(stackHist)
            
            scales = []
            if self._scaleSignal == "integral":
                for key in separateHistograms.keys():
                    if key not in self._datasampleIds:
                        hist = separateHistograms[key]
                        integral = histSumMC.Integral()
                        histIntegral = hist.Integral()
                        if histIntegral > 0.:
                            hist.Scale(integral/histIntegral)
                            scales.append(integral/histIntegral)
                        else:
                            scales.append(1.)
                        
            # BEGIN THE ACTUAL DRAWING HERE
            ymax = stack.GetMaximum()
            for key in separateHistograms.keys():
                hist = separateHistograms[key]
                if hist.GetMaximum() > 0:
                    ymax = max(hist.GetMaximum() + math.sqrt(hist.GetMaximum()), ymax)
            
            stack.SetMaximum(ymax * 1.3)
            stack.Draw('HIST') # INITIAL DRAW
            if logy:
                stack.SetMaximum(ymax * 140.)
                stack.SetMinimum(0.1)
            else:
                stack.GetYaxis().SetRangeUser(0.0, ymax * 1.3)

            stack.GetXaxis().SetTitle(labelx)
            stack.GetYaxis().SetTitle(labely)
            
            # if self._sysName:
            #     errorGraph = ROOT.TGraphAsymmErrors()
            
            if self._drawRatios:
                histPull = ROOT.TH1F(plotName+"pull", "", nbinsx, xmin, xmax)
                histPullHigher = ROOT.TH1F(plotName+"pulllow", "", nbinsx, xmin, xmax)
                histPullLower = ROOT.TH1F(plotName+"pullhigh", "", nbinsx, xmin, xmax)
                histPullLower.SetMarkerColor(14)
                histPullHigher.SetMarkerColor(14)
                histPullLower.SetMarkerStyle(23)
                histPullHigher.SetMarkerStyle(22)
                
                histData = 0
                for key in separateHistograms.keys():
                    if key in self._datasampleIds:
                        histData = separateHistograms[key]
                
                if histData == 0:
                    print "No data histogram found, but draw ratio mode on. Exiting..."
                    return
                
                #histDataSubtracted = ROOT.TH1F(plotName+"dataMinusMC", "", nbinsx, xmin, xmax)
                #histDataSubtracted.Add(histData, histSumMC, 1., -1.)
                #histPull.Divide(histDataSubtracted, histSumMC)
                histPull.Divide(histData, histSumMC)
                histPull.UseCurrentStyle()
    
                histPull.GetXaxis().SetTitle(labelx)
                histPull.GetYaxis().SetTitle("Data / MC")
                histPull.GetYaxis().SetRangeUser(-self._pullRange + 1., self._pullRange + 1.)
                
                ypos = self._pullRange - self._pullRange / 5. + 1.
                for iBin in range(histPull.GetNbinsX()):
                    if histPull.GetBinContent(iBin+1) > self._pullRange + 1.:
                        histPullHigher.SetBinContent(iBin+1, ypos)
                    else:
                        histPullHigher.SetBinContent(iBin+1, -self._pullRange - 1000.)
                    if histPull.GetBinContent(iBin+1) < -self._pullRange:
                        histPullLower.SetBinContent(iBin+1, -ypos)
                    else:
                        histPullLower.SetBinContent(iBin+1, -self._pullRange - 1000.)
                
                defaultXtoPixel = 696. # width in pixels of default canvas
                defaultYtoPixel = 472. # height in pixels of default canvas
                
                pad1XtoPixel = float(cv.GetPad(1).XtoPixel(1))
                pad1YtoPixel = float(cv.GetPad(1).YtoPixel(0))
                pad2XtoPixel = float(cv.GetPad(2).XtoPixel(1))
                pad2YtoPixel = float(cv.GetPad(2).YtoPixel(0))
        
                pad1XaxisFactor = defaultYtoPixel / pad1YtoPixel
                pad1YaxisFactor = defaultXtoPixel / pad1XtoPixel
                pad2XaxisFactor = defaultYtoPixel / pad2YtoPixel
                pad2YaxisFactor = defaultXtoPixel / pad2XtoPixel
                
                # Do some magic with the sizes so the titles look equal
                histPull.GetXaxis().SetLabelSize(stack.GetXaxis().GetLabelSize()*pad2XaxisFactor)
                histPull.GetXaxis().SetLabelOffset(stack.GetXaxis().GetLabelOffset()*pad2XaxisFactor)
                histPull.GetXaxis().SetTitleSize(stack.GetXaxis().GetTitleSize()*pad2XaxisFactor)
                histPull.GetXaxis().SetTitleOffset(stack.GetXaxis().GetTitleOffset()/pad2XaxisFactor*2.5)
    
    
                histPull.GetYaxis().SetLabelSize(stack.GetYaxis().GetLabelSize()*pad2XaxisFactor)
                histPull.GetYaxis().SetLabelOffset(stack.GetYaxis().GetLabelOffset()*pad2XaxisFactor)
                histPull.GetYaxis().SetTitleSize(stack.GetYaxis().GetTitleSize()*pad2XaxisFactor)
                histPull.GetYaxis().SetTitleOffset(stack.GetYaxis().GetTitleOffset()/pad2XaxisFactor)
    
                histPull.GetYaxis().CenterTitle()
    
                histPull.GetXaxis().SetTickLength(histPull.GetXaxis().GetTickLength()*pad2XaxisFactor)
                histPull.GetYaxis().SetNdivisions(306)
                stack.GetXaxis().SetTickLength(stack.GetXaxis().GetTickLength()*pad1XaxisFactor)
                stack.GetXaxis().SetLabelSize(0.) # to make sure this is hidden (due to margin stuff)
                stack.GetXaxis().SetTitleSize(0.) # to make sure this is hidden (due to margin stuff)
    
                stack.GetYaxis().SetLabelSize(stack.GetYaxis().GetLabelSize()*pad1XaxisFactor)
                stack.GetYaxis().SetLabelOffset(stack.GetYaxis().GetLabelOffset()*pad1XaxisFactor)
                stack.GetYaxis().SetTitleSize(stack.GetYaxis().GetTitleSize()*pad1XaxisFactor)
                stack.GetYaxis().SetTitleOffset(stack.GetYaxis().GetTitleOffset()/pad1XaxisFactor)

            
            for key in separateHistograms.keys():
                hist = separateHistograms[key]
                
                if key in self._datasampleIds:
                    hist.Draw("same PE")
                else:                
                    hist.Draw("same HIST")
                    if self._calculateSeparation:
                        separation = ROOT.TMVA.Tools.Instance().GetSeparation(hist, histSumMC)
                        rocIntegral = self.getROCIntegral(hist, histSumMC)
                        
                        separationList.append((separation, varName))
                        rocList.append((abs(rocIntegral - 0.5), varName))
                        
                        sepText = ROOT.TLatex(3.570061,23.08044, "Separation: "+str(round(separation, 2)) + ", ROC area: " + str(round(rocIntegral, 2)))
                        sepText.SetNDC()
                        sepText.SetTextAlign(13)
                        sepText.SetX(0.55)
                        sepText.SetY(0.99)
                        sepText.SetTextFont(42)
                        sepText.SetTextSizePixels(1)
                        if self._drawRatios:
                            sepText.SetTextSize(0.04 * pad1XaxisFactor)
                        else:
                            sepText.SetTextSize(0.04)
                        sepText.Draw()
            
            if inset != "":
                text1 = ROOT.TLatex(3.570061, 23.01044, inset)
                text1.SetNDC()
                text1.SetTextAlign(13)
                text1.SetX(0.188)
                if legendPos == "top left":
                    text1.SetX(0.6)
                text1.SetY(0.918)
                text1.SetTextFont(42)
                if self._drawRatios:
                    text1.SetTextSize(0.05 * pad1XaxisFactor)
                else:
                    text1.SetTextSize(0.05)
                text1.Draw()
            
            if legendPos != "none":
                for sampleId in reversed([s for s in self._sampleDict]):
                    label = self._sampleDict[sampleId]["label"]
                    if label in legendEntries and label!='':
                        legend.AddEntry(legendEntries[label]["hist"], label, legendEntries[label]["style"])
                        if sampleId in self._signalsampleIds and len(scales) > 0:
                            extra = " x {0:.1f}".format(scales.pop(0))
                            legend.AddEntry(0, extra, "")
                        del legendEntries[label]
                    
                legend.UseCurrentStyle()
                legend.SetFillColor(0)
                legend.SetLineColor(0)
                legend.SetLineWidth(0)
                legend.SetFillStyle(0)
                legend.SetLineStyle(0)
                legend.SetTextFont(42)
                if self._drawRatios:
                    legend.SetTextSize(0.05 * pad1XaxisFactor)
                else:
                    legend.SetTextSize(0.05)
                legend.Draw()
            
            if self._drawRatios:
                cv.cd(2)
                histPull.Draw()
                zeroGuide = ROOT.TLine(histPull.GetXaxis().GetBinLowEdge(1), 1., histPull.GetXaxis().GetBinUpEdge(histPull.GetNbinsX()), 1.)
                zeroGuide.SetLineWidth(1)
                zeroGuide.SetLineColor(14)
                zeroGuide.Draw()
                histPullHigher.Draw("same p")
                histPullLower.Draw("same p")
                
            cv.Update()
            
            for ending in self._endings:
                if logy:
                    cv.Print(self._directory + "/" + plotName + "_logy." + ending)
                else:
                    cv.Print(self._directory + "/" + plotName + "." + ending)
            cv.Print(self._directory + "/summary_"+title+".ps")
        
        multicv.Print(self._directory+"/summary_"+title+".ps]", "PORTRAIT")
        
        fSep = open(self._directory+"/separation_"+title+".txt", "w")
        separationList.sort()
        
        for entry in reversed(separationList):
            fSep.write(str(entry[0]) + ": " + str(entry[1]) + "\n")
        
        fSep.close()
        
        rocList.sort()
        
        fROC = open(self._directory + "/roc_" + title + ".txt", "w")
        for entry in reversed(rocList):
            fROC.write(str(entry[0]) + ": " + str(entry[1]) + "\n")
        
        fROC.close()
    
    @staticmethod
    def createPullCanvas(self, plotName, logy, errorBandFillColor=14, errorBandStyle=3354):
        cv = ROOT.TCanvas(plotName, plotName, 10, 10, 700, 600)
        #this is the tricky part...
        # Divide with correct margins
        cv.Divide(1, 2, 0.0, 0.0)
        # Set Pad sizes
        cv.GetPad(1).SetPad(0.0, 0.32, 1., 1.0)
        cv.GetPad(2).SetPad(0.0, 0.00, 1., 0.34)

        cv.GetPad(1).SetFillStyle(4000)
        cv.GetPad(2).SetFillStyle(4000)


        # Set pad margins 1
        cv.cd(1)
        ROOT.gPad.SetTopMargin(0.05)
        ROOT.gPad.SetLeftMargin(0.16)
        ROOT.gPad.SetBottomMargin(0.03)
        ROOT.gPad.SetRightMargin(0.05)
        # Set pad margins 2
        cv.cd(2)
        ROOT.gPad.SetBottomMargin(0.35)
        ROOT.gPad.SetLeftMargin(0.16)
        ROOT.gPad.SetRightMargin(0.05)
        
        bogyHist = ROOT.TH1F(plotName+"legendPseudoHist", "", 1, 1., 2.)
        bogyHist.SetFillColor(errorBandFillColor)
        bogyHist.SetFillStyle(errorBandStyle)
        bogyHist.SetLineColor(0)
        
        cv.cd(1)
        if logy:
            cv.GetPad(1).SetLogy(1)
        
        return cv
    
    # Calculate area under ROC curve
    # Pass two ROOT histograms
    @staticmethod
    def getROCIntegral(histS, histB):
        pdfS = ROOT.TMVA.PDF("PDF Sig", histS, ROOT.TMVA.PDF.kSpline3)
        pdfB = ROOT.TMVA.PDF("PDF Bkg", histB, ROOT.TMVA.PDF.kSpline3)
        
        xmin = ROOT.TMath.Min(pdfS.GetXmin(), pdfB.GetXmin())
        xmax = ROOT.TMath.Max(pdfS.GetXmax(), pdfB.GetXmax())
        
        integral = 0.
        nsteps = 1000
        step = (xmax - xmin)/float(nsteps)
        cut = xmin
        
        for i in range(0, nsteps):
            integral += (1. - pdfB.GetIntegral(cut, xmax)) * pdfS.GetVal(cut)
            cut += step
        
        return integral * step

if __name__ == '__main__':
    variables = [
    {'var':'BDTG', 'varname':'BDTG', 'legend':'top left', 'logy':False, 'title':'BDT score', 'unit':'', 'nbinsx':10, 'xmin':-1., 'xmax':1.0001},
    {'var':'Fisher', 'varname':'Fisher', 'legend':'top left', 'logy':False, 'title':'Fisher score', 'unit':'', 'nbinsx':10, 'xmin':-1., 'xmax':1.0001},
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
    {'var':'bdt_evt_HT', 'varname':'bdt_evt_HT', 'legend':'top right', 'logy':False, 'title':'#Sigma p_{T} (jets, leptons)', 'unit':'GeV', 'nbinsx':10, 'xmin':100., 'xmax':600.},
    {'var':'abs(bdt_evt_deltaeta)', 'varname':'abs_bdt_evt_deltaeta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(forward jet, muon)|', 'unit':'GeV', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'abs(bdt_muon_eta-bdt_tau_eta)', 'varname':'abs_bdt_muon_eta_MINUS_bdt_tau_eta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(#mu, #tau)|', 'unit':'GeV', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'abs(bdt_muon_eta-bdt_electron_eta)', 'varname':'abs_bdt_muon_eta_MINUS_bdt_electron_eta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(#mu, e)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'abs(bdt_muon_eta-bdt_tau_eta)', 'varname':'abs_bdt_muon_eta_MINUS_bdt_tau_eta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(#mu, #tau)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'abs(bdt_electron_eta-bdt_tau_eta)', 'varname':'bdt_electron_eta', 'legend':'top right', 'logy':False, 'title':'|#Delta #eta(e, #tau)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':5.},
    {'var':'bdt_evt_maxMT', 'varname':'bdt_evt_maxMT', 'legend':'top right', 'logy':False, 'title':'max(M_{T} #mu, e)', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_tau_MT', 'varname':'bdt_tau_MT', 'legend':'top right', 'logy':False, 'title':'M_{T} #tau', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_electron_MT', 'varname':'bdt_electron_MT', 'legend':'top right', 'logy':False, 'title':'M_{T} e', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'bdt_muon_MT', 'varname':'bdt_muon_MT', 'legend':'top right', 'logy':False, 'title':'M_{T} #mu', 'unit':'GeV', 'nbinsx':10, 'xmin':0., 'xmax':150.},
    {'var':'abs(bdt_evt_dphi_mete)', 'varname':'abs_bdt_evt_dphi_mete', 'legend':'top right', 'logy':False, 'title':'|#Delta #phi(E_{T}^{miss}, e)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':3.1415927},
    {'var':'abs(bdt_evt_dphi_metmu)', 'varname':'abs_bdt_evt_dphi_metmu', 'legend':'top right', 'logy':False, 'title':'|#Delta #phi(E_{T}^{miss}, #mu)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':3.1415927},
    {'var':'abs(bdt_evt_dphi_mettau)', 'varname':'abs_bdt_evt_dphi_mettau', 'legend':'top right', 'logy':False, 'title':'|#Delta #phi(E_{T}^{miss}, #tau)|', 'unit':'', 'nbinsx':5, 'xmin':0., 'xmax':3.1415927},

    ]

    sampleDict = {
        0:{'name':'WZ', 'colour':ROOT.TColor.GetColor(222,90,106), 'label':'WZ'},
        1:{'name':'ZZ', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':'ZZ'},
        2:{'name':'tt1l', 'colour':ROOT.TColor.GetColor(155,152,204), 'label':'t#bar{t} (1l)'},
        3:{'name':'tt2l', 'colour':ROOT.TColor.GetColor(155,152,204), 'label':'t#bar{t} (2l)'},
        4:{'name':'ttW', 'colour':ROOT.TColor.kGreen + 2, 'label':'t#bar{t}W'},
        5:{'name':'ttZ', 'colour':ROOT.TColor.kGreen + 3, 'label':'t#bar{t}Z'},
        6:{'name':'tH_YtMinus', 'colour':ROOT.TColor.kRed + 3, 'label':'tH (y_{t}=-1)'},
        7:{'name':'ttH', 'colour':ROOT.TColor.GetColor(248,206,104), 'label':'t#bar{t}H'},
        8:{'name':'reducible', 'colour':ROOT.TColor.GetColor(250,202,255), 'label':'Reducible'},
        9:{'name':'data', 'colour':1, 'label':'Data'}, # FIXME: 100?
    }
    p = Plotter(variables, sampleDict, fileName="BDT_training_mva.root")
    p.readTuples()
    p.makePlots(weight='bdt_evt_weight')
