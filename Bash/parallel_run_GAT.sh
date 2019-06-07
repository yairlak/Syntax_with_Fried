# 
queue='Global_short'
walltime='02:00:00'
K=1
PATIENTS="-p 479 -p 482 -p 502 -p 505"

for COMP in $(seq 0 35)
do
     path2script='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Code/Main/'
     filename_bash='RunScripts/bash_comparison_'$COMP'.sh'
     filename_py='run_GAT.py '$PATIENTS' --cat-k-timepoints '$K' -c '$COMP 
     output_log='Logs/log_o_comparison_'$COMP
     error_log='Logs/log_e_comparison_'$COMP
     job_name='Comparison_'$COMP

     rm -f $filename_bash
     touch $filename_bash
     echo "python $path2script$filename_py" >> $filename_bash
         
     qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
done

