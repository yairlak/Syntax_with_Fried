import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
# Display spikes waveforms
filename = '/home/yl254115/Projects/single_unit_syntax/Data/UCLA/patient_480/ChannelsCSC/times_CSC28.mat'

data = sio.loadmat(filename)

IX = data['cluster_class'][:, 0]
IX = np.asarray(np.where(IX == 1))[0]
spike_waveforms_cluster_1 = data['spikes'][IX, :]

plt.plot(np.transpose(spike_waveforms_cluster_1), color='k', linewidth=0.1)
plt.ylim([-500, 500])
plt.title('Channel 28, Cluster 1 (' + str(spike_waveforms_cluster_1.shape[0]) + ' spikes)')
plt.xlabel('Time')
# fig, ax = plt.subplot(111)
# ax.plot(spike_waveforms_cluster_1)
# plt.show()
plt.savefig('/home/yl254115/Projects/single_unit_syntax/Figures/Patient480_channel_28_cluster_1.png')


