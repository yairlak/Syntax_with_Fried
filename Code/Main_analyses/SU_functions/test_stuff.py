import scipy.io as scio
import os
hospital = 'UCLA'
patient = 'patient_480'
path2patient_folder = os.path.join('..', '..', '..', 'Data', hospital, patient)
sentences_start_filename = 'sentences_start_' + patient + '.mat'
data = scio.loadmat(os.path.join(path2patient_folder, sentences_start_filename))

# Beginning of sentences
sent_start = data['sentences_start']
sent_start = [i[0] for i in sent_start]
sentences_start = dict(zip(range(1,len(sent_start)+1, 1), sent_start))

# End of sentences
sent_end = []
for s in sent_start[1::]:
    sent_end.append(s-1)
sent_end.append(508)
sentences_end = dict(zip(range(1,len(sent_end)+1, 1), sent_end))

# Sentence length
sentences_length = [e-s+1 for (s,e) in zip(sent_start, sent_end)]

# Save
import pickle
output_filename = 'sentences_start_end_dict.pkl'
with open(os.path.join(path2patient_folder, output_filename), 'wb') as f:
    pickle.dump(sentences_start, f)
    pickle.dump(sentences_end, f)
    pickle.dump(sentences_length, f)

# Load
import pickle, os
output_filename = 'sentences_start_end_dict.pkl'
with open(os.path.join(path2patient_folder, output_filename), 'r') as f:
    sentences_start = pickle.load(f)
    sentences_end = pickle.load(f)
    sentences_length = pickle.load(f)
