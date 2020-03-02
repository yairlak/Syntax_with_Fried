

##########################
#### DOWNLOAD DATA #######
##########################

1. to list files on box: 'rclone lsd box:' 

2. Put the raw files in 'Raw' subfolder of patient folder. Make sure that only a single event file (nev) exist (the one with the larger file size)
Organize into
micro/ncs
macro/ncs


3. To transform raw to mat files, run: Spike_sorting/Neuralynx_pipeline/ncs2mat.m
matlab -nodisplay -nojvm 

4. Make sure the features.xls file is in /Paradigm


###################
####  LOGS ########
###################

# 
cd /Code/arielt/ucla/neuralynx/matlab/clock_sync/

# Make sure no previous nev files exist
rm *.nev

# Copy the new event file and rename it to nlx_new.nev
cp ../../../../../../Data/UCLA/patient_505/EXP6_Syntax/2018-12-07_15-48-17/*.nev nlx_new.nev

# Remove history log files to make sure there's only a single log file in the forma "events_log_yyyy-mm-dd_hh-mm-ss.log"
rm events_log_in_cheetah_clock.log
rm events_log.log
rm events_log_20*.log

# copy the new log for sync
cp ../../../../../../Data/UCLA/patient_505/log_patient/505/events_log_2018 . -v

# Launch the synch script
matlab -nodesktop -nodisplay -nojvm -r "clock_sync(false, 'events_log', 0, false, ''); exit"

# make sure the output is OK and if so copy the result to the destination folder
cp events_log_in_cheetah_clock.log ../../../../../../Data/UCLA/patient_505/log_patient/events_log_in_cheetah_clock_part1.log

!!!!!!!!!!!!!!!!!!!!!!!!
!!! The next step runs only on my laptop, under 'conda activate Syntax_with_Fried' and with python2.7
!!!!!!!!!!!!!!!!!!!!!!!!
3. To get time0 and timeEnd, run read_nev_files.py e.g. 'python2.7 read_nev_files.py patient_487'. Add these times to 'load_setting_params'

!!!!!!!!!!!!!!!!!!!!!
!!!! make sure before the next step that clock_sync was run on log files - see (README.yair). Then all logs are in the following format 'events_log_in_cheetah_clock_part*.log'
!!!!!!!!!!!!!!!!!!11

4. from GUI_mark_word_onsets/, launch: generate_logs_with_phonemes.py

5. Make sure that in function/load_settings_params.py all is well defined (prefix of log files, e.g., mouse_cheatha..part1)


############################
##### MICROPHONE CHECK #####
############################

- convert the ncs file for the mic to mat: Code/Spike_sorting/Neuralynx_pipeline/ncsMIC2CSC.m (matlab --nodisplay)

- Copy Microphone mat file to /Raw/micro/CSC_mat and name it CSC0.mat

- From Code/Main/micro, launch: python generate_multichannel_spectrotemporal_epochs.py --channels 0 --patient 505
which will generate the epochsTFR file in Data/UCLA/patient_???/Epochs/

- To plot, launch:
python plot_epochs_ERPs.py --patient 505 --channel 0 --tmin -1 --tmax 2 --baseline "(-1, 0)" --sort-key "['chronological_order']" --query "word_position == 1 and block in [2, 4, 6]"
python plot_epochs_ERPs.py --patient 505 --channel 0 --align end --block auditory --tmin -2 --tmax 1 --baseline "(0, 1)" --sort-key "['chronological_order']" # aligned to end


###############################
##### GENERATE EPOCH FILES ####
###############################
- convert the ncs file for the mic to mat: Code/Spike_sorting/Neuralynx_pipeline/ncs2CSC.m (matlab --nodisplay)
- from Code/Main/micro, launch generate_multichannel_spectrotemporal_epochs_micro.py
- from Code/Main/macro, launch generate_multichannel_spectrotemporal_epochs_macro.py

###############################
##### SPIKE SORTING        ####
###############################
# Run from Raw/micro/

# 0. rename ncs files to CSC?.ncs
# Copy the following file to /CSC_mat folder and run it
Code/Utils/spike_sorting/get_channel_names.py
# Copt the following to /ncs folder and run it
Code/Utils/spike_sorting/rename_channel_names_to_CSCs.py

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# All the following steps should be run from the folder: /CSC_ncs
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# 0. cd to path
cd /Raw/micro/CSC_ncs

# 1. (optional) generate overview plots for raw signal
css-plot-rawsignal
# check new subfolder overview


# 2. extract spikes (not yet sorted) from all channels
css-extract --files *.ncs > css_extract.log
# new subfolder CSC were genereted with data_CSC*.h5 files

# 3. find artifacts
css-find-concurrent

# 4. remove artifacts
css-mask-artifacts

# 5. prepare for sorting
- Use css-plot-extracted to create plots of the spikes after artifact removal. These plots display the different artifact types, and also visualize cumulative spike counts.
- Next, prepare a job file (do_sort_pos.txt) by using css-overview-gui (Actions-->init from current folder and then  Actions->Save actions to file): this will generate the job file.
- (!!--important--!!) remove duplications in this job file (not clear why it happens). Make sure you have #channels lines in this file, without duplications, before you continue.
- Note that you can also prepare a job file for negative spikes (do_neg*.txt). For this, use css-overview-gui (toggle sort negative) to change the values in the corresponding channel rows. This will generate a second job file (do_sort_neg.txt). You would then need to repeat the step below TWICE, once for pos and once for neg.

Run:
css-prepare-sorting --jobs do_sort_pos.txt
css-prepare-sorting --jobs do_sort_neg.txt --neg

# 6. Sorting
css-cluster --jobs sort_pos_yl2.txt
css-cluster --jobs sort_neg_yl2.txt

# 7. combine
css-combine --jobs sort_pos_yl2.txt
css-combine --jobs sort_neg_yl2.txt

# 8. (optional) generate sorting plots
css-plot-sorted --label sort_pos_yl2
plot_sorted_CSC.py
# still get errors (skip this step)


# 9. (optional) Use the GUIs to optimize results
css-overview-gui
# enter the sorting label sort_pos_abc and initialize the folder (from the menu or by pressing Ctrl+I).

# 10. Manual fix:
css-gui


####################
##### ANALYSES  ####
####################

See Bash/ folder.
