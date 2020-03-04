# 
#rm -r RunScripts 
#mkdir RunScripts

#RUN_GAT='' # ' --run-gat' or ''
#RUN_ERPS=' --run-erps' # ' --run-erps' or ''

echo "Which patient to run (e.g., 479, 482)?"
read PATIENT

echo "Which signal type (micro/macro/spike)?"
read SIGNAL_TYPE

echo "Run GAT ('0' or '1')?"
read GAT

if [ $GAT -eq 1 ]
then
    RUN_GAT=' --run-gat'
else
    RUN_GAT=''
fi

echo "Run ERPs/Rasters ('0' or '1')?"
read ERPS

if [ $ERPS -eq 1 ]
then
    RUN_ERPS=' --run-erps'
else
    RUN_ERPS=''
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
    walltime="72:00:00"
fi

echo "Local(0) or Alambic (1)?"
read CLUSTER



for COMP in $(seq 0 41)
#for COMP in 37 39
do
     path2script="/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/plotting/"
     arg_patient=''
     str_patients=''
     for patient in $PATIENT
     do
        arg_patient="${arg_patient} --patients ${patient}"
        str_patients="${str_patients}${patient}_"
     done
     filename_py="plot_comparison.py"$arg_patient" --comparisons "$COMP" --signal-type "$SIGNAL_TYPE$RUN_ERPS$RUN_GAT
     output_log='Logs/out_'$str_patients'_comp_'$COMP'_signal_'$SIGNAL_TYPE
     error_log='Logs/err_'$str_patients'_comp_'$COMP'_signal_'$SIGNAL_TYPE
     job_name='Comp_'$COMP'_p_'$str_patients

     CMD="python $path2script$filename_py"
       

    #filename_bash='RunScripts/'$str_patients'_comp_'$COMP'.sh'
    if [ $CLUSTER -eq 1 ]
    then
        #rm -f $filename_bash
        #touch $filename_bash
        #echo "python $path2script$filename_py" >> $filename_bash
        #echo qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
        echo $CMD | qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log
    else
        echo $CMD'&'
    fi
         
done

