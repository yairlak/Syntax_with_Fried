import os, argparse
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
from pprint import pprint
from functions import data_manip

parser = argparse.ArgumentParser()
parser.add_argument('--patient', action='append', default=[])
args=parser.parse_args()

patients = ['patient_' + p for p in args.patient]

def get_names(patient, micro_macro):
    path2channel_names = os.path.join('..', '..', 'Data', 'UCLA', patient, 'Raw', micro_macro, 'CSC_mat', 'channel_numbers_to_names.txt')
    try:
        with open(path2channel_names, 'r') as f:
            channel_names = f.readlines()
        channel_names = [l.strip().split('\t')[1] for l in channel_names]
        if micro_macro == 'micro':
            channel_names.pop(0) # remove MICROPHONE line
            channel_names = [s[4::] for s in channel_names] # remove prefix if exists (in micro: GA1-, GA2-, etc)
        channel_names = [s[:-5] for s in channel_names] # remove file extension and electrode numbering (e.g., LSTG1, LSTG2, LSTG3) 
        if (micro_macro == 'macro') & (patient == 'patient_502'):
            channel_names = [name for name in channel_names if name not in ['ROF', 'RAF']] # 502 has more macro than micro see Notes/log_summary.txt (March 2020)
            print('Macros also include ROF and RAF - see Notes/log_summary.txt (2020Mar02)')
    except:
        print('!!! - Missing %s channel-name files for %s' % (micro_macro, patient))
        return
    return sorted(list(set(channel_names)))


# MAIN

names_from_all_patients = []
for patient in patients:
    names_micro = get_names(patient, 'micro')
    names_macro = get_names(patient, 'macro')

    print('%s' % patient)
    if (names_micro is not None) & (names_macro is not None):
        if set(names_micro) != set(names_macro):
            print('!!! - Micro and macro electrode names are not the same - !!!')
            print('micro:', names_micro)
            print('macro:', names_macro)
        else:
            print(names_micro)
            names_from_all_patients.extend(names_micro)
    else:
        print('micro:', names_micro)
        print('macro:', names_macro)
    print('-'*100)

x = {}
probes = data_manip.get_probes2channels(patients)
for probe in probes['probe_names'].keys():
    if 'patients' in probes['probe_names'][probe].keys():
        x[probe] = ' '.join(probes['probe_names'][probe]['patients'])
dict_names = {k: v for k, v in sorted(x.items(), key=lambda item: len(item[1].split()), reverse=True)}
[print('%s (%i):%s'%(k,len(v.split()),v)) for (k,v) in dict_names.items()]

#x = {name:names_from_all_patients.count(name) for name in names_from_all_patients}
#dict_names = {k: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)}
#[print('%s:%i'%(k,v)) for (k,v) in dict_names.items()]
#pprint(dict_names)
#pprint(probes)
