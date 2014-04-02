import ROOT
import os
import NtupleTMVAEvaluate
import array
import math

from tmva_cat_training import training_vars

TMVA_tools = ROOT.TMVA.Tools.Instance()


def convertCompositeVariables(compositeVariables, readerVarDict):
    """ Example immplementation of compositeHandler.
        This function converts ROOT cut string parser expressions for the NtupleTMVAEvaluate class.
    """
    handledCompositeVariables = compositeVariables[:]

    # finish convert statement with 'continue'. Otherwise 
    for variableExpression in compositeVariables:
        if variableExpression == '(bdt_evt_max_jet_eta30*(bdt_evt_max_jet_eta30>0.))':
            val = readerVarDict['bdt_evt_max_jet_eta30'][0]
            readerVarDict[variableExpression][0] = val if val >0. else 0.
            continue
        elif 'abs' in variableExpression and '-' in variableExpression:
            vars = variableExpression.strip('abs')
            vars = vars.strip(' (')
            vars = vars.strip(' )')
            vars = vars.split('-')
            readerVarDict[variableExpression][0] = abs(readerVarDict[vars[0]][0] - readerVarDict[vars[1]][0])
            print variableExpression, 'abs and -', readerVarDict[variableExpression][0]
            if math.isnan(readerVarDict[variableExpression][0] ):
                import pdb; pdb.set_trace()
            continue
        elif '-' in variableExpression:
            vars = variableExpression.split('-')
            readerVarDict[variableExpression][0] = readerVarDict[vars[0]][0] - readerVarDict[vars[1]][0]
            continue
        elif '+' in variableExpression:
            vars = variableExpression.split('+')
            readerVarDict[variableExpression][0] = readerVarDict[vars[0]][0] + readerVarDict[vars[1]][0]
            continue
        elif '*' in variableExpression:
            vars = variableExpression.split('*')
            readerVarDict[variableExpression][0] = readerVarDict[vars[0]][0] * readerVarDict[vars[1]][0]
            continue
        elif '/' in variableExpression:
            vars = variableExpression.split('/')
            readerVarDict[variableExpression][0] = readerVarDict[vars[0]][0] / readerVarDict[vars[1]][0] if readerVarDict[vars[1]][0] > 0. else 0.
            continue
        elif variableExpression.startswith('abs'):
            var = variableExpression.strip('abs')
            var = var.strip(' (')
            var = var.strip(' )')
            readerVarDict[variableExpression][0] = abs(readerVarDict[var][0])
            print variableExpression, 'abs', readerVarDict[variableExpression][0]
            continue


            

        handledCompositeVariables = [v for v in handledCompositeVariables if v != variableExpression]

    return handledCompositeVariables



files = ['BDT_training.root' ]


for f in files:
    outf = f.replace('.root', '_mva.root')
    os.system('cp {file} {file_out}'.format(file=f, file_out=outf))


    n = NtupleTMVAEvaluate.NtupleTMVAEvaluate(outf)
    n.setCompositeVariableHandler(convertCompositeVariables)
    n.setVariables(training_vars)
    n.addMVAMethod('Fisher', 'Fisher', 'weights/TMVAClassification_Fisher.weights.xml')
    n.addMVAMethod('BDTG', 'BDTG', 'weights/TMVAClassification_BDTG.weights.xml')
    
    n.process()
