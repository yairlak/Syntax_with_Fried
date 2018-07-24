# How to run this script: 
# 
#    cd 
#    ./run_jobs.sh  <GROUP>
# 

#set GROUP = $1
rm -r Logs
rm -r RunScripts
mkdir Logs
mkdir RunScripts
#set st = `expr $GROUP \* 64 - 64 + 1`
#set ed = `expr $GROUP \* 64`
echo "Which group of channels to run (1: 1-64, 2: 65-128, ...)?"
read GROUP

for CH in $(seq $((1+($GROUP-1)*64)) $(($GROUP*64)))
do
         path2script='/neurospin/unicog/protocols/intracranial/single_unit_syntax_pipeline/Code/Main_analyses/'
         filename_bash=RunScripts/bash_channel_$CH.sh
	 filename_py='main_plot_trial_time_freq.py '$CH
	 output_log='Logs/log_o_channel_'$CH
	 error_log='Logs/log_e_channel_'$CH
	 queue='Unicog_long'
	 job_name='Channel_'$CH
	 walltime='72:00:00'

         rm -f $filename_bash
         touch $filename_bash
	 echo "python2.7 $path2script$filename_py" >> $filename_bash
         
	 #cho -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_py
	 qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
done

