import os
patient = 502

for ch in range(77, 97):
    block = 'auditory'
    align = 'first'
    tmin = -1
    tmax = 2
    cmd = 'python ../Code/Main/plot_rasters.py -patient %i -block %s -align %s -channel %i -tmin %1.2f -tmax %1.2f' % (patient, block, align, ch, tmin, tmax)
    os.system(cmd)
    
    block = 'visual'
    align = 'end'
    tmin = -2.5
    tmax = 1.2
    cmd = 'python ../Code/Main/plot_rasters.py -patient %i -block %s -align %s -channel %i -tmin %1.2f -tmax %1.2f' % (patient, block, align, ch, tmin, tmax)
    os.system(cmd)
