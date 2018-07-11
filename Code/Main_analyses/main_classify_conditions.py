from SU_functions import load_settings_params, read_logs_and_comparisons, auxilary_functions, classification
import os, sys, pickle

patients = ['patient_479', 'patient_482']
patients = ['patient_482']
if len(sys.argv) > 1:
    print 'Channel ' + sys.argv[1]
    ch = int(sys.argv[1])
    channels = range(ch, ch + 1, 1)
else:
    channels = range(49, 57)

print('Loading settings, params and preferences...')
settings = load_settings_params.Settings()
params = load_settings_params.Params()
preferences = load_settings_params.Preferences()

print('Metadata: Loading features and comparisons from Excel files...')
comparison_list, features = read_logs_and_comparisons.load_comparisons_and_features(settings)
comparisons = read_logs_and_comparisons.extract_comparison(comparison_list, features, settings, preferences)

print('Loop over all comparisons: prepare & save data for classification')
for i, comparison in enumerate(comparisons):
    settings.patients = patients
    settings.channels = channels
    epochs_all_queries = classification.get_multichannel_epochs_for_all_current_conditions(comparison, settings, preferences)
    classification.plot_generalizing_estimator(epochs_all_queries, comparison, settings)
