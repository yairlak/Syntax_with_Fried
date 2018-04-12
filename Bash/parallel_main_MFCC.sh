# How to run this script: 
# 
#    cd matlab/Scores/
#    source run_imagenet.sh  <SEED>
# 

set PROJECT = phonemeTIMIT
# set SEED = $1
set DIALECT = " 1 2 3 4 5 6 7 8"
set SRC_DIR = /home/lab/yairlak/Documents/MATLAB/phonemeTIMIT/Calc_MFCC_phonemesTIMIT
mkdir -p ${SRC_DIR}/tmp/Logs;
mkdir -p ${SRC_DIR}/RunScripts


cd ${SRC_DIR}

foreach DIALECT (${DIALECT})
         set parmstr = TIMIT.DIALECT.$DIALECT
         set filename = ${SRC_DIR}/RunScripts/run_$parmstr.m
         set logname = ${SRC_DIR}/tmp/Logs/log_$parmstr.txt

         rm -f $filename; 
         touch $filename
         # echo "FileNameSeed = sprintf('Seed%d.mat', $SEED);" >> $filename
         echo "dialect = $DIALECT;" >> $filename
         echo "run_melfcc_TIMIT_phonemes;" >> $filename
         echo "matlab < $filename >&! $logname"
      
         /cortex/packages/matlab/R2012b/bin/matlab < $filename >&! $logname &
end 

cd /home/lab/yairlak/Documnets/MATLAB
