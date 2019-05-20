function [stimuli_words, stimuli_wavs] = load_stimuli(params)

%%%%%%%%%%%%%%%%%%%%%%%%%
% Load the WAV segments
%---------------------

timestamp=gettimestamp();
subses=['S' num2str(params.subject) '_' num2str(params.session)];

for i=1:params.numTrialsAudioBlock
     wav_filename = fullfile(params.WAVpath, params.WAVnames{i});
%      copyfile(wav_filename, fullfile(params.defaultpath, '..', 'Logs', sprintf('%s_%s_%s',params.WAVnames{i},timestamp,subses)))
     temp = audioinfo(wav_filename);
     Fs(i) = temp.SampleRate;
     if Fs(i)~=params.freq
         warning(sprintf('WAV file sample rate not %d Hz', params.freq));
     end
     stimuli_wavs{i}(:,:) = audioread(wav_filename);
end
     

%%%%%%%%%%%%%%%%%%%%%%%%%
% Load the visual stimuli
%---------------------
text_filename = fullfile(params.Visualpath, params.text_filename);
fid_visual_stimuli = fopen(text_filename, 'r'); 
stimuli = textscan(fid_visual_stimuli,'%s','delimiter','\n');
fclose(fid_visual_stimuli);
stimuli_words = cellfun(@(x) regexp(x, ' ', 'split'), stimuli{1}, 'UniformOutput',false); % Cell of cells: cell for each sentence, containing cells for each word

end

