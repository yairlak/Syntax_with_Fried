# How to run this script: 
# 
#    cd 
#    ./run_jobs.sh  <GROUP>
# 

set GROUP = $1
#set SRC_DIR = "/neurospin/unicog/protocols/intracranial/Code"
#mkdir -p /tmp/Logs
#mkdir -p /RunScripts

set st = `expr $GROUP \* 40 - 40 + 1`
set ed = `expr $GROUP \* 40`

foreach COMP ( `seq ${st} ${ed}` )
         set filename_bash=RunScripts/run_classication_$COMP.sh
	 set filename_py='main_classify_conditions.py '$COMP
	 set output_log='Logs/log_classification_o_comparison_'$COMP
	 set error_log='Logs/log_classification_e_comparison_'$COMP
	 set queue='Unicog_long'
	 set job_name='Comparison_'$COMP
	 set walltime='02:00:00'

         rm -f $filename_bash
         touch $filename_bash
	 echo "python2.7 /neurospin/unicog/protocols/intracranial/single_unit_syntax_pipeline/Code/Main_analyses/$filename_py" >> $filename_bash
         
	 qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
end

