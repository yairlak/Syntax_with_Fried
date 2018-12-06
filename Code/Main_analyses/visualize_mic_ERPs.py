from SU_functions import load_settings_params, load_data, read_logs_and_comparisons, convert_to_mne, analyses_single_unit, analyses_electrodes, generate_plots
import matplotlib.pyplot as plt
import os, sys, argparse
import mne
mne.set_log_level('CRITICAL') # DEBUG, INFO, WARNING, ERROR, or CRITICAL
plt.switch_backend('agg')

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

parser = argparse.ArgumentParser(description='Microphone ERPs')
parser.add_argument('-p', '--patient', type=str, help='Patient, e.g., patient_479, patient_482')
parser.add_argument('-c', '--channel', type=int, action='append', help='Which channels to analyze')
parser.add_argument('-b', '--block', type=int, action='append', help='Which blocks to analyze')
parser.add_argument('-n', '--comparison', type=int, action='append', help='Which comparisons from the paragism to contrast')
parser.add_argument('--do-ablation', action='store_true', default=False)

# Argparse
args = parser.parse_args()
patient = args.patient
channels = args.channel
blocks = args.block

print('Loading settings, params and preferences...')
settings = load_settings_params.Settings(patient)
params = load_settings_params.Params()
preferences = load_settings_params.Preferences()

settings.comparisons = args.comparison

print('Metadata: Loading features and comparisons from Excel files...')
comparison_list, features = read_logs_and_comparisons.load_comparisons_and_features(settings)
comparisons = read_logs_and_comparisons.extract_comparison(comparison_list, features, settings, preferences)
comparisons = [comp for c, comp in enumerate(comparisons) if c in settings.comparisons] # run only a subset of comparisons

print('Logs: Reading experiment log files from experiment...')
log_all_blocks = []
for block in blocks:
    log = read_logs_and_comparisons.LogSingleUnit(settings, block) # Get log filename according to block number
    log_all_blocks.append(log.read_and_parse_log(settings))
del log, block

print('Loading POS tags for all words in the lexicon')
word2pos = read_logs_and_comparisons.load_POS_tags(settings)

print('Preparing meta-data')
metadata = read_logs_and_comparisons.prepare_metadata(log_all_blocks, features, word2pos, settings, params, preferences)

print('Generating event object for MNE from log data...')
events, events_spikes, event_id = convert_to_mne.generate_events_array(log_all_blocks, metadata, word2pos, settings, params, preferences)

#print('Loading electrode names for all channels...')
#electrode_names = load_data.electrodes_names(settings)

print('Plottoing paradigm timings')
generate_plots.plot_paradigm_timings(events_spikes, event_id, settings, params)

##### Single-unit analyses (generate rasters) #####
if preferences.analyze_micro_single:
    analyses_single_unit.generate_raster_plots(events_spikes, event_id, metadata, comparisons, settings, params, preferences)

##### Micro and macro electrodes analyses (Generates time-frequency plots) #####
if preferences.analyze_micro_raw:
    analyses_electrodes.generate_time_freq_plots(channels, events, event_id, metadata, comparisons, settings, params, preferences)
