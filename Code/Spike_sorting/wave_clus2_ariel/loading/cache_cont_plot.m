function [] = cache_cont_plot(ch_list)
% cache_cont_plot    

% Author: Ariel Tankus.
% Created: 22.06.2006.


if (nargin < 1)
    ch_list = 1:64;
end

for ch=ch_list
    fprintf('\nChannel %d:\n\n', ch);
    
    filename = sprintf('CSC%d.Ncs', ch);
    [time0, timeend, sr, timetotal] = read_main_time_stamps(filename);
    par = set_joint_parameters_CSC(sr);
    
    Samples = Nlx2MatCSC_v3(filename, [0,0,0,0,1], 0, 4, [time0, time0+60*1e6]);
    Samples = Samples(:)';

    %GETS THE GAIN AND CONVERTS THE DATA TO MICRO V.
    scale_factor = textread(['CSC', num2str(ch), '.Ncs'], '%s', 41);
    Samples = Samples*str2num(scale_factor{41})*1e6;

    % amp_detect_wc is required to display filtered continuous data:
    % Detection with amp. thresh.
    [spikes,thr,index] = amp_detect(Samples, par, ch);
end
