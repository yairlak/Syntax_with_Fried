import argparse, os, glob, sys
# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append('..')
from pprint import pprint
from functions import comparisons, data_manip, load_settings_params

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
# What to plot:
parser.add_argument('--comparisons', default=[], action='append',  help='comparison number from comparisons.py file.')
parser.add_argument('--patients', action='append', default=[], help='Patient string')
parser.add_argument('--signal-type', action='append', nargs=1,  choices=['micro','macro', 'spike'], default=[], help='electrode type')
parser.add_argument('--probe-names', action='append', nargs=1, default=[], help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all probe names found in the Epochs folder")
parser.add_argument('-channels', action='append', nargs='+', default=[], type=int, help='channel number (if empty list [] then all channels of patient are analyzed)')
# Figure setting:
parser.add_argument('--sort-key', default=['sentence_length'], help='Keys to sort according')
parser.add_argument('-tmin', type=float, default=-2.5, help='crop window')
parser.add_argument('-tmax', type=float, default=0.5, help='crop window')
parser.add_argument('-baseline', default=(None, None), type=str, help='Baseline to apply as in mne: (a, b), (None, b), (a, None) or None')
parser.add_argument('-SOA', default=500, help='SOA in design [msec]')
parser.add_argument('-word-ON-duration', default=250, help='Duration for which word word presented in the RSVP [msec]')
parser.add_argument('-y-tick-step', default=25, type=int, help='If sorted by key, set the yticklabels density')
parser.add_argument('-window-st', default=50, type=int, help='Regression start-time window [msec]')
parser.add_argument('-window-ed', default=450, type=int, help='Regression end-time window [msec]')
parser.add_argument('-vmin', default=-1.5, help='vmin of plot (default is in zscore, assuming baseline is zscore)')
parser.add_argument('-vmax', default=1.5, help='vmax of plot (default is in zscore, assuming baseline is zscore')
parser.add_argument('--baseline-mode', choices=['mean', 'ratio', 'logratio', 'percent', 'zscore', 'zlogratio'], default='zscore', help='Type of baseline method')
parser.add_argument('--remove-outliers', action="store_true", default=False, help='Remove outliers based on percentile 25 and 75')
parser.add_argument('--dont-regress', action="store_false", default=True, help='Remove outliers based on percentile 25 and 75')
parser.add_argument('--run-gat', action="store_true", default=False, help='Remove outliers based on percentile 25 and 75')
parser.add_argument('--run-erps', action="store_true", default=False, help='Remove outliers based on percentile 25 and 75')
args = parser.parse_args()

# What to do in case of input of empty lists (default)
if not args.patients:
    args.patients = ['479_11']
if not args.signal_type:
    for p in args.patients: # ALL signal types will be analyzed for ALL chosen patients. 
        args.signal_type.append(['micro', 'macro', 'spike'])
if not args.probe_names: # create a list of empty lists (i.e., all probes will be analyzed)
    for p in args.patients:
        args.probe_names.append([])
if not args.channels:
    for p in args.patients:
        args.channels.append([])

# Santiy checks
assert len(args.patients) == len(args.signal_type)
assert len(args.patients) == len(args.probe_names)
assert len(args.patients) == len(args.channels)

if isinstance(args.sort_key, str):
    args.sort_key = eval(args.sort_key)
if isinstance(args.baseline, str):
    args.baseline = eval(args.baseline)

pprint(args)

comparisons = comparisons.comparison_list()

if not args.comparisons:
    args.comparisons = range(len(comparisons))
print('Comparisons :')
print(args.comparisons)

rootpath2figures = '../../../Figures/Comparisons/'
for c in args.comparisons:
    comparison = comparisons[int(c)]
    if 'colors' not in comparison.keys(): # if no color info for current comparison in function/comparisons.py then fill-in default colors
        comparison['colors'] = ['r', 'g']        
    comparison_name_str = c + '_' + comparison['name']
    for p, patient in enumerate(args.patients):
        settings = load_settings_params.Settings('patient_'+patient)
        probes = data_manip.get_probes2channels('patient_'+patient)
        pprint(probes)
        for probe in set(probes.keys())-set(['MICROPHONE']):
            if probe in args.probe_names[p] or not args.probe_names[p]:
                for signal_type in args.signal_type[p]:
                    # MKDIR (Figures folder)
                    path2figures = os.path.join(rootpath2figures, comparison_name_str, 'patient_'+patient, probe, signal_type)
                    if not os.path.exists(path2figures):
                            os.makedirs(path2figures)
                    #########
                    # MICRO #
                    #########
                    if 'micro' in signal_type:
                        if args.run_erps:
                            for ch in probes[probe]['micro']:
                                cmd_micro = 'python plot_evoked_comparison.py --path2figures %s -patient %s --micro-macro %s -channel %i' % (path2figures, patient, 'micro', ch)
                                for condition_name, query, color in zip(comparison['train_condition_names'], comparison['train_queries'], comparison['colors']):
                                    cmd_micro += ' --queries-to-compare %s "%s" %s' % (condition_name, query, color)
                                if 'test_queries' in comparison:
                                    for condition_name, query, color in zip(comparison['test_condition_names'], comparison['test_queries'], comparison['colors']):
                                        cmd_micro += ' --queries-to-compare %s "%s" %s' % (condition_name, query, color)
                                print(cmd_micro)
                                os.system(cmd_micro)
                                print('-'*80)
                        if args.run_gat:
                            cmd_decode = 'python ../decoding/run_GAT.py -p %s --cat-k-timepoint 1 -c %s --picks-micro %s --picks-macro none --picks-spike none --path2figures %s' % (patient, c, probe, path2figures)
                            print(cmd_decode)
                            os.system(cmd_decode)
                            print('-'*80)
                    #########
                    # MACRO # 
                    #########
                    if 'macro' in signal_type:
                        if args.run_erps:
                            if probes[probe]['macro']:
                                ch = probes[probe]['macro'][0] # ONLY ONE CHANNEL FROM MACRO, since the biploar of macro 1_2 is usually of most interest
                                cmd_macro = 'python plot_evoked_comparison.py --path2figures %s -patient %s --micro-macro %s -channel %i' % (path2figures, patient, 'macro', ch)
                                for condition_name, query, color in zip(comparison['train_condition_names'], comparison['train_queries'], comparison['colors']):
                                    cmd_macro += ' --queries-to-compare %s "%s" %s' % (condition_name, query, color)
                                if 'test_queries' in comparison:
                                    for condition_name, query, color in zip(comparison['test_condition_names'], comparison['test_queries'], comparison['colors']):
                                        cmd_macro += ' --queries-to-compare %s "%s" %s' % (condition_name, query, color)
                                print(cmd_macro)
                                os.system(cmd_macro)
                                print('-'*80)
                        if args.run_gat:
                            cmd_decode = 'python ../decoding/run_GAT.py -p %s --cat-k-timepoint 1 -c %s --picks-micro none --picks-macro %s --picks-spike none --path2figures %s' % (patient, c, probe, path2figures)
                            print(cmd_decode)
                            os.system(cmd_decode)
                            print('-'*80)
                    ##########
                    # SPIKES #
                    ##########
                    if 'spike' in signal_type:
                        channels_with_spikes = data_manip.get_channels_with_spikes_from_combinato_sorted_h5(settings, ['pos']) # TODO: fox 'neg' case
                        channels_with_spikes = [sublist[0] for sublist in channels_with_spikes if (sublist[2]>0)|(sublist[3]>0)]
                        if args.run_erps:
                            for ch in sorted(probes[probe]['micro']):
                                if ch in channels_with_spikes:
                                    cmd_spike = 'python plot_evoked_comparison_rasters.py --path2figures %s -patient %s -channel %i' % (path2figures, patient, ch)
                                    for condition_name, query, color in zip(comparison['train_condition_names'], comparison['train_queries'], comparison['colors']):
                                        cmd_spike += ' --queries-to-compare %s "%s" %s' % (condition_name, query, color)
                                    if 'test_queries' in comparison:
                                        for condition_name, query, color in zip(comparison['test_condition_names'], comparison['test_queries'], comparison['colors']):
                                            cmd_spike += ' --queries-to-compare %s "%s" %s' % (condition_name, query, color)
                                    print(cmd_spike)
                                    os.system(cmd_spike)
                                    print('-'*80)
                        if args.run_gat:
                            cmd_decode = 'python ../decoding/run_GAT.py -p %s --cat-k-timepoint 1 -c %s --picks-micro none --picks-macro none --picks-spike %s --path2figures %s' % (patient, c, probe, path2figures)
                            print(cmd_decode)
                            os.system(cmd_decode)
                            print('-'*80)

