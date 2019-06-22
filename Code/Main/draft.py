import os
for ch in range(89):
    # Visual
    cmd = 'python plot_rasters.py -channel ' + str(ch) + ' -tmin -3 -tmax 1.2 -block visual -align end'
    os.system(cmd)

    # Auditory
    cmd = 'python plot_rasters.py -channel ' + str(ch) + ' -tmin -1.2 -tmax 2 -block auditory -align first'
    os.system(cmd)

    cmd = 'python plot_rasters.py -channel ' + str(ch) + ' -tmin -2 -tmax 1.2 -block auditory -align end'
    os.system(cmd)