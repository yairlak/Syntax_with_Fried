python /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/generate_multichannel_spectrotemporal_epochs_micro.py -patient 504 -channels 42 --path2epochs $TMPDIR
rsync -av $TMPDIR'/' '/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Data/UCLA/patient_504/Epochs/' -v
