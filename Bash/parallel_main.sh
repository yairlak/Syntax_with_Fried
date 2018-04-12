# How to run this script: 
# 
#    cd matlab/Scores/
#    source run_imagenet.sh  <SEED>
# 

set PROJECT = phonemeTIMIT
set SEED = $1
set DIALECT = "1 2 3 4 5 6 7 8"
set SRC_DIR = ~/Documents/MATLAB/phonemeTIMIT/
mkdir -p /tmp/Logs;
mkdir -p ${SRC_DIR}/RunScripts


cd ${SRC_DIR}
cd extract_phonemes_from_TIMIT

foreach CLASS (${DIALECT})
         set parmstr = TIMIT.DIALECT.$CLASS.SEED.$SEED
         set filename = ${SRC_DIR}/RunScripts/run_$parmstr.m
         set logname = /tmp/Logs/log_$parmstr.txt

         rm -f $filename; 
         touch $filename
         echo "FileNameSeed = sprintf('Seed%d.mat', $SEED);" >> $filename
         echo "dialect = $DIALECT;" >> $filename
         echo "main_phonemes_from_TIMIT;" >> $filename
         echo "matlab < $filename >&! $logname"
      
         matlab < $filename >&! $logname &
end 

