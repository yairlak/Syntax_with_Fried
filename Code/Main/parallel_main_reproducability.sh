# How to run this script: 
# 
#    cd 
#    ./run_jobs.sh  <GROUP>
# 

set GROUP = $1
#set SRC_DIR = "/neurospin/unicog/protocols/intracranial/Code"
#mkdir -p /tmp/Logs
#mkdir -p /RunScripts

set st = `expr $GROUP \* 32 - 32 + 1`
set ed = `expr $GROUP \* 32`

foreach CH ( `seq ${st} ${ed}` )
         set filename_bash=RunScripts/log_$CH.sh
	 set filename_py='main_reproducability.py '$CH
	 set output_log='Logs/log_o_channel_'$CH
	 set error_log='Logs/log_e_channel_'$CH
	 set queue='Unicog_long'
	 set job_name='Channel_'$CH
	 set walltime='72:00:00'

         rm -f $filename_bash
         touch $filename_bash
	 echo "python2.7 /neurospin/unicog/protocols/intracranial/single_unit_syntax_pipeline/Code/Main/$filename_py" >> $filename_bash
         
	 qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
end
