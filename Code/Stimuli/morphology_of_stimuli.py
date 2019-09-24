import sys
sys.path.insert(1, '../Main/functions')
import read_logs_and_features as rlf
import load_settings_params
settings = load_settings_params.Settings('patient_479_11')
features = rlf.load_features(settings)
sentences = features['fields'][1][1::]
print(sentences)
vocab = []
[vocab.extend(s.strip().strip('?').split(' ')) for s in sentences]
vocab = list(set(vocab))
print(vocab)
print('Num words: %i' % len(vocab))

morpheme_dict = {}
for w in vocab:
    if w.endswith('s'):
        morpheme = 's'
    elif w.endswith('ed'):
        morpheme = 'ed'
    elif w.endswith('es'):
        morpheme = 'es'
    elif w.endswith('ing'):
        morpheme = 'ing'
    elif w.endswith('y'):
        morpheme = 'y'
    else:
        morpheme = ''
    morpheme_dict[w] = morpheme
    print(w, morpheme)

morphemes = morpheme_dict.keys()


