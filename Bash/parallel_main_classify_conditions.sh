# How to run this script: 
# 

echo "How many comaprions to run?"
read LAST_COMP

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

rm Logs/log_classification_*
rm RnScripts/run_classification_*.sh

for COMP in $(seq 0 $LAST_COMP)
do
         path2script='/neurospin/unicog/protocols/intracranial/single_unit_syntax_pipeline/Code/Main_analyses/'
         filename_bash='RunScripts/run_classication_'$COMP'.sh'
	 filename_py='main_classify_conditions.py '$COMP
	 output_log='Logs/log_classification_o_comparison_'$COMP
	 error_log='Logs/log_classification_e_comparison_'$COMP
	 job_name='Comparison_'$COMP

         rm -f $filename_bash
         touch $filename_bash
         echo "python2.7 $path2script$filename_py" >> $filename_bash
         
	 qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
done

