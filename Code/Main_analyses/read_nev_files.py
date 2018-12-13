from SU_functions import load_settings_params
import os.path as op
from neo import io
import matplotlib.pyplot as plt
import numpy as np

recording_system = 'BlackRock'
settings = load_settings_params.Settings('Practice')
session_folder = op.join(settings.path2patient_folder, 'Raw')

if recording_system == 'Neuralynx':
    NIO = io.NeuralynxIO(session_folder)
    time0, timeend = NIO._timestamp_limits[0]
    print('time0, timeend = ', time0, timeend)
elif recording_system == 'BlackRock':
    NIO = io.BlackrockIO(op.join(session_folder, 'Yair_practice_2018Nov09001.nev'))
    events = NIO.nev_data['NonNeural']
    time_stamps = [e[0] for e in events]
    event_num = [e[4] for e in events]
    plt.plot(np.asarray(time_stamps)/40000, event_num, '.')
    plt.show()