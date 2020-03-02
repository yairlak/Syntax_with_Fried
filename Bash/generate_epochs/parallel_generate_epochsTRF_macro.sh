# 
#rm -r Logs
#rm -r RunScripts
#mkdir Logs
#mkdir RunScripts


qstat -q

echo "Choose queue (1: Unicog_long, 2: Nspin_long, 3: Unicog_short, 4: Nspin_short, 5: Unicog_run32, 6: Nspin_run32, 7: Unicog_run16, 8: Nspin_run16)"
read QUEUE

if [ $QUEUE -eq 1 ]
then
    queue="Unicog_long"
    walltime="72:00:00"
elif [ $QUEUE -eq 2 ]
then
    queue="Nspin_long"
    walltime="72:00:00"
elif [ $QUEUE -eq 3 ]
then
    queue="Unicog_short"
    walltime="02:00:00"
elif [ $QUEUE -eq 4 ]
then
    queue="Nspin_short"
    walltime="02:00:00"
elif [ $QUEUE -eq 5 ]
then
    queue="Unicog_run32"
    walltime="02:00:00"
elif [ $QUEUE -eq 6 ]
then
    queue="Nspin_run32"
    walltime="02:00:00"
elif [ $QUEUE -eq 7 ]
then
    queue="Unicog_run16"
    walltime="02:00:00"
elif [ $QUEUE -eq 8 ]
then
    queue="Nspin_run16"
    walltime="02:00:00"
elif [ $QUEUE -eq 9 ]
then
    queue="Nspin_bigM"
    walltime="02:00:00"
fi

for PATIENT in '479_11' '482' '487' '493' '502' '505' '513' '515'; do
     path2script='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/macro/'
     filename_bash='RunScripts/bash_'$PATIENT'.sh'
     filename_py='generate_multichannel_spectrotemporal_epochs_macro.py --patient '$PATIENT' --path2epochs '$TMPDIR
     output_log='Logs/out_mac_'$PATIENT
     error_log='Logs/err_mac_'$PATIENT
     job_name='mac_P_'$PATIENT

     rm -f $filename_bash
     touch $filename_bash
     echo "python $path2script$filename_py" >> $filename_bash
     echo "rsync -av \$TMPDIR'/' '/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Data/UCLA/patient_$PATIENT/Epochs/' -v" >> $filename_bash

     qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
done

