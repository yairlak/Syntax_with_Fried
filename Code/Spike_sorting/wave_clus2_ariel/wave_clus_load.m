function is_rejected = wave_clus_load(hObject, handles, filename, pathname)
% wave_clus_load    

% Author: Ariel Tankus.
% Created: 27.11.2005.


is_rejected = false;      % was the channel automatically rejected?

set(handles.status, 'string', ['Loading: ' pathname filename]);
drawnow;
cd(pathname);
switch char(handles.datatype)
    case 'Simulator'  
        load([pathname filename]);                      % Load data
        x.data=data;
        x.sr=1000./samplingInterval;

        timetotal = (length(data)-1).*samplingInterval;
        handles.par = set_parameters_simulation(x.sr,filename,handles,timetotal);     % Load parameters
        [pathstr, basename, ext, versn] = fileparts(filename);
        handles.par.fname = [handles.par.fname, '_', basename];
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));

        [spikes,thr,index] = amp_detect_wc(x.data,handles);     % Detection with amp. thresh.
        [inspk] = wave_features_wc(spikes,handles);        % Extract spike features.
        
        %Interaction with SPC
        save(handles.par.fname, 'inspk', '-ascii');
        [clu,tree] = run_cluster(handles);
        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        USER_DATA{7} = inspk;
        set(handles.wave_clus_figure,'userdata',USER_DATA)

    case 'CSC data'                %neuralynks (CSC files)
        if length(filename) == 8
            channel = filename(4);
        else
            channel = filename(4:5);
        end
        % ARIEL: comment out:
%        eval(['[TimeStamps] = Nlx2MatCSC(''CSC' channel '.Ncs'',1,0,0,0,0,0);']);
        % ARIEL:
        TimeStamps = read_time_stamps(['CSC', channel, '.Ncs']);

        time0 = TimeStamps(1); 
        timeend = TimeStamps(end);
        sr = 512*1e6/(TimeStamps(2)-TimeStamps(1));
        handles.par = set_parameters_CSC(sr,filename,(timeend - time0)*1E-6, ...
                                            handles);     % Load parameters
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        
        %Load continuous data 
        if strcmp(handles.par.tmax,'all')           %Loads all data
            index_all=[];
            spikes_all=[];
            lts = length(TimeStamps);
            %Segments the data in par.segments pieces
            segmentLength = floor (lts/handles.par.segments);
            tsmin = 1 : segmentLength :lts;
            tsmin = tsmin(1:handles.par.segments);
            tsmax = tsmin - 1;
            tsmax = tsmax (2:end);
            tsmax = [tsmax, lts];
            tsmin = TimeStamps(int64(tsmin));
            tsmax = TimeStamps(int64(tsmax));

            ncs_filename = ['CSC', num2str(channel) '.Ncs'];
            if (~exist(ncs_filename, 'file'))
                set(handles.status, 'String', ['File not found: ', ...
                                    ncs_filename]);
                drawnow;
                return;
            end
            for j=1:length(tsmin)
                % ARIEL: comment out:
%                eval(['[Samples] = Nlx2MatCSC(''CSC' num2str(channel) '.Ncs'',0,0,0,0,1,0, tsmin(j),tsmax(j));']);
                % ARIEL:
                Samples = Nlx2MatCSC_v3(ncs_filename, [0,0,0,0,1], 0, 4, ...
                            [tsmin(j), tsmax(j)]);
% xxx               eval(['[TimeStamps] = read_time_stamps(''CSC' channel '.Ncs'');']);
                x=Samples(:)'; clear Samples;
                
                %GETS THE GAIN AND CONVERTS THE DATA TO MICRO V.
                scale_factor=textread(['CSC', num2str(channel), '.Ncs'], ...
                            '%s', 41);
                x=x*str2num(scale_factor{41})*1e6;
                
                handles.flag = j;                   %flag for ploting only in the 1st loop
                [spikes,thr,index]  = amp_detect_wc(x,handles);       %detection with amp. thresh.
                index = index*1e6/sr+tsmin(j);
                index_all = [index_all index];
                spikes_all = [spikes_all; spikes];
            end
            index = (index_all-time0)/1000;
            spikes = spikes_all;
            USER_DATA = get(handles.wave_clus_figure,'userdata');
            USER_DATA{2}=spikes;
            USER_DATA{3}=index;
            set(handles.wave_clus_figure,'userdata',USER_DATA);
        else                                        %Loads a data segment
            tsmin = handles.par.tmin * 1e6;
            tsmax = handles.par.tmax * 1e6;
            % ARIEL: comment out:
%            eval(['[Samples] = Nlx2MatCSC(''' filename ''',0,0,0,0,1,0, time0+tsmin,time0+tsmin+tsmax);']);
            % ARIEL:
            Samples = Nlx2MatCSC_v3(filename, [0,0,0,0,1], 0, 4, ...
                        [time0+tsmin, time0+tsmin+tsmax]);
            x=Samples(:)'; clear Samples;
            [spikes,thr,index] = amp_detect_wc(x,handles);     % Detection with amp. thresh.
        end

        [inspk] = wave_features_wc(spikes,handles);        % Extract spike features.
        
        if handles.par.match == 'y';
            naux = min(handles.par.max_spk,size(inspk,1));
            inspk_aux = inspk(1:naux,:);
        else
            inspk_aux = inspk;
        end
            
        %Interaction with SPC
        save data inspk_aux -ascii
        [clu,tree] = run_cluster(handles);
        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        USER_DATA{7} = inspk;
        
        USER_DATA{30} = time0;
        USER_DATA{31} = timeend;
        set(handles.wave_clus_figure,'userdata',USER_DATA)
        
        
    case 'CSC data (pre-clustered)'                %neuralynks (CSC files)

t=tic;
        [channel, count] = sscanf(filename, 'CSC%d.Ncs');
        channel
        if (count == 0)
            set(handles.status, 'string', ['Loading: ' pathname filename]);
            drawnow;
            fprintf('Unknown file name format (expecting: CSC%d.Ncs).');
            return;
        end
        % ARIEL: comment out:
%        eval(['[TimeStamps] = Nlx2MatCSC(''CSC' channel '.Ncs'',1,0,0,0,0,0);']);
        % ARIEL:
        ncs_filename = ['CSC', num2str(channel) '.Ncs'];
        if (~exist(ncs_filename, 'file'))
            set(handles.status, 'String', ['File not found: ', ...
                                ncs_filename]);
            drawnow;
            return;
        end

fprintf('Before read time stamps:  ');
toc(t);
%        TimeStamps = read_time_stamps(ncs_filename);
%        TimeStamps = Nlx2MatCSC_v3(ncs_filename, [1,0,0,0,0], 0, 1);
        [first_time_stamps, last_time_stamp] = read_first_last_time_stamp(filename);
        fprintf('After read time stamps:  ');
toc(t);

        [time0, timeend, sr, timetotal] = read_main_time_stamps(filename);
        handles.par = set_parameters_CSC(sr,filename,timetotal,handles);     % Load parameters
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        
        %Load spikes and parameters
        times_filename = ['times_CSC', num2str(channel), '.mat'];
        if (~exist(times_filename, 'file'))
            set(handles.status, 'String', ['File not found: ', ...
                                times_filename]);
            drawnow;
            value = questdlg('Create dummy times_CSC file?', ...
                        'No times_CSC file found', 'Yes', 'No', 'Yes');
            if (strcmp(value, 'Yes'))
                make_cluster0_times_file(times_filename, handles, channel);
%                make_degen_times_file(times_filename, handles);
            end
            return;
        end
        load(times_filename);
        % ARIEL: don't use fast reject for the time being.
%        [is_rejected, channel_freq] = fast_reject_low_freq(cluster_class, ...
%                    inspk, handles.par, spikes, times_filename);
%        if (is_rejected)
%            set(handles.status, 'string', sprintf('%s rejected (%.2fHz).', ...
%                        filename, channel_freq));
%            display_file_name(pathname, filename, handles);  % for "Load next".
%            guidata(hObject, handles);
%            return;
%        end
        index=cluster_class(:,2)';

fprintf('Fast reject done:  ');
toc(t);

        %Load clustering results
        fname = ['data_ch' num2str(channel)];           %filename for interaction with SPC
        lab_filename = [fname, '.dg_01.lab'];
        if (~exist(lab_filename, 'file'))
            set(handles.status, 'String', ['File not found: ', lab_filename]);
            drawnow;
            return;
        end
        clu=load(lab_filename);
        dg_filename = [fname, '.dg_01'];
        if (~exist(lab_filename, 'file'))
            set(handles.status, 'String', ['File not found: ', dg_filename]);
            drawnow;
            return;
        end
        tree=load(dg_filename); 


fprintf('Load dg_01{,.lab}:  ');
toc(t);

        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{2} = spikes;
        USER_DATA{3} = index;
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        if exist('inspk');
            USER_DATA{7} = inspk;
        end
        
        USER_DATA{30} = time0;
        USER_DATA{31} = timeend;
        set(handles.wave_clus_figure,'userdata',USER_DATA)

fprintf('User data updated:  ');
toc(t);

        if (is_display_continous_data)
            load_samples_and_continuous_plot(filename, time0, channel, handles);
        end

fprintf('amp_detect_wc done:  ');
toc(t);


    case 'Neuroport data'

t=tic;

toc(t);
        channel = sscanf(filename, 'times_CSC%d.mat');

        load electrode_info.mat;
        sr = samp_freq_hz;
        timetotal_sec = (num_samples-1) ./ samp_freq_hz;

        handles.par = set_parameters_CSC(sr,filename,timetotal_sec,handles);     % Load parameters
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        
        %Load spikes and parameters
        times_filename = ['times_CSC', num2str(channel), '.mat'];
        if (~exist(times_filename, 'file'))
            set(handles.status, 'String', ['File not found: ', ...
                                times_filename]);
            drawnow;
            value = questdlg('Create dummy times_CSC file?', ...
                        'No times_CSC file found', 'Yes', 'No', 'Yes');
            if (strcmp(value, 'Yes'))
                make_cluster0_times_file(times_filename, handles, channel);
%                make_degen_times_file(times_filename, handles);
            end
            return;
        end
        load(times_filename);
        % ARIEL: don't use fast reject for the time being.
%        [is_rejected, channel_freq] = fast_reject_low_freq(cluster_class, ...
%                    inspk, handles.par, spikes, times_filename);
%        if (is_rejected)
%            set(handles.status, 'string', sprintf('%s rejected (%.2fHz).', ...
%                        filename, channel_freq));
%            display_file_name(pathname, filename, handles);  % for "Load next".
%            guidata(hObject, handles);
%            return;
%        end
        index=cluster_class(:,2)';

fprintf('Fast reject done:  ');
toc(t);

        %Load clustering results
        fname = ['data_ch' num2str(channel)];           %filename for interaction with SPC
        lab_filename = [fname, '.dg_01.lab'];
        if (~exist(lab_filename, 'file'))
            set(handles.status, 'String', ['File not found: ', lab_filename]);
            drawnow;
            return;
        end
        clu=load(lab_filename);
        dg_filename = [fname, '.dg_01'];
        if (~exist(lab_filename, 'file'))
            set(handles.status, 'String', ['File not found: ', dg_filename]);
            drawnow;
            return;
        end
        tree=load(dg_filename); 


fprintf('Load dg_01{,.lab}:  ');
toc(t);

        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{2} = spikes;
        USER_DATA{3} = index;
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        if exist('inspk');
            USER_DATA{7} = inspk;
        end
        
        USER_DATA{30} = time0;
        USER_DATA{31} = timeend;
        set(handles.wave_clus_figure,'userdata',USER_DATA)

fprintf('User data updated:  ');
toc(t);

%        if (is_display_continous_data)
%            load_samples_and_continuous_plot(filename, time0, channel, handles);
%        end

fprintf('amp_detect_wc done:  ');
toc(t);
        
    case 'Sc data'
        if length(filename) == 7
            channel = filename(3);
        else
            channel = filename(3:4);
        end
        [index, Samples] = Nlx2MatSE(['Sc', channel, '.Nse'], 1, 0, ...
                    0, 0, 1, 0);
        spikes(:,:)= Samples(:,1,:); clear Samples; spikes = spikes';
        handles.par = set_parameters_Sc(filename,handles);     % Load parameters
        
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        axes(handles.cont_data); cla
        
        [inspk] = wave_features_wc(spikes,handles);        % Extract spike features.

        if handles.par.match == 'y';
            naux = min(handles.par.max_spk,size(inspk,1));
            inspk_aux = inspk(1:naux,:);
        else
            inspk_aux = inspk;
        end
            
        %Interaction with SPC
        save data inspk_aux -ascii
        [clu,tree] = run_cluster(handles);
        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{2} = spikes;
        USER_DATA{3} = index/1000;
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        USER_DATA{7} = inspk;
        set(handles.wave_clus_figure,'userdata',USER_DATA)
        
        
    case 'MIT data'
        file = filename(1:end-2);
        eval(file);
        sr = 1e6/c.t{1}.electrode1.waveforms(1).samplingInterval_us;    %in Hz.
        handles.par = set_parameters_MIT(sr,filename,handles);     % Load parameters
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        axes(handles.cont_data); cla
        [spikes,index] = Clean_data_MIT(file,c,handles)
        
        [inspk] = wave_features_wc(spikes,handles);        % Extract spike features.

        if handles.par.match == 'y';
            naux = min(handles.par.max_spk,size(inspk,1));
            inspk_aux = inspk(1:naux,:);
        else
            inspk_aux = inspk;
        end
            
        %Interaction with SPC
        save data inspk_aux -ascii
        [clu,tree] = run_cluster(handles);
        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{2} = spikes;
        USER_DATA{3} = index;
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        USER_DATA{7} = inspk;
        set(handles.wave_clus_figure,'userdata',USER_DATA)
        
    case 'Sc data (pre-clustered)'
        if length(filename) == 7
            channel = filename(3);
        else
            channel = filename(3:4);
        end
        [index, Samples] = Nlx2MatSE(['Sc', channel, '.Nse'], 1, 0, 0, 0, 1, 0);
        spikes(:,:)= Samples(:,1,:); spikes = spikes';
        handles.par = set_parameters_Sc(filename,handles);     % Load parameters
        clear Samples;
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        axes(handles.cont_data); cla

        %Load clustering results
        fname = ['data_ch' num2str(channel)];           %filename for interaction with SPC
        clu=load([fname '.dg_01.lab']);
        tree=load([fname '.dg_01']); 

        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{2} = spikes;
        USER_DATA{3} = index/1000;
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        set(handles.wave_clus_figure,'userdata',USER_DATA)
        
        
    case 'ASCII'            % ASCII matlab files
        handles.par = set_parameters_ascii(filename,handles);     % Load parameters
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        
        index_all=[];
        spikes_all=[];
        for j=1:handles.par.segments        %that's for cutting the data into pieces
            % LOAD CONTINUOUS DATA
            load(filename);
            x=data(:)';
            tsmin = (j-1)*floor(length(data)/handles.par.segments)+1;
            tsmax = j*floor(length(data)/handles.par.segments);
            x=data(tsmin:tsmax); clear data; 
            handles.flag = 1;                   %flag for ploting only in the 1st loop
            
            % SPIKE DETECTION WITH AMPLITUDE THRESHOLDING
            [spikes,thr,index]  = amp_detect_wc(x,handles);       %detection with amp. thresh.
            index=index+tsmin-1;
            
            index_all = [index_all index];
            spikes_all = [spikes_all; spikes];
        end
        index = index_all *1e3/handles.par.sr;                  %spike times in ms.
        spikes = spikes_all;
        
        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{2}=spikes;
        USER_DATA{3}=index;
        set(handles.wave_clus_figure,'userdata',USER_DATA);

        [inspk] = wave_features_wc(spikes,handles);        % Extract spike features.

        if handles.par.match == 'y';
            naux = min(handles.par.max_spk,size(inspk,1));
            inspk_aux = inspk(1:naux,:);
        else
            inspk_aux = inspk;
        end
            
        %Interaction with SPC
        save data inspk_aux -ascii
        [clu,tree] = run_cluster(handles);
        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        USER_DATA{7} = inspk;
        set(handles.wave_clus_figure,'userdata',USER_DATA)
        
        
    case 'ASCII (pre-clustered)'                %ASCII matlab files
        handles.par = set_parameters_ascii(filename,handles);     % Load parameters
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        
        %Load spikes and parameters
        load(['times_', filename]);
        index=cluster_class(:,2)';

        %Load clustering results
        fname = ['data_' filename(1:end-4)];           %filename for interaction with SPC
        clu=load([fname '.dg_01.lab']);
        tree=load([fname '.dg_01']); 

        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{2} = spikes;
        USER_DATA{3} = index;
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        if exist('inspk');
            USER_DATA{7} = inspk;
        end
        set(handles.wave_clus_figure,'userdata',USER_DATA)

        %Load continuous data (for ploting)
        load(filename);
        x=data(:)'; 
        x(60*handles.par.sr+1:end)=[];      %will plot just 60 sec.

        [spikes,thr,index] = amp_detect_wc(x,handles);     % Detection with amp. thresh.
       
        
    case 'ASCII spikes'
        handles.par = set_parameters_ascii_spikes(filename,handles);     % Load parameters
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        axes(handles.cont_data); cla
        
        %Load spikes
        load(filename);
        
        [inspk] = wave_features_wc(spikes,handles);        % Extract spike features.

        if handles.par.match == 'y';
            naux = min(handles.par.max_spk,size(inspk,1));
            inspk_aux = inspk(1:naux,:);
        else
            inspk_aux = inspk;
        end
            
        %Interaction with SPC
        save data inspk_aux -ascii
        [clu,tree] = run_cluster(handles);
        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{2} = spikes;
        USER_DATA{3} = index(:)';
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        USER_DATA{7} = inspk;
        set(handles.wave_clus_figure,'userdata',USER_DATA)
        
        
    case 'ASCII spikes (pre-clustered)'
        handles.par = set_parameters_ascii_spikes(filename,handles);     % Load parameters
        set(handles.min_clus_edit,'string',num2str(handles.par.min_clus));
        axes(handles.cont_data); cla

        %Load spikes and parameters
        load(['times_', filename]);
        index=cluster_class(:,2)';

        %Load clustering results
        fname = ['data_' filename(1:end-4)];           %filename for interaction with SPC
        clu=load([fname '.dg_01.lab']);
        tree=load([fname '.dg_01']); 

        USER_DATA = get(handles.wave_clus_figure,'userdata');
        USER_DATA{2} = spikes;
        USER_DATA{3} = index(:)';
        USER_DATA{4} = clu;
        USER_DATA{5} = tree;
        set(handles.wave_clus_figure,'userdata',USER_DATA)
        
end    


temp=find_temp(tree,handles);                % Selects temperature.
axes(handles.temperature_plot);
switch handles.par.temp_plot
    case 'lin'
        plot([1 handles.par.num_temp],[handles.par.min_clus handles.par.min_clus],'k:',...
            1:handles.par.num_temp,tree(1:handles.par.num_temp,5:size(tree,2)),[temp temp],[1 tree(1,5)],'k:')
    case 'log'
        semilogy([1 handles.par.num_temp],[handles.par.min_clus handles.par.min_clus],'k:',...
            1:handles.par.num_temp,tree(1:handles.par.num_temp,5:size(tree,2)),[temp temp],[1 tree(1,5)],'k:')
end
xlim([0 handles.par.num_temp + 0.5])
xlabel('Temperature'); ylabel('Clusters size');
display_file_name(pathname, filename, handles);

% ARIEL: 2006-06-05
if (exist('cluster_class', 'var'))
    % already manually classified
    classes = cluster_class(:, 1)';    % override prev. def.
else
    if size(clu,2)-2 < size(spikes,1);
        classes = clu(temp,3:end)+1;
        classes = [classes(:)' zeros(1,size(spikes,1)-handles.par.max_spk)];
    else
%%% THIS PART IS BUGGY: See A14-ch45:  classes should have the size of
%                                      `spikes', even if `clu' is larger.
        classes = clu(temp,3:end)+1;
    end
end

if (exist('electrode_montage.m', 'file'))
    % display brain region
    set(handles.brain_region, 'String', find_brain_region(channel, false));
else
    set(handles.brain_region, 'String', '');
end

guidata(hObject, handles);
USER_DATA = get(handles.wave_clus_figure,'userdata');
USER_DATA{6} = classes(:)';
USER_DATA{8} = temp;
USER_DATA{9} = classes(:)';         % backup for non-forced classes.
USER_DATA{32} = channel;
set(handles.wave_clus_figure,'userdata',USER_DATA);

%clear_edit_objs;
plot_spikes(handles);
drawnow;
set(handles.status, 'String', 'Ready');

% restore comments:
if (exist('comments', 'var'))
    num_comments = length(comments);
else
    num_comments = 0;
end
for i=1:num_comments
    edit_obj = findobj('Tag', sprintf('edit%d', i-1));
    set(edit_obj, 'String', comments{i});
end
% clear comment field for the rest of the clusters:
for i=(num_comments+1):14
    edit_obj = findobj('Tag', sprintf('edit%d', i-1));
    set(edit_obj, 'String', '');
end
