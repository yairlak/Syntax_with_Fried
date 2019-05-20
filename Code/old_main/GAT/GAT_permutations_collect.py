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

def _get_chance_level(scorer, y_train):
    """Get the chance level."""
    # XXX JRK This should probably be solved within sklearn?
    if scorer.__name__ == 'accuracy_score':
        chance = np.max([np.mean(y_train == c) for c in np.unique(y_train)])
    elif scorer.__name__ == 'roc_auc_score':
        chance = 0.5
    else:
        chance = np.nan
        warn('Cannot find chance level from %s, specify chance level'
             % scorer.__name__)
    return chance

# Load data and raw object
num_perm = 100

curr_patient = 'En_02'
curr_block = 'sentences'
file_name = os.path.join('..', '..', 'Output', 'raw_data_with_events_to_python_all_comparisons_' + curr_patient + '_' + curr_block + '.mat')
mat = sio.loadmat(file_name)

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

for comparison, _ in enumerate(mat['custom_events_all_comparisons'][0]):
    print(comparison)
    curr_comparison_name = mat['comparison_name'][0, comparison][0]
    max_cluster_lengths = []
    for perm in range(0, num_perm, 1):

        #output_file_name = 'gat_' + curr_patient + '_' + curr_block + '_' + curr_comparison_name + '_' + lock_to_word[0][comparison][0] + '_perm_' + str(perm) + '.pkl'
        output_file_name = 'gat_' + curr_patient + '_' + curr_block + '_' + curr_comparison_name + '_' + 'last' + '_perm_' + str(perm) + '.pkl'
        output_file_name = os.path.join('..', '..', 'Output', output_file_name)

        with open(output_file_name, 'rb') as input:
            events = pickle.load(input)
            event_id = pickle.load(input)
            gat = pickle.load(input)

            accuracy_threshold = _get_chance_level(gat.scorer_, gat.y_train_)
            diag_val = gat.scores_.diagonal()
            IX = diag_val>accuracy_threshold

            max_cluster = 0
            cnt = 0
            for i in range(len(IX)):
                if IX[i] == 1:
                    cnt += 1
                else:
                    cnt = 0
                if cnt > max_cluster:
                    max_cluster = cnt

            max_cluster_lengths.append(max_cluster)
    cluster_length_hist, bin_edges = np.histogram(max_cluster_lengths, range(0, len(IX), 1))
    plt.hist(max_cluster_lengths)
    #fig_file_name = 'HistClusterLength_' + curr_patient + '_' + curr_block + '_' + curr_comparison_name + '_' + lock_to_word[0][comparison][0] + '.png'
    fig_file_name = 'HistClusterLength_' + curr_patient + '_' + curr_block + '_' + curr_comparison_name + '_' + 'last' + '.png'
    plt.savefig(os.path.join('..', '..', 'Figures', 'figures_GAT', fig_file_name))
    plt.close()

#    output_file_name = 'Hists_Cluster_Length_' + curr_patient + '_' + curr_block + '_' + curr_comparison_name + '_' + lock_to_word[0][comparison][0] + '.pkl'
    output_file_name = 'Hists_Cluster_Length_' + curr_patient + '_' + curr_block + '_' + curr_comparison_name + '_' + 'last' + '.pkl'
    output_file_name = os.path.join('..', '..', 'Output', output_file_name)

    with open(output_file_name, 'wb') as output:
         pickle.dump(cluster_length_hist, output, pickle.HIGHEST_PROTOCOL)
