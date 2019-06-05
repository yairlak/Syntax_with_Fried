import glob, os

path2logs = '/home/yl254115/Projects/intracranial/single_unit/Syntax_with_Fried/Data/UCLA/patient_505/Logs/505/'

files = sorted(glob.glob(path2logs + "events_log_20*.log"))
mega_log = ''

files_base_name = os.path.basename(files[0])[0:21]

with open(os.path.join(path2logs, '..', files_base_name + '_00-00-00.log'), 'w') as f_megalog:
    for log in files:
        with open(log, 'r') as f_temp:
            lines = f_temp.readlines()
        for l in lines:
            f_megalog.write(l)
