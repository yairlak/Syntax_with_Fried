function Get_spikes_CSC(channels,TimeStamps);
% function Get_spikes_CSC(channel,TimeStamps)
% Gets spikes from all channels in the .mat file channels. This batch is
% to be used with Neuralynx data.
% Saves spikes and spike times.
if nargin <1
    load channels
end
if nargin <2
    filename=sprintf('CSC%d.Ncs',channels(1));
    f=fopen(filename);
    fseek(f,16384,'bof'); % Skip Header, put pointer to the first record
    TimeStamps=fread(f,inf,'int64',(4+4+4+2*512)); %Read all TimeStamps
    fclose(f);
end

%Find the starting of the recording and gets sampling frequency
time0 = TimeStamps(1); 
timeend = TimeStamps(end);
sr = 512*1e6/(TimeStamps(2)-TimeStamps(1)); % ARIEL: sampling rate in Hz.

[handles.par.w_pre, handles.par.w_post] = w_pre_post_by_sr(sr);
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

% ARIEL: sr/1000 = #samples in 1ms.
% ARIEL: #samples in refrectory period (`ref') is taken as 1.5 this #.
%        (i.e., #samples in 1.5ms).
ref = floor(1.5 *sr/1000); handles.par.ref = ref;       %minimum refractory period (in ms)
handles.par.sr = sr; handles.par.ref = ref;

lts = length(TimeStamps);
handles.par.segments = ceil((timeend - time0) / (handles.par.segments_length * 1e6 * 60));

%That's for cutting the data into pieces
segmentLength = floor (length(TimeStamps)/handles.par.segments);
tsmin = 1 : segmentLength :length(TimeStamps);
tsmin = tsmin(1: handles.par.segments);
tsmax = tsmin - 1;
tsmax = tsmax (2:end);
tsmax = [tsmax, length(TimeStamps)];
recmax=tsmax;
recmin=tsmin;
tsmin = TimeStamps(int64(tsmin));
tsmax = TimeStamps(int64(tsmax));
clear TimeStamps;

%load channels
for k= 1:length(channels)
    tic
    index_all=[];
    spikes_all=[];
    channel=channels(k)
    filename=sprintf('CSC%d.Ncs',channel);
    f=fopen(filename,'r');
    fseek(f,16384+8+4+4+4,'bof'); % put pointer to the beginning of data
    
    %GETS THE GAIN AND CONVERTS THE DATA TO MICRO V.
    scale_factor = str2num(read_field_from_ncs_header(channel, '-ADBitVolts'));
    
    for j=1:length(tsmin)
        % LOAD CSC DATA
        Samples=fread(f,512*(recmax(j)-recmin(j)+1),'512*int16=>int16',8+4+4+4);
        x=double(Samples(:))'; clear Samples;
        x=x*str2num(scale_factor{41})*1e6;
        
        % SPIKE DETECTION WITH AMPLITUDE THRESHOLDING
        [spikes,thr,index] = amp_detect(x,handles.par);       %detection with amp. thresh.
        % ARIEL: was: index=index*1e6/sr+tsmin(j);
        % The above is a bug, which shifts all spike times by 1 sample (i.e.,
        % by 36 microsec.):  The index begins from 1, so the if the spike
        % occurred on the first time stamp, it would be assigned the time
        % stamp of: 1*1e6/27777+tsmin(j) = 36+tsmin(j), instead of tsmin(j):
        index=(index-1)*1e6/sr+tsmin(j);
        index_all = [index_all index];
        spikes_all = [spikes_all; spikes];
    end
    fclose(f);
    index = (index_all-time0)/1000;
    spikes = spikes_all;
    save(['CSC', num2str(channel), '_spikes'], 'spikes', 'index');    %saves Sc files
    toc
end   
