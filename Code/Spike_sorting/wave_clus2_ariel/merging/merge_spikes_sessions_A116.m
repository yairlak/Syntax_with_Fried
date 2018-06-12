function [] = merge_spikes_sessions_A116()
% merge_spikes_sessions_A116    

% Author: Ariel Tankus.
% Created: 31.07.2010.


dir1 = '/media/Linux2T2/arielt/analysis116/part1';
dir2 = '/media/Linux2T2/arielt/analysis116/part2';
ch_list = 1:64;
out_dir = '/media/Linux2T2/arielt/analysis116/merged_spikes';

merge_spikes_sessions(dir1, dir2, ch_list, out_dir);
