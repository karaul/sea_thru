import cv2
import numpy as np
from matplotlib import pyplot as plt
from os import listdir
import glob

def rgb_histogram(img):
    color = ('r','g','b')
    for i,col in enumerate(color):
        plt.hist(img[:,:,i],bins=256,range=[0,256])
    plt.show()

def generate_depth_quantized_histograms():
    raw_folder = 'D:/sea_thru/3148_3248/Raw/tifs/'
    depth_folder = 'D:/sea_thru/3148_3248/depthMaps/'
    histograms = 'D:/sea_thru/3148_3248/histograms/'
    drange = np.arange(0.5,1.76,0.01)
    N = drange.shape[0]-1

    for raw_file in listdir(raw_folder):
        depth_file = 'depth' + raw_file
        depth_hist = np.empty(shape=[256,3,N])
        bgr_img = cv2.imread(raw_folder+raw_file)
        b,g,r = cv2.split(bgr_img)
        depth = cv2.imread(depth_folder+depth_file,-1)
        d = cv2.resize(depth,(8000,5320))

        for i in range (N):
                norm = np.sum((d>drange[i]) & (d<drange[i+1]))
                if norm > 0 :
                    depth_hist[:,0,i] , bins =  np.histogram(r[(d>drange[i]) & (d<drange[i+1])],bins=256,range=[0,256])
                    depth_hist[:,1,i] , _ =  np.histogram(g[(d>drange[i]) & (d<drange[i+1])],bins=256,range=[0,256])
                    depth_hist[:,2,i] , _ =  np.histogram(b[(d>drange[i]) & (d<drange[i+1])],bins=256,range=[0,256])
                    depth_hist[:,:,i] /=norm
        np.save(histograms + raw_file.replace('tif','npy'),depth_hist)
    np.save('bins',bins)

def generate_depth_histogram(depthMaps_path):
    
    depth_hist = np.empty(shape=[200])
    for depth_file in listdir(depthMaps_path):    
        depth = cv2.imread(depthMaps_path+depth_file,-1)
        temp_hist , _ = np.histogram(depth.reshape([-1,1]),bins=200,range=(0,2))
        depth_hist += temp_hist
    
    return(depth_hist)
    
def plot_depth_quantized_histograms(histogram,bins,depth_bins):    
    for i in range(depth_bins.shape[0]-1):
        plt.figure()
        plt.hist(bins[:-1], bins, weights=histogram[:,0,i])
        # plt.ylim([0,3])
        plt.xlabel('Red channel values')
        plt.ylabel('Relative quantitiy')
        plt.title("from {0:.2f}m to {1:.2f}m | bincnt = {2:d}".format(depth_bins[i],depth_bins[i+1],int(np.sum(histogram[:,0,i]))))
        # plt.title('depth range ' + str(depth_bins[i]) + 'm to ' + str(depth_bins[i+1]) + 'm' 
        #  + '\nbinsum =' + str(np.sum(histogram[:,2,i])))
        plt.savefig('C:/Users/amirsaa/Documents/sea_thru_data/output/accumulated_depth_hist_' + str(i) + '.png')
        plt.close()

def accumulate_histograms(histograms_path,save=False):
    for i,file in enumerate(glob.glob(histograms_path)):
        hist = np.load(file)
        if i==0:
            summed_histogram = hist
        else:
            summed_histogram += hist
    
    if save:
        np.save('acc_hist.npy',summed_histogram/i)
    
    return(summed_histogram)

def depth_envelopes(histogram):
    histogram
    lower = np.percentile(histogram,5,axis=0)
    mid   = np.percentile(histogram,50,axis=0)
    upper = np.percentile(histogram,95,axis=0)
    return (lower,mid,upper)

    