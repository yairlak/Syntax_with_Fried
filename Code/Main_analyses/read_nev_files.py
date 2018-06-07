from SU_functions import load_settings_params
import os.path as op
from neo import io
import quantities as pq
import matplotlib.pyplot as plt

# BUGGY NEED TO BE FIXED
settings = load_settings_params.Settings()
session_folder = op.join(settings.path2patient_folder, 'Raw')
NIO = io.NeuralynxIO(session_folder)
time0, timeend = NIO._timestamp_limits[0]
print('time0, timeend = ', time0, timeend)