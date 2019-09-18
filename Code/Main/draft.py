import matplotlib.pyplot as plt
import numpy as np

with open('events_502.txt', 'r') as f:
    v = f.readlines()
v = np.asarray(v).astype(float)
d = np.diff(v)

plt.plot(v)
plt.show()






# import os
# patient = '505'
# # for ch in [10, 11, 12, 13, 14, 17, 36, 41, 42, 43, 44, 45, 47, 48, 49, 51, 53, 54]: #479
# for ch in [17, 19, 22, 23, 25, 26, 27, 28, 29, 31, 76, 79]: #505
#     # Visual
#     # cmd = 'python plot_rasters.py -patient ' + patient + ' -channel ' + str(ch) + ' -tmin -3 -tmax 1.2 --query "Declarative==1 and block in [2, 4, 6] and word_position==-1"'
#     # os.system(cmd)
#     #
#     # cmd = 'python plot_rasters.py -patient ' + patient + ' -channel ' + str(
#     #     ch) + ' -tmin -3 -tmax 1.2 --query "Question==1 and block in [2, 4, 6] and word_position==-1"'
#     # os.system(cmd)
#     #
#     # cmd = 'python plot_rasters.py -patient ' + patient + ' -channel ' + str(ch) + ' -tmin -2 -tmax 1.2 --query "Declarative==1 and block in [1, 3, 5] and word_position==-1"'
#     # os.system(cmd)
#     #
#     # cmd = 'python plot_rasters.py -patient ' + patient + ' -channel ' + str(ch) + ' -tmin -2 -tmax 1.2 --query "Question==1 and block in [1, 3, 5] and word_position==-1"'
#     # os.system(cmd)
#
# # for ch in range(90):
#     # Visual
#     cmd = 'python plot_rasters.py -patient ' + patient + ' -channel ' + str(ch) + ' -tmin -3 -tmax 1.2 -block visual -align end'
#     os.system(cmd)
#
#     # Auditory
#     cmd = 'python plot_rasters.py -patient ' + patient + ' -channel ' + str(ch) + ' -tmin -1.2 -tmax 2 -block auditory -align first'
#     os.system(cmd)
#
#     cmd = 'python plot_rasters.py -patient ' + patient + ' -channel ' + str(ch) + ' -tmin -2 -tmax 1.2 -block auditory -align end'
#     os.system(cmd)