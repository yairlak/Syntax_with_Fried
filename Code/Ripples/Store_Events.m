%% Load the information needed for the analysis
cd('/media/czacharo/TOSHIBA_EXT/NeuroSyntax2/Data/TS096/Ripples')
load('evtTime_TS096.mat');
load('high_freq_events_TS096.mat');
load('low_freq_events_TS096.mat');
cd( '/media/czacharo/TOSHIBA_EXT/NeuroSyntax2/Data/TS096')  ;   % Linux
load('data_ac.mat')
addpath('/home/czacharo/Applications/fieldtrip-20171218')            % Adds fieldtrip (just in case)

%% Store the number of events per channel
% Number_of_events = cell{1,185};
% clear Number_of_events
clear Number_of_events
for chani = 1:size(data_ac,1)
    Number_of_events{chani} = size(highfreq_events{chani},1);
end
Number_of_events{end} = [];                                               % Remove the trigger channel
Number_of_events = cell2mat(Number_of_events);          % Convert the cell to mat
[Val_Max, Idx_Max] = max(Number_of_events) ;               % Find the electrode with the most events
bar(Number_of_events)
xticks([1:185])                                               % Uncomment if you want to plot a tick for every channel
xlabel(['Channels'])
ylabel(['Number of Ripples detected'])
title({'Ripples detected per channel for patient TS096'})
%% Find the electrodes that show a significant number of events
threshold = 300;                                                                                                                                         % Threshold of significance measured in number of events
significant_electrodes = find(Number_of_events>threshold);
number_of_signi_electrodes = length(Number_of_events(find(Number_of_events>500))) ;             % Number of electrodes that detected a significant number of ripples


%% Check what electrode corresponds to what
% Load the files necessary for the labeling of the electrodes
filedir_patients = '/media/czacharo/TOSHIBA_EXT/NeuroSyntax2/Data/'  ;   % Linux
files = dir([filedir_patients '*.mat']);
patients = {files.name};
cd(filedir_patients);
load(patients{:,1});                                            % Creates the localization struct
location = localization.notes;
%% Select a number of electrodes and see their location
clc
clear position_interesting
interesting_electrodes = [158:167];
for electrodeInteresting = interesting_electrodes
    position_interesting(electrodeInteresting,:) = location(electrodeInteresting,:);
end
% Gives the labelling of the electrodes that the user would like to investigate

%% See the location of the significant electrodes (electrodes for which events greater than a given threshold e.g 400 were observed)

for electrodeSignificant = significant_electrodes
    position_Significant(electrodeSignificant,:) = location(electrodeSignificant,:);   % Gives the labelling of the electrodes that crossed a certain threshold
end

% Plot the bar with the rest being zeros
mySize_to_plot = Number_of_events;
mySize_to_plot(mySize_to_plot<threshold) = 0;
bar(mySize_to_plot)
xlabel(['Channels'])
ylabel(['Number of Ripples detected'])
xticks([significant_electrodes])
title({'Ripples detected per channel for patient TS096','(Significant Channels)'})
%% Read the excel file that contains the map between the freeSurfer labelling and the standard anatomical nomenclature
cd('/media/czacharo/TOSHIBA_EXT/NeuroSyntax2/Data/TS096')
[~,electrodeMap,~]=xlsread('freeSurfer.xls') ;
anatomical_nomeclature = electrodeMap(:,1);
freesurfer_labels = electrodeMap(:,2);
%% That remains to be fixed
location_of_significant_electrodes = location(significant_electrodes,:);
for strErase = 1:length(location_of_significant_electrodes)
    if contains('ctx_lh_',location_of_significant_electrodes(strErase) ) == 1
        newStr(strErase,:) = erase(location_of_significant_electrodes(strErase,:),"ctx_lh_");
    else
        newStr(strErase,:) =' ';
    end
end

%% Correlate the timing of Ripples with the occurence of events (for the significant electrodes)

% Use information from the behavioral data to correlate with the timing of
% the Ripples 
load('ttl_all.mat')                                                                                  % Loads the information regarding the triggers

% We have 4 different conditions (triggers)--> 7: Fixartion, 8: First word
% onset, 9: Last word onset, 10: First word probe onset

% Extract the indices of the events
event_type_one = find(ttl_all(5,:) == 7);
event_type_two = find(ttl_all(5,:) == 8);
event_type_three = find(ttl_all(5,:) == 9);
event_type_four = find(ttl_all(5,:) == 10);

% Extract the events in Sample Points
fixation = ttl_all(1,event_type_one);
first_word_onset = ttl_all(1,event_type_two);
last_word_onset = ttl_all(1,event_type_three);
first_word_probe_onset = ttl_all(1,event_type_four);


% Store the timing of the ripples for the significant electrodes
for signifI = 1:length(significant_electrodes)
    evtTime_Significant{signifI} = evtTime{significant_electrodes(signifI)};
end

%%
%  clear first_Ripple
% Extract the first occurence of the ripples in all significant channels
clear first_Ripple second_Ripple
for channel =  1:length(significant_electrodes)
    first_Ripple{channel,:} =  evtTime_Significant{channel}(1);
    second_Ripple{channel,:} =  evtTime_Significant{channel}(2);
end
first_Ripple = cell2mat(first_Ripple);
second_Ripple = cell2mat(second_Ripple);

%% 



