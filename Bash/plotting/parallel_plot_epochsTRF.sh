# 
rm -r Logs
rm -r RunScripts
mkdir Logs
mkdir RunScripts

echo "Which patient to run (e.g., 479, 482)?"
read PATIENT

echo "Which electrode type (micro/macro)?"
read ELEC_TYPE

PROBE='None'
if [ $ELEC_TYPE = "macro" ]
then
    echo "What is the probe name (LSTG, etc.)?"
    read PROBE
fi

echo "Which block to plot (auditory/visual/1/2/3/4/5/6)?"
read BLOCK

echo "Aligh figure to - (first/last/end)?"
read ALIGN

if [ $ELEC_TYPE = "micro" ]
then
  echo "From channel (integer)?"
  read CH_FROM

  echo "To channel (integer)?"
  read CH_TO
  ST=$CH_FROM
  ED=$CH_TO
elif [ $ELEC_TYPE = "macro" ]
then
  ST=1
  ED=1
fi

qstat -q

echo "Choose queue (1: Unicog_long, 2: Nspin_long, 3: Unicog_short, 4: Nspin_short, 5: Unicog_run32, 6: Nspin_run32, 7: Unicog_run16, 8: Nspin_run16, 9:Nspin_bigM)"
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


for CH in $(seq $ST $ED)
do
     path2script='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/'
     filename_bash='RunScripts/bash_channel_'$CH'.sh'
     filename_py='plot_epochs_ERPs.py -patient '$PATIENT' -block '$BLOCK' -align '$ALIGN' -channel '$CH' --micro-macro '$ELEC_TYPE' --probe-name '$PROBE
     output_log='Logs/log_o_channel_'$CH
     error_log='Logs/log_e_channel_'$CH
     job_name='Channel_'$CH

     rm -f $filename_bash
     touch $filename_bash
     echo "python $path2script$filename_py" >> $filename_bash
         
#echo -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_py
     qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
done

