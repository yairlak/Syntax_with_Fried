import argparse, os, glob, sys
# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append('..')
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

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
parser.add_argument('-patient', default='505', help='Patient string')
parser.add_argument('-block', choices=['visual','auditory', '1', '2', '3', '4', '5', '6', []], default='auditory', help='Block type')
parser.add_argument('--micro-macro', choices=['micro','macro'], default='micro', help='electrode type')
#parser.add_argument('--probe-name', default='LSTG', help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all channels found in the ChannelsCSC folder")
parser.add_argument('-channel', default=25, type=int, help='channel number (if empty list [] then all channels of patient are analyzed)')
parser.add_argument('--queries-to-compare', nargs = 3, action='append', default=[], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
parser.add_argument('-tmin', default=-0.5, type=float, help='crop window')
parser.add_argument('-tmax', default=1, type=float, help='crop window')
parser.add_argument('-baseline', default=(None, None), type=str, help='Baseline to apply as in mne: (a, b), (None, b), (a, None) or None')
parser.add_argument('-SOA', default=500, help='SOA in design [msec]')
parser.add_argument('-word-ON-duration', default=250, help='Duration for which word word presented in the RSVP [msec]')
parser.add_argument('--baseline-mode', choices=['mean', 'ratio', 'logratio', 'percent', 'zscore', 'zlogratio'], default='zscore', help='Type of baseline method')
parser.add_argument('--remove-outliers', action="store_true", default=False, help='Remove outliers based on percentile 25 and 75')
parser.add_argument('--path2figures', default=[], help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all channels found in the ChannelsCSC folder")
parser.add_argument('--over-write', default=False, action='store_true', help="If True then file will be overwritten")

# parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[("word_position==1 and block in [2, 4, 6]", "word_position==-1 and block in [2, 4, 6]")], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
args = parser.parse_args()
args.patient = 'patient_' + args.patient
if isinstance(args.baseline, str):
    args.baseline = eval(args.baseline)

pprint(args)



probes = data_manip.get_probes2channels(args.patient)

# 
plt.close('all')
if args.micro_macro == 'micro':
    if not isinstance(args.channel, int):
        filename = args.patient + '-tfr.h5'
    else:
        filename = args.patient + '_micro_*_ch_' + str(args.channel) + '-tfr.h5'
elif args.micro_macro == 'macro':
    probe_based_on_ch_num = [p for p in set(probes.keys())-set(['MICROPHONE']) if args.channel in probes[p]['macro']]
    assert len(probe_based_on_ch_num) == 1
    filename = args.patient + '_macro_' + probe_based_on_ch_num[0] + '_1_2-tfr.h5'


path2epochs = os.path.join('..', '..', '..', 'Data', 'UCLA', args.patient, 'Epochs')
print('Loading: %s' % os.path.join(path2epochs, filename))
filenames = glob.glob(os.path.join(path2epochs, filename))
assert len(filenames)==1
path2epochs = filenames[0]

if not args.path2figures:
    args.path2figures = os.path.join('..', '..', '..', 'Figures', args.patient, 'ERPs')
if not os.path.exists(args.path2figures):
    os.makedirs(args.path2figures)

print('Loading epochs object: ' + path2epochs)
epochsTFR = mne.time_frequency.read_tfrs(path2epochs)
print(epochsTFR[0])
print('Apply baseline:')
epochsTFR = epochsTFR[0]
epochsTFR.apply_baseline(args.baseline, mode=args.baseline_mode, verbose=True)

#condition_names = [c_name for (c_name, _, _) in args.queries_to_compare]
n = len(args.queries_to_compare)

# crop
if args.tmin is not None and args.tmax is not None:
    epochsTFR.crop(args.tmin, args.tmax)
else:
    epochsTFR.crop(min(epochsTFR.times) + 0.1, max(epochsTFR.times) - 0.1)

def get_averaged_power(epochsTFR, IX_ch):
    power_ave = np.average(epochsTFR.data[:, IX_ch, :, :], axis=1)
    # calculate interquartile range
    if args.remove_outliers:
        q25, q75 = percentile(power_ave, 25), percentile(power_ave, 75)
        iqr = q75 - q25
        #print('Percentiles: 25th=%.3f, 75th=%.3f, IQR=%.3f' % (q25, q75, iqr))
        # calculate the outlier cutoff
        cut_off = iqr * 1.5
        lower, upper = np.asarray(q25 - cut_off), np.asarray(q75 + cut_off)
        #print(lower, upper)
        # Put NaNs
        for i, (rw, l, u) in enumerate(zip(power_ave.T, lower, upper)):
            new_rw = scipy.stats.threshold(rw, l, u, np.nan)
            power_ave[i, :] = new_rw

        #power_ave[power_ave > upper] = np.nan
        #power_ave[power_ave < lower] = np.nan
        #print('Identified outliers: %d' % np.sum(power_ave > upper))
        #print('Identified outliers: %d' % np.sum(power_ave < lower))
    return power_ave


def get_median_power(epochsTFR, IX_ch):
    power_median = np.squeeze(np.median(epochsTFR.data[:, IX_ch, :, :], axis=1))
    # calculate interquartile range
    if args.remove_outliers:
        q25, q75 = percentile(power_median.flatten(), 25), percentile(power_median.flatten(), 75)
        iqr = q75 - q25
        print('Percentiles: 25th=%.3f, 75th=%.3f, IQR=%.3f' % (q25, q75, iqr))
        # calculate the outlier cutoff
        cut_off = iqr * 1.5
        lower, upper = np.asarray(q25 - cut_off), np.asarray(q75 + cut_off)
        print(lower, upper)
        # Put NaNs
        power_median[power_median > upper] = np.nan
        power_median[power_median < lower] = np.nan
        print('Identified outliers: %d' % np.sum(power_median > upper))
        print('Identified outliers: %d' % np.sum(power_median < lower))
    return power_median

#colors_dict = {}
#colors_dict[condition_names[0]] = '#ff966c'
#if n>1:
#    colors_dict[condition_names[1]] = '#7094b7'
#    for i in range(2, n):
#        colors_dict[condition_names[i]] = np.random.rand(3,)

for ch_name in epochsTFR.ch_names:
    # Check if output fig file already exists: 
    str_comparison = '_'.join([tup[0] for tup in args.queries_to_compare])
    filename_base = 'high_gamma_evoked_' + args.patient + '_ch_' + str(args.channel) + '_' + ch_name + '_' + str_comparison
    fig_fn = os.path.join(args.path2figures, filename_base + '.png') 
    if not os.path.exists(os.path.join(path2epochs, fig_fn)) or args.over_write:
         # Plot ERPs only for args.queries_to_compare:
        evoked_dict = dict()
        #color_dict = dict()
        #fix, ax = plt.subplots(figsize=(10, 10))
        colors_dict = {}
        for i, (condition_name, query, color) in enumerate(args.queries_to_compare):
            colors_dict[condition_name] = color # colors are taken from functions/comparisons.py
            IX_ch = mne.pick_channels(epochsTFR.ch_names, [ch_name])[0]
            power_ave = get_averaged_power(epochsTFR[query], IX_ch)
            power_ave = np.expand_dims(power_ave, axis=1)
            #power_median = get_median_power(epochsTFR[query], IX_ch)
            #curr_info = epochsTFR[query].info
            #curr_info['dig'] = {'kind':'FIFFV_POINT_EXTRA', 'r':[-38, -57, -13], 'identint':1, 'coord_frameint':'FIFFV_COORD_HEAD'}
            # Take MEDIAN not MEAN (robust to outliers)
            curr_condition_epochs = mne.EpochsArray(power_ave, epochsTFR.info, tmin=np.min(epochsTFR.times))
            #averaged_TFR = mne.EvokedArray(np.median(power_ave, axis=0, keepdims=True), info=curr_info, tmin=np.min(epochsTFR[query].times))
            #ax.plot(epochsTFR.times, 1e3*np.squeeze(np.median(power_ave, axis=0)), label=condition_name)
            #q25, q75 = percentile(power_ave, 25, axis=0), percentile(power_ave, 75, axis=0)
            #ax.fill_between(epochsTFR.times, q25, q75, alpha=0.8)
            evoked_dict[condition_name] = list(curr_condition_epochs.iter_evoked())
        #ax.set_xlabel('Time (s)', fontsize=16)
        #ax.set_ylabel('mV', fontsize=16)
        #ax.set_title(epochsTFR.info['chs'][0]['ch_name'], fontsize=16)
        print([k for k in evoked_dict.keys()])
        fig = mne.viz.plot_compare_evokeds(evoked_dict, show=False, colors=colors_dict, picks=[0])
        #fig = mne.viz.plot_compare_evokeds(evoked_dict, picks=['seeg'], show=False, colors=colors_dict)
        #plt.axvline(x=0, ls='--', color='k')
        #plt.axhline(y=0, color='k')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
        plt.subplots_adjust(right=0.6)

        # SAVE:
        plt.savefig(fig_fn)
        print('fig saved to: ' + os.path.join(args.path2figures, filename_base + '.png'))
        plt.close('All')
