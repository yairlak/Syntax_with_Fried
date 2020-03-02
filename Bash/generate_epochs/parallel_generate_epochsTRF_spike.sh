# 
#rm -r Logs
#rm -r RunScripts
#mkdir Logs
#mkdir RunScripts

echo "Which patient to run (e.g., 479, 482)?"
read PATIENT


echo "From channel (integer)?"
read CH_FROM
#CH_FROM=17

echo "To channel (integer)?"
read CH_TO
#CH_TO=100

qstat -q

echo "Choose queue (1: Unicog_long, 2: Nspin_long, 3: Unicog_short, 4: Nspin_short, 5: Unicog_run32, 6: Nspin_run32, 7: Unicog_run16, 8: Nspin_run16, 9: Nspin_bigM)"
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

for CH in $(seq $CH_FROM $CH_TO)
do


     path2script='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/spikes/'
     filename_bash='RunScripts/bash_channel_'$CH'.sh'
     filename_py='generate_multichannel_spike_epochs.py --patient '$PATIENT' --channels '$CH' --path2epochs $TMPDIR'
     output_log='Logs/out_spi_p_'$PATIENT'_ch_'$CH
     error_log='Logs/err_spi_p_'$PATIENT'_ch_'$CH
     job_name='spi_p_'$PATIENT'_ch_'$CH

     rm -f $filename_bash
     touch $filename_bash
     echo "python $path2script$filename_py" >> $filename_bash
     echo "rsync -av \$TMPDIR'/' '/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Data/UCLA/patient_$PATIENT/Epochs/' -v" >> $filename_bash

     qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
done

