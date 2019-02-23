from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, convert_to_mne, analyses_single_unit, analyses_electrodes, generate_plots
import matplotlib.pyplot as plt
import os
import mne
import argparse
mne.set_log_level('CRITICAL') # DEBUG, INFO, WARNING, ERROR, or CRITICAL
plt.switch_backend('agg')


parser = argparse.ArgumentParser(description='Extract features (e.g., high-gamma power) from raw data and save to data folder')
parser.add_argument('-p', '--patient', type=str, help='patient number (e.g., patient_479)')
parser.add_argument('-c', '--channel', type=int, help='Channel number to process')
parser.add_argument('-l', '--fmin', type=int, help='lower frequency of band filtering')
parser.add_argument('-h', '--fmax', type=int, help='higher frequency of band filtering')
parser.add_argument('-b', '--band', type=str, help='string for frquency band')
args = parser.parse_args()
channel = args.channel
band = args.band

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

print('Loading settings, params and preferences...')
settings = load_settings_params.Settings(args.patient)
settings.channel = channel
params = load_settings_params.Params()
preferences = load_settings_params.Preferences()

print('Metadata: Loading features from Excel files...')
_, features = read_logs_and_comparisons.load_comparisons_and_features(settings)

print('Logs: Reading experiment log files from experiment...')
log_all_blocks = []
for block in range(1, 7):
    log = read_logs_and_comparisons.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))
del log, block

print('Loading POS tags for all words in the lexicon')
word2pos = read_logs_and_comparisons.load_POS_tags(settings)

print('Preparing meta-data')
metadata = read_logs_and_comparisons.prepare_metadata(log_all_blocks, features, word2pos, settings, params, preferences)

print('Generating event object for MNE from log data...')
events, events_spikes, event_id = convert_to_mne.generate_events_array(metadata, params)

print('Loading CSC raw data...')
raw_CSC_data_in_mat, settings = load_data.micro_electrodes_raw(settings)
print 'Analyzing high-gamma for channel ' + str(channel)
# Line filter and resample, or load from file
file_name_epochs = 'micro_' + settings.hospital + '_' + settings.patient + '_channel_' + str(
    channel) + '_line_filtered_resampled-epo'

print('Generating MNE raw object for continuous data...')
raw = convert_to_mne.generate_mne_raw_object(raw_CSC_data_in_mat, settings, params)

#print('Line filtering...')
#raw.notch_filter(params.line_frequency, filter_length='auto', phase='zero')

print('Epoching data...')
epochs = mne.Epochs(raw, events, event_id, params.tmin, params.tmax, metadata=metadata, baseline=None,
                        preload=True)
print(epochs)

print('Original sampling rate:', epochs.info['sfreq'], 'Hz')
epochs.resample(params.downsampling_sfreq, npad='auto')
print('New sampling rate:', epochs.info['sfreq'], 'Hz')

del raw, raw_CSC_data_in_mat

print('Time-frequency analyses...')
print('Band: ' + band)

print('Contrast: ' + 'contrast_name')
# str_blocks = ['block == {} or '.format(block) for block in eval(comparison['blocks'])]
# str_blocks = '(' + ''.join(str_blocks)[0:-4] + ')'
# if comparison['align_to'] == 'FIRST':
#     str_align = 'word_position == 1'
# elif comparison['align_to'] == 'LAST':
#     str_align = 'word_position == sentence_length'
# elif comparison['align_to'] == 'END':
#     str_align = 'word_position == -1'
# elif comparison['align_to'] == 'EACH':
#     str_align = 'word_position > 0'
#
# for query_cond, label_cond in zip(comparison['query'], comparison['cond_labels']):
file_name_root = band + '_' + settings.patient
file_name = file_name_root + '_' + '_channel_' + str(settings.channel) + settings.channel_name

for key_sort in preferences.sort_according_to_key:
    file_name += '_' + key_sort + 'Sorted'

IX1 = settings.channel_name.find('_0019')
if IX1 == -1:
    IX1 = settings.channel_name.find('.ncs')
probe_name = settings.channel_name[0:IX1 - 1]

with open(os.path.join(settings.path2output, settings.patient, 'HighGamma', file_name_root + '.txt'), 'w') as f:
    stimuli_of_curr_query = list(set(list(metadata.query(query_cond)['sentence_string'])))
    stimuli_of_curr_query = [l+'\n' for l in stimuli_of_curr_query]
    f.writelines(stimuli_of_curr_query)

if (not os.path.isfile(
        os.path.join(settings.path2figures, settings.patient, 'HighGamma', probe_name,
                     file_name + '.png'))) or settings.overwrite_existing_output_files:

    query_baseline = query_cond + ' and word_position == 1 and ' + str_blocks
    _, _, baseline = average_high_gamma(epochs[query_baseline], band,
                                                 fmin, fmax, params.freq_step, None,
                                                 'trial_wise', params)

    query = query_cond + ' and ' + str_align + ' and ' + str_blocks
    if not comparison['align_to'] == 'EACH':
        power, power_ave, _ = average_high_gamma(epochs[query],
                                                          band,
                                                          fmin, fmax, params.freq_step,
                                                          baseline,
                                                          'trial_wise', params)
    else:
        power, power_ave, _ = average_high_gamma(epochs[query],
                                                          band,
                                                          fmin, fmax, params.freq_step,
                                                          [],
                                                          'no_baseline', params)

    if preferences.save_features_for_classification:
        epochs_power = epochs[query].copy()
        epochs_power.times = power.times
        epochs_power._data = power_ave
        epochs_power.metadata = epochs[query].metadata


        plot_and_save_high_gamma(epochs_power, comparison['align_to'], eval(comparison['blocks']),
                                          probe_name, file_name,
                                          settings, params, preferences)
        epochs_power._data = np.expand_dims(power_ave, axis=1) # To be compatible with MNE functions: add a middle singelton dimenstion for number of channels
        file_name = 'Feature_matrix_' + band + '_' + settings.patient + '_channel_' + str(
                settings.channel) + '_' + query

        with open(os.path.join(settings.path2output, settings.patient,
                               'feature_matrix_for_classification', file_name + '.pkl'), 'wb') as f:
            pickle.dump([epochs_power, query, settings, params, preferences], f)

        print('Save to: ' + file_name)
else:
    print('File already exists')