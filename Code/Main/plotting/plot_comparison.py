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
parser.add_argument('-r', '--root-path', default='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/', help='Path to parent project folder')
parser.add_argument('--comparisons', default=[], action='append', required=True, help='comparison number from comparisons.py file.')
parser.add_argument('--patient', action='append', required=True, help='Add patient.')
parser.add_argument('--signal-type', choices=['micro','macro', 'spike'], required=True, help='electrode type')
parser.add_argument('--probe-names', action='append', default=[], help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all probe names found in the Epochs folder")
# Figure setting:
parser.add_argument('--run-gat', action="store_true", default=False)
parser.add_argument('--run-erps', action="store_true", default=False)
parser.add_argument('--print-only', action="store_true", default=False, help='Dont execute commands. Print only')
parser.add_argument('--dont-overwrite', default=False, action='store_true', help="If True then file will be overwritten")
args = parser.parse_args()

'''
Launches ERPs (--run-erps) or GAT (--run-gat) plot generation, for a given PATIENT, PROBE NAME and SIGNAL-TYPE (micro/macro/spike).

'''
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
    # Get probes from all patients. Returns a dict. Each key is a probe name whose value is a dict:
    # micro: list of lists (per patient), with channel number that correspond to probe. macro: same. patients: which patients have this probe.
    probes = data_manip.get_probes2channels(['patient_'+p for p in args.patient])
    pprint(probes)
    for probe in list(set(probes['probe_names'].keys())-set(['MICROPHONE']))+['all']:
        if (probe in args.probe_names) or (not args.probe_names): # FILTER PROBES IF USER CHOSES
            # MKDIR (Figures folder)
            print(comparison_name_str, "_".join(['patient_'+p for p in args.patient]), probe, args.signal_type)
            ########
            # ERPs #
            ########
            if args.run_erps:
                for p, patient in enumerate(args.patient):
                    path2figures = os.path.join(rootpath2figures, comparison_name_str, 'patient_'+patient, probe, args.signal_type)
                    if not os.path.exists(path2figures):
                            os.makedirs(path2figures)
                    if probe!='all':
                        for ch in probes['probe_names'][probe][args.signal_type][p]:
                            if args.signal_type == 'spike':
                                script_fn = 'plot_evoked_comparison_rasters.py'
                                micro_macro = ''
                            else:
                                script_fn = 'plot_evoked_comparison.py'
                                micro_macro = ' --micro-macro %s' % args.signal_type
                            cmd = 'python %s --path2figures %s --patient %s%s --channel %i --comparison %s' % (script_fn, path2figures, patient, micro_macro, ch, c)
                            print(cmd)
                            print('-'*80)
                            if not args.print_only:
                                os.system(cmd)
                            if (args.signal_type == 'macro') & (ch == 1): # ONLY ONE CHANNEL FROM MACRO, since the biploar of macro 1_2 is usually of most interest
                                break
            ########
            # GAT  #
            ########
            if args.run_gat:
                path2figures_all_patients = os.path.join(rootpath2figures, comparison_name_str, "_".join(['patient'] + args.patient), probe, args.signal_type)
                if not os.path.exists(path2figures_all_patients):
                    os.makedirs(path2figures_all_patients)
                # Build command with basic args
                cmd_decode = 'python ../decoding/GAT.py --cat-k-timepoint 1 --path2figures %s' % (path2figures_all_patients)
                # Add train/test queries to GAT command
                cmd_decode += ' -r %s --train-queries "%s" --train-queries "%s"' % (args.root_path, comparison['train_queries'][0], comparison['train_queries'][1])
                if 'test_queries' in comparison:
                    cmd_decode += ' --test-queries "%s" --test-queries "%s"' % (comparison['test_queries'][0], comparison['test_queries'][1])
                # Add probe selection to GAT command
                IX_signal_type = ['micro', 'macro', 'spike'].index(args.signal_type)
                picks_list = ['none']*3
                picks_list[IX_signal_type] = probe
                for patient in args.patient:
                    cmd_decode += ' -s %s -p %s --picks-micro %s --picks-macro %s --picks-spike %s' % ('UCLA', 'patient_'+patient, picks_list[0], picks_list[1], picks_list[2])
                fname = comparison['name'] + "_patients_" + '_'.join(args.patient) + '_mic_'+ picks_list[0] + '_mac_' + picks_list[1] + '_spi_' + picks_list[2]
                cmd_decode += ' --output-filename %s' % fname
                if args.dont_overwrite:
                    cmd_decode += ' --dont-overwrite'
                print(cmd_decode)
                print('-'*80)
                if not args.print_only:
                    os.system(cmd_decode)
