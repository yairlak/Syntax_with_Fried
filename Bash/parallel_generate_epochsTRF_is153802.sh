# 
echo "Which patient to run (e.g., 479, 482)?"
read PATIENT

echo "From channel (integer)?"
read CH_FROM

echo "To channel (integer)?"
read CH_TO

for CH in $(seq $CH_FROM $CH_TO)
do
     path2script='/neurospin/unicog/protocols/intracranial/single_unit_syntax_pipeline/Code/Main/'
     filename='generate_multichannel_spectrotemporal_epochs'
     filename_py=$filename'.py -patient '$PATIENT' -channels '$CH' -blocks 2 4 6' 

     python $path2script$filename_py > 'Logs/'$filename'_patient_'$PATIENT'_ch_'$CH'.log' &
         
done

