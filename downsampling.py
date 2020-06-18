from scipy.signal import decimate
from PIL import Image 
import graphs
import numpy as np
import os
import glob



def downsample(directory, factor):
    """
    Creates folder of downsampled images.
    
    directory(string) =  location of folder containing the .tif files     
    """
    os.makedirs(directory + '\\' + 'downsampled_files')
    
    images, names = ([np.array(Image.open(f), dtype = np.int32) for f in 
            glob.glob(directory + '*' + '/*.tif')], 
            [n.replace(directory, "") for n in 
             glob.glob(directory + '*' + '/*.tif')])
    
    c = 0
    for f in images:
        Image.fromarray(decimate(decimate(f, factor, axis=0),
                                 factor, axis=1)).save(directory + '\\' + 
                                               'downsampled_files' + names[c])
        c += 1

    

#downsample(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\6-3-20\1.3mm_targs', 8)
#if __name__ == "__main__":
#    downsample(r'C:\Users\Elliot Prestidge\Documents\MATLAB\000045', 8)

#downsample(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\11-3-20\11-3-20-REF_files',8)
#r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\11-3-20\180_2ndhalf
#downsample(c',8)