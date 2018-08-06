from SU_functions import load_settings_params, read_logs_and_comparisons, auxilary_functions, classification
import os, sys, math

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

patients = ['patient_479', 'patient_482']
channels = [range(1, 129), range(1, 77)]
#channels = [range(1, 3), range(1, 3)]
#patients = ['patient_482']
#channels = [range(1, 77)]

#patients = ['patient_479']
#channels = [range(1, 129)]

if len(sys.argv) > 1:
    print 'comparison ' + sys.argv[1]
    comp = int(sys.argv[1])-1
else:
    comp = 107

print('Loading settings, params and preferences...')
settings = load_settings_params.Settings('patient_479')
params = load_settings_params.Params()
preferences = load_settings_params.Preferences()

print('Metadata: Loading features and comparisons from Excel files...')
comparison_list, features = read_logs_and_comparisons.load_comparisons_and_features(settings)
all_comparisons_in_xls = read_logs_and_comparisons.extract_comparison(comparison_list, features, settings, preferences)

# Run a single comparison from argument given from outside (for parallel)
comparisons_to_run = [comparison for i, comparison in enumerate(all_comparisons_in_xls) if i == comp][0]

# print('Loop over all comparisons: prepare & save data for classification')
# for i, comparison in enumerate(comparisons_to_run):
print('Generalization across time: %s' % comparisons_to_run['contrast_name'])
settings.patients = patients
settings.channels = channels

queries = auxilary_functions.get_queries(comparisons_to_run)
epochs_all_queries, stimuli_of_curr_query = classification.get_multichannel_epochs_for_all_current_conditions(comparisons_to_run, queries, settings, preferences)
classification.plot_generalizing_estimator(epochs_all_queries, comparison, comp, settings)

# Generalize across modality and/or contrast:
cond1_isnan = comparisons_to_run['generalize_to_blocks'] != comparisons_to_run['generalize_to_blocks']
cond2_isnan = comparisons_to_run['generalize_to_contrast'] != comparisons_to_run['generalize_to_contrast']

if (not cond1_isnan) or (not cond2_isnan):

    if not cond2_isnan:
        j = int(comparisons_to_run['generalize_to_contrast'])
        comparison_to_generalize = [comp for c, comp in enumerate(all_comparisons_in_xls) if c == j][0] # pop the relevant comparison
        queries_generalize_to = auxilary_functions.get_queries(comparison_to_generalize)
    else:
        comparison_to_generalize = comparisons_to_run.copy()
        comparison_to_generalize['blocks'] = comparisons_to_run['generalize_to_blocks']
        comparison_to_generalize['contrast_name'] = 'to blocks: '+ comparisons_to_run['generalize_to_blocks']
        queries_generalize_to = auxilary_functions.get_queries(comparison_to_generalize)

    if not queries_generalize_to == queries:
        print('Generalization across modality and/or contrast: %s --> %s' % (comparisons_to_run['contrast_name'], comparison_to_generalize['contrast_name']))
        epochs_all_queries_to_generalize, _ = classification.get_multichannel_epochs_for_all_current_conditions(comparison_to_generalize, queries_generalize_to, settings, preferences)
        classification.plot_generalizing_estimator_across_modalities(epochs_all_queries, epochs_all_queries_to_generalize, comparisons_to_run, comparison_to_generalize, comp, settings)
