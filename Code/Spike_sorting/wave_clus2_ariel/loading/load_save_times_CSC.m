function [] = load_save_times_CSC(ch, func_name, varargin)
% load_save_times_CSC    Execute a function on a times_CSC file, and save the
%                       result in that file.  The original file is overwritten.
%
%                       This function is intended for use with times_CSC
%                       handling functions written for interactive GUI, but
%                       for executing them directly on times_CSC%d.mat files.
%
%                       load_save_times_CSC(ch, func_name, varargin)
%                       ch - 1x1 - channel number on which the function is
%                                  executed.
%                       func_name - 1x1 - function_handle - the function to
%                                  execute.  The function should receive a
%                                  times_CSC struct as first input (see
%                                  load_time_CSC), maybe followed by other
%                                  arguments:
%                       varargin  - 1xn - additional arguments for func_name.
%                       
%                       See also: load_time_CSC, rm_high_spikes.

% Author: Ariel Tankus.
% Created: 06.02.2006.


times_CSC = load_times_CSC(ch, func_name, varargin{:});
save_times_CSC(ch, times_CSC);
