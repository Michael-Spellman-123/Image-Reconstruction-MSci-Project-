# -*- coding: utf-8 -*-


from PIL import Image
import numpy as np
import os
import glob
import graphs
import matplotlib.pyplot as plt
import scipy.optimize as spo



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



def sinfunc(t, A, w, p, c):  
    return A * np.sin(w*t + p) + c


def get_params(projs, n_fringes, guess):
    param_data = []
    for proj in projs:
        
        lhmean = []
        rhmean = []        
        for row in proj[0:1500,0:200]:
            lhmean.append(sum(row))
        for row in proj[0:1500,-200:]:
            rhmean.append(sum(row))            
        x = range(1500)
        g = 0
        temp_data = []
        while g < max(x) - int(max(x)/n_fringes):
            tempx = x[g:int(g+(max(x)/n_fringes))]
            lhparams = spo.curve_fit(sinfunc, tempx, lhmean[g:int(g+(max(x)/n_fringes))], p0=guess)[0]
            lhp = lhparams[2] * lhparams[0] / abs(lhparams[0])
            rhparams = spo.curve_fit(sinfunc, tempx, rhmean[g:int(g+(max(x)/n_fringes))], p0=guess)[0]
            rhp = rhparams[2] * rhparams[0] / abs(rhparams[0])
            temp_data.append([proj[g:int(g+(max(x)/n_fringes)),:],lhp,rhp])
            g = int(g+(max(x)/n_fringes))
        param_data.append(temp_data)
    return param_data    



def batch_best_reference(reference_location, target_image_location, n_fringes=12):

    targets, target_names = open_images(target_image_location)
    refs, ref_names = open_images(reference_location)
    
    guess_freq = n_fringes / 1500
    guess_amp = 50000
    guess_offset = 63000 
    guess = np.array([guess_amp, 2*np.pi*guess_freq, 0., guess_offset])

    refdata = get_params(refs, n_fringes, guess)
    targetdata = get_params(targets, n_fringes, guess)
    hybrid_refs = []
    for n in range(len(targets)):
        print(target_names[n])
        hybrid_ref = np.zeros(np.shape(targets[n]))
        g = 0
        for sect in range(len(targetdata[n])):
            lhp = targetdata[n][sect][1]
            rhp = targetdata[n][sect][2]
            sect_height = int(1500/n_fringes)
            best = 1E99
            for m in range(len(refdata)):
                ref = refdata[m]
                dif = abs(ref[sect][1] - lhp) + abs(ref[sect][2] - rhp) 
                if dif < best:
                    best = dif
                    best_sect = m
                   
            hybrid_ref[g:g + sect_height,:] = refs[best_sect][g:g+sect_height,:]
            g += sect_height
        hybrid_refs.append(hybrid_ref)
    return hybrid_refs


hybr = batch_best_reference(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\6-3-20\1.3mm_refs', r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\6-3-20\1.3mm_targs')

for r in hybr:
    graphs.colourmap(r)









