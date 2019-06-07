import argparse, os
from functions import load_settings_params, read_logs_and_features, convert_to_mne, data_manip, analyses
from mne.io import _merge_info
import numpy as np
from pprint import pprint

parser = argparse.ArgumentParser(description='Generate MNE-py epochs object for a specific frequency band for all channels.')
parser.add_argument('-patient', default='502', help='Patient string')
parser.add_argument('-channels', action='append', default=[], help="Channels to analyze and merge into a single epochs object (e.g. -c 1 -c 2). If empty then all channels found in the ChannelsCSC folder")
parser.add_argument('-blocks', type=int, default=[1, 2, 3, 4, 5, 6], nargs='+', help='Which blocks to analyze')
parser.add_argument('-tmin', default=-3, type=int, help='Patient string')
parser.add_argument('-tmax', default= 3, type=int, help='Patient string')
parser.add_argument('--out-fn', default=[], help='Output filename for Epochs object')
parser.add_argument('--iter-freqs', default=[], help="frequency band in load_setting_params iter_freqs = [('High-Gamma', 70, 150, 5)]")
parser.add_argument('--over-write', default=False, action='store_true', help="If True then file will be overwritten")
args = parser.parse_args()

# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# check if output filename already exists
args.patient = 'patient_' + args.patient
ch_str = '_ch_' + '_'.join(args.channels) if args.channels else ''
filename = args.patient + ch_str + '-tfr.h5' if not args.out_fn else args.out_fn
path2epochs = os.path.join('..', '..', 'Data', 'UCLA', args.patient, 'Epochs')

if not os.path.exists(os.path.join(path2epochs, filename)) or args.over_write:
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

    if args.iter_freqs:
        params.iter_freqs = eval(args.iter_freqs)

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
    events, events_spikes, event_id = convert_to_mne.generate_events_array(metadata, params)

    print('Analyze channels')
    channel_nums = data_manip.get_channel_nums(settings.path2rawdata_mat) if not args.channels else args.channels
    channel_nums.sort()
    for c, channel_num in enumerate(channel_nums):
        channel_data, channel_name = data_manip.load_channelsCSC_data(settings.path2rawdata_mat, channel_num)
        settings.channel_name = channel_name
        epochsTFR_channel = analyses.compute_time_freq(channel_num, channel_name, channel_data, events, event_id, metadata, settings, params)

        if c == 0:
            epochsTFR_all_channels = epochsTFR_channel.copy()
        else:
            data = [inst._data for inst in [epochsTFR_all_channels] + [epochsTFR_channel]]
            infos = [epochsTFR_all_channels.info] + [epochsTFR_channel.info]
            new_info = _merge_info(infos, force_update_to_first=False)
            # Now update the attributes
            epochsTFR_all_channels._data = np.concatenate(data, axis=1)
            epochsTFR_all_channels.info = new_info


    # Save epochs object to drive
    del epochsTFR_channel
    epochsTFR_all_channels.save(os.path.join(path2epochs, filename), overwrite=True)
    print('Epochs object saved to: ' + os.path.join(path2epochs, filename))
else:
    print('File already exists (choose flag --over-write if needed): ' + os.path.join(path2epochs, filename))
