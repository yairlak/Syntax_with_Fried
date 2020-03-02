import argparse, os, glob
import mne
import matplotlib.pyplot as plt
import numpy as np
from numpy import percentile
from sklearn import linear_model
from sklearn.metrics import r2_score
from operator import itemgetter
from pprint import pprint
from functions.auxilary_functions import  smooth_with_gaussian
from scipy.cluster.hierarchy import dendrogram, linkage

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
parser.add_argument('-patient', default='505', help='Patient string')
parser.add_argument('-hospital', default='UCLA', help='Hospital string')
parser.add_argument('-block', choices=['visual','auditory', '1', '2', '3', '4', '5', '6', []], default=[], help='Block type')
parser.add_argument('-align', choices=['first','last', 'end'], default=[], help='Block type')
parser.add_argument('-channel', default=17, type=int, help='channel number (if empty list [] then all channels of patient are analyzed)')
parser.add_argument('--sort-key', default=['morpheme'], help='Keys to sort according')
# parser.add_argument('--query', default='word_position>0 and block in [2, 4, 6]', help='Metadata query (e.g., word_position==1). See pandas query syntax for more')
parser.add_argument('--query', default=[], help='Metadata query (e.g., word_position==1). See pandas query syntax for more')
parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
parser.add_argument('-tmin', default=-0.5, type=float, help='crop window')
parser.add_argument('-tmax', default=1, type=float, help='crop window')
parser.add_argument('-baseline', default=None, type=str, help='Baseline to apply as in mne: (a, b), (None, b), (a, None) or None')
parser.add_argument('-SOA', default=500, help='SOA in design [msec]')
parser.add_argument('-word-ON-duration', default=250, help='Duration for which word word presented in the RSVP [msec]')
parser.add_argument('-y-tick-step', default=30, help='If sorted by key, set the yticklabels density')
parser.add_argument('-ylim-PSTH', default=20)
parser.add_argument('-window-st', default=0, help='Regression start-time window [msec]')
parser.add_argument('-window-ed', default=200, help='Regression end-time window [msec]')
# parser.add_argument('--baseline-mode', choices=['mean', 'ratio', 'logratio', 'percent', 'zscore', 'zlogratio'], default='zscore', help='Type of baseline method')
parser.add_argument('-sort-cluster', action="store_true", default=False)
parser.add_argument('--path2figures', default=[], help='Patient string')


args = parser.parse_args()
args.patient = 'patient_' + args.patient
if isinstance(args.sort_key, str):
    args.sort_key = eval(args.sort_key)
if isinstance(args.baseline, str):
    args.baseline = eval(args.baseline)

if args.block and args.align:
    if args.query:
        raise('query block and align are all non empty. Either specify a block+align, or a query, not both')
    else:
        if args.block == 'visual':
            block_str = 'block in [1, 3, 5]'
        elif args.block == 'auditory':
            block_str = 'block in [2, 4, 6]'
        else:
            block_str = 'block in [%s]' % args.block

        if args.align == 'first':
            align_str = "word_position == 1"
        elif args.align == 'last':
            align_str = "word_position == sentence_length"
        elif args.align == 'end':
            align_str = "word_position == -1"
        args.query = align_str + ' and ' + block_str
pprint(args)

# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# 
plt.close('all')
if not isinstance(args.channel, int):
    #filename = args.patient + '-tfr.h5'
    pass
else:
    filename = glob.glob(os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'Epochs', args.patient + '_spikes_*_ch_' + str(args.channel) + '-epo.fif'))
    print('Loading: %s' % filename)
    assert len(filename) == 1
    filename = os.path.basename(filename[0])
    path2epochs = os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'Epochs', filename)

if not args.path2figures:
    args.path2figures = os.path.join('..', '..', 'Figures', args.patient, 'Rasters')
if not os.path.exists(args.path2figures):
    os.makedirs(args.path2figures)

print('Loading epochs object: ' + path2epochs)
epochs_spikes = mne.read_epochs(path2epochs)
if args.tmin is not None and args.tmax is not None:
    epochs_spikes.crop(args.tmin, args.tmax)

epochs_spikes = epochs_spikes[args.query]
print(epochs_spikes)

sfreq = epochs_spikes.info['sfreq']
print('Sampling rate: %1.2f' % sfreq)
gaussian_width = 100 * 1e-3

for i_cluster, cluster in enumerate(np.arange(epochs_spikes.info['nchan'])):

    # Sort if needed
    if args.sort_key:
        fields_for_sorting = []
        for field in args.sort_key:
            fields_for_sorting.append(epochs_spikes.metadata[field])
        if len(fields_for_sorting) == 1:
            print(fields_for_sorting[0])
            mylist = [(i, j) for (i, j) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0])]
            IX = [i[0] for i in sorted(mylist, key=itemgetter(1))]
        elif len(fields_for_sorting) == 2:
            mylist = [(i, j, k) for (i, j, k) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0],
                                                     fields_for_sorting[1])]
            IX = [i[0] for i in sorted(mylist, key=itemgetter(1, 2))]
    else:
        IX = None

    if args.sort_cluster:
        import pandas as pd
        # Move to dataframe to facilitate averaging
        df = pd.DataFrame(data=np.squeeze(epochs_spikes._data[:, 0, :]))
        df['word_string'] = list(epochs_spikes.metadata['word_string'])
        df = df.groupby('word_string').apply(lambda x: x.mean())
        df = df.loc[:, df.columns != 'word_string']
        mat = df.values
        # Smooth AFTER averaging
        new_mat = []
        for l in mat:
            new_l = smooth_with_gaussian(l, sfreq, gaussian_width=gaussian_width * sfreq)  # smooth with 20ms gaussian
            new_mat.append(new_l)
        new_mat = np.asarray(new_mat)

        # hierarchical clustering
        linked = linkage(new_mat, method='complete', metric='seuclidean')

        plt.figure(figsize=(10, 7))
        dendrogram(linked, labels=list(set(epochs_spikes.metadata['word_string'])))
        plt.tick_params(axis='x', labelsize=10)
        plt.show()


    fig = epochs_spikes.plot_image(cluster, order=IX, vmin=0, vmax=1, colorbar=False, show=False)


    if args.sort_key:
        fig[0].axes[0].set_yticks(range(0, len(fields_for_sorting[0]), args.y_tick_step))
        # Change fields_for_sorting[1] instead of 0, if you want ticks to be based on second sort key
        yticklabels = np.asarray(fields_for_sorting[0])[IX][::args.y_tick_step]
        #yticklabels = yticklabels[::-1]
        fig[0].axes[0].set_yticklabels(yticklabels)
        plt.setp(fig[0].axes[0], ylabel=args.sort_key[0])

    mean_spike_count = np.mean(epochs_spikes._data[:, cluster, :], axis=0)
    new_y_smoothed = smooth_with_gaussian(mean_spike_count, sfreq,
                                          gaussian_width=gaussian_width * sfreq)  # smooth with 20ms gaussian

    x = fig[0].axes[1].lines[0]._x

    fig[0].axes[1].clear()

    fig[0].axes[1].plot(x, new_y_smoothed, 'k-')
    fig[0].axes[1].set_xlim([fig[0].axes[0].get_xlim()[0] / 1000, fig[0].axes[0].get_xlim()[1] / 1000])
    fig[0].axes[1].axvline(x=0, linestyle='--')

    plt.setp(fig[0].axes[1], ylim=[0, args.ylim_PSTH], xlabel='Time [sec]', ylabel='spikes / s')


    region = epochs_spikes.info['ch_names'][i_cluster]
    fname = 'raster_' + args.hospital + '_' + args.patient + '_' + region + '_ch_' + str(args.channel) + '_cluster_' + str(cluster) + '_' + args.query

    for key_sort in args.sort_key:
        fname += '_' + key_sort + 'Sorted'

    plt.savefig(os.path.join(args.path2figures, fname + '.png'))
    plt.close()
    print('Figures saved to %s:' % os.path.join(args.path2figures, fname + '.png'))
