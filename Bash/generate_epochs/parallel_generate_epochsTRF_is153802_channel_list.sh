# 
echo "Which patient to run (e.g., 479, 482)?"
read PATIENT

echo "Channel numbers (separated by spaces, e.g., 5 33 40)?"
read CH_FROM

for CH in ${CH_FROM[@]}
do
     path2script='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/'
     
     filename='generate_multichannel_spectrotemporal_epochs_micro'
     
     filename_py=$filename'.py -patient '$PATIENT' -channels '$CH 

     python $path2script$filename_py > 'Logs/'$filename'_patient_'$PATIENT'_ch_'$CH'.log' &
         
done

