import os, glob
import numpy as np
import scipy
import scipy.io as sio
import mne
from mne.decoding import GeneralizationAcrossTime
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import pickle
__author__ = 'yair'
curr_patient = 'patient_479'
curr_run = 'sentences'
blocks = range(1,3,1)
blocks_str = ''.join(str(x) for x in blocks)
block_type = 'mixed'
# Load data from MATLAB
file_name = os.path.join('..', '..', 'Output', 'raw_data_with_events_to_python_all_comparisons_' + curr_patient + '_' + curr_run + '_blocks_'+ blocks_str + '.mat')
print(file_name)
mat = sio.loadmat(file_name)

# Generate unit names (unique)
unit_names_temp = mat['unit_names']
unit_names_temp = unit_names_temp.tolist()
unit_names = []
for x in unit_names_temp[0]:
    unit_names_set = set(unit_names)
    propose_new_name = x[0]
    cnt = 1
    while propose_new_name in unit_names_set:
        cnt += 1
        propose_new_name = x[0] + str(cnt)
    unit_names.append(propose_new_name)

# Create Info object for MNE
ch_types=['eeg'] * len(unit_names)
sfreq = 1000 #Hz
info = mne.create_info(unit_names, sfreq, ch_types)
print(info)

# Load Raw data and create Raw object for MNE
custom_raw_smoothed_data = mat['custom_raw_smoothed']
raw_smoothed = mne.io.RawArray(custom_raw_smoothed_data, info)

for comparison, events in enumerate(mat['custom_events_all_comparisons'][0]):
    curr_comparison_name = mat['comparison_name'][0, comparison][0]

    # Create Events object for MNE
    event_id_temp = mat['event_id_all_comparisons'][0, comparison][0]
    event_id = {}
    for x, id in enumerate(event_id_temp):
        event_id[id[0]] = x
    events = events.astype(int)
    sort_IX = np.argsort(events[:, 0], axis=0)
    events = events[sort_IX, :]

    # Create Epochs object
    tmin = -0.5
    tmax = 1.5
    epochs = mne.Epochs(raw_smoothed, events, event_id, tmin, tmax, proj=True,
                    baseline=None, preload=True, verbose=False)
    print(epochs)
    epochs_data = epochs.get_data()

    for two_figs in range(0, 1):
        # Generate ERP figures
        fig_erp, axs = plt.subplots(4, 3)
#	plt.switch_backend('Qt5Agg')
        mng = plt.get_current_fig_manager()
	mng.window.showMaximized()
	#mng.frame.Maximize(True)
	# mng.window.state('zoomed')
#        mng.resize(*mng.window.maxsize())
        cnt = 0 + two_figs * 24

        for ax_erp in axs.reshape(-1):
            channel_to_plot = epochs_data[:, cnt, :]
            for cnd in range(0, len(event_id)):
                channel_to_plot_cnd = channel_to_plot[events[:, 2] == cnd, :]
                channel_to_plot_mean = channel_to_plot_cnd.mean(axis=0)
                PSTH = []
                timepoints = range(0, len(channel_to_plot_mean), 100)
                for i in timepoints:
                    PSTH.append(np.sum(channel_to_plot_mean[i:i+99]))
                PSTH = np.array(PSTH)

                color_vec = [0, (cnd+1) % 2, cnd]
                ax_erp.plot(1000*epochs[event_id.keys()[cnd]].average().times, channel_to_plot_mean, label=str(event_id.keys()[cnd]), linewidth=3.0, color=color_vec)
                ax_erp.bar(tmin*1000+np.array(timepoints), PSTH/100, width=100, color=color_vec, alpha=0.5)

            diff_means = channel_to_plot[events[:, 2] == 1, :].mean(axis=0) - channel_to_plot[events[:, 2] == 0, :].mean(axis=0)
            label_name = str(event_id.keys()[1]) + " - " + str(event_id.keys()[0])
            ax_erp.plot(1000*epochs[event_id.keys()[cnd]].average().times, diff_means, label=label_name, linewidth=2.0, color='r', linestyle='--')
            #l1 = ax_erp.plot(1000*epochs[0].average().times, np.transpose(epochs[0].average().data), label=str(event_id_temp[0][0]), color='blue')
            #l2 = ax_erp.plot(1000*epochs[1].average().times, np.transpose(epochs[1].average().data), label=str(event_id_temp[1][0]), color='green')
            #l3 = ax_erp.plot(1000*epochs[0].average().times, np.transpose(epochs[1].average().data)-np.transpose(epochs[0].average().data), label=str(event_id_temp[1][0]), color='red')
            ax_erp.set_xlim(1000*tmin, 1000*tmax)
            ax_erp.set_ylim(-3, 20)
            ax_erp.axvline(0, color='r', linestyle='--')
            # ax_erp.axvline(350, color='b', linestyle='--')
            ax_erp.set_title(unit_names[cnt] + ' #' + str(cnt+1), position=(0.72, 0.85))
            if cnt % 6 == 0:
                ax_erp.set_ylabel('Firing rate [Hz]')
            else:
                ax_erp.get_yaxis().set_ticks([])
            if cnt > 17 + 24 * two_figs:
                ax_erp.set_xlabel('Time [ms]')
            # else:
            #     ax_erp.get_xaxis().set_ticks([])
            # if cnt == 0:
            #     plt.legend(bbox_to_anchor=(0.2, 1.02, 2, .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            cnt += 1
            #del epochs
            if cnt == 11:
                break

        handles, labels = ax_erp.get_legend_handles_labels()
        plt.figlegend(handles, labels, loc=1)
        #plt.figlegend(handles, labels, bbox_to_anchor=(0.655, 0.93, 0.245, .15), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        main_title = 'Comparison name: ' + curr_comparison_name
      #  if curr_run in 'sentences':
       #     lock_to_word = mat['settings']['lock_to_word'][0][0][0]
       #     main_title = main_title + ', onset (red line) locked to word: ' + lock_to_word

        plt.suptitle(main_title, fontsize=20)
        fig_erp.set_facecolor(color='white')
        fig_file_name = 'ERP' + str(two_figs) + '_' + 'patient_479' + '_' + curr_run + '_' + curr_comparison_name + '_blocks_' + blocks_str + '_last' + '.png'
        fig_erp.show()
        fig_erp.savefig(os.path.join('..', '..', 'Figures', 'ERP', fig_file_name))
        plt.close(fig_erp)
