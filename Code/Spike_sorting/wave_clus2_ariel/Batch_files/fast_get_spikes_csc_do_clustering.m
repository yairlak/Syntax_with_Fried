function fast_get_spikes_csc_do_clustering
% fast_get_spikes_csc_do_clustering    

% Author: Ariel Tankus.
% Created: 13.01.2008.


ch_list = 1:64;

is_cont = check_continuity_all_ch(ch_list);
[s, w] = unix('get_spikes_csc_all');
if (s ~= 0)
    error('Error running unix script: get_spikes_csc_all');
end

ariel_do_clustering_csc(ch_list);
