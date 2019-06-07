import argparse, os
from functions import comparisons
#'Metadata query for training classes(e.g., word_position==1),\n metadata is word-based (events are word onsets) and contains the following keys:\n\nevent_time (in samples)\n\nsentence_number (integer)\n\nsentence_string (although each event corresponds to a word, the entire string of the sentence is stored for each event)\n\nword_position (integer representing the word position; -1 for the end of the sentence)\n\nword_string (str)\n\n pos (str: RBR, NN, TO, VB, VBZ, RBS, IN, VBN, PRP, POS, CD, VBP, PDT, WRB, JJR, NNP, MD, WP, RB, EX, PRP$, JJS, VBD, NNS, JJ, RP, DT, VBG, LS, WDT, CC, UH, FW\nnum_words (although each event corresponds to a word, the num_words of the entire sentence is stored for each event)\nlast_word (True/False)\n'

parser = argparse.ArgumentParser(description='Generate plots for TIMIT experiment')
#parser.add_argument('-r', '--root-path', default='/home/yl254115/Projects/intracranial/single_unit/Syntax_with_Fried/', help='Path to parent project folder')
parser.add_argument('-r', '--root-path', default='/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/', help='Path to parent project folder')
parser.add_argument('-c', '--comparisons', action='append', default=[], help='List of integers correspond to comparisons. If empty then all will be run')
parser.add_argument('-p', '--patients', action='append', help='patient label (e.g., 479, 487)')
parser.add_argument('-s', '--hospitals', action='append', help='list of hospital per patient')
parser.add_argument('-k', '--picks', action='append', help='List of lists (per patient) of channels to pick. Either a string ("all" (for all channels) or roi (e.g., "STG") or channel numbers as integers')
parser.add_argument('--cat-k-timepoints', type=int, default=1, help='How many time points to concatenate before classification')
args = parser.parse_args()

# Set current working directory to that of script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

args.patients = ['patient_'+p for p in args.patients]
if not args.hospitals:
    args.hospitals = ['UCLA' for _ in args.patients]
if not args.picks:
    args.picks = ['all' for _ in args.patients]

print(args)

comparisons = comparisons.comparison_list()

if not args.comparisons:
    args.comparisons = range(len(comparisons))

for c, comparison in comparisons.items():
    if c in [int(s) for s in args.comparisons]:
        #cmd = 'nohup python GAT.py -r %s --train-queries "%s" --train-queries "%s"' % (args.root_path, comparison['train_queries'][0], comparison['train_queries'][1])
        cmd = 'python GAT.py -r %s --train-queries "%s" --train-queries "%s"' % (args.root_path, comparison['train_queries'][0], comparison['train_queries'][1])
        if 'test_queries' in comparison:
            cmd += ' --test-queries "%s" --test-queries "%s"' % (comparison['test_queries'][0], comparison['test_queries'][1])

        for patient, hospital, pick in zip(args.patients, args.hospitals, args.picks):
            cmd += ' -s %s -p %s -k %s' % (hospital, patient, pick)
        cmd += ' --cat-k-timepoints %i' % args.cat_k_timepoints
        
        fname = comparison['name'] + "_patients_" + '_'.join([s.split('_')[1] for s in args.patients]) + '_cat-k_' + str(args.cat_k_timepoints)
        cmd += ' --output-filename %s' % fname

        #cmd += ' > Logs_GAT/%s.log 2>&1 &' % (comparison['name'] + '_cat-k_' + str(args.cat_k_timepoints))
        print(cmd)
        os.system(cmd)
