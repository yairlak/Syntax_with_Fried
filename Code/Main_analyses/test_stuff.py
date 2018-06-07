
import mne

# Load the data from the internet
path = mne.datasets.kiloword.data_path() + '/kword_metadata-epo.fif'
epochs = mne.read_epochs(path)

# The metadata exists as a Pandas DataFrame
print(epochs.metadata.head(10))
print(epochs.metadata.type())


###########################################################################

# mylist = ['a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e']
# key1 =   [3, 1, 3, 2, 1, 5, 2, 1, 4, 5]
# key2 =   [2, 2, 1, 2, 1, 2, 1, 1, 2, 1]
# mylist_tuple = [(i, j, k) for (i, j, k) in zip(mylist, key1, key2)]
# from operator import itemgetter
# # mylist_sorted = sorted(mylist, key=lambda x: (key2, key1))
# IX = [i[0] for i in sorted(mylist_tuple, key=itemgetter(1,2))]
# print(IX)
# mylist_sorted = sorted(mylist_tuple, key=itemgetter(1,2))
# print(mylist_sorted)


########################################################################
# import pickle
# from os import path as op
#
# file_name = 'word2POS.pkl'
# with open(op.join('..', '..', 'Paradigm', file_name), 'r') as f:
#     word2pos = pickle.load(f)
# print(word2pos)
#
# word2pos_simplified = {}
# for word, tag in word2pos.items():
#     if tag[0:2] == 'VB':
#         word2pos_simplified.update({word:'VB'})
#     else:
#         word2pos_simplified.update({word: tag})
# print(word2pos_simplified)
#
#
# file_name = 'word2POS_simplified.pkl'
# with open(op.join('..', '..', 'Paradigm', file_name), 'w') as f:
#      pickle.dump(word2pos_simplified, f)
#############################################################################

# from SU_functions import load_settings_params, load_data, read_logs_and_comparisons
# import numpy as np
# import nltk
# from os import path as op
#
# print('Loading settings, params and preferences...')
# settings = load_settings_params.Settings()
#
# _, features = read_logs_and_comparisons.load_comparisons_and_features(settings)
# stimuli = features['fields'][1][1::]
# trial_numbers = features['fields'][0][1::]
# IX_sort = np.argsort(trial_numbers)
# trial_numbers = trial_numbers[IX_sort]
# stimuli = stimuli[IX_sort]
# stimuli = [str(s) for s in stimuli]
# stimuli_tokenized = [s.split(" ") for s in stimuli]
# stimuli_POS = [nltk.pos_tag(s) for s in stimuli_tokenized]
# all_words = [w_POS[0] for s in stimuli_POS for w_POS in s]
# all_words = [w[0:-1].lower() if w[-1]=='.' or w[-1]=='?' else w.lower() for w in all_words]
# all_POS = [w_POS[1] for s in stimuli_POS for w_POS in s]
# POS = set(all_POS)
# lexicon = set(all_words)
# print(lexicon)
# word2POS = {}
# for word in lexicon:
#     IX = [i for i, w in enumerate(all_words) if word == w]
#     val = []
#     for ind in IX:
#         val.append(all_POS[ind])
#     word2POS.update({word:list(set(val))})
#
# file_name = 'word2POS.txt'
# with open(op.join('..', '..', 'Output', file_name), 'w') as f:
#     for key, value in word2POS.items():
#         f.write("%s, %s\n" % (key, value))
#
# print(word2POS)
# print(all_POS)
#
# file_name = 'word2POS _corrected.txt'
# with open(op.join('..', '..', 'Output', file_name), 'r') as f:
#     word2POS_corrected = f.readlines()
#
# word2POS = {}
# for pair in word2POS_corrected:
#     word, tag = pair.rsplit(', ')
#     pos_tag = tag.split('\'')[1]
#     word2POS.update({word: pos_tag})
# print(word2POS)
#
# import pickle
# file_name = 'word2POS.pkl'
# with open(op.join('..', '..', 'Paradigm', file_name), 'w') as f:
#     pickle.dump(word2POS, f)
#

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
# # Display spikes waveforms
# filename = '/home/yl254115/Projects/single_unit_syntax/Data/UCLA/patient_480/ChannelsCSC/times_CSC28.mat'
#
# data = sio.loadmat(filename)
#
# IX = data['cluster_class'][:, 0]
# IX = np.asarray(np.where(IX == 1))[0]
# spike_waveforms_cluster_1 = data['spikes'][IX, :]
#
# plt.plot(np.transpose(spike_waveforms_cluster_1), color='k', linewidth=0.1)
# plt.ylim([-500, 500])
# plt.title('Channel 28, Cluster 1 (' + str(spike_waveforms_cluster_1.shape[0]) + ' spikes)')
# plt.xlabel('Time')
# # fig, ax = plt.subplot(111)
# # ax.plot(spike_waveforms_cluster_1)
# # plt.show()
# plt.savefig('/home/yl254115/Projects/single_unit_syntax/Figures/Patient480_channel_28_cluster_1.png')
