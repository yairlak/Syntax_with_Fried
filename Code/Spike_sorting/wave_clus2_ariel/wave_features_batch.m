function inspk = wave_features_batch(spikes, par);
%Calculates the spike features

% Author: Ariel Tankus.
% Created: 25.10.2009.


scales  = par.scales;
feature = par.features;
inputs  = par.inputs;
nspk    = size(spikes, 1);
ls      = size(spikes, 2);

% CALCULATES FEATURES
switch feature
    case 'wav'
        cc=zeros(nspk,ls);
        for i=1:nspk                                % Wavelet decomposition
            [c,l]=wavedec(spikes(i,:),scales,'haar');
            cc(i,1:ls)=c(1:ls);
        end
        for i=1:ls                                  % KS test for coefficient selection   
            thr_dist = std(cc(:,i)) * 3;
            thr_dist_min = mean(cc(:,i)) - thr_dist;
            thr_dist_max = mean(cc(:,i)) + thr_dist;
            aux = cc(find(cc(:,i)>thr_dist_min & cc(:,i)<thr_dist_max),i);
            if aux < 10;
                [hh,pp,lstat,cv]=lillietest(aux);
                sd(i)=lstat;
            else
                sd(i)=0;
            end
        end
        [max ind]=sort(sd);
        coeff(1:inputs)=ind(ls:-1:ls-inputs+1);
    case 'pca'
        [C,S,L] = princomp(spikes);
        cc = S;
        inputs = 3; 
        coeff(1:3)=[1 2 3];
end

%CREATES INPUT MATRIX FOR SPC
inspk=zeros(nspk,inputs);
for i=1:nspk
    for j=1:inputs
        inspk(i,j)=cc(i,coeff(j));
    end
end
% for j=1:inputs
%     inspk(:,j)=inspk(:,j)/std(inspk(:,j));
% end
