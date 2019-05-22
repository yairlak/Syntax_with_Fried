import glob, os

path2logs = '/home/yl254115/Projects/intracranial/single_unit/Syntax_with_Fried/Data/UCLA/patient_505/Logs/505/'
log_basename = 'events_log_in_cheetah_clock_part'

megalog = glob.glob(os.path.join(path2logs, '..', 'events_log_in_cheetah_clock.log'))
assert len(megalog)==1

f_newlog = None
part = 0
with open(megalog[0], 'r') as f:
    for l in f:
        if l.find('DISPLAY_INSTRUCTIONS Stimuli/instructions')>0:
            part += 1
            new_log_fn = os.path.join(path2logs, '..', log_basename + str(part)+'.log')
            f_newlog = open(new_log_fn, 'w')
        if f_newlog is not None:
            f_newlog.write(l)