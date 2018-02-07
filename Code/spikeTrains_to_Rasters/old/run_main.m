clear all; close all; clc

%% Define comparisons of interest:
% zSXXX ZSXXX phrase type
comparisons{1} = {[5,6], [4,6]};
comparison_name{1} = 'Phrase type';
condition_labels{1} = {'zSXXX','ZSXXX'};
 
% zSXXX GSNXX  phrase vs sentence
comparisons{2} = {[5,6], [3,6,8]};
comparison_name{2} = 'Phrase vs sentence';
condition_labels{2} = {'zSXXX', 'GSNXX'};

% GSNXX DSNEX nominal vs verbal sentence
comparisons{3} = {[3,6,8], [1,6,8,13]};
comparison_name{3} = 'Nominal vs verbal sentence';
condition_labels{3} = {'GSNXX', 'DSNEX'};

% DSHEX DSHAX argument structure unacc vs unerg
comparisons{4} = {[1,6,11,13], [1,6,11,12]};
comparison_name{4} = 'Argument structure unacc vs unerg';
condition_labels{4} = {'DSHEX', 'DSHAX'};

% DSHTK DSHCK argument structure transitive vs causative
comparisons{5} = {[1,6,11,15,17], [1,6,11,14,17]};
comparison_name{5} = 'Argument structure transitive vs causative';
condition_labels{5} = {'DSHTK', 'DSHCK'};

% DSHEX WSXEX declarative vs question
comparisons{6} = {[1,6,11,13], [2, 6, 13]};
comparison_name{6} = 'Declarative vs question';
condition_labels{6} = {'DSHEX', 'WSXEX'};

% DSNEX DVNEX SV vs VS
comparisons{7} = {[1,6,8,13], [1,7,8,13]};
comparison_name{7} = 'SV vs VS';
condition_labels{7} = {'DSNEX', 'DVNEX'};
 
% WSRTX WSXEX subject vs object question
comparisons{8} = {[2,6,10,15], [2,6,13]};
comparison_name{8} = 'Subject vs object question';
condition_labels{8} = {'WSRTX', 'WSXEX'};
 
% DVNEX DSXAM VS with and without movement
comparisons{9} = {[1,7,8,13], [1,6,12,19]};
comparison_name{9} = 'VS with and without movement';
condition_labels{9} = {'DVNEX', 'DSXAM'};
 
% DSNEX DSPEX+DSHEX pronoun vs full NP subject: unerg
comparisons{10} = {[1,6,8,13], [1,6,13,22]};
comparison_name{10} = 'Pronoun vs full NP subject_ unerg';
condition_labels{10} = {'DSNEX', 'DSPEX__and__DSHEX'};
 
% DSNAM DSPAM+DSHAM pronoun vs full NP subject: unacc
comparisons{11} = {[1,6,8,12,19], [1,6,12,19,22]};
comparison_name{11} = 'Pronoun vs full NP subject_ unacc';
condition_labels{11} = {'DSNAM', 'DSPAM__and__DSHAM'};

% DSNTK DSHTK+DSPTK pronoun vs full NP subject: transitive
comparisons{12} = {[1,6,8,15,17], [1,6,15,17,22]};
comparison_name{12} = 'Pronoun vs full NP subject_ transitive';
condition_labels{12} = {'DSNTK', 'DSHTK__and__DSPTK'};

% first/second half
comparisons{13} = {20, 21};
comparison_name{13} = 'First and second half';
condition_labels{13} = {'First','second'};

%% HTML
file_name = sprintf('main_rasters_syntax_single_unit');

% open file
fid = fopen(fullfile('..', '..', [file_name '.html']), 'w');

% Begining of file
fprintf(fid, '<html>\n');
fprintf(fid, '<head>\n');
fprintf(fid, '<title>Raster plots</title>\n');
fprintf(fid, '</head>\n');
fprintf(fid, '<body>\n');


%% Generate raster for all condition comparisons
if length(comparisons) ~= length(condition_labels) ||  length(comparisons) ~= length(comparison_name) 
    error('not the same number of condition labels');
else 
    
    for compar = 1:length(comparisons)
        fprintf('%i. %s\n', compar, comparison_name{compar});
        settings = [];
        settings.conditions = comparisons{compar};
        settings.comparison_name = comparison_name{compar};
        settings.conditions_labels = condition_labels{compar};
        % Generate rasters
        main_spike_trains_to_rasters
        % generate HTML
        fprintf(fid, '<a href="%s.html" title="%s">%s</a>', comparison_name{compar}, comparison_name{compar}, comparison_name{compar});
        fprintf(fid, '<br>\n');
        generate_HTML_comparison(figure_names, comparison_name{compar}, settings)
        
    end
end 

fclose(fid);