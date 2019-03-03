# 
rm -r Logs
rm -r RunScripts
mkdir Logs
mkdir RunScripts

echo "Which patient to run (e.g., 479, 482)?"
read PATIENT

echo "Which group of channels to run (1: 1-64, 2: 65-128, ...)?"
read GROUP

qstat -q

echo "Choose queue (1: Unicog_long, 2: Global_long, 3: Unicog_short, 4: Global_short)"
read QUEUE

if [ $QUEUE -eq 1 ]
then
    queue="Unicog_long"
    walltime="72:00:00"
elif [ $QUEUE -eq 2 ]
then
    queue="Global_long"
    walltime="72:00:00"
elif [ $QUEUE -eq 3 ]
then
    queue="Unicog_short"
    walltime="02:00:00"
elif [ $QUEUE -eq 4 ]
then
    queue="Global_short"
    walltime="02:00:00"
fi

for CH in $(seq $((1+($GROUP-1)*64)) $(($GROUP*64)))
do
     path2script='/neurospin/unicog/protocols/intracranial/single_unit_syntax_pipeline/Code/Main/'
     filename_bash='RunScripts/bash_channel_'$CH'.sh'
     filename_py='generate_multichannel_spectrotemporal_epochs.py -patient '$PATIENT' -channels '$CH 
     output_log='Logs/log_o_channel_'$CH
     error_log='Logs/log_e_channel_'$CH
     job_name='Channel_'$CH

     rm -f $filename_bash
     touch $filename_bash
     echo "python $path2script$filename_py" >> $filename_bash
         
#echo -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_py
     qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
done

