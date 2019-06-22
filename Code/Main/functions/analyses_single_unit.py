from __future__ import division
import numpy as np
import os
import mne
import matplotlib.pyplot as plt
import pickle
from operator import itemgetter
from functions import load_data, convert_to_mne


def generate_epochs_spikes(channel_num, channel_name, events_spikes, event_id, metadata, settings, params, preferences):

    print('Loading h5 file for CSC%i'%channel_num)
    spikes, channel_name = load_data.load_combinato_sorted_h5(channel_num, channel_name, settings)


    if len(spikes) > 0:
        print('Generating MNE raw object for spikes...')
        raw_spikes = convert_to_mne.generate_mne_raw_object_for_spikes(spikes, channel_name, settings, params)

        print('Epoching spiking data...')
        epochs_spikes = mne.Epochs(raw_spikes, events_spikes, event_id, params.tmin, params.tmax, metadata=metadata,
                                   baseline=None, preload=True, picks=None)
        print(epochs_spikes)
    else:
        epochs_spikes = []

    return epochs_spikes

