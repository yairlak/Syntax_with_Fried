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


from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, convert_to_mne, analyses_single_unit
from scipy import io
import os, glob
import mne
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
from mne.decoding import GeneralizingEstimator
from sklearn.svm import LinearSVC
import sys
import pickle

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# channels_micro = range(1,7,1)
# channels_macro = range(1,2,1)
train_times = {}
train_times["start"] = -1.0
train_times["stop"] = 1.05
train_times["step"] = 0.01
test_times = {}
test_times["start"] = -1.0
test_times["stop"] = 1.05
test_times["step"] = 0.01

band = 'High-Gamma'

# ------------ START MAIN --------------
print('Loading settings, params and preferences...')
settings = load_settings_params.Settings()
params = load_settings_params.Params()
preferences = load_settings_params.Preferences()

print('Metadata: Loading features and comparisons from Excel files...')
comparison_list, features = read_logs_and_comparisons.load_comparisons_and_features(settings)
comparisons = read_logs_and_comparisons.extract_comparison(comparison_list, features, settings, preferences)

print('Loop over all comparisons: prepare & save data for classification')
for comparison in comparisons:
    contrast_name = comparison[2]
    print(contrast_name)
    if preferences.run_contrasts:
        file_name = 'Feature_matrix_' + band + '_' + settings.patient + '_' + contrast_name + '_' + comparison[
            1] + '_blocks_' + str(settings.blocks)
    elif preferences.run_POS:
        file_name = 'Feature_matrix_' + band + '_' + settings.patient + '_POS_blocks_' + str(settings.blocks)

    print('Loading feature matrix')
    with open(os.path.join(settings.path2output, settings.patient, 'feature_matrix_for_classification',
                           file_name + '.pkl'), 'rb') as f:
        epochs_all_channels = pickle.load(f)
    print(epochs_all_channels)
    # epochs_all_channels.decim = 100

    # gat = GeneralizationAcrossTime(clf=LinearSVC(), predict_mode='cross-validation', n_jobs=30)
    print('Define GAT model..')
    gat = GeneralizationAcrossTime(clf=LinearSVC(), scorer = 'roc_auc', train_times=train_times, test_times=test_times,
                                 predict_mode='cross-validation', n_jobs=4)

    class_1 = []; class_2 = [] 
    if preferences.run_POS:
	epochs_all_channels = epochs_all_channels['NN_block_1', 'NN_block_3', 'NN_block_5', 'VB_block_1', 'VB_block_3', 'VB_block_5']
        print(epochs_all_channels)
	class_1 = [100, 200, 300]
        class_2 = [101, 201, 301]
	for rw in range(epochs_all_channels.events.shape[0]):
            if epochs_all_channels.events[rw, 2] in class_1:
                epochs_all_channels.events[rw, 2] = 1
            if epochs_all_channels.events[rw, 2] in class_2:
                epochs_all_channels.events[rw, 2] = 2
    elif preferences.run_contrasts:
        for key, value in epochs_all_channels.event_id.items():
            if value % 100 == 0:
                class_1.append(value)
            elif value % 100 == 1:
                class_2.append(value)
        for rw in range(epochs_all_channels.events.shape[0]):
            if epochs_all_channels.events[rw, 2] in class_1:
                epochs_all_channels.events[rw, 2] = 1
            if epochs_all_channels.events[rw, 2] in class_2:
                epochs_all_channels.events[rw, 2] = 2

    print(epochs_all_channels.events)
    # fit and score
    print('Fit model')
    gat.fit(epochs_all_channels)
    print('Score model')
    y = gat.y_train_; y[y==1] = False; y[y==2] = True # if scorer='roc_auc' transform to binary
    gat.score(epochs_all_channels, y)

    fig_gat, ax = plt.subplots(1, 1)
    # Define time limits
    tn_times = gat.train_times_['times']
    tt_times = gat.test_times_['times']
    tlim = [tt_times[0][0], tt_times[-1][-1], tn_times[0], tn_times[-1]]
    # Plot scores
    im = ax.imshow(gat.scores_, interpolation='nearest', origin='lower', extent=tlim)
    ax.set_xlabel('Testing Time (s)')
    ax.set_ylabel('Training Time (s)')
    ax.set_title('Contrast: ' + contrast_name)
    ax.axvline(0, color='k')
    ax.axhline(0, color='k')
    ax.set_xlim(tlim[:2])
    ax.set_ylim(tlim[2:])
    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('AUC', rotation=270, fontsize=20, labelpad=25)

    fig_file_name = 'GAT_' + band + '_' + settings.patient + '_' + contrast_name + '_' + comparison[1] + '.png' # + curr_patient + '_' + curr_run + '_' + curr_comparison_name + '_blocks_' + blocks_str + '_last' + '.png'
    fig_gat.savefig(os.path.join(settings.path2figures, settings.patient, 'GAT', fig_file_name))
    plt.close(fig_gat)


    # Get scores from identical training and testing times even if GAT
    # is not square.
    fig_diag, ax_diag = plt.subplots(1, 1)
    scores = np.zeros(len(gat.scores_))
    for train_idx, train_time in enumerate(gat.train_times_['times']):
        for test_time in gat.test_times_['times']:
            # find closest testing time from train_time
            lag = test_time - train_time
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
    ax_diag.set_title(contrast_name)
    ax_diag.set_xlabel('Time (s)')
    ax_diag.set_ylabel('Classif. score ({0})'.format('AUC' if 'roc' in repr(gat.scorer_) else r'%'))
    ax_diag.legend(loc='best')

    fig_diag_file_name = 'gat_diag_' + settings.patient + '_' + contrast_name + '_' + comparison[1] + '.png'
    fig_diag.savefig(os.path.join(settings.path2figures, settings.patient, 'GAT', fig_diag_file_name))
    plt.close(fig_diag)

    if preferences.run_POS: break 
