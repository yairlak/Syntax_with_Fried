function PSTH = calc_PSTH(raster, bin_size)
    raster_mean = mean(raster, 1);
    bin = 1;
    for st = 1:bin_size:length(raster_mean)
        ed = (st+bin_size-1);
        if ed >length(raster_mean)
            ed = length(raster_mean);
        end
        PSTH(bin) = sum(raster_mean(st:ed));
        bin = bin + 1;
    end
    PSTH = PSTH*1000/bin_size; % from spike count to Hz
end