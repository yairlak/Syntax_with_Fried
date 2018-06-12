function [] = merge_fictitious_ch(first_fict_ch)
% merge_fictitious_ch    

% Author: Ariel Tankus.
% Created: 19.06.2006.


if (nargin < 1)
    first_fict_ch = 1000;
end

ch_cl = recluster_cut;
split_some_clusters_from_another_ch(ch_cl, first_fict_ch);

elec_info = ['.', filesep, 'electrode_info.mat.bkp_fict'];
if (exist(elec_info, 'file'))
    [status, message, messageid] = movefile(elec_info, ...
                                         ['.', filesep, 'electrode_info.mat']);
    if (status == 0)
        error('Cannot restore back %s up: %s', elec_info, message);
    end
    fprintf('electrode_info.mat restored.\n');
end

fprintf('Make sure to re-check clusters after merge!\n');
