function [stimuli_words, WAVstimulus, AudioStimArr] = load_stimuli(params, timestamp, subses)

%%%%%%%%%%%%%%%%%%%%%%%%%
% Load the WAV segments
%---------------------
     

for i=1:params.numWAVs
     wav_filename = fullfile(params.WAVpath, params.WAVnames{i});
     copyfile(wav_filename, fullfile(params.defaultpath, '..', 'Logs', sprintf('%s_%s_%s',params.WAVnames{i},timestamp,subses)))
     temp = audioinfo(wav_filename);
     Fs(i) = temp.SampleRate;
     if Fs(i)~=params.freq
         warning(sprintf('WAV file sample rate not %d Hz', params.freq));
     end
     WAVstimulus{i}(:,:) = audioread(wav_filename);
     stimDur(i)=size(WAVstimulus{i},1);  %in samples
     WAVTTL{i} = ones(1,stimDur(i));

end
     

%Set up non-randomised vector of trials 
AudioStimArr=zeros(params.numTrials+params.numSilents,1);   %leaves numSilents of zeros
for i=1:params.numWAVs
 AudioStimArr((i-1)*params.numPerWAV+1:i*params.numPerWAV)=i;
end

%set up array of start times (with jitter)
% jitterArr=unifrnd(-ones(params.numBlocks * (params.numTrials+params.numSilents),1),ones(params.numBlocks * (params.numTrials+params.numSilents),1)) * ...
%  params.jitter/1000 + params.stimSeparation;   %array of times from end of stim to start of next    


%%%%%%%%%%%%%%%%%%%%%%%%%
% Load the visual stimuli
%---------------------
text_filename = fullfile(params.Visualpath, params.text_filename);
copyfile(text_filename, fullfile(params.defaultpath, '..', 'Logs', sprintf('%s_%s_%s',params.text_filename,timestamp,subses)))
fid_visual_stimuli = fopen(text_filename, 'r'); 
stimuli = textscan(fid_visual_stimuli,'%s','delimiter','\n');
fclose(fid_visual_stimuli);
stimuli_words = cellfun(@(x) strsplit(x, ' '), stimuli{1}, 'UniformOutput',false);

end

