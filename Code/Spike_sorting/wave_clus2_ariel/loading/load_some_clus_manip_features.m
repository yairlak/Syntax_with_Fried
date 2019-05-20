function [h_feat, feature_handles, h_all_spikes, h_all_spikes_avg] = ...
    load_some_clus_manip_features(num_features, filename)
% load_some_clus_manip_features    

% Author: Ariel Tankus.
% Created: 08.02.2006.


[h_feat, feature_handles, h_feat_fname, h_all_spikes, h_all_spikes_avg] = ...
    load_clus_manip_features;
set(h_feat, 'Name', 'Clus_Manip Features #1');
set(h_feat_fname, 'String', filename);

num_combinations = sum(1:(num_features-1));  % #pairs of features.
for i=1:(ceil(num_combinations ./ length(feature_handles)) - 1)
    [tmp_h_feat, tmp_feature_handles, tmp_h_feat_fname, tmp_h_all_spikes, ...
     tmp_h_all_spikes_avg] = ...
        load_clus_manip_features;
    set(tmp_h_feat, 'Name', sprintf('Clus_Manip Features #%d', i+1));
    set(tmp_h_feat_fname, 'String', filename);

    h_feat = [h_feat, tmp_h_feat];
    feature_handles = [feature_handles, tmp_feature_handles];
end
