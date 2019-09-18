import argparse, os, glob
import mne
import matplotlib.pyplot as plt
import numpy as np
import scipy
from numpy import percentile
from sklearn import linear_model
from sklearn.metrics import r2_score
from operator import itemgetter
from pprint import pprint
from functions import data_manip
from functions.auxilary_functions import  smooth_with_gaussian

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
parser.add_argument('-patient', default='479_11', help='Patient string')
parser.add_argument('-hospital', default='UCLA', help='Hospital string')
parser.add_argument('-block', choices=['visual','auditory', '1', '2', '3', '4', '5', '6', []], default='auditory', help='Block type')
parser.add_argument('-align', choices=['first','last', 'end'], default=[], help='Block type')
#parser.add_argument('--probe-name', default='LSTG', help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all channels found in the ChannelsCSC folder")
parser.add_argument('-channel', default=15, type=int, help='channel number (if empty list [] then all channels of patient are analyzed)')
parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[('First', "block in [2, 4, 6] and word_position==1"), ('End', "block in [2, 4, 6] and word_position==-1")], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
parser.add_argument('--sort-key', default=['word_string'], help='Keys to sort according')
parser.add_argument('-tmin', default=-0.5, type=float, help='crop window')
parser.add_argument('-tmax', default=1, type=float, help='crop window')
parser.add_argument('-SOA', default=500, help='SOA in design [msec]')
parser.add_argument('-word-ON-duration', default=250, help='Duration for which word word presented in the RSVP [msec]')
parser.add_argument('--over-write', default=False, action='store_true', help="If True then file will be overwritten")
parser.add_argument('--gaussian-smooth-width', default=0.1, help='[sec] Window width for Gaussian smoothing of the firing rate')
parser.add_argument('-y-tick-step', default=10, help='If sorted by key, set the yticklabels density')
parser.add_argument('-ylim-PSTH', default=20)
parser.add_argument('--path2figures', default=[], help='Patient string')


# parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[("word_position==1 and block in [2, 4, 6]", "word_position==-1 and block in [2, 4, 6]")], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
args = parser.parse_args()
args.patient = 'patient_' + args.patient
if isinstance(args.sort_key, str):
    args.sort_key = eval(args.sort_key)
pprint(args)

# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


probes = data_manip.get_probes2channels(args.patient)

# 
filename = glob.glob(os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'Epochs', args.patient + '_spikes_*_ch_' + str(args.channel) + '-epo.fif'))
assert len(filename) == 1
filename = os.path.basename(filename[0])
path2epochs = os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'Epochs', filename)


if not args.path2figures:
    args.path2figures = os.path.join('..', '..', 'Figures', args.patient, 'ERPs')
if not os.path.exists(args.path2figures):
    os.makedirs(args.path2figures)

print('Loading: %s' % os.path.join(path2epochs, filename))
epochs_spikes = mne.read_epochs(path2epochs)
if args.tmin is not None and args.tmax is not None:
    epochs_spikes.crop(args.tmin, args.tmax)
sfreq = epochs_spikes.info['sfreq']
print('Sampling rate: %1.2f' % sfreq)


def plot_axes(ax, fig=None, geometry=(1,1,1)):
    if fig is None:
        fig = plt.figure()
    if ax.get_geometry() != geometry :
        ax.change_geometry(*geometry)
    ax = fig.axes.append(ax)
    return fig

main_fig = plt.figure()
# Plot ERPs only for args.queries_to_compare:
for i_cluster, cluster_name in enumerate(epochs_spikes.info['ch_names']):
    evoked_dict = dict()
    print('i_clu %i, clu %s' % (i_cluster, cluster_name))
    epochs_spikes_cluster = epochs_spikes.pick_channels([cluster_name])
    condition_names = []
    for (condition_name, curr_query) in args.queries_to_compare:
        condition_names.append(condition_name)
        epochs_spikes_query = epochs_spikes_cluster[curr_query]
        print(epochs_spikes_query)
        # Sort if needed
        if args.sort_key:
            fields_for_sorting = []
            for field in args.sort_key:
                fields_for_sorting.append(epochs_spikes_query.metadata[field])
            if len(fields_for_sorting) == 1:
                mylist = [(i, j) for (i, j) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0])]
                IX = [i[0] for i in sorted(mylist, key=itemgetter(1))]
            elif len(fields_for_sorting) == 2:
                mylist = [(i, j, k) for (i, j, k) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0],
                                                         fields_for_sorting[1])]
                IX = [i[0] for i in sorted(mylist, key=itemgetter(1, 2))]
        else:
            IX = None

        fig_raster = epochs_spikes_query.plot_image(0, order=IX, vmin=0, vmax=1, colorbar=False, show=False)

        if args.sort_key:
            fig_raster[0].axes[0].set_yticks(range(0, len(fields_for_sorting[0]), args.y_tick_step))
            # Change fields_for_sorting[1] instead of 0, if you want ticks to be based on second sort key
            yticklabels = np.asarray(fields_for_sorting[0])[IX][::args.y_tick_step]
            #yticklabels = yticklabels[::-1]
            fig_raster[0].axes[0].set_yticklabels(yticklabels)
            plt.setp(fig_raster[0].axes[0], ylabel=args.sort_key[0])

        main_fig = plot_axes(fig_raster[0].axes[0], main_fig)
        plt.close(fig_raster[0])

        # Gausssian smoothing of curr raster	    
        smoothed_epochs = []
        for e in range(epochs_spikes_query._data.shape[0]):
            smoothed_epochs.append(smooth_with_gaussian(epochs_spikes_query._data[e, i_cluster, :], sfreq, gaussian_width=args.gaussian_smooth_width * sfreq))
        smoothed_epochs = np.expand_dims(np.asarray(smoothed_epochs), axis=1) # add singleton add channel dimension
        
        # Generate new epochs array for smoothed raster and through into evoked dict
        curr_condition_epochs = mne.EpochsArray(smoothed_epochs, epochs_spikes_query.info, tmin=np.min(epochs_spikes_query.times))
        evoked_dict[condition_name] = list(curr_condition_epochs.iter_evoked())

	    

    #fig_evoked = mne.viz.plot_compare_evokeds(evoked_dict, show=False)
    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
    #plt.subplots_adjust(right=0.6)
    #main_fig = plot_axes(fig_evoked.axes[0], main_fig)

    # Save main figure
    fname = 'evoked_raster_' + args.hospital + '_' + args.patient + '_' + cluster_name + '_ch_' + str(args.channel) + '_cluster_' + str(i_cluster) + '_vs_'.join(condition_names)

    for key_sort in args.sort_key:
        fname += '_' + key_sort + 'Sorted'

    plt.savefig(os.path.join(args.path2figures, fname + '.png'))
    plt.close()
    print('Figures saved to %s:' % os.path.join(args.path2figures, fname + '.png'))

