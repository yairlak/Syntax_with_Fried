import os
for ch in range(89):
    cmd = 'python plot_rasters.py -channel ' + str(ch) + ' -tmin -3 -tmax 1 -block visual'
    os.system(cmd)