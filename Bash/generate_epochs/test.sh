python /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/generate_multichannel_spectrotemporal_epochs_micro.py -patient 505 -channels 2
echo $TMPDIR
rsync -av $TMPDIR'/' '/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Data/UCLA/patient_505/Epochs/' -v
