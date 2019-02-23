subjects = ['he', 'she', 'they', 'the boy', 'the girl', 'the boys', 'the man', 'the men', 'the woman', 'the women']
verbs_mental = ['think', 'thinks', 'believe', 'believes', 'know', 'knows']
verbs_unergative = ['cry', 'cries', 'sneeze', 'sneezes']



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

