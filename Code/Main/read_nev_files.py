from SU_functions import load_settings_params
from neo import rawio
import os.path as op


# BUGGY NEED TO BE FIXED
settings = load_settings_params.Settings()
reader = rawio.NeuralynxRawIO(dirname=op.join(settings.path2patient_folder, 'nev_files'))
'Events.nev'
nev = rawio.neuralynxio(op.join(settings.path2patient_folder, 'nev_files', 'events.nev'))  # Load event data into a dictionary
nev['event'][0]  # Access the first event
