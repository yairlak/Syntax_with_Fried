# How to run this script: 
# 
#    cd matlab/Scores/
#    source run_imagenet.sh  <SEED>
# 

set PROJECT = phonemeTIMIT
set DIALECT = $1
set LAMBDA_ORDERS = "-3 -2 -1 0 1 2 3"
set SPLITS = " 1 2 3"
set SRC_DIR = /home/lab/yairlak/Documents/MATLAB/phonemes
mkdir -p ${SRC_DIR}/tmp/Logs;
mkdir -p ${SRC_DIR}/RunScripts


cd ${SRC_DIR}

foreach SPLIT (${SPLITS})
foreach LAMBDA_ORDER (${LAMBDA_ORDERS})
         set parmstr = SPLIT${SPLIT}ORDER${LAMBDA_ORDER}DIALECT${DIALECT}
         set filename = ${SRC_DIR}/RunScripts/run_$parmstr.m
         set logname = ${SRC_DIR}/tmp/Logs/log_$parmstr.txt

         rm -f $filename; 
         touch $filename
         # echo "FileNameSeed = sprintf('Seed%d.mat', $SEED);" >> $filename
         echo "addpath('/home/lab/yairlak/Documents/MATLAB/phonemes')" >> $filename
         echo "dialect = $DIALECT;" >> $filename
	 echo "params.split = $SPLIT;" >> $filename
	 echo "for lambda = (1:9) * (10 ^ $LAMBDA_ORDER);" >> $filename
	 echo "params.lambda = lambda;" >> $filename
         echo "main_LASSO;" >> $filename
	 echo "end" >> $filename
         echo "matlab < $filename >&! $logname"
      
         /cortex/packages/matlab/R2012b/bin/matlab < $filename >&! $logname &
end 
end

cd /home/lab/yairlak/Documnets/MATLAB
