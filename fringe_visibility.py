# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:04:10 2020

@author: MS XPS
"""

from PIL import Image
import numpy as np
import os
import glob
import matplotlib.pyplot as plt

directory = (r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\17-2-20_argon\17-2-20-100bar-narrow-1st-shot')


def open_images(directory):
    """
    Returns a list of np.arrays of all the .tif files in the specified directory
    and a list of the file names
    
    directory(string) =  location of folder containing references & target image 
    
    For example:
    images, names = open_images(directory)
    
    """
    return ([np.array(Image.open(f), dtype = np.int32) for f in 
            glob.glob(directory + '*' + '/*.tif')], 
            [n.replace(directory, "") for n in 
             glob.glob(directory + '*' + '/*.tif')])




max_amp = [] 
def fringe_vis(directory):
    """
    directory(string) =  location of folder containing references & target image
    
    target_image(string) = name of .tif file of the target image
    """    
    images, names = open_images(directory)    
    for image in images:
        max_amp.append(np.mean([max(np.abs(np.fft.fft(np.sum(image[:,:200],1)))[1:]),
                    max(np.abs(np.fft.fft(np.sum(image[:,-200:],1)))[1:])]))        
    return max_amp


images, names = open_images(directory)
new_images = []
def delete_fuzzy_images(directory):
        #images, names = open_images(directory)
        c=0 
        for image in images:
            #print(max_amp[c])

            if max_amp[c] > 0.5*np.max(max_amp):
                new_images.append(image)
            c += 1
        return new_images

#amps = fringe_vis(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\Data_17_2\17-2-20-100bar-narrow')
amps = fringe_vis(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\17-2-20_argon\17-2-20-100bar-narrow-1st-shot')
delete_fuzzy_images(directory)
plt.figure()
plt.plot(amps)
plt.xlabel('Frame')
plt.ylabel('Maximum amplitude in spectrum')
plt.grid()

    
#batch_best_reference(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\Data_17_2\References-narrow_half',r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\Data_17_2\Targets-narrow')






#"""
#folder = "29-1-20"
#directory = os.getcwd() + "\\" + folder
## or can set directory outside of spyder project:
#directory = r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\Data_17_2\003662'
#
##images, names = open_images(directory)
#
#best = best_reference(directory, "003662.tif")
#print(best)
#"""
    












