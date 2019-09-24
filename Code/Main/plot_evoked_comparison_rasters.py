import argparse, os, glob
import mne
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
from pprint import pprint
from functions.auxilary_functions import  smooth_with_gaussian

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
parser.add_argument('-patient', default='479_11', help='Patient string')
parser.add_argument('-hospital', default='UCLA', help='Hospital string')
parser.add_argument('-block', choices=['visual','auditory', '1', '2', '3', '4', '5', '6', []], default='auditory', help='Block type')
parser.add_argument('-align', choices=['first','last', 'end'], default=[], help='Block type')
#parser.add_argument('--probe-name', default='LSTG', help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all channels found in the ChannelsCSC folder")
parser.add_argument('-channel', default=15, type=int, help='channel number (if empty list [] then all channels of patient are analyzed)')
parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
parser.add_argument('--sort-key', default=['num_letters', 'morpheme_type'], help='Keys to sort according')
parser.add_argument('-tmin', default=-0.5, type=float, help='crop window')
parser.add_argument('-tmax', default=1, type=float, help='crop window')
parser.add_argument('-SOA', default=500, help='SOA in design [msec]')
parser.add_argument('-word-ON-duration', default=250, help='Duration for which word word presented in the RSVP [msec]')
parser.add_argument('--over-write', default=False, action='store_true', help="If True then file will be overwritten")
parser.add_argument('--gaussian-smooth-width', default=0.01, help='[sec] Window width for Gaussian smoothing of the firing rate')
parser.add_argument('-y-tick-step', default=50, help='If sorted by key, set the yticklabels density')
parser.add_argument('-field-for-ylabels', default='word_string', help='Field from metadata to use for yticklabels')
parser.add_argument('-ylim-PSTH', default=20)
parser.add_argument('--path2figures', default=[], help='Patient string')


args = parser.parse_args()
args.patient = 'patient_' + args.patient
if isinstance(args.sort_key, str):
    args.sort_key = eval(args.sort_key)
pprint(args)

# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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

condition_names = [c_name for (c_name, _) in args.queries_to_compare]
n = len(args.queries_to_compare)
h_delta = 0.05
h_subplot = (0.55 - h_delta*(n-1))/n

# Plot ERPs only for args.queries_to_compare:
for i_cluster, cluster_name in enumerate(epochs_spikes.info['ch_names']):
    main_fig, axs = plt.subplots(nrows=len(args.queries_to_compare)+1)
    ax_pos = [ax.get_position() for ax in main_fig.axes]
    ax_pos[n].x0 = 0.15
    ax_pos[n].x1 = 0.95
    ax_pos[n].y0 = 0.1
    ax_pos[n].y1 = 0.25

    [ax.remove() for ax in main_fig.axes]
    smoothed_epochs_dict = dict()
    print('i_clu %i, clu %s' % (i_cluster, cluster_name))
    epochs_spikes_cluster = epochs_spikes.copy().pick_channels([cluster_name])
    #condition_names = []
    for q, (condition_name, curr_query) in enumerate(args.queries_to_compare):
        ax_pos[q].x0 = 0.15
        ax_pos[q].x1 = 0.95
        ax_pos[q].y0 = 0.25 + h_delta + q*(h_delta + h_subplot)
        ax_pos[q].y1 = 0.25 + (q+1)*(h_delta + h_subplot)
        
        #condition_names.append(condition_name)
        epochs_spikes_query = epochs_spikes_cluster[curr_query]
        print(epochs_spikes_query)
        #print('word string')
        #print(epochs_spikes_query.metadata['word_string'])

        # Gausssian smoothing of curr raster
        smoothed_epochs = []
        num_trials = epochs_spikes_query._data.shape[0]
        for e in range(num_trials):
            smoothed_epochs.append(smooth_with_gaussian(epochs_spikes_query._data[e, 0, :], sfreq,
                                                        gaussian_width=args.gaussian_smooth_width * sfreq))
        smoothed_epochs = np.expand_dims(np.asarray(smoothed_epochs), axis=1)  # add singleton add channel dimension

        # Generate new epochs array for smoothed raster and through into evoked dict
        curr_condition_epochs = mne.EpochsArray(smoothed_epochs, epochs_spikes_query.info,
                                                tmin=np.min(epochs_spikes_query.times))
        smoothed_epochs_dict[condition_name] = curr_condition_epochs

        # Smooth also raster with 1e-3sec wide Gaussian
        smoothed_epochs = []
        num_trials = epochs_spikes_query._data.shape[0]
        for e in range(num_trials):
            smoothed_epochs.append(smooth_with_gaussian(epochs_spikes_query._data[e, 0, :], sfreq,
                                                        gaussian_width=1e-3 * sfreq))
        smoothed_epochs = np.expand_dims(np.asarray(smoothed_epochs), axis=1)  # add singleton add channel dimension

        # Generate new epochs array for smoothed raster and through into evoked dict
        curr_condition_epochs = mne.EpochsArray(smoothed_epochs, epochs_spikes_query.info,
                                                tmin=np.min(epochs_spikes_query.times))

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

        fig_raster = curr_condition_epochs.plot_image(0, order=IX, vmin=0, vmax=1, colorbar=False, show=False)

        if args.sort_key:
            IX_key = 0
            #if len(fiels_for_sorting) == 2:
            #    IX_key = args.key_for_ylabels
            fig_raster[0].axes[0].set_yticks(range(0, len(fields_for_sorting[IX_key]), args.y_tick_step))
            # Change fields_for_sorting[1] instead of 0, if you want ticks to be based on second sort key
            #yticklabels = np.asarray(fields_for_sorting[IX_key])[IX][::args.y_tick_step]
            yticklabels = np.asarray(epochs_spikes_query.metadata[args.field_for_ylabels])[IX][::args.y_tick_step]
            #yticklabels = yticklabels[::-1]
            fig_raster[0].axes[0].set_yticklabels(yticklabels)
            plt.setp(fig_raster[0].axes[0], ylabel=args.sort_key[IX_key])


        # fig_raster[0].axes[1].remove()
        fig_raster[0].axes[0].figure = main_fig
        main_fig.axes.append(fig_raster[0].axes[0])
        main_fig.add_axes(fig_raster[0].axes[0])

        # dummy = main_fig.add_subplot(3,1,q+1)
        # fig_raster[0].axes[0].set_position(dummy.get_position())
        fig_raster[0].axes[0].set_position(ax_pos[q])
        # dummy.remove()
        plt.close(fig_raster[0])

        main_fig.axes[-1].set_position(ax_pos[q])
        main_fig.axes[-1].set_title(condition_name)


    # fig_evoked = mne.viz.plot_compare_evokeds(evoked_dict, picks=0, show=False)
    # Evoked
    fig_evoked, ax = plt.subplots()
    colors_dict = {}
    colors_dict[condition_names[0]] = '#ff966c'
    if n>1:
        colors_dict[condition_names[1]] = '#7094b7'
        for i in range(2, n):
            colors_dict[condition_names[i]] = np.random.rand(3,)

    for i, k in enumerate(smoothed_epochs_dict.keys()):
        x = smoothed_epochs_dict[k].times
        y = np.squeeze(np.mean(smoothed_epochs_dict[k]._data, axis=0))
        yerr = np.squeeze(np.std(smoothed_epochs_dict[k]._data, axis=0))/np.sqrt(smoothed_epochs_dict[k]._data.shape[0])
        plt.plot(x, y, color=colors_dict[k], label=k)
        plt.fill_between(x, y-yerr, y+yerr, alpha=0.5, edgecolor=colors_dict[k], facecolor=colors_dict[k])

    fig_evoked.axes[0].figure = main_fig
    main_fig.axes.append(fig_evoked.axes[0])
    main_fig.add_axes(fig_evoked.axes[0])

    fig_evoked.axes[0].set_position(ax_pos[-1])
    plt.close(fig_evoked)
    plt.setp(main_fig.axes[-1], xlabel='Time [sec]', title='', ylim=[0, args.ylim_PSTH])
    main_fig.axes[-1].set_ylabel('spikes / s', labelpad=5)
    main_fig.axes[-1].legend(loc=1)
    #main_fig.axes[-1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
    main_fig.axes[-1].set_xlim([min(x), max(x)])
    plt.suptitle(cluster_name)
    # Save main figure

    fname = 'evoked_raster_' + args.hospital + '_' + args.patient + '_' + cluster_name + '_ch_' + str(args.channel) + '_cluster_' + str(i_cluster) + '_' + '_vs_'.join(condition_names)

    for key_sort in args.sort_key:
        fname += '_' + key_sort + 'Sorted'

    plt.savefig(os.path.join(args.path2figures, fname + '.png'))
    plt.close()
    print('Figures saved to %s:' % os.path.join(args.path2figures, fname + '.png'))


