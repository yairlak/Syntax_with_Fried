import os, pickle
import mne
import matplotlib.pyplot as plt
import numpy as np
plt.switch_backend('agg')


def prepare_data_for_GAT(patients, picks_all_patients, query_classes_train, query_classes_test, root_path, epochs_fname = '-epo.fif'):
    # Times
    train_times = {}
    train_times["start"] = -0.5
    train_times["stop"] = 0.9
    train_times["step"] = 0.01

    X_train = []; y_train = []; X_test = []; y_test = []
    for patient, picks in zip(patients, picks_all_patients):
        print('Loading epochs object', patient)
        epochs_fname = patient + epochs_fname
        epochs = mne.read_epochs(os.path.join(root_path, 'Data', patient, 'Epochs', epochs_fname))
        
        # Train set
        for q, query_class_train in enumerate(query_classes_train):
            epochs_class_train = epochs[query_class_train]
            epochs_class_train.crop(train_times["start"], train_times["stop"])
            #epochs_class1_train.decimate(decim=10)
            X_train.append(epochs_class_train.get_data())  # signals: n_epochs, n_channels, n_times
            num_samples_curr_class = X_train[q].shape[0]
            y_train.append((q+1) * np.ones(num_samples_curr_class).astype(int))  # targets
            print('Number of samples in training class %i : %i' % (q+1, num_samples_curr_class))

        # Test set
        if query_classes_test is not None:
            for q, query_class_test in enumerate(query_classes_test):
                epochs_class_test = epochs[query_class_test]
                epochs_class_test.crop(train_times["start"], train_times["stop"])
                #epochs_class1_test.decimate(decim=10)
                X_test.append(epochs_class_test.get_data())  # signals: n_epochs, n_channels, n_times
                num_samples_curr_class = X_test[q].shape[0]
                y_test.append((q+1) * np.ones(num_samples_curr_class).astype(int))  # targets
                print('Number of samples in test class %i : %i' % (q+1, num_samples_curr_class))
            X_test = np.vstack(X_test)
            y_test = np.hstack(y_test)
        else: # no test queries (generalization across time only, not conditions)
            X_test = None; y_test = None

    return epochs_class_train[0].times, np.vstack(X_train), np.hstack(y_train), X_test, y_test


def train_test_GAT(X_train, y_train, X_test, y_test):
    from sklearn.svm import LinearSVC
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from mne.decoding import (GeneralizingEstimator, Scaler, cross_val_multiscore, LinearModel, get_coef, Vectorizer)

    # Define a classifier for GAT
    #clf = make_pipeline(StandardScaler(), LinearSVC())
    clf = make_pipeline(StandardScaler(), LinearModel(LogisticRegression(solver='lbfgs')))
    # Define the Temporal Generalization object
    time_gen = GeneralizingEstimator(clf, n_jobs=-2, scoring='roc_auc', verbose=True)
    # Fit model
    if (X_test is not None) and (y_test is not None): # Generalization across conditions 
        #print(X_train, y_train, X_test, y_test)
        #print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
        time_gen.fit(X_train, y_train)
        scores = time_gen.score(X_test, y_test)
        scores = np.expand_dims(scores, axis=0) # For later compatability (plot_GAT() np.mean(scores, axis=0))
        #print(scores)
    else: # Generlization across time only (not across conditions or modalities)
        scores = cross_val_multiscore(time_gen, X_train, y_train, cv=5, n_jobs=-1)

    return time_gen, scores


def plot_GAT(times, time_gen, scores):
    # Plot the diagonal
    # Mean scores across cross-validation splits
    scores = np.mean(scores, axis=0)
    fig1, ax = plt.subplots()
    ax.plot(times, np.diag(scores), label='score')
    ax.axhline(.5, color='k', linestyle='--', label='chance')
    ax.set_xlabel('Times')
    ax.set_ylabel('AUC')
    ax.legend()
    ax.axhline(.5, color='k', linestyle='--', label='chance')
    ax.set_xlabel('Times')
    ax.set_ylabel('AUC')
    ax.legend()
    ax.axvline(.0, color='k', linestyle='-')
    ax.set_title('Decoding over time')

    # Plot the full GAT matrix
    fig2, ax = plt.subplots(1, 1)
    im = ax.imshow(scores, interpolation='lanczos', origin='lower', cmap='RdBu_r',
                   extent=times[[0, -1, 0, -1]])#, vmin=0., vmax=1.)
    ax.set_xlabel('Testing Time (s)')
    ax.set_ylabel('Training Time (s)')
    ax.set_title('Temporal Generalization')
    ax.axvline(0, color='k')
    ax.axhline(0, color='k')
    plt.colorbar(im, ax=ax)

    return fig1, fig2

    # file_name = 'GeneralizingEstimatorAcrossModalities_' + str(comp) + '_' + comparison[
    #     'contrast_name'] + '_' + '_'.join(settings.patients) + '_generalize_' + comparison_to_generalize[
    #                 'contrast_name']
    # plt.savefig(os.path.join(settings.path2figures, 'Decoding', file_name + '.png'))
    # plt.close()
    # print('Saved to: ' + os.path.join(settings.path2figures, 'Decoding', file_name + '.png'))

#     def get_multichannel_epochs_for_all_current_conditions(comparison, queries, settings, preferences):
#     epochs_all_queries = []
#     for q, query in enumerate(queries):
#         for p, patient in enumerate(settings.patients):
#             # High-gamma features
#             for c, channel in enumerate(settings.channels[p]):
#                 settings.channel = channel
#                 if preferences.analyze_micro_raw:
#                     band = 'High-Gamma'
#                     print('contrast: ' + comparison['contrast_name'] + '; ' + band + '; channel ' + str(channel) + '; ' + patient)
#                     file_name = 'Feature_matrix_' + band + '_' + patient + '_channel_' + str(
#                         settings.channel) + '_' + query
#                     with open(os.path.join(settings.path2output, patient, 'feature_matrix_for_classification',
#                                                file_name + '.pkl'), 'rb') as f:
#                         curr_data = pickle.load(f)
#                         #print(curr_data[0].events.shape[0])
#                         if c == 0 and p==0:
#                             epochs_all_channels = curr_data[0]
#                             events_shared_for_all_patients = curr_data[0].events
#                             #info_shared_for_all_channels
#
#                             # collect stimuli info
#                             stimuli_of_curr_query = []
#                             label_cond = comparison['cond_labels'][q]
#                             file_name_root = band + '_' + patient + '_Blocks_' + comparison['blocks'] + '_' + label_cond + '_' + comparison['align_to']
#                             with open(os.path.join(settings.path2output, settings.patient, 'HighGamma', file_name_root + '.txt'), 'r') as f:
#                                 stimuli_of_curr_query.append(f.readlines())
#                         else:
#                             curr_data[0].events = events_shared_for_all_patients
#                             epochs_all_channels = mne.epochs.add_channels_epochs([epochs_all_channels, curr_data[0]])
#             # Single-unit features
#             if preferences.analyze_micro_single:
#                 print('contrast: ' + comparison['contrast_name'] + '; Single-units channel ' + str(channel) + '; ' + patient)
#                 file_name = 'Feature_matrix_rasters_' + settings.patient + '_' + query
#                 with open(os.path.join(settings.path2output, patient, 'feature_matrix_for_classification',
#                                        file_name + '.pkl'), 'rb') as f:
#                     curr_data = pickle.load(f)
#                 epochs_all_channels = mne.epochs.add_channels_epochs([epochs_all_channels, curr_data[0]])
#         epochs_all_channels.events[:, 2] = q
#         epochs_all_channels.event_id = {}
#         epochs_all_channels.event_id[comparison['cond_labels'][q]] = q
#         epochs_all_queries.append(epochs_all_channels)
#         print(stimuli_of_curr_query)
#
#     epochs_all_queries = mne.concatenate_epochs(epochs_all_queries)
#     print(epochs_all_queries)
#
#     return epochs_all_queries, stimuli_of_curr_query
#
#
# def get_multichannel_epochs_for_all_current_conditions_from_all_trials(comparison, queries, settings, preferences):
#     epochs_all_queries = []
#     for q, query in enumerate(queries):
#         for p, patient in enumerate(settings.patients):
#             # High-gamma features
#             for c, channel in enumerate(settings.channels[p]):
#                 settings.channel = channel
#                 if preferences.analyze_micro_raw:
#                     band = 'High-Gamma'
#                     print('contrast: ' + comparison['contrast_name'] + '; ' + band + '; channel ' + str(channel) + '; ' + patient)
#                     file_name = 'Feature_matrix_' + band + '_' + patient + '_channel_' + str(
#                         settings.channel) + '_' + 'All_trials' #ALL_TRIALS
#                     # file_name = 'Feature_matrix_' + band + '_' + patient + '_channel_' + str(
#                     #     settings.channel) + '_' + query
#                     with open(os.path.join(settings.path2output, patient, 'feature_matrix_for_classification',
#                                                file_name + '.pkl'), 'rb') as f:
#                         curr_data = pickle.load(f)
#                         #print(curr_data[0].events.shape[0])
#                         if c == 0 and p==0: # initialize epochs and events objects at the first patient-channel
#
#                             # ---- generate the epochs object -----
#                             # 1. Get query
#                             # 2. Extract reduced epochs object based on query
#                             # 3. Get shared events for all patients
#                             # 4. Extract sentence/word stimuli
#
#
#                             #epochs_all_channels = curr_data[0]
#                             #events_shared_for_all_patients = curr_data[0].events
#                             #info_shared_for_all_channels
#
#                             # collect stimuli info
#                             stimuli_of_curr_query = []
#                             label_cond = comparison['cond_labels'][q]
#                             file_name_root = band + '_' + patient + '_Blocks_' + comparison['blocks'] + '_' + label_cond + '_' + comparison['align_to']
#                             with open(os.path.join(settings.path2output, settings.patient, 'HighGamma', file_name_root + '.txt'), 'r') as f:
#                                 stimuli_of_curr_query.append(f.readlines())
#                         else:
#                             #curr_data[0].events = events_shared_for_all_patients
#                             epochs_all_channels = mne.epochs.add_channels_epochs([epochs_all_channels, curr_data[0]])
#             # Single-unit features
#             if preferences.analyze_micro_single:
#                 print('contrast: ' + comparison['contrast_name'] + '; Single-units channel ' + str(channel) + '; ' + patient)
#                 file_name = 'Feature_matrix_rasters_' + settings.patient + '_' + query
#                 with open(os.path.join(settings.path2output, patient, 'feature_matrix_for_classification',
#                                        file_name + '.pkl'), 'rb') as f:
#                     curr_data = pickle.load(f)
#                 epochs_all_channels = mne.epochs.add_channels_epochs([epochs_all_channels, curr_data[0]])
#         epochs_all_channels.events[:, 2] = q
#         epochs_all_channels.event_id = {}
#         epochs_all_channels.event_id[comparison['cond_labels'][q]] = q
#         epochs_all_queries.append(epochs_all_channels)
#         print(stimuli_of_curr_query)
#
#     epochs_all_queries = mne.concatenate_epochs(epochs_all_queries)
#     print(epochs_all_queries)
#
#     return epochs_all_queries, stimuli_of_curr_query
#
#
# def plot_generalizing_estimator(epochs_all_queries, comparison, comp, settings):
#     train_times = {}
#     train_times["start"] = -2.5
#     train_times["stop"] = 2.5
#     train_times["step"] = 0.01
#     # test_times = {}
#     # test_times["start"] = -1.0
#     # test_times["stop"] = 1.05
#     # test_times["step"] = 0.01
#
#     epochs_all_queries.crop(train_times["start"], train_times["stop"])
#     epochs_all_queries.decimate(decim=10)
#
#     X = epochs_all_queries.get_data()  # MEG signals: n_epochs, n_channels, n_times
#     y = epochs_all_queries.events[:, 2]  # target: Audio left or right
#
#     # Define a classifier for GAT
#     clf = make_pipeline(StandardScaler(), LinearSVC())
#     # Define the Temporal Generalization object
#     time_gen = GeneralizingEstimator(clf, n_jobs=-2, scoring='roc_auc')
#     # Score CV
#     scores = cross_val_multiscore(time_gen, X, y, cv=5, n_jobs=-2)
#     # Mean scores across cross-validation splits
#     scores = np.mean(scores, axis=0)
#
#     # Plot the diagonal
#     fig, ax = plt.subplots()
#     ax.plot(epochs_all_queries.times, np.diag(scores), label='score')
#     ax.axhline(.5, color='k', linestyle='--', label='chance')
#     ax.set_xlabel('Times')
#     ax.set_ylabel('AUC')
#     ax.legend()
#     ax.axvline(.0, color='k', linestyle='-')
#     ax.set_title('Decoding over time')
#
#     file_name = 'SlidingEstimator_' + str(comp) + '_' + comparison['contrast_name'] + '_' + '_'.join(settings.patients)+comparison['align_to']
#     plt.savefig(os.path.join(settings.path2figures, 'Decoding', file_name + '.png'))
#     plt.close()
#     print('Saved to: ' + os.path.join(settings.path2figures, 'Decoding', file_name + '.png'))
#
#     # Plot the full GAT matrix
#     fig, ax = plt.subplots(1, 1)
#     im = ax.imshow(scores, interpolation='lanczos', origin='lower', cmap='RdBu_r',
#                    extent=epochs_all_queries.times[[0, -1, 0, -1]], vmin=0., vmax=1.)
#     ax.set_xlabel('Testing Time (s)')
#     ax.set_ylabel('Training Time (s)')
#     ax.set_title('Temporal Generalization')
#     ax.axvline(0, color='k')
#     ax.axhline(0, color='k')
#     plt.colorbar(im, ax=ax)
#
#     file_name = 'GeneralizingEstimator_' + str(comp) + '_' + comparison['contrast_name'] + '_' + '_'.join(settings.patients)+comparison['align_to']
#     plt.savefig(os.path.join(settings.path2figures, 'Decoding', file_name + '.png'))
#     plt.close()
#     print('Saved to: ' + os.path.join(settings.path2figures, 'Decoding', file_name + '.png'))
#
#
# def plot_generalizing_estimator_across_modalities(epochs_all_queries, epochs_all_queries_to_generalize, comparison, comparison_to_generalize, comp, settings):
#     train_times = {}
#     train_times["start"] = -2.5
#     train_times["stop"] = 2.5
#     train_times["step"] = 0.01
#
#     epochs_all_queries.crop(train_times["start"], train_times["stop"])
#     epochs_all_queries.decimate(decim=10)
#     epochs_all_queries_to_generalize.crop(train_times["start"], train_times["stop"])
#     epochs_all_queries_to_generalize.decimate(decim=10)
#
#     X = epochs_all_queries.get_data()  # MEG signals: n_epochs, n_channels, n_times
#     y = epochs_all_queries.events[:, 2]  # target: Audio left or right
#
#     # Define a classifier for GAT
#     clf = make_pipeline(StandardScaler(), LinearSVC())
#     # Define the Temporal Generalization object
#     time_gen = GeneralizingEstimator(clf, n_jobs=-2, scoring='roc_auc')
#     # Fit model
#     time_gen.fit(X, y)
#     # Score on other modality
#     X = epochs_all_queries_to_generalize.get_data()  # MEG signals: n_epochs, n_channels, n_times
#     y = epochs_all_queries_to_generalize.events[:, 2]  # target: Audio left or right
#     scores = time_gen.score(X, y)
#
#
#     # Plot the diagonal
#     fig, ax = plt.subplots()
#     ax.plot(epochs_all_queries.times, np.diag(scores), label='score')
#     ax.axhline(.5, color='k', linestyle='--', label='chance')
#     ax.set_xlabel('Times')
#     ax.set_ylabel('AUC')
#     ax.legend()
#     ax.axvline(.0, color='k', linestyle='-')
#     ax.set_title('Decoding over time')
#
#     file_name = 'SlidingEstimatorAcrossModalities_' + str(comp) + '_' + comparison['contrast_name'] + '_' + '_'.join(settings.patients) + '_generalize_' + comparison_to_generalize['contrast_name']
#     plt.savefig(os.path.join(settings.path2figures, 'Decoding', file_name + '.png'))
#     plt.close()
#     print('Saved to: ' + os.path.join(settings.path2figures, 'Decoding', file_name + '.png'))
#
#     # Plot the full GAT matrix
#     fig, ax = plt.subplots(1, 1)
#     im = ax.imshow(scores, interpolation='lanczos', origin='lower', cmap='RdBu_r',
#                    extent=epochs_all_queries.times[[0, -1, 0, -1]], vmin=0., vmax=1.)
#     ax.set_xlabel('Testing Time (s)')
#     ax.set_ylabel('Training Time (s)')
#     ax.set_title('Temporal Generalization')
#     ax.axvline(0, color='k')
#     ax.axhline(0, color='k')
#     plt.colorbar(im, ax=ax)
#
