# How to run this script: 
# 
#    cd 
#    source run_jobs.sh  <GROUP>
# 

#set PROJECT = "macro_contacts_analysis"
set GROUP = $1
set CHANNELS = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30"
#set SRC_DIR = "/neurospin/unicog/protocols/intracranial/Code"
#mkdir -p /tmp/Logs
#mkdir -p /RunScripts


#cd ${SRC_DIR}
#cd ${PROJECT}

foreach CH (${CHANNELS})
         set parmstr = CHANNEL_$CH
         set filename = RunScripts/run_$parmstr.m
         set logname = Logs/log_$parmstr.txt

         rm -f $filename 
         touch $filename
         echo "channel = ($GROUP-1) * 30 + $CH;" >> $filename
         echo "main_Ripples" >> $filename
      
         matlab -nodisplay < $filename >&! $logname &
end

