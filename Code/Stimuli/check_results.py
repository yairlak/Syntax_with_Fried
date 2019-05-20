import pickle
stimuli = pickle.load(open('coordination_embedding.pkl', 'rb'))
and_ = [1 for s in stimuli if s['conj']=='and']
that_ = [1 for s in stimuli if s['conj']=='that']
and_ = [1 for s in stimuli if s['conj']=='and']
N1_pro = [1 for s in stimuli if s['N1_type']=='pronoun']
N1_full = [1 for s in stimuli if s['N1_type']=='full-noun']
N1_singular = [1 for s in stimuli if s['N1_number']=='singular']
N1_plural = [1 for s in stimuli if s['N1_number']=='plural']
N1_male = [1 for s in stimuli if s['N1_gender']=='male']
N1_female = [1 for s in stimuli if s['N1_gender']=='female']
N2_pro = [1 for s in stimuli if s['N2_type']=='pronoun']
N2_full = [1 for s in stimuli if s['N2_type']=='full-noun']
N2_singular = [1 for s in stimuli if s['N2_number']=='singular']
N2_plural = [1 for s in stimuli if s['N2_number']=='plural']
N2_male = [1 for s in stimuli if s['N2_gender']=='male']
N2_female = [1 for s in stimuli if s['N2_gender']=='female']
print('Number of stimuli: ', len(stimuli))
print('Number of coordinations and embeddings resepectively', sum(and_), sum(that_))
print('N1_pro', sum(N1_pro), 'N1_full', sum(N1_full), 'N1_sing',sum(N1_singular), 'N1_plural', sum(N1_plural), 'N1_male', sum(N1_male), 'N1_female', sum(N1_female))
print(sum(N2_pro), sum(N2_full), sum(N2_singular), sum(N2_plural), sum(N2_male), sum(N2_female))
