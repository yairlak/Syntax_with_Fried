import argparse, os, glob
from pprint import pprint
from functions import comparisons, data_manip

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
# What to plot:
parser.add_argument('--comparisons', default=[], action='append',  help='comparison number from comparisons.py file.')
parser.add_argument('--patients', action='append', default=[], help='Patient string')
parser.add_argument('--signal-type', choices=['micro','macro', 'spike'], default=[], help='electrode type')
parser.add_argument('--probe-name', default=[], help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all probe names found in the Epochs folder")
parser.add_argument('-channels', default=[], type=int, help='channel number (if empty list [] then all channels of patient are analyzed)')
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
args = parser.parse_args()

# What to do in case of input of empty lists (default)
if not args.patients:
    args.patients = ['479_11']
if not args.signal_type:
    for p in args.patients: # ALL signal types will be analyzed for ALL chosen patients. 
        args.signal_type.append(['micro', 'macro', 'spike'])
if not args.probe_name: # create a list of empty lists (i.e., all probes will be analyzed)
    for p in args.patients:
        args.probe_name.append([])
if not args.channels:
    for p in args.patients:
        args.channels.append([])

# Santiy checks
assert len(args.patients) == len(args.signal_type)
assert len(args.patients) == len(args.probe_name)
assert len(args.patients) == len(args.channels)

if isinstance(args.sort_key, str):
    args.sort_key = eval(args.sort_key)
if isinstance(args.baseline, str):
    args.baseline = eval(args.baseline)

#pprint(args)

# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

comparisons = comparisons.comparison_list()

if not args.comparisons:
    args.comparisons = range(len(comparisons))
print('Comparisons :')
print(args.comparisons)

rootpath2figures = '../../Figures/Comparisons/'
for c in args.comparisons:
    comparison = comparisons[int(c)]
    comparison_name_str = c + '_' + comparison['name']
    for p, patient in enumerate(args.patients):
        probes = data_manip.get_probes2channels('patient_'+patient)
        print(probes)
        for probe in set(probes.keys())-set(['MICROPHONE']):
            for signal_type in args.signal_type[p]:
                # MKDIR (Figures folder)
                path2figures = os.path.join(rootpath2figures, comparison_name_str, 'patient_'+patient, probe, signal_type)
                if not os.path.exists(path2figures):
                        os.makedirs(path2figures)
                # MICRO ERPs
                if 'micro' in signal_type:
                    for ch in probes[probe]['micro']:
                        cmd_micro = 'python plot_evoked_comparison.py --path2figures %s -patient %s --micro-macro %s -channel %i --queries-to-compare %s "%s" --queries-to-compare %s "%s"' %\
                                (path2figures, patient, 'micro', ch, comparison['train_condition_names'][0], comparison['train_queries'][0], comparison['train_condition_names'][1], comparison['train_queries'][1])
                        if 'test_queries' in comparison:
                                cmd_micro += ' --queries-to-compare %s "%s" --queries-to-compare %s "%s"' % (comparison['test_condition_names'][0], comparison['test_queries'][0], comparison['test_condition_names'][1], comparison['test_queries'][1])
                        print(cmd_micro)
                        #os.system(cmd_micro)
                        print('-'*80)
                    cmd_decode = 'python run_GAT.py -p %s --cat-k-timepoint 1 -c %s --picks-micro %s --picks-macro none --picks-spike none --path2figures %s' % (patient, c, probe, path2figures)
                    print(cmd_decode)
                    #os.system(cmd_decode)
                    print('-'*80)
                # MACRO ERPs
                if 'macro' in signal_type:
                    if probes[probe]['macro']:
                        ch = probes[probe]['macro'][0] # ONLY ONE CHANNEL FROM MACRO, since only the biploar of macro 1_2 is of interest
                        cmd_macro = 'python plot_evoked_comparison.py --path2figures %s -patient %s --micro-macro %s -channel %i --queries-to-compare %s "%s" --queries-to-compare %s "%s"' % (path2figures, patient, 'macro', ch, comparison['train_condition_names'][0], comparison['train_queries'][0], comparison['train_condition_names'][1], comparison['train_queries'][1])
                        if 'test_queries' in comparison:
                            cmd_macro += ' --queries-to-compare %s "%s" --queries-to-compare %s "%s"' % (comparison['test_condition_names'][0], comparison['test_queries'][0], comparison['test_condition_names'][1], comparison['test_queries'][1])
                        print(cmd_macro)
                        #os.system(cmd_macro)
                        print('-'*80)
                    #cmd_decode = 'python run_GAT.py -p %s --cat-k-timepoint 1 -c %s --picks-micro none --picks-macro %s --picks-spike none --path2figures %s' % (patient, c, probe, path2figures)
                    print(cmd_decode)
                    #os.system(cmd_decode)
                    print('-'*80)
                # RASTERS
                if 'spike' in signal_type:
                    for ch in probes[probe]['micro']:
                        for query in comparison['train_queries']:
                            cmd_spike = 'python plot_rasters.py --path2figures %s -patient %s -channel %i --query "%s"' % (path2figures, patient, ch, query)
                            print(cmd_spike)
                            os.system(cmd_spike)
                            print('-'*80)
                    # DECODING
                    cmd_decode = 'python run_GAT.py -p %s --cat-k-timepoint 1 -c %s --picks-micro none --picks-macro none --picks-spike %s --path2figures %s' % (patient, c, probe, path2figures)
                    print(cmd_decode)
                    #os.system(cmd_decode)
                    print('-'*80)

print(probes.keys())
