import argparse, os
from functions import load_settings_params, read_logs_and_features, convert_to_mne, data_manip, analyses_single_unit
from mne.io import _merge_info
import numpy as np
from pprint import pprint

parser = argparse.ArgumentParser(description='Generate MNE-py epochs object for a specific frequency band for all channels.')
parser.add_argument('-patient', default='502', help='Patient string')
parser.add_argument('-channels', action='append', default=list(range(97)), help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all channels found in the ChannelsCSC folder")
parser.add_argument('-blocks', type=int, default=[1, 2, 3, 4, 5, 6], nargs='+', help='Which blocks to analyze')
parser.add_argument('-tmin', default=-3, type=int, help='Patient string')
parser.add_argument('-tmax', default= 3, type=int, help='Patient string')
parser.add_argument('--out-fn', default=[], help='Output filename for Epochs object')
parser.add_argument('--overwrite', default=False, action='store_true', help="If True then file will be overwritten")
args = parser.parse_args()


# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# check if output filename already exists
args.patient = 'patient_' + args.patient
ch_str = '_ch_' + '_'.join(map(str, args.channels)) if args.channels else ''
filename = args.patient + ch_str + '-tfr.h5' if not args.out_fn else args.out_fn
path2epochs = os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'Epochs')

print(args)
#TODO: add log to power

# Paths
if not os.path.exists(path2epochs):
    os.makedirs(path2epochs)

print('Loading settings, params and preferences...')
settings = load_settings_params.Settings(args.patient)
params = load_settings_params.Params(args.patient)
preferences = load_settings_params.Preferences()
params.tmin=settings.tmin if not args.tmin else args.tmin
params.tmax=settings.tmax if not args.tmax else args.tmax

# Get channels
args.channels = sorted(data_manip.get_channel_nums(settings.path2rawdata_mat)) if not args.channels else args.channels

pprint(preferences.__dict__); pprint(settings.__dict__); pprint(params.__dict__)

print('Metadata: Loading features and comparisons from Excel files...')
features = read_logs_and_features.load_features(settings)

print('Logs: Reading experiment log files from experiment...')
log_all_blocks = {}
for block in args.blocks:
    log = read_logs_and_features.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks[block] = log.read_and_parse_log(settings)
del log, block
print(log_all_blocks)

print('Loading POS tags for all words in the lexicon')
word2pos = read_logs_and_features.load_POS_tags(settings)

print('Preparing meta-data')
metadata = read_logs_and_features.prepare_metadata(log_all_blocks, features, word2pos, settings, params, preferences)

print('Generating event object for MNE from log data...')
_, events_spikes, _, event_id = convert_to_mne.generate_events_array(metadata, params)

print('Analyze channels')
path2ChannelCSC = os.path.join(settings.path2rawdata, 'micro', 'ChannelsCSC')
with open(os.path.join(path2ChannelCSC, 'channel_numbers_to_names.txt')) as f_channel_names:
    channel_names = f_channel_names.readlines()

for ch in args.channels:
    channel_name = [l.strip('\n').split('\t')[1] for l in channel_names][ch]
    filename = args.patient + '_epochs_spikes_ch_' + str(ch) + '.fif' if not args.out_fn else args.out_fn
    if not os.path.exists(os.path.join(path2epochs, filename)) or args.over_write:
        epochs_spikes = analyses_single_unit.generate_epochs_spikes(ch, channel_name, events_spikes, event_id, metadata, settings, params, preferences)
        if len(epochs_spikes) > 0:
            epochs_spikes.save(os.path.join(path2epochs, filename))
            print('Epochs object saved to: ' + os.path.join(path2epochs, filename))
    else:
        print('File already exists (choose flag --overwrite if needed): ' + os.path.join(path2epochs, filename))
