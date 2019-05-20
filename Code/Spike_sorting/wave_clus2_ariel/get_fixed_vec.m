function fixed_vec_bool = get_fixed_vec(par, handles)
% get_fixed_vec    

% Author: Ariel Tankus.
% Created: 13.06.2006.


fixed_vec_bool     = zeros(1, par.max_clus);
new_fixed_vec_bool = zeros(1, par.max_clus);
for i=1:par.max_clus
    if (i < 4)
        fixed_vec_bool(i) = get(handles.(['fix', num2str(i), '_button']), ...
                    'value');
    else
        % Get fixed clusters from aux figures
        fixed_vec_bool(i) = par.(['fix', num2str(i)]);
    end
end
