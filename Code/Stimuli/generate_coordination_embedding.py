import random
import numpy as np
from tqdm import tqdm
import argparse
import pickle

parser = argparse.ArgumentParser(description='Stimulus generator: cooridnation vs. embedding')
parser.add_argument('-n', '--num-samples', type=int, default=1, help='How many sentences to sample from each sentence type')
parser.add_argument('-r', '--num-random', type=int, default=10000, help='How many random sentences to generate before filtering')
parser.add_argument('-o', '--output', type=str, default='coordination_embedding.pkl', help='Path to output pickle file')
args = parser.parse_args()

subjects = ['he', 'she', 'they', 'the boy', 'the girl', 'the boys', 'the man', 'the men', 'the woman', 'the women']
verbs_mental = ['think', 'thinks', 'believe', 'believes', 'know', 'knows']
verbs = ['cry', 'cries', 'sneeze', 'sneezes']


subject_features = {'he':['pronoun', 'singular', 'male'],
                    'the boy':['full-noun', 'singular', 'male'],
                    'she':['pronoun', 'singular', 'female'],
                    'the girl':['full-noun', 'singular', 'female'],
                    'the girls':['full-noun', 'plural', 'female'],
                    'they':['pronoun', 'plural', ''],
                    'the boys':['full-noun', 'plural', 'male'],
                    'the man':['full-noun', 'singular', 'male'],
                    'the men':['full-noun', 'plural', 'male'],
                    'the woman':['full-noun', 'singular', 'female'],
                    'the women':['full-noun', 'plural', 'female'],
                    }

verb_features = {'think':['mental', 'plural', 'present'],
                 'thinks':['mental', 'singular', 'present'],
                 'believe':['mental', 'plural', 'present'],
                 'believes':['mental', 'singular', 'present'],
                 'know': ['mental', 'plural', 'present'],
                 'knows': ['mental', 'singular', 'present'],
                 'cry':['unergative', 'plural', 'present'],
                 'cries':['unergative', 'singular', 'present'],
                 'sneeze': ['unergative', 'plural', 'present'],
                 'sneezes': ['unergative', 'singular', 'present'],
                 }

features_to_numbers = {'':0,
                       'pronoun':1,
                       'full-noun':2,
                       'singular':1,
                       'plural':2,
                       'male':1,
                       'female':2,
                       'mental': 1,
                       'unergative':2,
                       'present':2,
                       'and': 1,
                       'that':2
                       }


stimuli = []; features = []
for trial in tqdm(range(args.num_random)):
    for conj in ['and', 'that']:
        # while features_are_not_balanced(cnt_1, cnt_2):
        subj1 = subjects[np.random.choice(len(subjects), 1)]
        verb1 = verbs_mental[np.random.choice(len(verbs_mental), 1)]
        while subject_features[subj1][1] != verb_features[verb1][1]: # check number agreement
            verb1 = verbs_mental[np.random.choice(len(verbs_mental), 1)]
        # second conjunct
        subj2 = subjects[np.random.choice(len(subjects), 1)]
        verb2 = verbs[np.random.choice(len(verbs), 1)]
        while subject_features[subj2][1] != verb_features[verb2][1]: # check number agreement
            verb2 = verbs[np.random.choice(len(verbs), 1)]
        # sentence
        sentence = subj1.capitalize() + ' ' + verb1 + ' ' +  conj + ' ' +  subj2 + ' ' +  verb2 + '.'
        feature_vec = subject_features[subj1] + verb_features[verb1] + [conj] + subject_features[subj2] + verb_features[verb2]
        feature_vec = [features_to_numbers[f] for f in feature_vec]
        curr_stimuli = {'sentence':sentence,
                        'feature_vec':feature_vec,
                        'N1_type':subject_features[subj1][0],
                        'N1_number':subject_features[subj1][1],
                        'N1_gender':subject_features[subj1][2],
                        'V1_type':verb_features[verb1][0],
                        'V1_number':verb_features[verb1][1],
                        'V1_tense': verb_features[verb1][2],
                        'conj':conj,
                        'N2_type': subject_features[subj2][0],
                        'N2_number': subject_features[subj2][1],
                        'N2_gender': subject_features[subj2][2],
                        'V2_type': verb_features[verb2][0],
                        'V2_number': verb_features[verb2][1],
                        'V2_tense': verb_features[verb2][2]
                        }
        stimuli.append(curr_stimuli)

# print(stimuli[0])

# find the unique set of features across all sentences from which to uniformally sample
features = np.asarray([s['feature_vec'] for s in stimuli])
dt = np.dtype([('a', features.dtype), ('b', features.dtype), ('c', features.dtype), ('d', features.dtype), ('e', features.dtype), ('f', features.dtype), ('g', features.dtype), ('h', features.dtype), ('i', features.dtype), ('j', features.dtype), ('k', features.dtype), ('l', features.dtype), ('m', features.dtype)])
y = features.view(dtype=dt).squeeze()
unique_features = np.unique(y, return_index=False, return_inverse=False)
unique_features = unique_features.view((int, len(unique_features.dtype.names)))
dims = np.max(np.vstack(unique_features), axis=0)
num_unique = unique_features.shape[0]
# Filter stimuli
cnt = np.zeros(shape=dims+1)
# print(cnt.shape)
not_all_found = True
filtered_stimuli = []
n=args.num_samples
while len(filtered_stimuli)<n*num_unique:
    indices = [i for i in range(len(stimuli))]
    random.shuffle(indices)
    for index in indices:
        curr_stimulus = stimuli[index]
        curr_features = np.asarray(curr_stimulus['feature_vec'])
        not_already_existing = all([curr_stimulus['sentence'] != s['sentence'] for s in filtered_stimuli])
        correction_factor = 1
        N1_they = False; N2_they = False
        if curr_features[0]==1 and curr_features[1]==2 and curr_features[2]==0: N1_they = True
        if curr_features[7] == 1 and curr_features[8] == 2 and curr_features[9] == 0: N2_they = True
        if N1_they: correction_factor = 2
        # if N1_they and N2_they: correction_factor = 4
        if cnt[tuple(curr_features)] < n*correction_factor and not_already_existing:
            cnt[tuple(curr_features)]+=1
            filtered_stimuli.append(curr_stimulus)
            # print(curr_stimulus['sentence'], len(filtered_stimuli))

with open(args.output, 'wb') as f:
    pickle.dump(filtered_stimuli, f)
print('\n'.join([s['sentence'] for s in filtered_stimuli]))
# print(len(filtered_stimuli),num_unique)