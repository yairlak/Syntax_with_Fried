function handles = TASMC_default_params()
% TASMC_default_params    Parameters used for TASMC epilepsy pt recordings.

% Author: Ariel Tankus.
% Created: 13.03.2013.


%handles.par.detection = 'pos';              %type of threshold
handles.par.detection = 'both';              %type of threshold
handles.par.stdmin = 5;                     %minimum threshold
handles.par.stdmax = 50;                    %maximum threshold
handles.par.interpolation = 'y';            %interpolation for alignment
handles.par.int_factor = 2;                 %interpolation factor
handles.par.detect_fmin = 300;              %high pass filter for detection
handles.par.detect_fmax = 1000;             %low pass filter for detection
%handles.par.detect_fmin = 1000;              %high pass filter for detection
%handles.par.detect_fmax = 5000;             %low pass filter for detection
handles.par.sort_fmin = 300;                %high pass filter for sorting
%handles.par.sort_fmax = 5000;               %low pass filter for sorting
handles.par.sort_fmax = 3000;               %low pass filter for sorting
%handles.par.segments_length = 5;            %length of segments in 5' in which the data is cutted.
handles.par.min_rec_for_segmentation_min = 45;  % if total recording time is
                                                % longer than this minimum,
                                                % break into segments for
                                                % spike extraction [mins].
handles.par.segments_length = 5;            %length of segments in 15' in which the data is cutted.
handles.par.notch_filter_half_width = 1;                % Hz.
handles.par.high_voltage_thresh = 750;                  % No spikes with voltage above
handles.par.bit_resolution = 250;           % nV per LSB. From the User
                                            % Manual: "16-bit digital output, with 0.25 ÂÂ¦ÌV per bit resolution".
%handles.par.bit_resolution = 250;           % nV per LSB.
