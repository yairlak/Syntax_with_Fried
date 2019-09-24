nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_position==1 and block in [2, 4, 6]" --train-queries "word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_first_last_word_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_position==-1 and sentence_length==2 and block in [2, 4, 6]" --train-queries "word_position==-1 and sentence_length==5 and block in [2, 4, 6]" > Logs_GAT/gat_sentence_length_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='NN' or pos=='NNS' and block in [2, 4, 6]" --train-queries "pos=='VBP' or pos=='VBZ' and block in [2, 4, 6]" > Logs_GAT/gat_nouns_verbs_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='NN' and block in [2, 4, 6]" --train-queries "pos=='NNS' and block in [2, 4, 6]" > Logs_GAT/gat_grammatical_number_nouns_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='VBZ' and block in [2, 4, 6]" --train-queries "pos=='VBP' and block in [2, 4, 6]" > Logs_GAT/gat_grammatical_number_verbs_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='VBZ' and block in [2, 4, 6]" --train-queries "pos=='VBP' and block in [2, 4, 6]" --test-queries "pos=='NN' and block in [2, 4, 6]" --test-queries "pos=='NNS' and block in [2, 4, 6]" > Logs_GAT/gat_grammatical_number_verbs2nouns_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --test-queries "pos=='VBZ' and block in [2, 4, 6]" --test-queries "pos=='VBP' and block in [2, 4, 6]" --train-queries "pos=='NN' and block in [2, 4, 6]" --train-queries "pos=='NNS' and block in [2, 4, 6]" > Logs_GAT/gat_grammatical_number_nouns2verbs_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "Declarative==1 and word_position==-1 and block in [2, 4, 6]" --train-queries "Question==1 and word_position==-1 and block in [2, 4, 6]" > Logs_GAT/gat_declarative_question_audio.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_position==1 and block in [1, 3, 5]" --train-queries "word_position==-1 and block in [1, 3, 5]" > Logs_GAT/gat_first_last_word_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_position==-1 and sentence_length==2 and block in [1, 3, 5]" --train-queries "word_position==-1 and sentence_length==5 and block in [1, 3, 5]" > Logs_GAT/gat_sentence_length_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='NN' or pos=='NNS' and block in [1, 3, 5]" --train-queries "pos=='VBP' or pos=='VBZ' and block in [1, 3, 5]" > Logs_GAT/gat_nouns_verbs_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='NN' and block in [1, 3, 5]" --train-queries "pos=='NNS' and block in [1, 3, 5]" > Logs_GAT/gat_grammatical_number_nouns_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='VBZ' and block in [1, 3, 5]" --train-queries "pos=='VBP' and block in [1, 3, 5]" > Logs_GAT/gat_grammatical_number_verbs_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='VBZ' and block in [1, 3, 5]" --train-queries "pos=='VBP' and block in [1, 3, 5]" --test-queries "pos=='NN' and block in [1, 3, 5]" --test-queries "pos=='NNS' and block in [1, 3, 5]" > Logs_GAT/gat_grammatical_number_verbs2nouns_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --test-queries "pos=='VBZ' and block in [1, 3, 5]" --test-queries "pos=='VBP' and block in [1, 3, 5]" --train-queries "pos=='NN' and block in [1, 3, 5]" --train-queries "pos=='NNS' and block in [1, 3, 5]" > Logs_GAT/gat_grammatical_number_nouns2verbs_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "Declarative==1 and word_position==-1 and block in [1, 3, 5]" --train-queries "Question==1 and word_position==-1 and block in [1, 3, 5]" > Logs_GAT/gat_declarative_question_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='NN' and block in [1, 3, 5]" --train-queries "pos=='NNS' and block in [1, 3, 5]" --test-queries "pos=='NN' and block in [2, 4, 6]" --test-queries "pos=='NNS' and block in [2, 4, 6]" > Logs_GAT/gat_grammatical_number_nouns_visual2auditory.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --test-queries "pos=='NN' and block in [2, 4, 6]" --test-queries "pos=='NNS' and block in [2, 4, 6]" --train-queries "pos=='NN' and block in [1, 3, 5]" --train-queries "pos=='NNS' and block in [1, 3, 5]" > Logs_GAT/gat_grammatical_number_nouns_auditory2visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "pos=='VBZ' and block in [1, 3, 5]" --train-queries "pos=='VBP' and block in [1, 3, 5]" --test-queries "pos=='VBZ' and block in [2, 4, 6]" --test-queries "pos=='VBP' and block in [2, 4, 6]" > Logs_GAT/gat_grammatical_number_verbs_visual2auditory.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all --test-queries "pos=='VBZ' and block in [2, 4, 6]" --test-queries "pos=='VBP' and block in [2, 4, 6]" --train-queries "pos=='VBZ' and block in [1, 3, 5]" --train-queries "pos=='VBP' and block in [1, 3, 5]" > Logs_GAT/gat_grammatical_number_verbs_auditory2visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all --train-queries "pos=='VBZ' and block in [1, 3, 5]" --train-queries "pos=='VBP' and block in [1, 3, 5]" --test-queries "pos=='NN' and block in [2, 4, 6]" --test-queries "pos=='NNS' and block in [2, 4, 6]" > Logs_GAT/gat_grammatical_number_verbsvisual2nounauditory.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all --train-queries "pos=='VBZ' and block in [2, 4, 6]" --train-queries "pos=='VBP' and block in [2, 4, 6]" --test-queries "pos=='NN' and block in [1, 3, 5]" --test-queries "pos=='NNS' and block in [1, 3, 5]" > Logs_GAT/gat_grammatical_number_verbsauditory2nounsvisual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all --train-queries "pos=='NN' and block in [1, 3, 5]" --train-queries "pos=='NNS' and block in [1, 3, 5]" --test-queries "pos=='VBZ' and block in [2, 4, 6]" --test-queries "pos=='VBP' and block in [2, 4, 6]" > Logs_GAT/gat_grammatical_number_nounsvisual2verbsauditory.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all --train-queries "pos=='NN' and block in [2, 4, 6]" --train-queries "pos=='NNS' and block in [2, 4, 6]" --test-queries "pos=='VBZ' and block in [1, 3, 5]" --test-queries "pos=='VBP' and block in [1, 3, 5]" > Logs_GAT/gat_grammatical_number_nounsauditory2verbsvisual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all --train-queries "pos in ['NN', 'NNS', 'PRP'] and block in [1, 3, 5]" --train-queries "pos in ['VBP', 'VBZ', 'VBD', 'VBG', 'VBN'] and block in [1, 3, 5]" > Logs_GAT/gat_nouns_verbs_visual.log 2>&1 &

nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all -s UCLA -p patient_482 -k all --train-queries "pos in ['NN', 'NNS', 'PRP'] and block in [2, 4, 6]" --train-queries "pos in ['VBP', 'VBZ', 'VBD', 'VBG', 'VBN'] and block in [2, 4, 6]" > Logs_GAT/gat_nouns_verbs_auditory.log 2>&1 &

