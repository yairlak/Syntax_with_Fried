# 
#rm -r Logs
mkdir Logs

echo "Which patient to run (e.g., 479, 482)?"
read PATIENT

echo "Which block to plot (auditory/visual/1/2/3/4/5/6)?"
read BLOCK

echo "Aligh figure to - (first/last/end)?"
read ALIGN

echo "Which group of channels to run (1: 1-64, 2: 65-128, ...)?"
read GROUP

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
    walltime="72:00:00"
fi

for CH in $(seq $((1+($GROUP-1)*80)) $(($GROUP*80)))
do
     path2script='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/'
     filename_py='plot_rasters.py -patient '$PATIENT' -block '$BLOCK' -align '$ALIGN' -channel '$CH' -tmin -3 -tmax 1'
     output_log='Logs/log_o_channel_'$CH
     error_log='Logs/log_e_channel_'$CH
     job_name='Channel_'$CH

     CMD="python $path2script$filename_py"

     echo $CMD | qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log # $filename_bash
         
         
done

