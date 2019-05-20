clear all; close all; clc

%% Load code data
xls_file = fullfile('..','Paradigm', 'words and sentences naama for analysis 220117.xlsx');
[num, txt, ~] = xlsread(xls_file, 'block2 2word sentences ordered');
IX_in_exp = num(:,1);
codes = txt(2:181,4);
items = txt(2:181,2);

%%
cat_values{1} = {'D', 'W', 'G', 'Z', 'z'};
cat_values{2} = {'S', 'V'};
cat_values{3} = {'N', 'P', 'R', 'H'}; % X
cat_values{4} = {'A','E','C','T', 't'}; %X
cat_values{5} = {'K', 'O', 'M'}; %X

labels = [];
cnt = 1;
for cat = 1:5
    curr_values = cat_values{cat};
    last_cnt = cnt;
    for val  = 1:length(curr_values)
        IX_val = [];
        curr_val = curr_values{val};
        labels{cnt} = curr_val;
        IX_val = cellfun(@(x) x(cat)==curr_val, codes);
        values_mat(:, cnt) = double(IX_val);
        cnt = cnt + 1;
    end
    % Change to '-1' all features with 'X' in their category code
    IX_val = [];
    curr_val = 'X';
    IX_val = cellfun(@(x) x(cat)==curr_val, codes);
    values_mat(IX_val, last_cnt:cnt-1) = -1;    
end

file_name = fullfile('..','Paradigm', 'CODES sentences 220117.xlsx');
xlswrite(file_name, double(values_mat), 1, 'D2');
xlswrite(file_name, IX_in_exp, 1, 'A2');
xlswrite(file_name, items, 1, 'B2');
xlswrite(file_name, codes, 1, 'C2');
xlswrite(file_name, labels, 1, 'D1');