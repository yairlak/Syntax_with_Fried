import argparse, os, glob, re, sys
# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
sys.path.append('..')
from functions import load_settings_params, read_logs_and_features, convert_to_mne, data_manip, analyses
from mne.io import _merge_info
import numpy as np
from pprint import pprint

parser = argparse.ArgumentParser(description='Generate MNE-py epochs object for a specific frequency band for all channels.')
parser.add_argument('--patient', default='479_11', help='Patient string')
parser.add_argument('--probe-names', default=[], help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all channels found in the ChannelsCSC folder")
parser.add_argument('--blocks', type=int, default=[1, 2, 3, 4, 5, 6], nargs='+', help='Which blocks to analyze')
parser.add_argument('--tmin', default=-3, type=int, help='Patient string')
parser.add_argument('--tmax', default= 3, type=int, help='Patient string')
parser.add_argument('--out-fn', default=[], help='Output filename for Epochs object')
parser.add_argument('--iter-freqs', default=[], help="frequency band in load_setting_params iter_freqs = [('High-Gamma', 70, 150, 5)]")
parser.add_argument('--contact-pairs', default=[(0, 1), (1, 2), (2, 3)], help="List of tuples for which bi-polar ref will be made. [(0, 1), (1, 2)] means that two inner most ref channels will be generated.")
parser.add_argument('--over-write', default=True, action='store_false', help="If True then file will be overwritten")
parser.add_argument('--path2epochs', default=[], help='Output folder where epochs will be saved')
args = parser.parse_args()


# check if output filename already exists
args.patient = 'patient_' + args.patient
if not args.path2epochs:
    path2epochs = os.path.join('..', '..', '..', 'Data', 'UCLA', args.patient, 'Epochs')
    #path2epochs = os.environ['TMPDIR']
else:
    path2epochs = args.path2epochs

path2raw_macro = os.path.join('..', '..', '..', 'Data', 'UCLA', args.patient, 'Raw', 'macro', 'ncs')
if not args.probe_names:
    ncs_files = glob.glob(os.path.join(path2raw_macro, '*.ncs'))
    args.probe_names = list(set([re.split('(\d+)', os.path.basename(f))[0] for f in ncs_files]))

# Paths
if not os.path.exists(path2epochs):
    os.makedirs(path2epochs)

print('Loading settings, params and preferences...')
settings = load_settings_params.Settings(args.patient)
params = load_settings_params.Params(args.patient)
preferences = load_settings_params.Preferences()
params.tmin=settings.tmin if not args.tmin else args.tmin
params.tmax=settings.tmax if not args.tmax else args.tmax

if args.iter_freqs:
    params.iter_freqs = eval(args.iter_freqs)

pprint(preferences.__dict__); pprint(settings.__dict__); pprint(params.__dict__)

print('Metadata: Loading features and comparisons from Excel files...')
features = read_logs_and_features.load_features(settings)

print('Logs: Reading experiment log files from experiment...')
log_all_blocks = {}
for block in args.blocks:
    log = read_logs_and_features.read_log(block, settings)
    log_all_blocks[block] = log

print('Loading POS tags for all words in the lexicon')
word2pos = read_logs_and_features.load_POS_tags(settings)

print('Preparing meta-data')
metadata = read_logs_and_features.prepare_metadata(log_all_blocks, features, word2pos, settings, params, preferences)

print('Generating event object for MNE from log data...')
_, _, events_macro, event_id = convert_to_mne.generate_events_array(metadata, params)

print(args.probe_names)
for probe_name in args.probe_names:
    #TODO: add log to power
    macro_data_all_4_channels = data_manip.load_macro_data(os.path.join(settings.path2rawdata), probe_name)
    for channel_pair in args.contact_pairs:
        if len(macro_data_all_4_channels[channel_pair[0]])>0 and len(macro_data_all_4_channels[channel_pair[1]])>0: # make sure channels are not empty
            macro_data = macro_data_all_4_channels[channel_pair[1]] - macro_data_all_4_channels[channel_pair[0]]
            settings.channel_name = '%s_%i_%i' % (probe_name, channel_pair[0]+1, channel_pair[1]+1)
            filename = args.patient + '_macro_' + settings.channel_name + '-tfr.h5' if not args.out_fn else args.out_fn
            if not os.path.exists(os.path.join(path2epochs, filename)) or args.over_write:
                print(args)
                print('Analyze channels')
                epochsTFR_channel = analyses.compute_time_freq(probe_name, probe_name, macro_data, 'macro', events_macro, event_id, metadata, settings, params)
                # Save epochs object to drive
                epochsTFR_channel.save(os.path.join(path2epochs, filename), overwrite=True)
                print('Epochs object saved to: ' + os.path.join(path2epochs, filename))
            else:
                print('-'*100)
                print('!!!!---File already exists (choose flag --over-write if needed): ' + os.path.join(path2epochs, filename))
                print('-'*100)
        else:
            print('-'*100)
            print('Macro data is empty')
            print('-'*100)
