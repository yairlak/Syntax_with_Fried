import argparse, os
from functions import load_settings_params, read_logs_and_features, convert_to_mne, data_manip, analyses


parser = argparse.ArgumentParser(description='Generate MNE-py epochs object for a specific frequency band for all channels.')
parser.add_argument('-patient', default='patient_487', help='Patient string')
parser.add_argument('-channels', nargs = 1, action='append', default=[], help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all channels found in the ChannelsCSC folder")
args = parser.parse_args()

# Paths
# path2data = os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'ChannelsCSC')
path2epochs = os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'Epochs')
if not os.path.exists(path2epochs):
    os.makedirs(path2epochs)

print('Loading settings, params and preferences...')
settings = load_settings_params.Settings(args.patient)
params = load_settings_params.Params()
preferences = load_settings_params.Preferences()

print('Metadata: Loading features and comparisons from Excel files...')
features = read_logs_and_features.load_features(settings)

print('Logs: Reading experiment log files from experiment...')
log_all_blocks = []
for block in range(1, 7):
    log = read_logs_and_features.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))
del log, block
print(log_all_blocks)

print('Loading POS tags for all words in the lexicon')
word2pos = read_logs_and_features.load_POS_tags(settings)

print('Preparing meta-data')
metadata = read_logs_and_features.prepare_metadata(log_all_blocks, features, word2pos, settings, params, preferences)

print('Generating event object for MNE from log data...')
events, events_spikes, event_id = convert_to_mne.generate_events_array(metadata, params)

print('Analyze channels')
channel_nums = data_manip.get_channel_nums(settings.path2rawdata_mat) if not args.channels else args.channels
channel_nums.sort()
for c, channel_num in enumerate(channel_nums):
    channel_data, channel_name = data_manip.load_channelsCSC_data(settings.path2rawdata_mat, channel_num)
    settings.channel_name = channel_name
    epochs_power_curr_channel = analyses.compute_time_freq(channel_num, channel_name, channel_data, events, event_id, metadata, settings, params)
    epochs_power_all_channels = epochs_power_curr_channel.copy() if c == 0 else epochs_power_all_channels.add_channels([epochs_power_curr_channel])

# Save epochs object to drive
filename = args.patient + '-epo.fif'
epochs_power_all_channels.save(os.path.join(path2epochs, filename))
print('Epochs object saved to: ' + os.path.join(path2epochs, filename))
