function classes = min_clus_size(classes, min_clus)
% min_clus_size    Enforce minimal cluster size.  If clusters of less spikes
%                  exist, they are erased (=added to cluster 0).
%
%                  classes = min_clus_size(classes, min_clus)
%                  classes  - 1xn - class ID for each spike.
%                  min_clus - 1x1 - minimal number of spikes in a class.

% Author: Ariel Tankus.
% Created: 15.11.2009.


class_ids = setdiff(unique(classes), 0);
num_classes = length(class_ids);

for i=1:num_classes
    cur_class_inds = (classes == class_ids(i));
    if (sum(cur_class_inds) < min_clus)
        % current class too small; delete it: 
        classes(cur_class_inds) = 0;
    end
end
