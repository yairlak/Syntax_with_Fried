function load_samples_and_continuous_plot(filename, time0, channel, handles)
% load_samples_and_continuous_plot    

% Author: Ariel Tankus.
% Created: 22.06.2006.


%cache_file = sprintf('./waveform_params_cache%d.mat', channel);
%if (exist(cache_file, 'file'))
%    load(cache_file);
%    read only beginning!
%    Plot_continuous_data(xf,handles,thr,thrmax);
%    return;
%end

    
%Load continuous data (for ploting)
% ARIEL: comment out:
%        eval(['[Samples] = Nlx2MatCSC(''' filename ''',0,0,0,0,1,0, time0,time0+60*1e6);']);
% ARIEL:
Samples = Nlx2MatCSC_v3(filename, [0,0,0,0,1], 0, 4, [time0, time0+60*1e6]);
x=Samples(:)';
clear Samples;

%GETS THE GAIN AND CONVERTS THE DATA TO MICRO V.
scale_factor=textread(['CSC', num2str(channel), '.Ncs'], '%s', 41);
x=x*str2num(scale_factor{41})*1e6;

% amp_detect_wc is required to display filtered continuous data. 
% It produces a cache for later faster load.
% Detection with amp. thresh. 
[spikes,thr,index] = fast_amp_detect_wc(x,handles,channel);
