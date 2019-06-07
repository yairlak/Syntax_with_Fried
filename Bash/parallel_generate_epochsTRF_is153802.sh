# 
echo "Which patient to run (e.g., 479, 482)?"
read PATIENT
PATIENT=502

echo "From channel (integer)?"
read CH_FROM
CH_FROM=17

echo "To channel (integer)?"
read CH_TO
CH_TO=100

for CH in $(seq $CH_FROM $CH_TO)
do
     path2script='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/'
     
     filename='generate_multichannel_spectrotemporal_epochs'
     
     filename_py=$filename'.py -patient '$PATIENT' -channels '$CH 

     python $path2script$filename_py > 'Logs/'$filename'_patient_'$PATIENT'_ch_'$CH'.log'
         
done

