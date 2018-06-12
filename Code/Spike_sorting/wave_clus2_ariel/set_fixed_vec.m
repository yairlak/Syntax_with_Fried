function par = set_fixed_vec(par, handles, fixed_vec_bool)
% set_fixed_vec    
%
%                  See also:  get_fixed_vec, unfix_all, shift_fixed_buttons.

% Author: Ariel Tankus.
% Created: 13.06.2006.


if (length(fixed_vec_bool) < par.max_clus)
    % un-fix remaining (empty) clusters:
    fixed_vec_bool = [fixed_vec_bool, ...
                      zeros(1, par.max_clus - length(fixed_vec_bool))];
end
    
for i=1:par.max_clus
    if (i < 4)
        set(handles.(['fix', num2str(i), '_button']), 'value', ...
                          fixed_vec_bool(i));
    else
        % Get fixed clusters from aux figures
        par.(['fix', num2str(i)]) = fixed_vec_bool(i);
    end
end
