import os, glob
import numpy as np
import scipy
import scipy.io as sio
import mne
from mne.decoding import GeneralizationAcrossTime
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
import pickle

from sklearn.svm import SVC

__author__ = 'yair'

# Load data and raw object
num_perm = 100
np.random.seed = 1

curr_patient = 'En_02'
curr_block = 'sentences'
file_name = os.path.join('..', '..', 'Output', 'raw_data_with_events_to_python_all_comparisons_' + curr_patient + '_' + curr_block + '.mat')
mat = sio.loadmat(file_name)

# Generate unit names (unique)
lock_to_word = mat['lock_to_word_array']
unit_names_temp = mat['unit_names']
unit_names_temp = unit_names_temp.tolist()
unit_names = []
for x in unit_names_temp[0]:
    unit_names_set = set(unit_names)
    propose_new_name = x.tostring()
    cnt = 1
    while propose_new_name in unit_names_set:
        cnt += 1
        propose_new_name = x.tostring() + str(cnt)
    unit_names.append(propose_new_name)

# Create Info object for MNE
ch_types=['eeg'] * len(unit_names)
sfreq = 1000 #Hz
info = mne.create_info(unit_names, sfreq, ch_types)
print(info)

# Load Raw data and create Raw object for MNE
custom_raw_data = mat['custom_raw_smoothed']
raw = mne.io.RawArray(custom_raw_data, info)

for comparison, events in enumerate(mat['custom_events_all_comparisons'][0]):
    print(comparison)
    curr_comparison_name = mat['comparison_name'][0, comparison][0]

    # Create Events object for MNE
    event_id_temp = mat['event_id_all_comparisons'][0, comparison][0]
    event_id = {}
    for x, id in enumerate(event_id_temp):
        event_id[id[0]] = x
    events = events.astype(int)
    sort_IX = np.argsort(events[:, 0], axis=0)
    events = events[sort_IX, :]

    for perm in range(0, num_perm, 1):
        # SHUFFLE LABELS
        labels = events[:, 2]
        perm_vec = np.random.permutation(events.shape[0])
        labels = labels[perm_vec]
        events[:, 2] = labels

        # REGENERATE Epochs object
        #picks = range(0, 2)
        #decim = 20  # decimate to make the example faster to run
        st_time = -2.1 # in [sec]
        ed_time = 1.1 # in [sec]
        epochs = mne.Epochs(raw, events, event_id, st_time, ed_time, proj=True,
                            baseline=None, preload=True, verbose=False)#, decim=decim, picks=picks)

        print(epochs)

        train_times = {}
        train_times["start"] = -2.0
        train_times["stop"] = 1.05
        train_times["step"] = 0.1
        test_times = {}
        test_times["start"] = -2.0
        test_times["stop"] = 1.05
        test_times["step"] = 0.1


        if len(event_id) > 1:


            # Define decoder. The decision function is employed to use cross-validation
            gat = GeneralizationAcrossTime(clf=LinearSVC(), train_times=train_times, test_times=test_times,
                                           predict_mode='cross-validation', n_jobs=1)

            # fit and score
            print('Fit model')
            gat.fit(epochs)
            print('Score model')
            gat.score(epochs)

            #output_file_name = 'gat_' + curr_patient + '_' + curr_block + '_' + curr_comparison_name + '_' + lock_to_word[0][comparison][0] + '_perm_' + str(perm) + '.pkl'
            output_file_name = 'gat_' + curr_patient + '_' + curr_block + '_' + curr_comparison_name + '_' + 'last' + '_perm_' + str(perm) + '.pkl'
            output_file_name = os.path.join('..', '..', 'Output', output_file_name)

            with open(output_file_name, 'wb') as output:
                #pickle.dump(info, output, pickle.HIGHEST_PROTOCOL)
                #pickle.dump(epochs, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(events, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(event_id, output, pickle.HIGHEST_PROTOCOL)
                pickle.dump(gat, output, pickle.HIGHEST_PROTOCOL)
