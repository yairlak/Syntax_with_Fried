function end_of_sentence = analyze_end_of_sentence_response(rasters, trials_info, settings, num_dim)
num_bins = 1;
latency = 0;
window_size = 500;

%%
unit_names = fieldnames(rasters);
num_units = length(unit_names);
cnt = 1;
for u = 1:num_units
    for bin = 1:num_bins
        var_names{cnt} = [unit_names{u}(1:(strfind(unit_names{u}, '_')-1)), '__bin' num2str(bin)];
        cnt = cnt + 1;
    end
end

%% Get sentences from stimuli
sentences =[];
for cnd = 1:length(settings.conditions)
    sentences = [sentences; trials_info.stimuli{cnd}];
end
words = cellfun(@strsplit, sentences, 'uniformoutput', false);
num_words = cellfun(@length, words, 'uniformoutput', false);

%%
for unit = 1:num_units
    curr_unit = unit_names{unit};
    for s = 1:length(sentences)
        curr_sentence = strrep(sentences{s}, ' ', '_');
        curr_sentence = strrep(curr_sentence, '?', '');
        curr_sentence = strrep(curr_sentence, '!', '');
        curr_sentence = strrep(curr_sentence, '.', '');
        end_of_sentence.(curr_unit).responses.(curr_sentence) = [];
    end
end

for unit = 1:num_units
    curr_unit = unit_names{unit};
    curr_raster = rasters.(curr_unit).All__trials.matrix;
    for trial = 1:size(curr_raster, 1)
        curr_spike_train = curr_raster(trial, :);
        curr_sentence = strrep(sentences{trial}, ' ', '_');
        curr_sentence = strrep(curr_sentence, '?', '');
        curr_sentence = strrep(curr_sentence, '!', '');
        curr_sentence = strrep(curr_sentence, '.', '');
        
%         st = latency + settings.duration_before_stimulus_onset + ...
%                             (num_words{trial}-1)*settings.SOA;
        st = latency + settings.duration_before_stimulus_onset;
        ed = st + window_size;
        curr_response = curr_spike_train(st:ed);
        end_of_sentence.(curr_unit).responses.(curr_sentence) = ...
            [end_of_sentence.(curr_unit).responses.(curr_sentence); ... 
                                                curr_response];
        
    end
end
%%
for unit = 1:num_units
    curr_unit = unit_names{unit};
    for s = 1:length(sentences)
        curr_sentence = strrep(sentences{s}, ' ', '_');
        curr_sentence = strrep(curr_sentence, '?', '');
        curr_sentence = strrep(curr_sentence, '!', '');
        curr_sentence = strrep(curr_sentence, '.', '');
        end_of_sentence.(curr_unit).ave_responses.(curr_sentence) = ...
            mean(end_of_sentence.(curr_unit).responses.(curr_sentence), 1);
    end
end

design_matrix = [];
for s = 1:length(sentences)
    curr_sentence = strrep(sentences{s}, ' ', '_');
    curr_sentence = strrep(curr_sentence, '?', '');
    curr_sentence = strrep(curr_sentence, '!', '');
    curr_sentence = strrep(curr_sentence, '.', '');
    feature_vector = [];
    for unit = 1:num_units
        curr_unit = unit_names{unit};
        bin_size = floor(length(end_of_sentence.(curr_unit).ave_responses.(curr_sentence))/num_bins);
        curr_features = [];
        for bin = 1:num_bins
            st = 1+(bin-1)*bin_size;
            ed = bin * bin_size;
            curr_features = [curr_features, sum(end_of_sentence.(curr_unit).ave_responses.(curr_sentence)(st:ed))];
        end
%         curr_features = sum(end_of_sentence.(curr_unit).ave_responses.(curr_sentence));
        feature_vector = [feature_vector, curr_features];
    end
    design_matrix = [design_matrix; feature_vector];
end
[coeff, score, latent] = pca(design_matrix);
f = figure('color', [1 1 1], 'visible', 'off', 'Units', 'Normalized', 'position', [0 0 1 1]);
biplot(coeff(:,1:num_dim),'scores',score(:,1:num_dim),'varlabels',var_names, 'obslabels', sentences);
hold on
% Add labels
[p,d] = size(coeff);
n = size(score,1);
[~,maxind] = max(abs(coeff),[],1);
colsign = sign(coeff(maxind + (0:p:(d-1)*p)));
score = (score ./ max(abs(score(:)))) .* repmat(colsign, n, 1)/1;

% This code plots the labels, just slightly away from the points themselves.
delx = .01*diff(get(gca,'XLim'));
dely = .01*diff(get(gca,'YLim'));
delz = .01*diff(get(gca,'ZLim'));
% delx = 0;
% dely = 0;
% delz = 0;
text(score(:,1)+delx,score(:,2)+dely,score(:,3)+delz,sentences, 'color', 'r');

% max_score = max(max(abs(score)));
% % max_coeff = max(norm(coeff(:,1)));
% if num_dim == 2
%     text(score(:,1)/max_score, score(:,2)/max_score, sentences, 'color', 'r')
% elseif num_dim == 3
%     text(score(:,1)/max_score, score(:,2)/max_score, score(:,3)/max_score, sentences, 'color', 'r')
% end

settings_fields = {'patient', 'comparison_name', 'blocks_str'};
params = []; params_fields = [];
file_name = get_file_name_curr_run(settings, params, settings_fields, params_fields);
file_name = ['pca_sentences_' file_name '.png'];
saveas(f, fullfile('..', '..', 'Figures', 'PCA', file_name), 'png')
close(f)
end
