function file_name = get_file_name_curr_run(settings, params, settings_fields, params_fields)

for f = settings_fields
    field_value = num2str(settings.(f{1}));
    field_value = strrep(field_value, '[', '_');
    field_value = strrep(field_value, ']', '_');
    field_value = strrep(field_value, ':', '_');
    field_value = strrep(field_value, ',', '_');
    filename_struct.(f{1}) = field_value;
end
for f = params_fields
    field_value = num2str(params.(f{1}));
    field_value = strrep(field_value, '[', '_');
    field_value = strrep(field_value, ']', '_');
    field_value = strrep(field_value, ':', '_');
    field_value = strrep(field_value, ',', '_');
    filename_struct.(f{1}) = field_value;
end

%%
file_name = buildStringFromStruct(filename_struct, '_');

end