function [index, spikes, part_id] = multi_part_spikes(index_cell, spikes_cell)
% multi_part_spikes    Merge multiple spike sets into one set, and keep an
%                      indication of the origin of each.
%
%                      [index, spikes, part_id] = multi_part_spikes(index_cell,
%                          spikes_cell)
%                      index_cell - cell 1xk or kx1 - each element: 1xn_i -
%                                            spike times of k parts.  Part i has
%                                            n_i spikes.
%                      spikes_cell - cell 1xk or kx1 - each element: n_i x l -
%                                            waveforms of spikes of k parts.
%                                            Each waveform consists of l
%                                            samples.
%                      index   - 1 x sum(n_i) - spike times.
%                      spikes  - sum(n_i) x l - spike waveforms.
%                      part_id - 1 x sum(n_i) - unique ID for every part.
%
%                      See also:  create_fictitious_ch, merge_fictitious_ch.

% Author: Ariel Tankus.
% Created: 26.03.2008.


index = [];
spikes = [];

num_parts = length(index_cell);
total_num_spikes = sum(cellfun('length', index_cell));

index   = zeros(1, total_num_spikes);
spikes  = zeros(total_num_spikes, size(spikes_cell{1}, 2));
part_id = zeros(1, total_num_spikes);

next_first_ind = 1;
for i=1:num_parts
    
    cur_num_spikes = length(index_cell{i});
    next_last_ind  = next_first_ind + cur_num_spikes - 1;
    inds           = next_first_ind:next_last_ind;

    index(inds)     = index_cell{i};
    spikes(inds, :) = spikes_cell{i};
    part_id(inds)   = i;
    
    next_first_ind = next_last_ind + 1;
    
end
