import argparse, os
import mne
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
#arser.add_argument('-i', '--path2epochs', default='/neurospin/unicog/protocols/intracranial/TIMIT_syntax/Data/EC33/Epochs/EC33-epo.fif', help='Path to parent project folder')
#arser.add_argument('-o', '--path2figures', default='/neurospin/unicog/protocols/intracranial/TIMIT_syntax/Figures/EC33/ERPs', help='Path to parent project folder')
#parser.add_argument('-q', '--query', default="word_string in ['END']", help='Metadata query (e.g., word_position==1)')
parser.add_argument('-i', '--path2epochs', default='/neurospin/unicog/protocols/intracranial/TIMIT_syntax/Data/EC33/Epochs/EC33_from_epoched_mat-epo.fif', help='Path to parent project folder')
parser.add_argument('-o', '--path2figures', default='/volatile/TIMIT_syntax/Figures', help='Path to parent project folder')
parser.add_argument('-q', '--query', default="word_position==1", help='Metadata query (e.g., word_position==1)')
parser.add_argument('--queries-to-compare', nargs = 2, action='append', default=[], help="Pairs of condition-name and a metadata query. For example, --queries-to-compare FIRST_WORD word_position==1 --queries-to-compare LAST_WORD word_string in ['END']")

args = parser.parse_args()
print(args)
# patient = args.patient

# path2epochs = os.path.join(args.root_path, 'Data', patient, 'Epochs')
# path2figures = os.path.join(args.root_path, 'Figures', patient, 'ERPs')
if not os.path.exists(args.path2figures):
    os.makedirs(args.path2figures)

print('Loading epochs object')
# epochs_fname = os.path.join(args.path2epochs, patient + '-epo.fif')
epochs = mne.read_epochs(args.path2epochs)

for ch in range(150,256):
    # Plot all trials and ERP for args.query
    fig, ax = plt.subplots(figsize=(10, 10))
    curr_epochs = epochs[args.query]#.drop_bad()
    IX = np.argsort(curr_epochs.metadata['num_words'].values)
    curr_epochs.plot_image(picks=[ch], order=IX, show=False)
    filename = 'high_gamma_epochs_ch_' + str(ch + 1) + '_' + args.query + '.png'
    plt.savefig(os.path.join(args.path2figures, filename))
    print('fig saved to: ' + os.path.join(args.path2figures, filename))
    plt.close(fig)

    if not args.queries_to_compare:
        # Plot ERPs only for args.queries_to_compare
        evoked_dict = dict()
        for (condition_name, query) in args.queries_to_compare:
            evoked_dict[condition_name] = epochs[query].average(picks=[ch])
        mne.viz.plot_compare_evokeds(evoked_dict)
