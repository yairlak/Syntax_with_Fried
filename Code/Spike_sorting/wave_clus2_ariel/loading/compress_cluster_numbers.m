function times_CSC = compress_cluster_numbers(times_CSC)
% compress_cluster_numbers    Ensure the cluster numbers are successive
%                             natural numbers.
%
%                             times_CSC = compress_cluster_numbers(times_CSC)
%                             times_CSC - struct - see load_save_time_CSC.
%
%                             See also: load_save_time_CSC,
%                                       compress_cluster_ids.

% Author: Ariel Tankus.
% Created: 07.02.2006.
% Modified: 02.09.2008.


times_CSC.cluster_class = compress_cluster_ids(times_CSC.cluster_class)
