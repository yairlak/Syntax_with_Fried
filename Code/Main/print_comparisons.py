from functions import comparisons
from pprint import pprint
import argparse

#parser = argparse.ArgumentParser
#parser.add_argument('--queries', action='store_true', default=False)
#args = parser.parse_args()

comparison_list = comparisons.comparison_list()
for k, v in comparison_list.items():
    print('%i: %s' % (k, v['name']))
    print('Training contrast')
    for query_name, query in zip(v['train_condition_names'], v['train_queries']):
        print('%s: %s' % (query_name, query))
    if 'test_queries' in v.keys():
        print('Test contrast')
        for query_name, query in zip(v['test_condition_names'], v['test_queries']):
            print('%s: %s' % (query_name, query))

    print('-'*100)

