from functions import comparisons
from pprint import pprint
import argparse

#parser = argparse.ArgumentParser
#parser.add_argument('--queries', action='store_true', default=False)
#args = parser.parse_args()

comparison_list = comparisons.comparison_list()
for k, v in comparison_list.items():
    print('%i: %s' % (k, v['name']))

