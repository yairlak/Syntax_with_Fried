def comparison_list():
    comparisons = {}

# Sanity checks:
    comparisons[0] = {}
    comparisons[0]['name'] = 'first_last_word_audio'
    comparisons[0]['train_queries'] = ["word_position==1 and block in [2, 4, 6]", "word_position==-1 and block in [2, 4, 6]"]
    comparisons[0]['train_condition_names'] = ['First_word', 'Last_word']

    comparisons[1] = {}
    comparisons[1]['name'] = 'first_last_word_visual'
    comparisons[1]['train_queries'] = ["word_position==1 and block in [1, 3, 5]", "word_position==-1 and block in [1, 3, 5]"]
    comparisons[1]['train_condition_names'] = ['First_word', 'Last_word']


# GRAMMATICAL NUMBER:
    # Nouns:
    comparisons[2] = {}
    comparisons[2]['name'] = 'grammatical_number_nouns_audio'
    comparisons[2]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='girl' or word_string=='man' or word_string=='woman') and block in [2, 4, 6]", "word_position==2 and (word_string=='boys' or word_string=='girls' or word_string=='men' or word_string=='women') and block in [2, 4, 6]"]
    comparisons[2]['train_condition_names'] = ['Singular', 'Plural']

    comparisons[3] = {}
    comparisons[3]['name'] = 'grammatical_number_nouns_visual'
    comparisons[3]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='girl' or word_string=='man' or word_string=='woman') and block in [1, 3, 5]", "word_position==2 and (word_string=='boys' or word_string=='girls' or word_string=='men' or word_string=='women') and block in [1, 3, 5]"]
    comparisons[3]['train_condition_names'] = ['Singular', 'Plural']

    comparisons[4] = {}
    comparisons[4]['name'] = 'grammatical_number_nouns_audio2visual'
    comparisons[4]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='girl' or word_string=='man' or word_string=='woman') and block in [2, 4, 6]", "word_position==2 and (word_string=='boys' or word_string=='girls' or word_string=='men' or word_string=='women') and block in [2, 4, 6]"]
    comparisons[4]['test_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='girl' or word_string=='man' or word_string=='woman') and block in [1, 3, 5]", "word_position==2 and (word_string=='boys' or word_string=='girls' or word_string=='men' or word_string=='women') and block in [1, 3, 5]"]
    comparisons[4]['train_condition_names'] = ['Singular', 'Plural']
    comparisons[4]['test_condition_names'] = ['Singular', 'Plural']

    # Verbs:
    comparisons[5] = {}
    comparisons[5]['name'] = 'grammatical_number_verbs_audio'
    comparisons[5]['train_queries'] = ["pos=='VBZ' and block in [2, 4, 6]", "pos=='VBP' and block in [2, 4, 6]"]
    comparisons[5]['train_condition_names'] = ['Singular', 'Plural']

    comparisons[6] = {}
    comparisons[6]['name'] = 'grammatical_number_verbs_visual'
    comparisons[6]['train_queries'] = ["pos=='VBZ' and block in [1, 3, 5]", "pos=='VBP' and block in [1, 3, 5]"]
    comparisons[6]['train_condition_names'] = ['Singular', 'Plural']

    comparisons[7] = {}
    comparisons[7]['name'] = 'grammatical_number_verbs_audio2visual'
    comparisons[7]['train_queries'] = ["pos=='VBZ' and block in [2, 4, 6]", "pos=='VBP' and block in [2, 4, 6]"]
    comparisons[7]['test_queries'] = ["pos=='VBZ' and block in [1, 3, 5]", "pos=='VBP' and block in [1, 3, 5]"]
    comparisons[7]['train_condition_names'] = ['Singular', 'Plural']
    comparisons[7]['test_condition_names'] = ['Singular', 'Plural']

    # Pronouns:
    comparisons[8] = {}
    comparisons[8]['name'] = 'grammatical_number_pronouns_audio'
    comparisons[8]['train_queries'] = ["word_position==1 and (word_string=='he' or word_string=='she') and block in [2, 4, 6]", "word_position==1 and (word_string=='they') and block in [2, 4, 6]"]
    comparisons[8]['train_condition_names'] = ['Singular', 'Plural']

    comparisons[9] = {}
    comparisons[9]['name'] = 'grammatical_number_pronouns_visual'
    comparisons[9]['train_queries'] = ["word_position==1 and (word_string=='he' or word_string=='she') and block in [1, 3, 5]", "word_position==1 and (word_string=='they') and block in [1, 3, 5]"]
    comparisons[9]['train_condition_names'] = ['Singular', 'Plural']

    comparisons[10] = {}
    comparisons[10]['name'] = 'grammatical_number_pronouns_audio2visual'
    comparisons[10]['train_queries'] = ["word_position==1 and (word_string=='he' or word_string=='she') and block in [2, 4, 6]", "word_position==1 and (word_string=='they') and block in [2, 4, 6]"]
    comparisons[10]['test_queries'] = ["word_position==1 and (word_string=='he' or word_string=='she') and block in [1, 3, 5]", "word_position==1 and (word_string=='they') and block in [1, 3, 5]"]
    comparisons[10]['train_condition_names'] = ['Singular', 'Plural']
    comparisons[10]['test_condition_names'] = ['Singular', 'Plural']

    #Nouns2Verbs-audio
    comparisons[11] = {}
    comparisons[11]['name'] = 'grammatical_number_verbs2nouns_audio'
    comparisons[11]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='girl' or word_string=='man' or word_string=='woman') and block in [2, 4, 6]", "word_position==2 and (word_string=='boys' or word_string=='girls' or word_string=='men' or word_string=='women') and block in [2, 4, 6]"]
    comparisons[11]['test_queries'] = ["pos=='VBZ' and block in [2, 4, 6]", "pos=='VBP' and block in [2, 4, 6]"]
    comparisons[11]['train_condition_names'] = ['Singular', 'Plural']
    comparisons[11]['test_condition_names'] = ['Singular', 'Plural']

    #Nouns2Verbs-visual
    comparisons[12] = {}
    comparisons[12]['name'] = 'grammatical_number_verbs2nouns_visual'
    comparisons[12]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='girl' or word_string=='man' or word_string=='woman') and block in [1, 3, 5]", "word_position==2 and (word_string=='boys' or word_string=='girls' or word_string=='men' or word_string=='women') and block in [1, 3, 5]"]
    comparisons[12]['test_queries'] = ["pos=='VBZ' and block in [1, 3, 5]", "pos=='VBP' and block in [1, 3, 5]"]
    comparisons[12]['train_condition_names'] = ['Singular', 'Plural']
    comparisons[12]['test_condition_names'] = ['Singular', 'Plural']

    #Nouns2Pronouns-audio
    comparisons[13] = {}
    comparisons[13]['name'] = 'grammatical_number_nouns2pronouns_audio'
    comparisons[13]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='girl' or word_string=='man' or word_string=='woman') and block in [2, 4, 6]", "word_position==2 and (word_string=='boys' or word_string=='girls' or word_string=='men' or word_string=='women') and block in [2, 4, 6]"]
    comparisons[13]['test_queries'] = ["word_position==1 and (word_string=='he' or word_string=='she') and block in [2, 4, 6]", "word_position==1 and (word_string=='they') and block in [2, 4, 6]"]
    comparisons[13]['train_condition_names'] = ['Singular', 'Plural']
    comparisons[13]['test_condition_names'] = ['Singular', 'Plural']

    #Nouns2Pronouns-visual
    comparisons[14] = {}
    comparisons[14]['name'] = 'grammatical_number_nouns2pronouns_visual'
    comparisons[14]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='girl' or word_string=='man' or word_string=='woman') and block in [1, 3, 5]", "word_position==2 and (word_string=='boys' or word_string=='girls' or word_string=='men' or word_string=='women') and block in [1, 3, 5]"]
    comparisons[14]['test_queries'] = ["word_position==1 and (word_string=='he' or word_string=='she') and block in [1, 3, 5]", "word_position==1 and (word_string=='they') and block in [1, 3, 5]"]
    comparisons[14]['train_condition_names'] = ['Singular', 'Plural']
    comparisons[14]['test_condition_names'] = ['Singular', 'Plural']

    #Pronouns2Verbs-audio
    comparisons[15] = {}
    comparisons[15]['name'] = 'grammatical_number_pronouns2verbs_audio'
    comparisons[15]['train_queries'] = ["word_position==1 and (word_string=='he' or word_string=='she') and block in [2, 4, 6]", "word_position==1 and (word_string=='they') and block in [2, 4, 6]"]
    comparisons[15]['test_queries'] = ["pos=='VBZ' and block in [2, 4, 6]", "pos=='VBP' and block in [2, 4, 6]"]
    comparisons[15]['train_condition_names'] = ['Singular', 'Plural']
    comparisons[15]['test_condition_names'] = ['Singular', 'Plural']

    #Pronouns2Verbs-visual
    comparisons[16] = {}
    comparisons[16]['name'] = 'grammatical_number_pronouns2verbs_visual'
    comparisons[16]['train_queries'] = ["word_position==1 and (word_string=='he' or word_string=='she') and block in [1, 3, 5]", "word_position==1 and (word_string=='they') and block in [1, 3, 5]"]
    comparisons[16]['test_queries'] = ["pos=='VBZ' and block in [1, 3, 5]", "pos=='VBP' and block in [1, 3, 5]"]
    comparisons[16]['train_condition_names'] = ['Singular', 'Plural']
    comparisons[16]['test_condition_names'] = ['Singular', 'Plural']

# Nouns vs. verbs

    comparisons[17] = {}
    comparisons[17]['name'] = 'nouns_verbs_audio'
    comparisons[17]['train_queries'] = ["(pos=='NN' or pos=='NNS') and block in [2, 4, 6]", "(pos=='VBZ' or pos=='VBP') and block in [2, 4, 6]"]
    comparisons[17]['train_condition_names'] = ['Noun', 'Verb']

    comparisons[18] = {}
    comparisons[18]['name'] = 'nouns_verbs_visual'
    comparisons[18]['train_queries'] = ["(pos=='NN' or pos=='NNS') and block in [1, 3, 5]", "(pos=='VBZ' or pos=='VBP') and block in [1, 3, 5]"]
    comparisons[18]['train_condition_names'] = ['Noun', 'Verb']

    comparisons[19] = {}
    comparisons[19]['name'] = 'nouns_verbs_audio2visual'
    comparisons[19]['train_queries'] = ["(pos=='NN' or pos=='NNS') and block in [2, 4, 6]", "(pos=='VBZ' or pos=='VBP') and block in [2, 4, 6]"]
    comparisons[19]['test_queries'] = ["(pos=='NN' or pos=='NNS') and block in [1, 3, 5]", "(pos=='VBZ' or pos=='VBP') and block in [1, 3, 5]"]
    comparisons[19]['train_condition_names'] = ['Noun', 'Verb']
    comparisons[19]['test_condition_names'] = ['Noun', 'Verb']

# Gender
    
    comparisons[20] = {}
    comparisons[20]['name'] = 'gender_pronouns_audio'
    comparisons[20]['train_queries'] = ["word_position==1 and word_string=='he' and block in [2, 4, 6]", "word_position==1 and word_string=='she' and block in [2, 4, 6]"]
    comparisons[20]['train_condition_names'] = ['Masculine', 'Feminine']

    comparisons[21] = {}
    comparisons[21]['name'] = 'gender_pronouns_visual'
    comparisons[21]['train_queries'] = ["word_position==1 and word_string=='he' and block in [1, 3, 5]", "word_position==1 and word_string=='she' and block in [1, 3, 5]"]
    comparisons[21]['train_condition_names'] = ['Masculine', 'Feminine']


    comparisons[22] = {}
    comparisons[22]['name'] = 'gender_pronouns_audio2visual'
    comparisons[22]['train_queries'] = ["word_position==1 and word_string=='he' and block in [2, 4, 6]", "word_position==1 and word_string=='she' and block in [2, 4, 6]"]
    comparisons[22]['test_queries'] = ["word_position==1 and word_string=='he' and block in [1, 3, 5]", "word_position==1 and word_string=='she' and block in [1, 3, 5]"]
    comparisons[22]['train_condition_names'] = ['Masculine', 'Feminine']
    comparisons[22]['test_condition_names'] = ['Masculine', 'Feminine']
    
    comparisons[23] = {}
    comparisons[23]['name'] = 'gender_nouns_audio'
    comparisons[23]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='boys' or word_string=='man' or word_string=='men') and block in [2, 4, 6]", "word_position==2 and (word_string=='girl' or word_string=='girls' or word_string=='woman' or word_string=='women') and block in [2, 4, 6]"]
    comparisons[23]['train_condition_names'] = ['Masculine', 'Feminine']

    comparisons[24] = {}
    comparisons[24]['name'] = 'gender_nouns_visual'
    comparisons[24]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='boys' or word_string=='man' or word_string=='men') and block in [1, 3, 5]", "word_position==2 and (word_string=='girl' or word_string=='girls' or word_string=='woman' or word_string=='women') and block in [1, 3, 5]"]
    comparisons[24]['train_condition_names'] = ['Masculine', 'Feminine']

    comparisons[25] = {}
    comparisons[25]['name'] = 'gender_nouns_audio2visual'
    comparisons[25]['train_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='boys' or word_string=='man' or word_string=='men') and block in [2, 4, 6]", "word_position==2 and (word_string=='girl' or word_string=='girls' or word_string=='woman' or word_string=='women') and block in [2, 4, 6]"]
    comparisons[25]['test_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='boys' or word_string=='man' or word_string=='men') and block in [1, 3, 5]", "word_position==2 and (word_string=='girl' or word_string=='girls' or word_string=='woman' or word_string=='women') and block in [1, 3, 5]"]
    comparisons[25]['train_condition_names'] = ['Masculine', 'Feminine']
    comparisons[25]['test_condition_names'] = ['Masculine', 'Feminine']
    
    comparisons[26] = {}
    comparisons[26]['name'] = 'gender_pronoun2noun_audio'
    comparisons[26]['train_queries'] = ["word_position==1 and word_string=='he' and block in [2, 4, 6]", "word_position==1 and word_string=='she' and block in [2, 4, 6]"]
    comparisons[26]['test_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='boys' or word_string=='man' or word_string=='men') and block in [2, 4, 6]", "word_position==2 and (word_string=='girl' or word_string=='girls' or word_string=='woman' or word_string=='women') and block in [2, 4, 6]"]
    comparisons[26]['train_condition_names'] = ['Masculine', 'Feminine']
    comparisons[26]['test_condition_names'] = ['Masculine', 'Feminine']

    comparisons[27] = {}
    comparisons[27]['name'] = 'gender_pronoun2noun_visual'
    comparisons[27]['train_queries'] = ["word_position==1 and word_string=='he' and block in [1, 3, 5]", "word_position==1 and word_string=='she' and block in [1, 3, 5]"]
    comparisons[27]['test_queries'] = ["word_position==2 and (word_string=='boy' or word_string=='boys' or word_string=='man' or word_string=='men') and block in [1, 3, 5]", "word_position==2 and (word_string=='girl' or word_string=='girls' or word_string=='woman' or word_string=='women') and block in [1, 3, 5]"]
    comparisons[27]['train_condition_names'] = ['Masculine', 'Feminine']
    comparisons[27]['test_condition_names'] = ['Masculine', 'Feminine']

# Sentence type
    
    comparisons[28] = {}
    comparisons[28]['name'] = 'declarative_questions_auditory'
    comparisons[28]['train_queries'] = ["Declarative==1 and block in [2, 4, 6] and word_position==-1", "Question==1 and block in [2, 4, 6] and word_position==-1"]
    comparisons[28]['train_condition_names'] = ['Declarative', 'Question']

    comparisons[29] = {}
    comparisons[29]['name'] = 'declarative_questions_visual'
    comparisons[29]['train_queries'] = ["Declarative==1 and block in [1, 3, 5] and word_position==-1", "Question==1 and block in [1, 3, 5] and word_position==-1"]
    comparisons[29]['train_condition_names'] = ['Declarative', 'Question']

    comparisons[30] = {}
    comparisons[30]['name'] = 'declarative_questions_auditory2visual'
    comparisons[30]['train_queries'] = ["Declarative==1 and block in [2, 4, 6] and word_position==-1", "Question==1 and block in [2, 4, 6] and word_position==-1"]
    comparisons[30]['test_queries'] = ["Declarative==1 and block in [1, 3, 5] and word_position==-1", "Question==1 and block in [1, 3, 5] and word_position==-1"]
    comparisons[30]['train_condition_names'] = ['Declarative', 'Question']
    comparisons[30]['test_condition_names'] = ['Declarative', 'Question']
    
# Embedding

    comparisons[31] = {}
    comparisons[31]['name'] = 'embedding_auditory'
    comparisons[31]['train_queries'] = ["Embedding == 1 and word_position==-1 and block in [2, 4, 6]", "Declarative==1 and sentence_length==5 and Embedding==0 and word_position==-1 and block in [2, 4, 6]"]
    comparisons[31]['train_condition_names'] = ['Embedding', 'Long_declarative']

    comparisons[32] = {}
    comparisons[32]['name'] = 'embedding_visual'
    comparisons[32]['train_queries'] = ["Embedding == 1 and word_position==-1 and block in [1, 3, 5]", "Declarative==1 and sentence_length==5 and Embedding==0 and word_position==-1 and block in [1, 3, 5]"]
    comparisons[32]['train_condition_names'] = ['Embedding', 'Long_declarative']

    comparisons[33] = {}
    comparisons[33]['name'] = 'embedding_audio2visual'
    comparisons[33]['train_queries'] = ["Embedding == 1 and word_position==-1 and block in [2, 4, 6]", "Declarative==1 and sentence_length==5 and Embedding==0 and word_position==-1 and block in [2, 4, 6]"]
    comparisons[33]['test_queries'] = ["Embedding == 1 and word_position==-1 and block in [1, 3, 5]", "Declarative==1 and sentence_length==5 and Embedding==0 and word_position==-1 and block in [1, 3, 5]"]
    comparisons[33]['train_condition_names'] = ['Embedding', 'Long_declarative']
    comparisons[33]['test_condition_names'] = ['Embedding', 'Long_declarative']

# Number of letters
    comparisons[34] = {}
    comparisons[34]['name'] = 'word_length_audio'
    comparisons[34]['train_queries'] = ["word_string.str.len()<4 and block in [2, 4, 6]", "word_string.str.len()>7 and block in [2, 4, 6]"]
    comparisons[34]['train_condition_names'] = ['Short_word', 'Long_word']

    comparisons[35] = {}
    comparisons[35]['name'] = 'word_length_visual'
    comparisons[35]['train_queries'] = ["word_string.str.len()<4 and block in [1, 3, 5]", "word_string.str.len()>7 and block in [1, 3, 5]"]
    comparisons[35]['train_condition_names'] = ['Short_word', 'Long_word']
    
    return comparisons
