
close all;

for D=[5]
folder = ['../sandbox/D' num2str(D) '/'];
savepath = ['../sandbox/D' num2str(D) '/fixed/'];
strMeanHist=['../statistics/mean_hist_D' num2str(D) '_unnormalized.csv'];
strBSHist=['../statistics/bs_D' num2str(D) '_0.05_unnormalized.csv'];
dngs = dir([folder,'*.dng']);
deps = dir([folder,'*.tif']);
files=length(dngs);
for file = 1:files
    
    strDNG = [folder,dngs(file).name];
    strDepth = [folder,deps(file).name];
    
    blur_red=0; sigma_red=10;
    blur_depth=0; sigma_depth=1;
    withNorm=0; normMeanVal=10.234190813810601;
    
    for option = 4
        if option==1
            attenFixVer=1;
            lambda=ones(1,3)*10; betaBtype='const'; DC=1; WB=0;
            contStr=1; fix_non_depth=1;
        elseif option==2
            attenFixVer=1;
            lambda=ones(1,3)*2; betaBtype='const'; DC=0; WB=3;
            contStr=1; fix_non_depth=1;
        elseif option==3
            attenFixVer=1;
            lambda=ones(1,3)*2; betaBtype='atten'; DC=0; WB=3;
            contStr=0; fix_non_depth=1;
        elseif option==4
            attenFixVer=3;
            lambda=ones(1,3)*2; betaBtype='atten'; DC=0; WB=3;
            contStr=1; fix_non_depth=0;
        end
        
        if file == 1
            isplot=1;
        else
            isplot=0;
        end
        
       % Ifixed = fixProcess(strDNG,strDepth,strMeanHist,strBSHist,withNorm,normMeanVal,attenFixVer,lambda,betaBtype,DC,WB,contStr,fix_non_depth,blur_red,sigma_red,blur_depth,sigma_depth,isplot);
        Ifixed = fixProcess(strDNG,strDepth,strMeanHist,strBSHist,withNorm,normMeanVal,attenFixVer,lambda,betaBtype,DC,WB,contStr,fix_non_depth,blur_red,sigma_red,blur_depth,sigma_depth,isplot);

        f3=figure(3);
        imshow(Ifixed,[]);
        saveas(f3,[savepath,strrep(dngs(file).name,'.dng',['_op' num2str(option) '.png'])]);
            
        if file == 1
            f1=figure(1);
            saveas(f1,[savepath 'fit_op' num2str(option) '.png']);
            f2=figure(2);
            saveas(f2,[savepath 'fix_op' num2str(option) '.png']);
        end
        close all;
        
    end
end
end