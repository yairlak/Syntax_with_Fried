function [] = rel_times_to_abs_verify_phg()
% rel_times_to_abs_verify_phg    

% Author: Ariel Tankus.
% Created: 15.09.2009.


name_suffix = '../'; 
req_type    = 1;
ch_list     = 1:64;
last_dir    = 20;

[dir_list, id_list] = create_phg_dir_list(name_suffix);
[dir_list, id_list] = req_session_type(dir_list, id_list, req_type);

batch_eval_multidir(dir_list(1:last_dir), @rel_times_to_abs_verify, ch_list);
