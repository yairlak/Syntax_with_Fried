function [] = merge_spikes_sessions_A103()
% merge_spikes_sessions_A103    

% Author: Ariel Tankus.
% Created: 14.08.2009.


dir1 = '/media/linux2/arielt/analysis103_p1';
dir2 = '/media/linux2/arielt/analysis103';
ch_list = 1:64;
out_dir = '/media/linux2/arielt/analysis103_merged';

merge_spikes_sessions(dir1, dir2, ch_list, out_dir);
