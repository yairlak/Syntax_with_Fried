function [evtDetect,pvals]=sigDetectThres(Hresh,DetectMode,thres_method,evtStat)
%SIG_DETECT - detect outliers in a positive signal
%[evtDetect,pvals]=SIG_DETECT(Hresh,DetectMode,thres_method)
%
%  inputs
%
%	Hresh - Non-negative signal (time x experiment x component)
%
%	DetectMode - type of detection algorithm: chi2_1 assumes a chi2 distribution with one degree of freeedom under H0
%
%	thres_method - 'noncor', 'fdr', or a number indicating the square root of a multiple of the
%	mean input signal (corresponding to multiple of the standard deviation if the input signal is squared: if you want to threshold to 3 standard deviations, indicate 3!) 
%
%  outputs
%
%	evtDetect - location of the detection
%
%	pvals - pvalue for each detection
%
%
% Author : Michel Besserve, MPI for Intelligent Systems, MPI for Biological Cybernetics, Tuebingen, GERMANY

if nargin<4
    evtStat=[];
end

switch DetectMode
    case {'madgauss','stdgauss'}
        if all(Hresh>0)
            warning('Method is using gaussian assumptions so does not apply to positive signals, consider changing DetectMode')
        end
    otherwise
        if any(Hresh<0)
            warning('Method applyies to chi squared signals but input has negative values: taking the square of the input')
            Hresh=Hresh.^2;
        end
end
            
switch DetectMode
    %use mean absolute deviation under gaussian assumption to estimate
    %variance
    
    case {'madgauss','stdgauss'}
        if ischar(thres_method)
            error('thres_method should be a positve real number')
        end
       switch DetectMode
           case 'madgauss'
                nStd=1.4826*median(abs(Hresh-repmat(median(Hresh),[size(Hresh,1),1,1])));
                % robust estimate of STD using median absolute deviation (factor uses guaussian assumptions, to be fixed...)
           otherwise
                nStd=std(Hresh);
       end
        evtDetect=abs(Hresh-repmat(median(Hresh),[size(Hresh,1),1,1]))>thres_method*repmat(nStd,[size(Hresh,1),1,1]);
        pvals=~evtDetect;
     %use chi2 with one degrees of freedom to model the squared time series
     %under gaussian assumptions
    case 'chi2_1'
        Ef=chisq_absdep(1);
        nStd=mean(abs(Hresh-repmat(median(Hresh),[size(Hresh,1),1,1])))/Ef;%robust estimate of the scale of the chi2
       
        switch thres_method
                case 'noncor'
                     pvals=1-chi2cdfoct(Hresh./repmat(nStd,[size(Hresh,1),1,1]),1);
                     if ~isempty(evtStat)
                          Hsort=sort(-Hresh);
                         for kcomp=1:size(Hsort,2), Hthres(kcomp)=-Hsort(min(evtStat(kcomp)*10,end),kcomp);end
                         
                         
                        evtDetect=bsxfun(@ge,Hresh,Hthres);
                     else
                        evtDetect=Hresh>(chi2inv(.95,1)*repmat(nStd,[size(Hresh,1),1,1]));
                     end
                case 'fdr'
                    pvals=1-chi2cdfoct(Hresh./repmat(nStd/Ef,[size(Hresh,1),1,1]),1);
                    if ~isempty(evtStat)
                          Hsort=sort(-Hresh);
                         for kcomp=1:size(Hsort,2), Hthres(kcomp)=-Hsort(min(evtStat(kcomp)*10,end),kcomp);end
                         
                         
                        evtDetect=bsxfun(@ge,Hresh,Hthres);
                     else
                    p_thres=FDR_thres(pvals,.05);
                    
                    evtDetect=pvals<p_thres;
                    end
        end
       
    %use chi2 with two degrees of freedom to model a constant spectrum in
    %the most skewed case (a single frequency component)
    case 'chi2'
        Ef=chisq_absdep(2);
        nStd=mean(abs(Hresh-repmat(median(Hresh),[size(Hresh,1),1,1])))/Ef;%robust estimate of the scale of the chi2
        evtDetect=Hresh>(chi2inv(.95,2)*repmat(nStd,[size(Hresh,1),1,1]));
        
    %use chi2 with an estimation of the degrees of freedom for each
    %component
     case 'chi2bis'
       
        nStd=mean(abs(Hresh-repmat(median(Hresh),[size(Hresh,1),1,1])));%robust estimate of the scale of the chi2
        nMed=(median(Hresh));
        for kexp=1:size(nStd,2)
            for kcomp=1:size(nStd,3)
                Kest(kexp,kcomp)=chi2est(nStd(1,kexp,kcomp),nMed(1,kexp,kcomp));
            end
        end
        Kest=mode(Kest,1);
        Ef=chisq_absdep(Kest);
  
        for kcomp=1:length(Kest)
            switch thres_method
                case 'noncor'
                    evtDetect(:,:,kcomp)=Hresh(:,:,kcomp)>(chi2inv(1-pvalDetect,Kest(kcomp))*repmat(nStd(:,:,kcomp)/Ef(kcomp),[size(Hresh,1),1,1]));
                case 'fdr'
                    pvals=1-chi2cdfoct(Hresh(:,:,kcomp)./repmat(nStd(:,:,kcomp)/Ef(kcomp),[size(Hresh,1),1,1]),Kest(kcomp));
                    p_thres=FDR_thres(pvals,.05);
                    evtDetect(:,:,kcomp)=pvals<p_thres;
            end
        end
        
    otherwise
        error('unknown detection method')
end
end
