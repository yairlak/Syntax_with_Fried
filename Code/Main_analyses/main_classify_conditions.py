from SU_functions import load_settings_params, read_logs_and_comparisons, auxilary_functions, classification
import os, sys, pickle

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

patients = ['patient_479', 'patient_482']
channels = [range(1, 129), range(1, 77)]

#patients = ['patient_482']
#channels = [range(1, 77)]

#patients = ['patient_479']
#channels = [range(1, 129)]

if len(sys.argv) > 1:
    print 'Channel ' + sys.argv[1]
    comp = int(sys.argv[1])-1
else:
    comp = 0

print('Loading settings, params and preferences...')
settings = load_settings_params.Settings()
params = load_settings_params.Params()
preferences = load_settings_params.Preferences()

print('Metadata: Loading features and comparisons from Excel files...')
comparison_list, features = read_logs_and_comparisons.load_comparisons_and_features(settings)
comparisons = read_logs_and_comparisons.extract_comparison(comparison_list, features, settings, preferences)

# Run a single comparison from argument given from outside (for parallel)
comparisons = [comparison for i, comparison in enumerate(comparisons) if i == comp]

print('Loop over all comparisons: prepare & save data for classification')
for i, comparison in enumerate(comparisons):
    settings.patients = patients
    settings.channels = channels
    epochs_all_queries, stimuli_of_curr_query = classification.get_multichannel_epochs_for_all_current_conditions(comparison, settings, preferences)
    classification.plot_generalizing_estimator(epochs_all_queries, comparison, settings)