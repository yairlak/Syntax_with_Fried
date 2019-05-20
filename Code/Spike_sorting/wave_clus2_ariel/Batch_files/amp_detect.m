function [spikes,thr,index] = amp_detect(x,par, ts_ind, save_filt_data, channel);
% Detect spikes with amplitude thresholding. Uses median estimation.
% Detection is done with filters set by fmin_detect and fmax_detect. Spikes
% are stored for sorting using fmin_sort and fmax_sort. This trick can
% eliminate noise in the detection but keeps the spikes shapes for sorting.

% Modified: 23.07.2009 (Ariel, Roy & Omri).  Order of ellip filter
%                      changed from 2 to 4.

sr=par.sr(ts_ind);
w_pre=par.w_pre(ts_ind);
w_post=par.w_post(ts_ind);
ref=par.ref(ts_ind);
detect = par.detection;
stdmin = par.stdmin;
stdmax = par.stdmax;
fmin_detect = par.detect_fmin;
fmax_detect = par.detect_fmax;
fmin_sort = par.sort_fmin;
fmax_sort = par.sort_fmax;

% HIGH-PASS FILTER OF THE DATA
if exist('ellip')                         %Checks for the signal processing toolbox
    xf=zeros(length(double(x)),1);
    [b,a]=ellip(2,0.1,40,[fmin_detect fmax_detect]*2/sr);
    %[b,a]=butter(2,[fmin_detect fmax_detect]*2/sr);
    xf_detect=filtfilt(b,a,double(x));
    [b,a]=ellip(2,0.1,40,[fmin_sort fmax_sort]*2/sr);
    %[b,a]=butter(2,[fmin_sort fmax_sort]*2/sr);
    xf=filtfilt(b,a,double(x));
else
    xf=fix_filter(double(x));                   %Does a bandpass filtering between [300 3000] without the toolbox.
    xf_detect = xf;
end
lx=length(xf);
%keyboard
clear x;

noise_std_detect = quickselect_median(abs(xf_detect))/0.6745;
noise_std_sorted = quickselect_median(abs(xf))/0.6745;

thr = stdmin * noise_std_detect;        %thr for detection is based on detect settings.
thrmax = stdmax * noise_std_sorted;     %thrmax for artifact removal is based on sorted settings.

if (save_filt_data)
    filt_fname = sprintf('CSC%d_filt', channel);
    save(filt_fname, 'xf', 'a', 'b', 'fmin_sort', 'fmax_sort', 'xf_detect', ...
         'fmin_detect', 'fmax_detect', 'lx', 'noise_std_detect', ...
         'noise_std_sorted', 'thr', 'thrmax');
end

index = [];

% LOCATE SPIKE TIMES
switch detect
 case 'pos'
  xaux = find(xf_detect(w_pre+2:end-w_post-2) > thr) +w_pre+1;
  if (~enforce_ref_period)
      [index, nspk] = find_spike_max(xf, xaux);
  else
      nspk = 0;
      xaux0 = 0;
      for i=1:length(xaux)
          if xaux(i) >= xaux0 + ref
              [maxi iaux]=max((xf(xaux(i):xaux(i)+floor(ref/2)-1)));    %introduces alignment
              nspk = nspk + 1;
              index(nspk) = iaux + xaux(i) -1;
              xaux0 = index(nspk);
          end
      end
  end
 case 'neg'
  xaux = find(xf_detect(w_pre+2:end-w_post-2) < -thr) +w_pre+1;
  if (~enforce_ref_period)
      [index, nspk] = find_spike_max(-xf, xaux);
  else
      nspk = 0;
      xaux0 = 0;
      for i=1:length(xaux)
          if xaux(i) >= xaux0 + ref
              [maxi iaux]=min((xf(xaux(i):xaux(i)+floor(ref/2)-1)));    %introduces alignment
              nspk = nspk + 1;
              index(nspk) = iaux + xaux(i) -1;
              xaux0 = index(nspk);
          end
      end
  end
  
 case 'both'
  if (~enforce_ref_period)
        xaux = find(xf_detect(w_pre+2:end-w_post-2) > thr) +w_pre+1;
        [index1, nspk1] = find_spike_max(xf, xaux);
        xaux = find(xf_detect(w_pre+2:end-w_post-2) < -thr) +w_pre+1;
        [index2, nspk2] = find_spike_max(-xf, xaux);
        nspk = nspk1 + nspk2;
        index = [index1, index2];
  else
        nspk = 0;
        xaux = find(abs(xf_detect(w_pre+2:end-w_post-2)) > thr) +w_pre+1;
        xaux0 = 0;
        for i=1:length(xaux)
            if xaux(i) >= xaux0 + ref
                [maxi iaux]=max(abs(xf(xaux(i):xaux(i)+floor(ref/2)-1)));    %introduces alignment
                nspk = nspk + 1;
                index(nspk) = iaux + xaux(i) -1;
                xaux0 = index(nspk);
            end
        end
  end
end
index = unique(index);      % will also sort the indices.
nspk = length(index);

% SPIKE STORING (with or without interpolation)
ls=w_pre+w_post;
spikes=zeros(nspk,ls+4); 
xf=[xf zeros(1,w_post)];
for i=1:nspk                          %Eliminates artifacts
    if max(abs( xf((index(i)-w_pre):(index(i)+w_post+2)) )) < thrmax               
        spikes(i,:)=xf((index(i)-w_pre-1):(index(i)+w_post+2));
    end
end
aux = find(spikes(:,w_pre)==0);       %erases indexes that were artifacts
spikes(aux,:)=[];
index(aux)=[];
        
switch par.interpolation
    case 'n'
        spikes(:,end-1:end)=[];       %eliminates borders that were introduced for interpolation 
        spikes(:,1:2)=[];
    case 'y'
        %Does interpolation
        spikes = int_spikes(spikes,par,ts_ind);
end
