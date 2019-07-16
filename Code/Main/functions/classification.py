import sys, os, pickle
import mne
import matplotlib.pyplot as plt
import numpy as np
plt.switch_backend('agg')


def prepare_data_for_GAT(args):
    '''

    :param patients: (list) 
    :param hospitals: (list) same len as patients
    :param picks_all_patients: (list of channel numbers or 'all') same len as patients
    :param query_classes_train: (list of len 2) two queries for the two classes (if no test queries then 5-fold CV is used)
    :param query_classes_test: (optional - list of len 2) two queries for the two test classes.
    :param root_path:
    :param k: (scalar) number of subsequent time points to cat
    :return:
    1. times
    2. X_train_query
    3. y_train_query
    4. X_test_query
    5. y_test_query
    '''
    patients = args.patients; hospitals=args.hospitals
    picks_micro=args.picks_micro; picks_macro=args.picks_macro; picks_spike=args.picks_spike
    query_classes_train=args.query_classes_train; query_classes_test=args.query_classes_test; 
    root_path=args.root_path
    k=args.k

    # Times
    train_times = {}
    train_times["start"] = -0.1
    train_times["stop"] = 0.9
    # train_times["step"] = 0.01

    X_train = [[], []]; y_train = []; X_test = [[], []]; y_test = [] # assuming for now only two classes (two empty lists)
    for i, (patient, hospital, pick_micro, pick_macro, pick_spike) in enumerate(zip(patients, hospitals, picks_micro, picks_macro, picks_spike)):
        if pick_micro == 'all':
            import glob
            epochs_filenames = glob.glob(os.path.join(root_path, 'Data', hospital, patient, 'Epochs', '*.h5'))
            channels = [int(filename[filename.find('_ch_')+4:filename.find('-tfr.h5')]) for filename in epochs_filenames]
        else:
            channels = [int(c) for c in picks]

        for c, ch in enumerate(channels):
            print('-'*80)
            print('Loading TRAIN epochs object of patient %s channel %i' % (patient, ch))
            print('-'*80)
            try:
                epochs_fname = patient + '_ch_' + str(ch) + '-tfr.h5'
                path2epochs = os.path.join(root_path, 'Data', hospital, patient, 'Epochs', epochs_fname)
                epochsTFR = mne.time_frequency.read_tfrs(path2epochs)[0]
                print(epochsTFR)
                for q, query_class_train in enumerate(query_classes_train):
                    epochs_class_train = epochsTFR[query_class_train]
                    epochs_class_train.crop(train_times["start"], train_times["stop"])
                    print('epochsTRF num_epochs X num_channels X num_freq X num_timepoints:', epochs_class_train.data.shape)
                    curr_data = np.squeeze(np.average(epochs_class_train.data, axis=2))
                    print('Curr train data: ', curr_data.shape)
                    if c == 0 and i==0:
                        print(epochs_class_train.metadata['sentence_string'])
                        print(', '.join(epochs_class_train.metadata['word_string']))
                    X_train[q].append(curr_data)
                    del curr_data
                if query_classes_test is not None:
                    for q, query_class_test in enumerate(query_classes_test):
                        epochs_class_test = epochsTFR[query_class_test]
                        epochs_class_test.crop(train_times["start"], train_times["stop"])
                        curr_data = np.squeeze(np.average(epochs_class_test.data, axis=2))
                        X_test[q].append(curr_data)
                        print('Curr test data: ', curr_data.shape)
                        if c==0 and i==0:
                            print(epochs_class_test.metadata['sentence_string'])
                            print(', '.join(epochs_class_test.metadata['word_string']))
                else: # no test queries (generalization across time only, not conditions)
                    X_test = None; y_test = None
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print('!!!!!! ERROR !!!!!!: patient %s channel %i \n %s line %s' % (patient, ch, e, exc_tb.tb_lineno))

    X_train = [np.dstack(d) for d in X_train] # signals: n_epochs, n_times, n_channels
    X_train = [np.swapaxes(d, 1, 2) for d in X_train] # Swap dimensions: n_epochs, n_channels, n_times
    y_train = np.hstack((np.ones(X_train[0].shape[0]).astype(int), 2*np.ones(X_train[1].shape[0]).astype(int)))  # targets
    print('Number of samples in training class %i : %i' % (1, X_train[0].shape[0]))
    print('Number of samples in training class %i : %i' % (2, X_train[1].shape[0]))
    X_train = np.concatenate(X_train, axis=0)

    if query_classes_test is not None:
        X_test = [np.dstack(d) for d in X_test] # signals: n_epochs, n_times, n_channels
        X_test = [np.swapaxes(d, 1, 2) for d in X_test] # Swap dimensions: n_epochs, n_channels, n_times
        y_test = np.hstack((np.ones(X_test[0].shape[0]).astype(int), 2*np.ones(X_test[1].shape[0]).astype(int)))  # targets
        print('Number of samples in test class %i : %i' % (1, X_test[0].shape[0]))
        print('Number of samples in test class %i : %i' % (2, X_test[1].shape[0]))
        X_test = np.concatenate(X_test, axis=0)

    data = {}
    data['times'] = epochs_class_train[0].times
    data['X_train'] = X_train
    data['X_test'] = X_test
    data['y_train'] = y_train
    data['y_test'] = y_test

    del X_train, X_test, y_train, y_test, epochs_class_train
    if k > 1:
        data = cat_subsequent_timepoints(k, data)

    return data

def cat_subsequent_timepoints(k, data):
    '''
    :param k: (scalar) number of subsequent time points
    :param data: (dict) has the following keys -
           times: n_times
           X_train: n_epochs, n_channels, n_times
           y_train: n_epochs
           X_test: n_epochs, n_channels, n_times
           y_test: n_epochs
    :return:
    new_times = floor(n_times/k)
    new_X_train: n_epochs, n_channels * k, floor(n_times/k)
    new_X_test: n_epochs, n_channels * k, floor(n_times/k)
    '''

    n_epochs, n_channels, n_times = data['X_train'].shape
    n_times_round = int(k*np.floor(n_times/k)) # remove residual mod k
    assert n_times_round > 0
    data['X_train'] = data['X_train'][:,:,0:n_times_round]

    new_data = data.copy()
    new_data['times'] = data['times'][0:n_times_round:k]
    new_data['X_train'] = data['X_train'].reshape((n_epochs, -1, int(n_times_round/k)), order='F')

    if data['X_test'] is not None:
        n_epochs_test = data['X_test'].shape[0]
        data['X_test'] = data['X_test'][:, :, 0:n_times_round]
        new_data['X_test'] = data['X_test'].reshape((n_epochs_test, -1, int(n_times_round/k)), order='F')


    return new_data


def train_test_GAT(data):
    from sklearn.svm import LinearSVC
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from mne.decoding import (GeneralizingEstimator, Scaler, cross_val_multiscore, LinearModel, get_coef, Vectorizer)

    # Define a classifier for GAT
    #clf = make_pipeline(StandardScaler(), LinearSVC())
    clf = make_pipeline(StandardScaler(), LinearModel(LogisticRegression(solver='lbfgs')))
    # Define the Temporal Generalization object
    time_gen = GeneralizingEstimator(clf, n_jobs=1, scoring='roc_auc', verbose=True)
    # Fit model
    if (data['X_test'] is not None) and (data['y_test'] is not None): # Generalization across conditions
        #print(X_train, y_train, X_test, y_test)
        #print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
        time_gen.fit(data['X_train'], data['y_train'])
        scores = time_gen.score(data['X_test'], data['y_test'])
        scores = np.expand_dims(scores, axis=0) # For later compatability (plot_GAT() np.mean(scores, axis=0))
        #print(scores)
    else: # Generlization across time only (not across conditions or modalities)
        scores = cross_val_multiscore(time_gen, data['X_train'], data['y_train'], cv=5, n_jobs=1)

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

