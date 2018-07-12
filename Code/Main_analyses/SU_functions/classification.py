import auxilary_functions
import os, pickle
import mne
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from mne.decoding import (SlidingEstimator, GeneralizingEstimator,
                          cross_val_multiscore, LinearModel, get_coef)
import numpy as np

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

    epochs_all_queries.crop(train_times["start"], train_times["stop"])
    epochs_all_queries.decimate(decim=10)

    X = epochs_all_queries.get_data()  # MEG signals: n_epochs, n_channels, n_times
    y = epochs_all_queries.events[:, 2]  # target: Audio left or right

    # Define a classifier for GAT
    clf = make_pipeline(StandardScaler(), LinearSVC())
    # Define the Temporal Generalization object
    time_gen = GeneralizingEstimator(clf, n_jobs=-2, scoring='roc_auc')
    # Score CV
    scores = cross_val_multiscore(time_gen, X, y, cv=5, n_jobs=-2)
    # Mean scores across cross-validation splits
    scores = np.mean(scores, axis=0)

    # Plot the diagonal
    fig, ax = plt.subplots()
    ax.plot(epochs_all_queries.times, np.diag(scores), label='score')
    ax.axhline(.5, color='k', linestyle='--', label='chance')
    ax.set_xlabel('Times')
    ax.set_ylabel('AUC')
    ax.legend()
    ax.axvline(.0, color='k', linestyle='-')
    ax.set_title('Decoding over time')

    file_name = 'SlidingEstimator_' + comparison['contrast_name']
    plt.savefig(os.path.join(settings.path2figures, file_name + '.png'))
    plt.close()

    # Plot the full GAT matrix
    fig, ax = plt.subplots(1, 1)
    im = ax.imshow(scores, interpolation='lanczos', origin='lower', cmap='RdBu_r',
                   extent=epochs_all_queries.times[[0, -1, 0, -1]], vmin=0., vmax=1.)
    ax.set_xlabel('Testing Time (s)')
    ax.set_ylabel('Training Time (s)')
    ax.set_title('Temporal Generalization')
    ax.axvline(0, color='k')
    ax.axhline(0, color='k')
    plt.colorbar(im, ax=ax)

    file_name = 'GeneralizingEstimator_' + comparison['contrast_name']
    plt.savefig(os.path.join(settings.path2figures, file_name + '.png'))
    plt.close()