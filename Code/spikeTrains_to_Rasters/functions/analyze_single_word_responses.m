function single_words = analyze_single_word_responses(rasters, trials_info, settings, num_dim)
          
unit_names = fieldnames(rasters);
num_units = length(unit_names);
for u = 1:num_units
    var_names{u} = unit_names{u}(1:(strfind(unit_names{u}, '_')-1));
end

%% Get lexicon from stimuli
sentences =[];
for cnd = 1:length(settings.conditions)
    sentences = [sentences; trials_info.stimuli{cnd}];
end
words = cellfun(@strsplit, sentences, 'uniformoutput', false);
word_lengths = cellfun(@length, words, 'uniformoutput', false);
lexicon = [];
for w = 1:length(word_lengths)
    lexicon = [lexicon words{w}];
end
% Omit '?'/'!'/'.'
for w = 1:length(lexicon)
    if lexicon{w}(end) == '?' || lexicon{w}(end) == '.' || lexicon{w}(end) == '!'
        lexicon{w} = lexicon{w}(1:end-1);
    end
end
% Make lower case
lexicon = lower(lexicon);
lexicon = union(lexicon, lexicon);

%% Load syntactic features from an Excel file, for each word in the lexicon
[path2paradigm, sentence_filename, ext] = fileparts(settings.feautre_codes_file);
[num, txt, ~] = xlsread(fullfile(path2paradigm, [sentence_filename ' words' ext]));
word_features = num(:, 3:end);
nouns.IX = logical(word_features(:,1));
verbs.IX = logical(word_features(:,2));
function_words.IX = any(word_features(:,3:5), 2);
if length(lexicon) < size(num, 1)
    mat_IX =[];
    for w = 1:length(lexicon)
        mat_IX = [mat_IX, strcmp(lexicon{w}, txt(2:end,1))];
    end
    nouns.IX = nouns.IX(any(mat_IX, 2));
    verbs.IX = verbs.IX(any(mat_IX, 2));
    function_words.IX = function_words.IX(any(mat_IX, 2));
end
%% Calc spike counts from raster files
for unit = 1:num_units
    curr_unit = unit_names{unit};
    for w = 1:length(lexicon)
        curr_word = lexicon(w);
        single_words.(curr_unit).responses.(curr_word{1}) = [];
    end
end

for unit = 1:num_units
    curr_unit = unit_names{unit};
    curr_raster = rasters.(curr_unit).All__trials.matrix;
    for trial = 1:size(curr_raster, 1)
        curr_spike_train = curr_raster(trial, :);
        for w = 1:word_lengths{trial}
            curr_word = lower(words{trial}{w});
            if curr_word(end) == '?' || curr_word(end) == '.' || curr_word(end) == '!'
                curr_word = curr_word(1:end-1);
            end 
            
            
%             window_size = settings.SOA - settings.window_latency -1;
            st = settings.duration_before_stimulus_onset + ...
                 settings.window_latency + ...
                 (w-1)*settings.SOA;
            ed = st + settings.window_size;
            curr_response = curr_spike_train(st:ed);
            single_words.(curr_unit).responses.(curr_word) = [single_words.(curr_unit).responses.(curr_word); ... 
                                                curr_response];
        end
    end
end
%% Calc mean spike counts
for unit = 1:num_units
    curr_unit = unit_names{unit};
    for w = 1:length(lexicon)
        curr_word = lexicon{w};
        single_words.(curr_unit).ave_responses.(curr_word) = ...
            mean(single_words.(curr_unit).responses.(curr_word), 1);
    end
end

design_matrix = [];
for w = 1:length(lexicon)
    curr_word = lexicon{w};
    feature_vector = [];
    for unit = 1:num_units
        curr_unit = unit_names{unit};
        curr_features = sum(single_words.(curr_unit).ave_responses.(curr_word));
        feature_vector = [feature_vector, curr_features];
    end
    design_matrix = [design_matrix; feature_vector];
end

[coeff, score, latent] = pca(design_matrix);
f = figure('color', [1 1 1], 'visible', 'off');
biplot(coeff(:,1:num_dim),'scores',score(:,1:num_dim),'varlabels',var_names, 'obslabels', lexicon);
hold on
max_score = max(max(abs(score)));
if num_dim == 2
    text(score(nouns.IX,1)/max_score, score(nouns.IX,2)/max_score, lexicon(nouns.IX), 'color', 'b')
    text(score(verbs.IX,1)/max_score, score(verbs.IX,2)/max_score, lexicon(verbs.IX), 'color', 'r')
    text(score(function_words.IX,1)/max_score, score(function_words.IX,2)/max_score, lexicon(function_words.IX), 'color', 'g')
elseif num_dim == 3
    text(score(nouns.IX,1)/max_score, score(nouns.IX,2)/max_score, score(nouns.IX,3)/max_score, lexicon(nouns.IX), 'color', 'b')
    text(score(verbs.IX,1)/max_score, score(verbs.IX,2)/max_score, score(verbs.IX,3)/max_score, lexicon(verbs.IX), 'color', 'r')
    text(score(function_words.IX,1)/max_score, score(function_words.IX,2)/max_score, score(function_words.IX,3)/max_score, lexicon(function_words.IX), 'color', 'g')
end

settings_fields = {'patient', 'block_type', 'window_latency', 'window_size'};
params = []; params_fields = [];
file_name = get_file_name_curr_run(settings, params, settings_fields, params_fields);
file_name = ['pca_' file_name];
saveas(f, fullfile('../../Figures/pca', [file_name '.png']), 'png')
saveas(f, fullfile('../../Figures/pca', [file_name '.fig']), 'fig')
close(f)

%% Sumarize the results
for pc = 1:length(coeff)
    nouns.mean(pc) = mean(score(nouns.IX , pc));
    nouns.std(pc) = std(score(nouns.IX , pc));
    verbs.mean(pc) = mean(score(verbs.IX , pc));
    verbs.std(pc) = std(score(verbs.IX , pc));
    function_words.mean(pc) = mean(score(function_words.IX , pc));
    function_words.std(pc) = std(score(function_words.IX , pc));
end

%%
% f_dist = figure('color', [1 1 1]);
% hold on
% hist3([score(nouns.IX, 1) score(nouns.IX, 2)] ,[10 10],'FaceAlpha',.3);
% hist3([score(verbs.IX, 1) score(verbs.IX, 2)] ,[10 10],'FaceAlpha',.3, 'facecolor', 'r');
% hist3([score(function_words.IX, 1) score(function_words.IX, 2)] ,[10 10],'FaceAlpha',.3, 'facecolor', 'g');
% xlabel('Score (PC1)'); ylabel('Score (PC2)');
% set(gcf,'renderer','opengl');

f_dist = figure('color', [1 1 1], 'visible', 'off');
edges = -2:0.2:4;
h1 = histcounts(score(nouns.IX, 1),edges);
h2 = histcounts(score(verbs.IX, 1),edges);
h3 = histcounts(score(function_words.IX, 1),edges);
bar(edges(1:end-1),[h1; h2; h3]', 'barwidth', 1.2)

% hold on
% histogram(score(nouns.IX, 1), 20, 'binwidth', 0.2, 'facecolor', 'b','FaceAlpha',.3);
% histogram(score(verbs.IX, 1), 20, 'binwidth', 0.2, 'facecolor', 'r','FaceAlpha',.3);
% histogram(score(function_words.IX, 1), 20, 'binwidth', 0.2, 'facecolor', 'g','FaceAlpha',.3);
legend({'Nouns', 'Verbs', 'Function words'}, 'location', 'northeast', 'fontsize', 12);
xlabel('Score (PC1)', 'fontsize', 16)

settings_fields = {'patient', 'block_type', 'window_latency', 'window_size'};
params = []; params_fields = [];
file_name = get_file_name_curr_run(settings, params, settings_fields, params_fields);
file_name = ['pc1_dist_' file_name];
saveas(f_dist, fullfile('../../Figures/pca', [file_name '.png']), 'png')
close(f_dist)
    

end