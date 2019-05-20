function [low_isi_inds_in_cl, cl_inds] = find_low_isi_inds(times_CSC, cl, th)
% find_low_isi_inds    

% Author: Ariel Tankus.
% Created: 20.02.2006.


if (nargin < 3)
    th = 2.5;     % ms
end

cl_inds = find(times_CSC.cluster_class(:, 1) == cl);
isi = diff(times_CSC.cluster_class(cl_inds, 2));
low_isi_inds_in_cl = find(isi < th);
