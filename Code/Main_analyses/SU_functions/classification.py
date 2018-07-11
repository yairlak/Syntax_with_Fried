import auxilary_functions
import os, pickle
import mne
import matplotlib.pyplot as plt
from mne.decoding import GeneralizingEstimator
from sklearn.svm import LinearSVC


def get_multichannel_epochs_for_all_current_conditions(comparison, settings, preferences):
    queries = auxilary_functions.get_queries(comparison)
    epochs_all_queries = []
    for q, query in enumerate(queries):
        for p, patient in enumerate(settings.patients):
            # High-gamma features
            for c, channel in enumerate(settings.channels):
                settings.channel = channel
                if preferences.analyze_micro_raw:
                    band = 'High-Gamma'
                    print('contrast: ' + comparison['contrast_name'] + '; ' + band + '; channel ' + str(channel) + '; ' + patient)

                    # channel_names = []; channel_info = []
                    # preferences.sort_according_to_key = [s.strip().encode('ascii') for s in comparison['sorting']]

                    file_name = 'Feature_matrix_' + band + '_' + patient + '_channel_' + str(
                        settings.channel) + '_' + query
                    with open(os.path.join(settings.path2output, patient, 'feature_matrix_for_classification',
                                               file_name + '.pkl'), 'rb') as f:
                        curr_data = pickle.load(f)
                        if c == 0 and p==0:
                            epochs_all_channels = curr_data[0]
                        else:
                            epochs_all_channels = mne.epochs.add_channels_epochs([epochs_all_channels, curr_data[0]])
            # Single-unit features
            if preferences.analyze_micro_single:
                print('contrast: ' + comparison['contrast_name'] + '; Single-units channel ' + str(channel) + '; ' + patient)
                file_name = 'Feature_matrix_rasters_' + settings.patient + '_' + query
                with open(os.path.join(settings.path2output, patient, 'feature_matrix_for_classification',
                                       file_name + '.pkl'), 'rb') as f:
                    curr_data = pickle.load(f)
                epochs_all_channels = mne.epochs.add_channels_epochs([epochs_all_channels, curr_data[0]])
        epochs_all_channels.events[:, 2] = q
        epochs_all_channels.event_id = {}
        epochs_all_channels.event_id[comparison['cond_labels'][q]] = q
        epochs_all_queries.append(epochs_all_channels)
    epochs_all_queries = mne.concatenate_epochs(epochs_all_queries)

    return epochs_all_queries


def plot_generalizing_estimator(epochs_all_queries, comparison, settings):
    train_times = {}
    train_times["start"] = -1.0
    train_times["stop"] = 1.05
    train_times["step"] = 0.01
    test_times = {}
    test_times["start"] = -1.0
    test_times["stop"] = 1.05
    test_times["step"] = 0.01
    time_gen = GeneralizingEstimator(base_estimator=LinearSVC(), scoring='roc_auc', n_jobs=-2)

    # fit and score
    time_gen.fit(X=epochs_all_queries.get_data(), y=epochs_all_queries.events[:, 2])

    # Score on the epochs where the stimulus was presented to the right.
    scores = time_gen.score(X=epochs_all_queries.get_data(), y=epochs_all_queries.events[:, 2])

    # Plot
    fig, ax = plt.subplots(1)
    im = ax.matshow(scores, vmin=0, vmax=1., cmap='RdBu_r', origin='lower',
                    extent=epochs_all_queries.times[[0, -1, 0, -1]])
    ax.axhline(0., color='k')
    ax.axvline(0., color='k')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlabel('Testing Time (s)')
    ax.set_ylabel('Training Time (s)')
    ax.set_title('Generalization across time and condition')
    plt.colorbar(im, ax=ax)

    file_name = comparison['contrast_name']
    plt.savefig(os.path.join(settings.path2figures, file_name + '.png'))