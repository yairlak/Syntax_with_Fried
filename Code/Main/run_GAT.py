import argparse, os
import mne
from functions import classification

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
parser.add_argument('-r', '--root-path', default='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/', help='Path to parent project folder')
#parser.add_argument('-r', '--root-path', default='/home/yl254115/Projects/single_unit_syntax', help='Path to parent project folder. If empty list then assumes epochsTFRs are stored in Data/UCLA/patient/Epochs')
#parser.add_argument('--query-class-train', default="word_string in ['END'] and num_words == 3", help='Metadata query (e.g., word_position==1)')
parser.add_argument('--train-queries', action='append', help='Metadata query for training classes(e.g., word_position==1),\n metadata is word-based (events are word onsets) and contains the following keys:\n\nevent_time (in samples)\n\nsentence_number (integer)\n\nsentence_string (although each event corresponds to a word, the entire string of the sentence is stored for each event)\n\nword_position (integer representing the word position; -1 for the end of the sentence)\n\nword_string (str)\n\n pos (str: RBR, NN, TO, VB, VBZ, RBS, IN, VBN, PRP, POS, CD, VBP, PDT, WRB, JJR, NNP, MD, WP, RB, EX, PRP$, JJS, VBD, NNS, JJ, RP, DT, VBG, LS, WDT, CC, UH, FW\nnum_words (although each event corresponds to a word, the num_words of the entire sentence is stored for each event)\nlast_word (True/False)\n')
parser.add_argument('--test-queries', action='append', default=None, help="Metadata query for generalization test (e.g., word_position==1, word_string in ['END']")
parser.add_argument('-p', '--patients', action='append', help='patient label (e.g., 479, 487)')
parser.add_argument('-s', '--hospitals', action='append', help='list of hospital per patient')
parser.add_argument('-k', '--picks', action='append', help='List of lists (per patient) of channels to pick. Either a string ("all" (for all channels) or roi (e.g., "STG") or channel numbers as integers')

print(mne.__version__)
args = parser.parse_args()
print(args)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


# 1. Prepare data
classification_data = classification.prepare_data_for_GAT(args.patients, args.hospitals, args.picks,
                                                           args.train_queries, args.test_queries,
                                                           args.root_path)

# 1.1 Change classification data to have k subsequent time points
k = 5
classification_data = classification.cat_subsequent_timepoints(k, classification_data)



# 2. Train-test GAT
time_gen, scores = classification.train_test_GAT(X_train_query, y_train_query, X_test_query, y_test_query)

# 3. Plot GAT
fig1, fig2 = classification.plot_GAT(times, time_gen, scores)

# 4. Save to png
if args.test_queries is not None:
    fname = "_".join(args.patients) + "_train_" + "_".join(args.train_queries) + "_test_" + "_".join(args.test_queries)
else:
    fname = "_".join(args.patients) + "_train_" + "_".join(args.train_queries)

fig1.savefig(os.path.join('..', '..', 'Figures', 'Decoding', fname + '_GAT_diag.png'))
fig2.savefig(os.path.join('..', '..', 'Figures', 'Decoding', fname + '_GAT.png'))
print('Figures saved to: ' + os.path.join('..', '..', 'Figures', 'Decoding', fname + '_GAT_*.png'))

#    CC coordinating conjunction
#    CD cardinal digit
#    DT determiner
#    EX existential there (like: “there is” … think of it like “there exists”)
#    FW foreign word
#    IN preposition/subordinating conjunction
#    JJ adjective ‘big’
#    JJR adjective, comparative ‘bigger’
#    JJS adjective, superlative ‘biggest’
#    LS list marker 1)
#    MD modal could, will
#    NN noun, singular ‘desk’
#    NNS noun plural ‘desks’
#    NNP proper noun, singular ‘Harrison’
#    NNPS proper noun, plural ‘Americans’
#    PDT predeterminer ‘all the kids’
#    POS possessive ending parent’s
#    PRP personal pronoun I, he, she
#    PRP$ possessive pronoun my, his, hers
#    RB adverb very, silently,
#    RBR adverb, comparative better
#    RBS adverb, superlative best
#    RP particle give up
#    TO, to go ‘to’ the store.
#    UH interjection, errrrrrrrm
#    VB verb, base form take
#    VBD verb, past tense took
#    VBG verb, gerund/present participle taking
#    VBN verb, past participle taken
#    VBP verb, sing. present, non-3d take
#    VBZ verb, 3rd person sing. present takes
#    WDT wh-determiner which
#    WP wh-pronoun who, what
#    WP$ possessive wh-pronoun whose
#    WRB wh-abverb where, when
