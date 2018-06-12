function times_CSC = load_times_CSC(ch, func_name, varargin)
% load_save_time_CSC    Execute a function on a times_CSC file, and returns
%                       the modified fields.
%
%                       This function is intended for use with times_CSC
%                       handling functions written for interactive GUI, but
%                       for executing them directly on times_CSC%d.mat files.
%
%                       times_CSC = load_time_CSC(ch, func_name, varargin)
%                       ch - 1x1 - channel number on which the function is
%                                  executed.
%                       func_name - 1x1 - function_handle - the function to
%                                  execute.  The function should receive a
%                                  times_CSC struct as first input.
%                                  times_CSC is a structure with the
%                                  following fields:
%                                  spikes - nxk - n spikes, each described by
%                                                 k observations of its
%                                                 waveform.
%                                  clustr_class - nx2 - [class, time] -
%                                                 the class of the spike (0:l)
%                                                 and the time of the spike.
%                                  par - struct - parameters.
%                                  inspk  - nxm - features (usually wavelet
%                                                 coefficients) of each
%                                                 spike.
%                                  comments - (l+1)x1 - cell of strings - opt.-
%                                                 comment for each cluster
%                                                 (including the null one,
%                                                 which serves for general
%                                                 comments).
%                                  More arguments maybe supplied to the function
%                                  in:
%                       varargin  - 1xn - additional arguments for func_name.
%                       
%                       See also: rm_high_spikes.

% Author: Ariel Tankus.
% Created: 06.02.2006.


filename = sprintf('times_CSC%d.mat', ch);
load(filename);

% convert to struct
times_CSC = struct(...
    'spikes',        spikes, ... 
    'cluster_class', cluster_class, ...
    'par',           par, ...
    'inspk',         inspk ...
);
if (exist('comments', 'var'))
    times_CSC.comments = comments;
end
if (exist('time0', 'var'))
    times_CSC.time0 = time0;
end
if (exist('timeend', 'var'))
    times_CSC.timeend = timeend;
end

% execute function varargin{1} on the arguments.
times_CSC = func_name(times_CSC, varargin{:});
