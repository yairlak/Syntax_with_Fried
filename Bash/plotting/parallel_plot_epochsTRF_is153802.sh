# 
echo "Which patient to run (e.g., 479, 482)?"
read PATIENT

echo "From channel (integer)?"
read CH_FROM

echo "To channel (integer)?"
read CH_TO

echo "Which block to plot (a/v/1/2/3/4/5/6, a - auditory, v - visual blocks)?"
read BLOCK
if [[ "$BLOCK" == "a" ]];
then
    BLOCK="auditory"
fi
if [[ "$BLOCK" == "v" ]];
then
    BLOCK="visual"
fi


echo "Aligh figure to - (first/last/end)?"
read ALIGN

for CH in $(seq $CH_FROM $CH_TO)
do
     path2script='/neurospin/unicog/protocols/intracranial/single_unit_syntax_pipeline/Code/Main/'
     cmd='plot_epochs_ERPs.py -patient '$PATIENT' -block '$BLOCK' -align '$ALIGN' -filename patient_'$PATIENT'_ch_'$CH'-tfr.h5'
     python $path2script$cmd &
         
done

