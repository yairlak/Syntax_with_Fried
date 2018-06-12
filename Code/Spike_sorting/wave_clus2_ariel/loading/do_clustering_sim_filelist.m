function [] = do_clustering_sim_filelist(filename)
% do_clustering_sim_filelist    Do clustering of a sequence of Simulator files.
%
%                               do_clustering_sim_filelist(filename)
%                               filename - string - name of file
%                                          containing a list of Simulator
%                                          filenames, each on a separate line.
%                                          The filenames should contain
%                                          NO suffix.
%
%                               See also: do_clustering_sim_file,
%                                         ext_do_clustering_from_file,
%                                         ext_do_clustering.

% Author: Ariel Tankus.
% Created: 05.09.2008.



log_file = 'cluster_sim.log';

if (nargin < 1)
    filename = 'file_list.txt';
end

if (exist(log_file, 'file'))
    delete(log_file);
end
diary(log_file);

file_list = textread(filename, '%s');

for i=1:length(file_list)
    fprintf('Clustering %s:\n', file_list{i});
    do_clustering_sim_file(file_list{i});
end

diary off;
