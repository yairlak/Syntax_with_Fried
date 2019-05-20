function filter_spec = get_filter_spec_by_datatype(datatype_str)
% get_filter_spec_by_datatype    Get the filter specification for the
%                                filename of a given type based on the data
%                                type.  The filter specification is a string
%                                (with wildcards) describing filenames of the
%                                specified type.
%
%                                filter_spec =
%                                    get_filter_spec_by_datatype(datatype_str)
%                                datatype_str - string - One of:
%                                                 'Simulator'
%                                                 'CSC data'
%                                                 'CSC data (pre-clustered)'
%                                                 'Sc data'
%                                                 'Sc data (pre-clustered)'
%                                                 'MIT data'
%                                                 'ASCII'
%                                                 'ASCII (pre-clustered)'
%                                                 'ASCII spikes'
%                                                 'ASCII spikes (pre-clustered)'
%                                filter_spec  - string - filter for filenames.
%
%                                See also: wave_clus, uigetfile.

% Author: Ariel Tankus.
% Created: 27.11.2005.


switch char(datatype_str)
 case 'Simulator'
  filter_spec = 'C_*.mat';
 case {'CSC data', 'CSC data (pre-clustered)'}
  filter_spec = '*.Ncs';
 case 'Neuroport data'
%  filter_spec = {'CSC[0-9].mat;CSC[0-9][0-9].mat;CSC[0-9][0-9][0-9].mat;CSC[0-9][0-9][0-9][0-9].mat' 'CSC*.mat'};
%  filter_spec = {'CSC?.mat;CSC??.mat;CSC???.mat;CSC????.mat' 'CSC[0-9]+.mat'};
%  filter_spec = {'times_CSC?.mat;times_CSC??.mat;times_CSC???.mat;times_CSC????.mat' 'times_CSC[0-9]+.mat'};
  filter_spec = 'times_CSC*.mat';
 case {'Sc data', 'Sc data (pre-clustered)'}
  filter_spec = '*.Nse';
 case 'MIT data'
  filter_spec = '*.m';
 case {'ASCII', 'ASCII (pre-clustered)', 'ASCII spikes', 'ASCII spikes (pre-clustered)'}
  filter_spec = '*.mat';
end
