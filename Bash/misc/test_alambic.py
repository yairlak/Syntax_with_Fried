import argparse, os
parser = argparse.ArgumentParser()
parser.add_argument('-n', type=str)
args = parser.parse_args()
fn = args.n + '.txt'
with open(os.path.join('/neurospin/unicog/protocols/intracranial/Syntax_with_Fried/Bash', fn), 'w') as f:
    f.write('test')
