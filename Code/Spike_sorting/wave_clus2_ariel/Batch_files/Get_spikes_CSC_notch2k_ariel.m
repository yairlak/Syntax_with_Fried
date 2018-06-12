function Get_spikes_CSC_notch2k_ariel(channels,TimeStamps);
% function Get_spikes_CSC(channel,TimeStamps)
% Gets spikes from all channels in the .mat file channels. This batch is
% to be used with Neuralynx data.
% Saves spikes and spike times.

% Modified: 23.07.2009 (Ariel, Roy & Omri).  Order of ellip filter
%                      changed from 2 to 4.

if nargin <1
    load channels
end
if (exist(sprintf('CSC%d.Ncs',channels(1)), 'file'))
    fname_prefix = 'CSC';
    fname_suffix = 'Ncs';
else
    % Cheetah5 conventions:
    fname_prefix = 'csc';
    fname_suffix = 'ncs';
end

if nargin <2
end

%    % make gap_inds relative to filled-in time stamps:
%    gap_inds(2:end) = gap_inds(2:end) + cumsum(gap_lens);

handles.par.detection = 'pos';              %type of threshold
handles.par.stdmin = 5;                     %minimum threshold
handles.par.stdmax = 50;                    %maximum threshold
handles.par.interpolation = 'y';            %interpolation for alignment
handles.par.int_factor = 2;                 %interpolation factor
handles.par.detect_fmin = 300;              %high pass filter for detection
handles.par.detect_fmax = 1000;             %low pass filter for detection
handles.par.sort_fmin = 300;                %high pass filter for sorting
handles.par.sort_fmax = 3000;               %low pass filter for sorting
handles.par.segments_length = 5;            %length of segments in 5' in which the data is cutted.
notch_filter_half_width = 1;                % Hz.
high_voltage_thresh = 750;                  % No spikes with voltage above
                                            % this threshold.

for k=1:length(channels)

    tic

    channel = channels(k)
    TimeStamps = read_ncs_time_stamps(channel);

    %Find the starting of the recording and gets sampling frequency
    time0 = TimeStamps(1); 
    timeend = TimeStamps(end);
    sr = 512*1e6/(TimeStamps(2)-TimeStamps(1)); % ARIEL: sampling rate in Hz.

    % ARIEL: sr/1000 = #samples in 1ms.
    % ARIEL: #samples in refrectory period (`ref') is taken as 1.5 this #.
    %        (i.e., #samples in 1.5ms).
    ref = floor(1.5 *sr/1000);       %minimum refractory period (in ms)
    handles.par.ref = ref;
    handles.par.sr = sr;
    [handles.par.w_pre, handles.par.w_post] = w_pre_post_by_sr(sr);

    lts = length(TimeStamps);
    handles.par.segments = ceil((timeend - time0) / ...
                                (handles.par.segments_length * 1e6 * 60));
    
    %That's for cutting the data into pieces
    segmentLength = floor (length(TimeStamps)/handles.par.segments);
    tsmin_ind = 1 : segmentLength :length(TimeStamps);
    tsmin_ind = tsmin_ind(1: handles.par.segments);
    tsmax_ind = tsmin_ind - 1;
    tsmax_ind = tsmax_ind(2:end);
    tsmax_ind = [tsmax_ind, length(TimeStamps)];
    recmax=tsmax_ind;
    recmin=tsmin_ind;
    tsmin = TimeStamps(int64(tsmin_ind));
    tsmax = TimeStamps(int64(tsmax_ind));
    %clear TimeStamps;

    index_all  = [];
    spikes_all = [];
    
    [gap_inds, gap_times, gap_lens, true_dt] = ...
        detect_recording_gaps(TimeStamps, channel);
    new_TimeStamps = fill_time_stamp_gaps(TimeStamps, gap_inds, true_dt);

    [fid, filename] = open_ncs_file(channel);
    fseek(fid, 16384+8+4+4+4, 'bof'); % put pointer to the beginning of data
    
    % GETS THE GAIN AND CONVERTS THE DATA TO MICRO V.
    scale_factor=str2double(read_field_from_ncs_header(channel, '-ADBitVolts'));

    BadFrequenciesAccum          = cell(1, length(tsmin));
    BadFrequenciesThresholdAccum = NaN(1, length(tsmin));

    HighVoltageIndsAll  = [];
    HighVoltageTimesAll = [];
    
    for j=1:length(tsmin)
        % LOAD CSC DATA
        Samples = fread(fid, 512*(recmax(j)-recmin(j)+1), '512*int16=>int16',...
                    8+4+4+4);
        Samples = fill_recording_gaps(Samples, tsmin_ind(j), tsmax_ind(j), ...
                    gap_inds, gap_lens);
        x = double(Samples(:))';
        clear Samples;
        %x=x*str2num(scale_factor{41})*1e6;
        x = x*scale_factor*1e6;

        % detect and filter out bad frequencies:
        [BadFrequencies, BadFrequenciesThreshold] = GetBadFrequencies(x, sr);
        BadFrequenciesAccum{j} = BadFrequencies;
        BadFrequenciesThresholdAccum(j) = BadFrequenciesThreshold;
        for bf_index = 1:length(BadFrequencies)
            if ((bf_index == 1) || (BadFrequencies(bf_index) - ...
                BadFrequencies(bf_index-1) >= notch_filter_half_width))
                fprintf(['Channel %d, chunk %d/%d: Filtering frequency ', ...
                         '%.2f .\n'], channel, j, length(tsmin), ... 
                        BadFrequencies(bf_index));
                [b,a]=ellip(2,0.5,20,[BadFrequencies(bf_index)-notch_filter_half_width, BadFrequencies(bf_index)+notch_filter_half_width]*2/sr,'stop');
                x=filtfilt(b,a,x);
            else
                % No point in a separate filter for the current frequency, as
                % it has already been filter due to the previous one, which
                % was close enough to the current:
                fprintf(['Channel %d, chunk %d/%d: Skipping frequency ', ...
                         '%.2f .\n'], channel, j, length(tsmin), ...
                        BadFrequencies(bf_index));
            end
            
        end
        HighVoltageInds     = find(x > high_voltage_thresh);
        HighVoltageIndsAll  = [HighVoltageInds, HighVoltageIndsAll + ...
                                                tsmin_ind(j) - 1];
        HighVoltageTimes    = (HighVoltageInds-1)*1e6/sr+tsmin(j);
        HighVoltageTimesAll = [HighVoltageTimesAll, HighVoltageTimes];
        
        % SPIKE DETECTION WITH AMPLITUDE THRESHOLDING
        [spikes,thr,index] = amp_detect(x,handles.par);       %detection with amp. thresh.
        % ARIEL: was: index=index*1e6/sr+tsmin(j);
        % The above is a bug, which shifts all spike times by 1 sample (i.e.,
        % by 36 microsec.):  The index begins from 1, so the if the spike
        % occurred on the first time stamp, it would be assigned the time
        % stamp of: 1*1e6/27777+tsmin(j) = 36+tsmin(j), instead of tsmin(j):
%       ARIEL: Comment out, 24.07.2009:
%        index=(index-1)*1e6/sr+tsmin(j);
        index = index_to_sample_time(index, recmin(j), new_TimeStamps);
        index_all = [index_all index];
        spikes_all = [spikes_all; spikes];
    end
    fclose(fid);
%    index = (index_all-time0)/1000;
%    HighVoltageTimesAll = (HighVoltageTimesAll - time0) ./ 1000;
    index = index_all ./ 1000;
    HighVoltageTimesAll = HighVoltageTimesAll ./ 1000;
    spikes = spikes_all;
    save(['CSC', num2str(channel), '_spikes'], 'spikes', 'index');
    save(sprintf('BadFrequencies%d.mat', channel), 'BadFrequenciesAccum', ...
         'BadFrequenciesThresholdAccum');
    save(sprintf('HighVoltageTimes%d.mat', channel), 'HighVoltageTimesAll', ...
         'HighVoltageIndsAll');
    fprintf('Detected %d cases of too-high voltage.\n', ...
            length(HighVoltageTimesAll));
    toc

end   
