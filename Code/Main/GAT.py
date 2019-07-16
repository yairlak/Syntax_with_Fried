import argparse, os
import mne
from functions import classification

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
# parser.add_argument('-r', '--root-path', default='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/', help='Path to parent project folder')
parser.add_argument('-r', '--root-path', default='/home/yl254115/Projects/intracranial/single_unit/Syntax_with_Fried/', help='Path to parent project folder. If empty list then assumes epochsTFRs are stored in Data/UCLA/patient/Epochs')
parser.add_argument('--train-queries', action='append', help='Metadata query for training classes(e.g., word_position==1),\n metadata is word-based (events are word onsets) and contains the following keys:\n\nevent_time (in samples)\n\nsentence_number (integer)\n\nsentence_string (although each event corresponds to a word, the entire string of the sentence is stored for each event)\n\nword_position (integer representing the word position; -1 for the end of the sentence)\n\nword_string (str)\n\n pos (str: RBR, NN, TO, VB, VBZ, RBS, IN, VBN, PRP, POS, CD, VBP, PDT, WRB, JJR, NNP, MD, WP, RB, EX, PRP$, JJS, VBD, NNS, JJ, RP, DT, VBG, LS, WDT, CC, UH, FW\nnum_words (although each event corresponds to a word, the num_words of the entire sentence is stored for each event)\nlast_word (True/False)\n')
parser.add_argument('--test-queries', action='append', default=None, help="Metadata query for generalization test (e.g., word_position==1, word_string in ['END']")
parser.add_argument('-p', '--patients', action='append', help='patient label (e.g., 479, 487)')
parser.add_argument('-s', '--hospitals', action='append', help='list of hospital per patient')
parser.add_argument('--picks-micro', action='append', help='List of lists (per patient) of channels to pick. Either a string ("all" (for all channels) or roi (e.g., "STG") or channel numbers as integers')
parser.add_argument('--picks-macro', action='append', help='List of lists (per patient) of channels to pick. Either a string ("all" (for all channels) or roi (e.g., "STG") or channel numbers as integers')
parser.add_argument('--picks-spike', action='append', help='List of lists (per patient) of channels to pick. Either a string ("all" (for all channels) or roi (e.g., "STG") or channel numbers as integers')
parser.add_argument('-o', '--output-filename', type=str, help='Output filename')
parser.add_argument('--cat-k-timepoints', type=int, default=1, help='How many time points to concatenate before classification')

print(mne.__version__)
args = parser.parse_args()
print(args)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


# 1. Prepare data based on queries
classification_data = classification.prepare_data_for_GAT(args)


# 2. Train-test GAT
time_gen, scores = classification.train_test_GAT(classification_data)

# 3. Plot GAT
fig1, fig2 = classification.plot_GAT(classification_data['times'], time_gen, scores)

# 4. Save to png
fig1.savefig(os.path.join('..', '..', 'Figures', 'Decoding', args.output_filename + '_GAT_diag.png'))
fig2.savefig(os.path.join('..', '..', 'Figures', 'Decoding', args.output_filename + '_GAT.png'))
print('Figures saved to: ' + os.path.join('..', '..', 'Figures', 'Decoding', args.output_filename + '_GAT_*.png'))

