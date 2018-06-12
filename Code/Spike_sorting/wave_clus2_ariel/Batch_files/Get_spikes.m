% PROGRAM Get_spikes.
% Gets spikes from all files in Files.txt.
% Saves spikes and spike times.

handles.par.w_pre=20;                       %number of pre-event data points stored
handles.par.w_post=44;                      %number of post-event data points stored
handles.par.detection = 'pos';              %type of threshold
handles.par.stdmin = 5;                     %minimum threshold
handles.par.stdmax = 50;                    %maximum threshold
handles.par.interpolation = 'y';            %interpolation for alignment
handles.par.int_factor = 2;                 %interpolation factor
handles.par.detect_fmin = 300;              %high pass filter for detection
handles.par.detect_fmax = 3000;             %low pass filter for detection
handles.par.sort_fmin = 300;                %high pass filter for sorting
handles.par.sort_fmax = 3000;               %low pass filter for sorting
handles.par.segments = 1;                   %nr. of segments in which the data is cutted.
handles.par.sr = 24000;                     %sampling frequency, in Hz.
handles.par.ref = floor(1.5 *handles.par.sr/1000);   %minimum refractory period (in ms)

files = textread('Files.txt','%s');

for k= 1:length(files)
    tic
    file_to_cluster = files(k);
    index_all=[];
    spikes_all=[];
    for j=1:handles.par.segments        %that's for cutting the data into pieces
        % LOAD CONTINUOUS DATA
        eval(['load ' char(file_to_cluster) ';']);
        tsmin = (j-1)*floor(length(data)/handles.par.segments)+1;
        tsmax = j*floor(length(data)/handles.par.segments);
        x=data(tsmin:tsmax); clear data; 
        
        % SPIKE DETECTION WITH AMPLITUDE THRESHOLDING
        [spikes,thr,index]  = amp_detect(x,handles.par);       %detection with amp. thresh.
        index=index+tsmin-1;
        
        index_all = [index_all index];
        spikes_all = [spikes_all; spikes];
    end
    index = index_all *1e3/handles.par.sr;                  %spike times in ms.
    spikes = spikes_all;
    eval(['save ' char(file_to_cluster) '_spikes spikes index']);    %saves Sc files
    toc
end   
