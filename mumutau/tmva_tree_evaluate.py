import ROOT
import os
import math
import sys
import optparse

sys.path.append("../Common")
import NtupleTMVAEvaluate

from tmva_cat_training import training_vars

TMVA_tools = ROOT.TMVA.Tools.Instance()

def parse_options():
    usage = '''
%prog [options]
'''
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--input', dest='input_file', help='input file name', default='/afs/cern.ch/user/y/ytakahas/public/forJan/tH_BDTtraining_20141009/BDT_training_ss_f12_nottbar.root', type='string')
    parser.add_option('-o', '--out_postfix', dest='out_postfix', help='output file postfix', default='', type='string')
    opts, args = parser.parse_args()
    return opts, args

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
        elif variableExpression == 'log(abs(bdt_muon_dz))':
            val = readerVarDict['bdt_muon_dz'][0]
            readerVarDict[variableExpression][0] = math.log(abs(val))
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


if __name__ == '__main__':
    opts, args = parse_options()

    input_file = opts.input_file
    postfix = opts.out_postfix

    outf = input_file.split('/')[-1].replace('.root', '_mva.root')
    os.system('cp {file} {file_out}'.format(file=input_file, file_out=outf))

    n = NtupleTMVAEvaluate.NtupleTMVAEvaluate(outf)
    n.setCompositeVariableHandler(convertCompositeVariables)
    n.setVariables(training_vars)
    n.addMVAMethod('Fisher', 'Fisher', 'weights/TMVAClassification_Fisher{postfix}.weights.xml'.format(postfix=postfix))
    n.addMVAMethod('BDTG', 'BDTG', 'weights/TMVAClassification_BDTG{postfix}.weights.xml'.format(postfix=postfix))
    
    n.process()
