function SNR = cluster_SNR(spikes, cluster_inds)
% cluster_SNR    Based on pp. 527-528 of:
%
% Suner S, Fellows M R, Vargas-Irwin C, Nakata G K and
% Donoghue J P 2005 Reliability of signals from a chronically
% implanted, silicon-based electrode array in non-human primate
% primary motor cortex IEEE Trans. Neural Syst. Rehabil. Eng.
% 13 524-541.  
%
% Good signal (3): Able to set a threshold to detect one or
% more waveforms of unique shape from the signal above
% the background. The waveforms in these signals are easily
% distinguished with the naked eye without any signal pro-
% cessing or special sorting. Generally, these signals were
% later verified to have signal-to-noise ratio (SNR) above 4.
%
% Fair Signal (2): Able to set a threshold to detect and sort
% at least one waveform from the signal. The waveforms
% in these signals are less easily distinguished from others
% in the recording, but the confidence of being able to sort
% unique waveforms is high. These signals typically have
% SNR between 2 and 4.
%
% Poor signal (1): Able to identify mixed waveforms con-
% tained in the signal. It is not possible to identify unique
% waveforms in these signals with the naked eye and the
% confidence of being able to sort units is low. These sig-
% nals generally have SNR less than 2.
%
% No signal (0): Unable to distinguish signal from back-
% ground noise or a faulty electrode. SNR for these signals
% is less than 1 or the signal consists of waveforms identified
% as originating from a nonbiological source such as 60-Hz
% interference.

% Author: Ariel Tankus.
% Created: 06.03.2016.


mean_waveform = mean(spikes(cluster_inds, :));
A = max(mean_waveform) - min(mean_waveform);    % amplitude

e_noise = spikes(cluster_inds, :) - ...
          ones(length(cluster_inds), 1)*mean_waveform;
SD_noise = std(e_noise(:));  % the standard deviation taken over all values
                             % in e_noise, irrespective of their position in
                             % the matrix.

SNR = A ./ (2*SD_noise);
