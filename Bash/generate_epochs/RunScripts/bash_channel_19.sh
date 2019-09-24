python /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/generate_multichannel_spectrotemporal_epochs_micro.py -patient 479_11 -channels 19 --path2epochs $TMPDIR
rsync -av $TMPDIR'/' '/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Data/UCLA/patient_479_11/Epochs/' -v
