import os, glob
import numpy as np
import scipy
import scipy.io as sio
import mne
from mne.decoding import GeneralizationAcrossTime
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
import pickle
import shelve
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

def generate_PSTH_and_save(epochs, events, which_event, unt):
    # which_event is either 1 or two
    # PLOT PSTH
    epochs_data = epochs.get_data()
    channel_to_plot = epochs_data[:, unt, :]
    channel_to_plot = channel_to_plot[events[:, 2] == which_event, :]
    channel_to_plot = channel_to_plot.mean(axis=0)
    PSTH = []
    timepoints = range(0, len(channel_to_plot), 100)
    for i in timepoints:
        PSTH.append(np.sum(channel_to_plot[i:i+99]))
    PSTH = np.array(PSTH)
    # Normalize PSTH if Gaussian kernel is not normalized
    #PSTH = PSTH/(100*(2*3.14159)**0.5)
    # fig, ax = plt.subplots()
    plt.bar(-100 + np.array(timepoints), PSTH/0.1, width=100, color="blue")
    # rects1 = ax.bar(-100 + np.array(timepoints), PSTH*10, width=100, color='b')
    ax = plt.gca()
    ax.set_xlabel('Time [ms]')
    ax.set_ylabel('Spikes/sec')
    ax.set_ylim([0, 20])

    # plt.show()
    fig = plt.gcf()
    return fig, ax

# Load data and raw object
curr_patient = 'patient_479'
curr_run = 'sentences'
blocks = range(1,3,1)
blocks_str = ''.join(str(x) for x in blocks)

file_name = os.path.join('..', '..', 'Output', 'raw_data_with_events_to_python_all_comparisons_' + curr_patient + '_' + curr_run + '_blocks_' + blocks_str + '.mat')
mat = sio.loadmat(file_name)

# Generate unit names (unique)
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
print('Loading data...')
custom_raw_data = mat['custom_raw_smoothed']
raw = mne.io.RawArray(custom_raw_data, info)

print('Loop over all comparisons:')
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

    # Create Epochs object
    picks = range(0, 2)
    decim = 20  # decimate to make the example faster to run
    epochs = mne.Epochs(raw, events, event_id, -3, 3, proj=True,
                        baseline=None, preload=True, verbose=False, decim=decim, picks=picks)

    print(epochs)
    
    # Genereate PSTH
    generate_PSTH = False
    if generate_PSTH:
        for unit in epochs.picks:
            for evnt in range(0, 2):
                fig_PSTH, ax = generate_PSTH_and_save(epochs, events, evnt, unit)
                fig_PSTH_file_name = []
                for k, val in event_id.iteritems():
                    if val == evnt:
                        fig_PSTH_file_name = 'PSTH_unit_' + str(unit+1) + '_event_' + k + '.png'
                ax.set_title('Unit ' + str(unit+1) + ' Event' + k)
                fig_PSTH.savefig(os.path.join('figures_PSTH', fig_PSTH_file_name))
                plt.close(fig_PSTH)

    # epochs[0].average().plot()
    #train_times = {}
    #train_times["start"] = -1.0
    #train_times["stop"] = 1.05
    #train_times["step"] = 0.05
    #test_times = {}
    #test_times["start"] = -1.0
    #test_times["stop"] = 1.05
    #test_times["step"] = 0.05

    if len(event_id) > 1:

        # Define decoder. The decision function is employed to use cross-validation
        gat = GeneralizationAcrossTime(clf=LinearSVC(), predict_mode='cross-validation', n_jobs=30)
        #gat = GeneralizationAcrossTime(clf=LinearSVC(), train_times=train_times, test_times=test_times,
         #                              predict_mode='cross-validation', n_jobs=30)
        # fit and score
        print('Fit model')
        gat.fit(epochs)
        print('Score model')
        gat.score(epochs)

        #filename = os.path.join('..', 'Output', 'gat_' + curr_patient + '_' + curr_block + '_' + curr_comparison_name + '.pickle')
        #with open(filename, 'w') as f:
         #   pickle.dump([gat], f)
	
	#my_shelf = shelve.open(filename,'n') # 'n' for new
	#for key in dir():
	 #   try:
	  #      my_shelf[key] = globals()[key]
           # except TypeError:
        	#
	        # __builtins__, my_shelf, and imported modules can not be shelved.
	        #
            #	print('ERROR shelving: {0}'.format(key))
	#my_shelf.close()

        # Plot and save results
        fig_gat, ax = plt.subplots(1, 1)
        # Define time limits
        tn_times = gat.train_times_['times']
        tt_times = gat.test_times_['times']
        tlim = [tt_times[0][0], tt_times[-1][-1], tn_times[0], tn_times[-1]]
        # Plot scores
        im = ax.imshow(gat.scores_, interpolation='nearest', origin='lower',
                       extent=tlim)
        ax.set_xlabel('Testing Time (s)')
        ax.set_ylabel('Training Time (s)')
        ax.set_title(curr_comparison_name)
        ax.axvline(0, color='k')
        ax.axhline(0, color='k')
        ax.set_xlim(tlim[:2])
        ax.set_ylim(tlim[2:])
        plt.colorbar(im, ax=ax)
        fig_file_name = 'gat_' + curr_patient+ '_' + curr_run + '_' + curr_comparison_name + '_blocks_' + blocks_str +  '_last' + '.png'
        fig_gat.savefig(os.path.join('..', '..', 'Figures', 'GAT', fig_file_name))
        plt.close(fig_gat)



        # Get scores from identical training and testing times even if GAT
        # is not square.
        fig_diag, ax_diag = plt.subplots(1, 1)
        scores = np.zeros(len(gat.scores_))
        for train_idx, train_time in enumerate(gat.train_times_['times']):
            for test_times in gat.test_times_['times']:
                # find closest testing time from train_time
                lag = test_times - train_time
                test_idx = np.abs(lag).argmin()
                # check that not more than 1 classifier away
                if np.abs(lag[test_idx]) > gat.train_times_['step']:
                    score = np.nan
                else:
                    score = gat.scores_[train_idx][test_idx]
                scores[train_idx] = score
        # kwargs = dict()
        # if color is not None:
        #     kwargs['color'] = color
        kwargs = dict()
        label='Classif. score'
        ax_diag.plot(gat.train_times_['times'], scores, label=str(label), **kwargs)
        chance = True
        if chance is True:
                chance = _get_chance_level(gat.scorer_, gat.y_train_)
        chance = float(chance)
        if np.isfinite(chance):  # don't plot nan chance level
            ax_diag.axhline(chance, color='k', linestyle='--',
                       label="Chance level")
        ax_diag.axvline(0, color='k', label='')
        ax_diag.set_title(curr_comparison_name)
        ax_diag.set_xlabel('Time (s)')
        ax_diag.set_ylabel('Classif. score ({0})'.format('AUC' if 'roc' in repr(gat.scorer_) else r'%'))
        ax_diag.legend(loc='best')

        fig_diag_file_name = 'gat_diag_' + curr_patient+ '_' + curr_run + '_' + curr_comparison_name + '_blocks_' + blocks_str + '_last' + '.png'
        fig_diag.savefig(os.path.join('..', '..', 'Figures', 'GAT', fig_diag_file_name))
        plt.close(fig_diag)


        # Save workspace to drive:
