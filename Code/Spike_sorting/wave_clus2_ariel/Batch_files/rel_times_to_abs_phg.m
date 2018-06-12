function [] = rel_times_to_abs_phg()
% rel_times_to_abs_phg    

% Author: Ariel Tankus.
% Created: 14.09.2009.


name_suffix = '../'; 
req_type    = 1;
ch_list     = 1:64;
last_dir    = 20;

[dir_list, id_list] = create_phg_dir_list(name_suffix);
[dir_list, id_list] = req_session_type(dir_list, id_list, req_type);

batch_eval_multidir(dir_list(13:last_dir), @rel_times_to_abs, ch_list);
