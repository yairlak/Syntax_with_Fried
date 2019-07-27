import argparse, os, glob
import mne
import matplotlib.pyplot as plt
import numpy as np
from numpy import percentile
from sklearn import linear_model
from sklearn.metrics import r2_score
from operator import itemgetter
from pprint import pprint

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
parser.add_argument('-patient', default='505', help='Patient string')
parser.add_argument('-block', choices=['visual','auditory', '1', '2', '3', '4', '5', '6', []], default='auditory', help='Block type')
parser.add_argument('--micro-macro', choices=['micro','macro'], default='micro', help='electrode type')
parser.add_argument('--probe-name', default='LSTG', help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all channels found in the ChannelsCSC folder")
parser.add_argument('-channel', default=25, type=int, help='channel number (if empty list [] then all channels of patient are analyzed)')
#parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[["num_letters=2", "word_position>0 and num_letters==2 and block in [1, 3, 5]"], ["num_letters=2", "word_position>0 and num_letters==2 and block in [1, 3, 5]"], ["num_letters=3", "word_position>0 and num_letters==3 and block in [1, 3, 5]"], ["num_letters=4", "word_position>0 and num_letters==4 and block in [1, 3, 5]"], ["num_letters=5", "word_position>0 and num_letters==5 and block in [1, 3, 5]"], ["num_letters=6", "word_position>0 and num_letters==6 and block in [1, 3, 5]"], ["num_letters=7", "word_position>0 and num_letters==7 and block in [1, 3, 5]"], ["num_letters=8", "word_position>0 and num_letters==8 and block in [1, 3, 5]"], ["num_letters=9", "word_position>0 and num_letters==9 and block in [1, 3, 5]"], ["num_letters=10", "word_position>0 and num_letters==10 and block in [1, 3, 5]"]],
#                    help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[["Short words", "word_position>0 and num_letters<5 and block in [1, 3, 5]"], ["Intermediate", "word_position>0 and (num_letters>=5 or num_letters<9) and block in [1, 3, 5]"], ["Long words", "word_position>0 and num_letters>=9 and block in [1, 3, 5]"]],
                    help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
parser.add_argument('-tmin', default=-0.3, type=float, help='crop window')
parser.add_argument('-tmax', default=0.5, type=float, help='crop window')
parser.add_argument('-baseline', default=(None, None), type=str, help='Baseline to apply as in mne: (a, b), (None, b), (a, None) or None')
parser.add_argument('-SOA', default=500, help='SOA in design [msec]')
parser.add_argument('-word-ON-duration', default=250, help='Duration for which word word presented in the RSVP [msec]')
parser.add_argument('--baseline-mode', choices=['mean', 'ratio', 'logratio', 'percent', 'zscore', 'zlogratio'], default='zscore', help='Type of baseline method')
parser.add_argument('--remove-outliers', action="store_true", default=False, help='Remove outliers based on percentile 25 and 75')

# parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[("word_position==1 and block in [2, 4, 6]", "word_position==-1 and block in [2, 4, 6]")], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")
args = parser.parse_args()
args.patient = 'patient_' + args.patient
if isinstance(args.baseline, str):
    args.baseline = eval(args.baseline)

pprint(args)

# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# 
plt.close('all')
if args.micro_macro == 'micro':
    if not isinstance(args.channel, int):
        filename = args.patient + '-tfr.h5'
    else:
        filename = args.patient + '_micro_*_ch_' + str(args.channel) + '-tfr.h5'
elif args.micro_macro == 'macro':
    filename = args.patient + '_macro_' + args.probe_name + '_1_2-tfr.h5'


path2epochs = os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'Epochs')
filenames = glob.glob(os.path.join(path2epochs, filename))
assert len(filenames)==1
path2epochs = filenames[0]

path2figures = os.path.join('..', '..', 'Figures', args.patient, 'ERPs')
if not os.path.exists(path2figures):
    os.makedirs(path2figures)

print('Loading epochs object: ' + path2epochs)
epochsTFR = mne.time_frequency.read_tfrs(path2epochs)
print(epochsTFR[0])
print('Apply baseline:')
epochsTFR = epochsTFR[0]
epochsTFR.apply_baseline(args.baseline, mode=args.baseline_mode, verbose=True)

# crop
if args.tmin is not None and args.tmax is not None:
    epochsTFR.crop(args.tmin, args.tmax)
else:
    epochsTFR.crop(min(epochsTFR.times) + 0.1, max(epochsTFR.times) - 0.1)

def get_averaged_power(epochsTFR, IX_ch):
    power_ave = np.squeeze(np.average(epochsTFR.data[:, IX_ch, :, :], axis=1))
    # calculate interquartile range
    if args.remove_outliers:
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
        print('Identified outliers: %d' % np.sum(power_ave > upper))
        print('Identified outliers: %d' % np.sum(power_ave < lower))
    return power_ave

for ch, ch_name in enumerate(epochsTFR.ch_names):
     # Plot ERPs only for args.queries_to_compare
    evoked_dict = dict()
    for (condition_name, query) in args.queries_to_compare:
        IX_ch = mne.pick_channels(epochsTFR.ch_names, [ch_name])[0]
        power_ave = get_averaged_power(epochsTFR[query], IX_ch)
        curr_info = epochsTFR[query].info
        curr_info['dig'] = {'kind':'FIFFV_POINT_EXTRA', 'r':[-38, -57, -13], 'identint':1, 'coord_frameint':'FIFFV_COORD_HEAD'}
        averaged_TFR = mne.EvokedArray(np.mean(power_ave, axis=0, keepdims=True), info=curr_info, tmin=np.min(epochsTFR[query].times))
        evoked_dict[condition_name] = averaged_TFR
    fig = mne.viz.plot_compare_evokeds(evoked_dict, picks=['seeg'], show=False)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
    plt.subplots_adjust(right=0.6)


    str_comparison = '_'.join([tup[0] for tup in args.queries_to_compare])
    filename_base = 'high_gamma_evoked_ch_' + str(args.channel) + '_' + ch_name + '_' + str_comparison
    plt.savefig(os.path.join(path2figures, filename_base + '.png'))
    print('fig saved to: ' + os.path.join(path2figures, filename_base + '.png'))
    plt.close('All')