def comparison_list():
    comparisons = {}

# Sanity checks:
    comparisons[0] = {}
    comparisons[0]['name'] = 'first_last_word_audio'
    comparisons[0]['train_queries'] = ["word_position==1 and block in [2, 4, 6]", "word_position==-1 and block in [2, 4, 6]"]

    comparisons[1] = {}
    comparisons[1]['name'] = 'first_last_word_visual'
    comparisons[1]['train_queries'] = ["word_position==1 and block in [1, 3, 5]", "word_position==-1 and block in [1, 3, 5]"]


# GRAMMATICAL NUMBER:
    # Nouns:
    comparisons[2] = {}
    comparisons[2]['name'] = 'grammatical_number_nouns_audio'
    comparisons[2]['train_queries'] = ["pos=='NN' and block in [2, 4, 6]", "pos=='NNS' and block in [2, 4, 6]"]

    comparisons[3] = {}
    comparisons[3]['name'] = 'grammatical_number_nouns_visual'
    comparisons[3]['train_queries'] = ["pos=='NN' and block in [1, 3, 5]", "pos=='NNS' and block in [1, 3, 5]"]

    comparisons[4] = {}
    comparisons[4]['name'] = 'grammatical_number_nouns_audio2visual'
    comparisons[4]['train_queries'] = ["pos=='NN' and block in [2, 4, 6]", "pos=='NNS' and block in [2, 4, 6]"]
    comparisons[4]['test_queries'] = ["pos=='NN' and block in [1, 3, 5]", "pos=='NNS' and block in [1, 3, 5]"]

    # Verbs:
    comparisons[5] = {}
    comparisons[5]['name'] = 'grammatical_number_verbs_audio'
    comparisons[5]['train_queries'] = ["pos=='VBZ' and block in [2, 4, 6]", "pos=='VBP' and block in [2, 4, 6]"]

    comparisons[6] = {}
    comparisons[6]['name'] = 'grammatical_number_verbs_visual'
    comparisons[6]['train_queries'] = ["pos=='VBZ' and block in [1, 3, 5]", "pos=='VBP' and block in [1, 3, 5]"]

    comparisons[7] = {}
    comparisons[7]['name'] = 'grammatical_number_verbs_audio2visual'
    comparisons[7]['train_queries'] = ["pos=='VBZ' and block in [2, 4, 6]", "pos=='VBP' and block in [2, 4, 6]"]
    comparisons[7]['test_queries'] = ["pos=='VBZ' and block in [1, 3, 5]", "pos=='VBP' and block in [1, 3, 5]"]

    #Nouns2Verbs-audio
    comparisons[8] = {}
    comparisons[8]['name'] = 'grammatical_number_verbs2nouns_audio'
    comparisons[8]['train_queries'] = ["pos=='VBZ' and block in [2, 4, 6]", "pos=='VBP' and block in [2, 4, 6]"]
    comparisons[8]['test_queries'] = ["pos=='NN' and block in [2, 4, 6]", "pos=='NNS' and block in [2, 4, 6]"]

# Nouns vs. verbs

    comparisons[9] = {}
    comparisons[9]['name'] = 'nouns_verbs_audio'
    comparisons[9]['train_queries'] = ["pos=='NN' or pos=='NNS' and block in [2, 4, 6]", "pos=='VBZ' or pos=='VBP' and block in [2, 4, 6]"]

    comparisons[10] = {}
    comparisons[10]['name'] = 'nouns_verbs_visual'
    comparisons[10]['train_queries'] = ["pos=='NN' or pos=='NNS' and block in [1, 3, 5]", "pos=='VBZ' or pos=='VBP' and block in [1, 3, 5]"]

    comparisons[11] = {}
    comparisons[11]['name'] = 'nouns_verbs_audio2visual'
    comparisons[11]['train_queries'] = ["pos=='NN' or pos=='NNS' and block in [2, 4, 6]", "pos=='VBZ' or pos=='VBP' and block in [2, 4, 6]"]
    comparisons[11]['test_queries'] = ["pos=='NN' or pos=='NNS' and block in [1, 3, 5]", "pos=='VBZ' or pos=='VBP' and block in [1, 3, 5]"]

# Gender
    
    comparisons[12] = {}
    comparisons[12]['name'] = 'he_she_audio'
    comparisons[12]['train_queries'] = ["word_position==1 and word_string=='he' and block in [2, 4, 6]", "word_position==1 and word_string=='she' and block in [2, 4, 6]"]

    comparisons[13] = {}
    comparisons[13]['name'] = 'he_she_visual'
    comparisons[13]['train_queries'] = ["word_position==1 and word_string=='he' and block in [1, 3, 5]", "word_position==1 and word_string=='she' and block in [1, 3, 5]"]


    comparisons[14] = {}
    comparisons[14]['name'] = 'he_she_audio2visual'
    comparisons[14]['train_queries'] = ["word_position==1 and word_string=='he' and block in [2, 4, 6]", "word_position==1 and word_string=='she' and block in [2, 4, 6]"]
    comparisons[14]['test_queries'] = ["word_position==1 and word_string=='he' and block in [1, 3, 5]", "word_position==1 and word_string=='she' and block in [1, 3, 5]"]
    
    comparisons[15] = {}
    comparisons[15]['name'] = 'boy_girl_audio'
    comparisons[15]['train_queries'] = ["word_position==2 and word_string=='boy' and block in [2, 4, 6]", "word_position==2 and word_string=='girl' and block in [2, 4, 6]"]

    comparisons[16] = {}
    comparisons[16]['name'] = 'boy_girl_visual'
    comparisons[16]['train_queries'] = ["word_position==2 and word_string=='boy' and block in [1, 3, 5]", "word_position==2 and word_string=='girl' and block in [1, 3, 5]"]

    comparisons[17] = {}
    comparisons[17]['name'] = 'boy_girl_audio2visual'
    comparisons[17]['train_queries'] = ["word_position==2 and word_string=='boy' and block in [2, 4, 6]", "word_position==2 and word_string=='girl' and block in [2, 4, 6]"]
    comparisons[17]['test_queries'] = ["word_position==2 and word_string=='boy' and block in [1, 3, 5]", "word_position==2 and word_string=='girl' and block in [1, 3, 5]"]
    
    comparisons[18] = {}
    comparisons[18]['name'] = 'gender_pronoun2noun_audio'
    comparisons[18]['train_queries'] = ["word_position==1 and word_string=='he' and block in [2, 4, 6]", "word_position==1 and word_string=='she' and block in [2, 4, 6]"]
    comparisons[18]['test_queries'] = ["word_position==2 and word_string=='boy' and block in [2, 4, 6]", "word_position==2 and word_string=='girl' and block in [2, 4, 6]"]

    comparisons[19] = {}
    comparisons[19]['name'] = 'gender_pronoun2noun_visual'
    comparisons[19]['train_queries'] = ["word_position==1 and word_string=='he' and block in [1, 3, 5]", "word_position==1 and word_string=='she' and block in [1, 3, 5]"]
    comparisons[19]['test_queries'] = ["word_position==2 and word_string=='boy' and block in [1, 3, 5]", "word_position==2 and word_string=='girl' and block in [1, 3, 5]"]


#nohup python ../Code/Main/run_GAT.py -r /neurospin/unicog/protocols/intracranial/Syntax_with_Fried/ -s UCLA -p patient_479 -k all --train-queries "word_string=='he' and block in [1, 3, 5]" --train-queries "word_string=='she' and block in [1, 3, 5]" > Logs_GAT/gat_he_she_visual.log 2>&1 &

    return comparisons
