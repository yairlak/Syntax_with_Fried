fn = '../../../sentences_Eng_rand_En02.txt'
with open(fn, 'r') as f:
    sents = f.readlines()

for i, sent in enumerate(sents):
    sent = sent.strip().strip('?')
    sent = sent.strip('.').upper()
    fn_lab = '%i.lab' % (i+1)
    with open(fn_lab, 'w') as f_temp:
        f_temp.write(sent+'\n')
    print(sent)
