### To produce input datacards:

# Run the TMVA training (using f3 as input)

python tmva_cat_training.py -i /afs/cern.ch/user/y/ytakahas/public/forJan/tH_BDTtraining_20141009/BDT_training_ss_f3_nottbar.root 

# Attach the BDTG and Fisher output values to the input trees (using f12 as input, can also run it for f3 but beware overtraining!)

python tmva_tree_evaluate.py -i /afs/cern.ch/user/y/ytakahas/public/forJan/tH_BDTtraining_20141009/BDT_training_ss_f12_nottbar.root 

# Make the plots including the datacards

python make_plots.py -b


### NOTES

# - include only the appropriate samples in make_plots.py - in particular make sure to not include data as long as we're blinded
# - the current MVA training is done with events from the 'f3' region and applied to the 'f12' region, so there's no risk of overtraining
