# How to run this script: 
# 
#    cd 
#    source run_jobs.sh  <GROUP>
# 

#set PROJECT = "macro_contacts_analysis"
set GROUP = $1
set CHANNELS = "1 11 21 31 41 51 61 71 81 91 101 111 121 131 141 151 161 171 181 191 201"
#set SRC_DIR = "/neurospin/unicog/protocols/intracranial/Code"
#mkdir -p /tmp/Logs
#mkdir -p /RunScripts


#cd ${SRC_DIR}
#cd ${PROJECT}

foreach CH (${CHANNELS})
         set parmstr = CHANNEL_$CH
         set filename = RunScripts/run_$parmstr.py
         set logname = Logs/log_$parmstr.txt

         rm -f $filename 
         touch $filename
	 echo "import os" >> $filename
         echo "os.system('python2.7 main_alignment_model.py $CH')" >> $filename
      
         python $filename >&! $logname &
end

