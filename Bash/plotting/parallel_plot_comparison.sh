# 
#rm -r Logs
#rm -r RunScripts
#mkdir Logs
#mkdir RunScripts

echo "Which patient to run (e.g., 479, 482)?"
read PATIENT

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


for COMP in $(seq 0 35)
do
     path2script='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/'
     filename_bash='RunScripts/bash_'$PATIENT'_comp_'$COMP'.sh'
     filename_py='plot_comparison.py --patients '$PATIENT' --comparisons '$COMP' --run-gat --signal-type spike'
     output_log='Logs/log_o_'$PATIENT'_comp_'$COMP
     error_log='Logs/log_e_'$PATIENT'_comp_'$COMP
     job_name='Comp_'$COMP'_p_'$PATIENT

     rm -f $filename_bash
     touch $filename_bash
     echo "python $path2script$filename_py" >> $filename_bash
         
#echo -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_py
     qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
done

