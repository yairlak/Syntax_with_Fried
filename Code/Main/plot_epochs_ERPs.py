import argparse, os
import mne
import matplotlib.pyplot as plt
import numpy as np
from numpy import percentile
from sklearn import linear_model
from sklearn.metrics import r2_score
from operator import itemgetter

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
parser.add_argument('-patient', default='505', help='Patient string')
parser.add_argument('-block', choices=['visual','auditory', '1', '2', '3', '4', '5', '6', []], default='auditory', help='Block type')
parser.add_argument('-align', choices=['first','last', 'end'], default='first', help='Block type')
parser.add_argument('-filename', default='patient_505_ch_0-tfr.h5', help='Input filename (if empty list [] then will be assigned based on patient name)')
parser.add_argument('--sort-key', default=['sentence_length'], help='Keys to sort according')
parser.add_argument('--query', default=[], help='Metadata query (e.g., word_position==1)')
parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
parser.add_argument('-tmin', default=None, type=float, help='crop window')
parser.add_argument('-tmax', default=None, type=float, help='crop window')
parser.add_argument('-SOA', default=500, help='SOA in design [msec]')
parser.add_argument('-word-ON-duration', default=250, help='Duration for which word word presented in the RSVP [msec]')
parser.add_argument('-y-tick-step', default=20, help='If sorted by key, set the yticklabels density')
parser.add_argument('-window-st', default=0, help='Regression start-time window [msec]')
parser.add_argument('-window-ed', default=200, help='Regression end-time window [msec]')
# parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[("word_position==1 and block in [2, 4, 6]", "word_position==-1 and block in [2, 4, 6]")], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
args = parser.parse_args()
args.patient = 'patient_' + args.patient
if isinstance(args.sort_key, str):
    args.sort_key = eval(args.sort_key)
print(args)

if args.block and args.align:
    if args.query:
        raise('query block and align are all non empty. Either specify a block+align, or a query, not both')
    else:
        if args.block == 'visual':
            block_str = 'block in [1, 3, 5]'
        elif args.block == 'auditory':
            block_str = 'block in [2, 4, 6]'

        if args.align == 'first':
            align_str = "word_position == 1"
        elif args.align == 'last':
            align_str = "word_position == sentence_length"
        elif args.align == 'end':
            align_str = "word_position == -1"
        args.query = align_str + ' and ' + block_str

# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# 
plt.close('all')
filename = args.patient + '-tfr.h5' if not args.filename else args.filename
path2epochs = os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'Epochs', filename)
path2figures = os.path.join('..', '..', 'Figures', args.patient, 'ERPs')
if not os.path.exists(path2figures):
    os.makedirs(path2figures)

print('Loading epochs object: ' + path2epochs)
epochsTFR = mne.time_frequency.read_tfrs(path2epochs)
epochsTFR = epochsTFR[0][args.query]
if args.tmin is not None and args.tmax is not None:
    epochsTFR.crop(args.tmin, args.tmax)
else:
    epochsTFR.crop(min(epochsTFR.times) + 0.1, max(epochsTFR.times) - 0.1)
#epochsTFR.apply_baseline((None, None), 'zscore')
print(epochsTFR)

for ch, ch_name in enumerate(epochsTFR.ch_names):
    # Plot all trials and ERP for args.query
    fig = plt.subplots(figsize=(10, 10))
    IX_ch = mne.pick_channels(epochsTFR.ch_names, [ch_name])[0]
    power_ave = np.squeeze(np.average(epochsTFR.data[:, IX_ch, :, :], axis=1))
    # calculate interquartile range
    q25, q75 = percentile(power_ave.flatten(), 25), percentile(power_ave.flatten(), 75)
    iqr = q75 - q25
    print('Percentiles: 25th=%.3f, 75th=%.3f, IQR=%.3f' % (q25, q75, iqr))
    # calculate the outlier cutoff
    cut_off = iqr * 1.5
    lower, upper = np.asarray(q25 - cut_off), np.asarray(q75 + cut_off)
    print(lower, upper)
    # Put NaNs 
    power_ave[power_ave > upper] = np.nan
    power_ave[power_ave < lower] = np.nan
    print(power_ave)
    print('Identified outliers: %d' % np.sum(power_ave > upper))
    print('Identified outliers: %d' % np.sum(power_ave < lower))
    # zscore data
    power_ave -= np.nanmean(power_ave)
    power_ave = power_ave / np.nanstd(power_ave)

    # Sort if needed
    if not args.sort_key:
        r2_string = 'No regression calc'
    else:
        fields_for_sorting = []
        for field in args.sort_key:
            fields_for_sorting.append(epochsTFR.metadata[field])
        if len(fields_for_sorting) == 1:
            mylist = [(i, j) for (i, j) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0])]
            IX = [i[0] for i in sorted(mylist, key=itemgetter(1))]
            mylist_sorted = sorted(mylist, key=itemgetter(1))
        elif len(fields_for_sorting) == 2:
            mylist = [(i, j, k) for (i, j, k) in zip(range(len(fields_for_sorting[0])), fields_for_sorting[0],
                                                     fields_for_sorting[1])]
            IX = [i[0] for i in sorted(mylist, key=itemgetter(1, 2))]
            mylist_sorted = sorted(mylist, key=itemgetter(1, 2))
        power_ave = power_ave[IX, :]

        # Run a linear regression if sorted according to, e.g., sentence length
        IX = (epochsTFR.times > args.window_st / 1e3) & (epochsTFR.times < args.window_ed / 1e3)
        X = np.asarray([tup[1] for tup in mylist_sorted])
        print(power_ave[:, IX].shape)
        y = np.nanmean(power_ave[:, IX], axis=1)  # mean activity in params.window_st-ed.
        IX_nan = np.isnan(y)
        X, y = X[~IX_nan], y[~IX_nan]
        regr = linear_model.LinearRegression()
        regr.fit(np.expand_dims(X, 1), y)
        y_pred = regr.predict(np.expand_dims(X, 1))
        r2 = r2_score(y, y_pred)
        r2_string = '%s $ R^2=%1.2f$' % (args.sort_key[0], r2)

    # Plot
    # fig = plt.figure(figsize=(10, 12))
    ax0 = plt.subplot2grid((12, 13), (0, 0), rowspan=10, colspan=10)
    ax1 = plt.subplot2grid((12, 13), (0, 10), rowspan=10, colspan=2)
    ax2 = plt.subplot2grid((12, 13), (10, 0), rowspan=2, colspan=10)
    cbaxes = plt.subplot2grid((12, 13), (0, 12), rowspan=10)

    im = ax0.imshow(power_ave,
                     interpolation='nearest',
                     aspect='auto', vmin=-0.5, vmax=0.5, cmap='viridis')
    cbar = plt.colorbar(im, cax=cbaxes)
    cbar.set_label(label='z-score of power)', size=22)

    ax0.set_ylabel('Trial', fontsize=24)
    ax0.tick_params(axis='x', which='both', bottom='off', labelbottom='off')

    if not args.sort_key:
        pass
    else:
        ax0.set_yticks(range(0, len(fields_for_sorting[0]), args.y_tick_step))
        yticklabels = np.sort(fields_for_sorting[0])[::args.y_tick_step]
        yticklabels = yticklabels[::-1]
        ax0.set_yticklabels(yticklabels)
        plt.setp(ax0, ylabel=args.sort_key[0])

    ax1.plot(np.nanmean(power_ave[:, IX], axis=1), np.arange(1, 1 + power_ave.shape[0]))
    ax1.set_xlabel('Mean activity\n' + r2_string)
    ax1.set_ylim([1, 1 + power_ave.shape[0]])
    ax1.set_xlim([0, np.nanmean(power_ave) + 3 * np.nanstd(power_ave)])
    ax1.tick_params(axis='y', which='both', left='off', labelleft='off', direction='in')

    ax2.plot(epochsTFR.times, np.nanmean(power_ave, axis=0))
    ax2.set_xlabel('Time [sec]', fontsize=24)
    ax2.set_ylabel('Mean activity (zscore)', fontsize=18)
    ax2.set_xlim([np.min(epochsTFR.times) + 0.2, np.max(epochsTFR.times) - 0.2])
    #ax2.axhline(y=3, linestyle='--', linewidth=3, color='g')
    #ax2.axhline(y=-3, linestyle='--', linewidth=3, color='g')
    ax2.set_ylim([-3, 3])
    #
    # # Add vertical lines
    ax0.axvline(x=0, linestyle='--', linewidth=3, color='k')
    ax2.axvline(x=0, linestyle='--', linewidth=3, color='k')


    if "block in [1, 3, 5]" in args.query:
        if "word_position == 1" in args.query:
            ax2.axvline(x=args.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
            ax2.axvline(x=2 * args.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
            ax2.axvline(x=3 * args.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        elif "word_position == sentence_length" in args.query:
            ax2.axvline(x=-args.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
            ax2.axvline(x=-2 * args.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
            ax2.axvline(x=-3 * args.SOA * 1e-3, linestyle='--', linewidth=1, color='b')
        elif "word_position == -1" in args.query:
            ax2.axvline(x=-args.word_ON_duration * 1e-3, linestyle='--', linewidth=1, color='b')
            ax2.axvline(x=(-args.SOA - args.word_ON_duration) * 1e-3, linestyle='--', linewidth=1, color='b')
            ax2.axvline(x=(-2 * args.SOA - args.word_ON_duration) * 1e-3, linestyle='--', linewidth=1, color='b')

    # Plot
    filename_base = 'high_gamma_epochs_ch_' + ch_name + '_' + args.query
    filename_base += '_' + '_'.join(args.sort_key)
    plt.savefig(os.path.join(path2figures, filename_base + '.png'))
    print('fig saved to: ' + os.path.join(path2figures, filename_base + '.png'))
    plt.close('All')

    if not args.queries_to_compare:
        print('no comparison')
    else:
        # Plot ERPs only for args.queries_to_compare
        evoked_dict = dict()
        for (condition_name, query) in args.queries_to_compare:
            evoked_dict[condition_name] = epochsTFR[query].average()
        mne.viz.plot_compare_evokeds(evoked_dict)
