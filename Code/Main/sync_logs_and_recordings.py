import os, argparse, glob
from neo import io
#from neo-0.8.0.dev0-py3.7.egg import io
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Synchronize triggers channel and paradigm logs.')
parser.add_argument('--logs-folder', default="../../Data/UCLA/patient_504/Logs/original/", help="Path to original log files")
parser.add_argument('--ttl-file', default="../../Data/UCLA/patient_504/Raw/nev_files/EXP12_Syntax001.nev", help="Path to triggers file. WITHOUT extension for Blackrock")
parser.add_argument('--recording-system', choices=['Neuralynx', 'BlackRock'], default='BlackRock')
args = parser.parse_args()
print(args)


CHEETAH_str = 'CHEETAH_SIGNAL'

# -------------------
# ---- functions ----
# -------------------

def remove_false_TTLs(times, event_nums):
    IX_to_keep = []
    for i, (t, e) in enumerate(zip(times, event_nums)):
        if i > 1:
            previous_t = times[i - 1]
            previous_e = event_nums[i-1]
            prev_prev_e = event_nums[i - 2]
            if e!=0 and previous_e!=0 and prev_prev_e==0 and (t-previous_t)<35000: # shorter than 35000microsec
                curr_event_bin = np.binary_repr(int(e), 16)
                prev_event_bin = np.binary_repr(int(previous_e), 16)
                keep = False
                for (bit_curr, bit_prev) in zip(curr_event_bin, prev_event_bin):
                    if int(bit_curr) > int(bit_prev):
                        keep = True
                        break
                if keep:
                    IX_to_keep.append(i)
            else:
                IX_to_keep.append(i)
        else:
            IX_to_keep.append(i)
    return np.asarray(times)[IX_to_keep], np.asarray(event_nums)[IX_to_keep]

def remove_events_zero(times, event_nums):
    IX_to_keep = []
    for i, e in enumerate(event_nums):
        if e>0:
            IX_to_keep.append(i)
    return np.asarray(times)[IX_to_keep], np.asarray(event_nums)[IX_to_keep]


def find_beginning_of_blocks(d_times_ttl, d_events_ttl):
    delta_thresh = 1.1*1e6 # time deltas around event=100 in microsec. I set it to >1sec, which is the largest ISI, assuming it takes more than a sec to start the block
    IXs_onsets = []
    for i, (delta_t, e) in enumerate(zip(d_times_ttl, d_events_ttl)):
        if i == 0:
            prev_delta_t = delta_thresh + 1
        else:
            prev_delta_t = d_times_ttl[i-1]

        if e==100:
            if delta_t > delta_thresh and prev_delta_t > delta_thresh: # check if duration after and before event=100 is greater than 1500ms
                IXs_onsets.append(i)
    # assert len(IXs_onsets) == 6 # Make sure only 6 block onsets were found
    return IXs_onsets


# -----------------------------
# ----------- events file -----
# -----------------------------

# Load events from nev file
if args.recording_system == 'Neuralynx':
    print(args.ttl_file)
    NIO = io.NeuralynxIO(os.path.dirname(args.ttl_file))
    time0, timeend = NIO._timestamp_limits[0]
    print('time0, timeend = ', time0, timeend)
    events = NIO._nev_memmap[os.path.basename(args.ttl_file)[:-4]]
    times_ttl = [float(e[3]) for e in events]
    event_nums_ttl = [float(e[5]) for e in events]

elif args.recording_system == 'BlackRock':
    NIO = io.BlackrockIO(args.ttl_file)
    events = NIO.nev_data['NonNeural']
    assert NIO._BlackrockRawIO__nev_basic_header[6] == NIO._BlackrockRawIO__nev_basic_header[7] # I wasnt sure if these two represent indeed sampling rate
    sr = NIO._BlackrockRawIO__nev_basic_header[6]
    times_ttl = [1e6*e[0]/sr for e in events[0]] # transfrom from samples to microsec, like with Neuralynx
    event_nums_ttl = [e[4] for e in events[0]]
    # fix, ax = plt.subplots(1)

    # !!!! ONLY for patient 504 - for some reason event numbers in first block were shifted upwards
    event_nums_ttl = [e - 128 if e > 65400 else e for e in event_nums_ttl]
    # plt.plot(event_nums_ttl)
    # plt.show()
    # ----- !!!!!!!!!!!!!!! ---------------
    event_nums_ttl = [e - min(event_nums_ttl) for e in event_nums_ttl]



# Remove false triggers
times_ttl, event_nums_ttl = remove_false_TTLs(times_ttl, event_nums_ttl)
times_ttl, event_nums_ttl = remove_events_zero(times_ttl, event_nums_ttl) # Should only come after remove_false_TTLs

diff_times_ttl = np.diff(times_ttl)
diff_events_ttl = event_nums_ttl[0:-1]
IXs_block_onsets = find_beginning_of_blocks(diff_times_ttl, diff_events_ttl) # find block onsets based on event=100

# Plot events of all experiment
plt.scatter(times_ttl, event_nums_ttl)
plt.scatter(times_ttl[IXs_block_onsets], event_nums_ttl[IXs_block_onsets], color='r')
plt.show()

# Split event times and numbers to blocks
events_blocks = []
times_ttl_blocks = []
for block in range(6):
    IX_curr_block_onset = IXs_block_onsets[block]
    if block < 5:
        IX_curr_block_offset = IXs_block_onsets[block+1]
    else: # last block (6th)
        IX_curr_block_offset = len(times_ttl)

    events_blocks.append(event_nums_ttl[IX_curr_block_onset:IX_curr_block_offset])
    times_ttl_blocks.append(times_ttl[IX_curr_block_onset:IX_curr_block_offset])

# -----------------------
# --- LOGS --------------
# -----------------------

# Load paradigm times from log file
times_logs = []
log_filenames = glob.glob(os.path.join(args.logs_folder, 'events_log_20*.log'))
log_filenames.sort()
for block, fn in enumerate(log_filenames):
    with open(fn, 'r') as f_log:
        log = f_log.readlines()
    curr_times_log = [float(l.split(' ')[3])*1e6 for l in log if l.split(' ')[1] == CHEETAH_str]
    times_logs.append(np.asarray(curr_times_log))



# -----------------------
# --- Loop over blocks --
# -----------------------

for block, (times_events_block, times_log_block, events_num_block) in enumerate(zip(times_ttl_blocks, times_logs, events_blocks)):
    thresh = 10000
    false_ttl_found = True
    while false_ttl_found:
        false_ttl_found = False

        d_times_ttl_block = np.diff(times_events_block)
        d_times_log_block = np.diff(times_log_block)

        for i in range(d_times_log_block.shape[0]):
            if abs(d_times_ttl_block[i] - d_times_log_block[i]) > thresh:
                false_ttl_found = True
                times_events_block = np.delete(times_events_block, i+1)
                events_num_block = np.delete(events_num_block, i+1)
                break

    print(times_events_block.shape[0], times_log_block.shape[0])
    assert times_events_block.shape[0] == times_log_block.shape[0]

    # Generate new log files with times based on TTLs
    with open(log_filenames[block], 'r') as f_log:
        log_block = f_log.readlines()

    new_log = []
    IX_sync_times = -1
    for i, l in enumerate(log_block):
        if l.split(' ')[1] == CHEETAH_str:
            IX_sync_times += 1
            last_log_time = times_log_block[IX_sync_times]
            last_TTL_time = times_events_block[IX_sync_times]
            new_time = last_TTL_time
        else:
            old_time = float(l.split(' ')[0])*1e6 # in microsec
            new_time = old_time - last_log_time + last_TTL_time

        new_line = ' '.join([str(int(new_time))] + l.split(' ')[1:])
        new_log.append(new_line)

    with open(os.path.join(os.path.dirname(log_filenames[block]), '..', 'events_log_in_cheetah_clock_part%i.log'%(block+1)), 'w') as f_new:
        for l in new_log:
            f_new.write("%s" % l)
    print('New log file was saved to: %s' % os.path.join(os.path.dirname(log_filenames[block]), '..', 'events_log_in_cheetah_clock_part%i.log'%(block+1)))
