import os
patient = 479_11

for ch in range(1, 65):
    block = 'auditory'
    align = 'end'
    tmin = -1.5
    tmax = 1.2
    cmd = 'python plot_rasters.py -patient %i -block %s -align %s -channel %i -tmin %1.2f -tmax %1.2f' % (patient, block, align, ch, tmin, tmax)
    print(cmd)
    os.system(cmd)
    
    block = 'visual'
    align = 'end'
    tmin = -2.5
    tmax = 1.2
    cmd = 'python plot_rasters.py -patient %i -block %s -align %s -channel %i -tmin %1.2f -tmax %1.2f' % (patient, block, align, ch, tmin, tmax)
    print(cmd)
    os.system(cmd)
