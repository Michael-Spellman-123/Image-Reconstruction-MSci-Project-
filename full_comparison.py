# -*- coding: utf-8 -*-
"""
Aim to compare SIRT and FBP over a range of angles both with and without noise.

Offset90_v2 seems to give best results even though the theory seems wrong.
"""

import astra1
import phantoms
import graphs
import numpy as np
import offset90
import offset90_v2
import offset90_v3
import matplotlib.pyplot as plt

def error(p, r):
    # Finds the error relative to the value of the phantom in that same cell...
    # ... rather than relative to the mean of the phantom as done before....
    # ... Returns the mean of these errors.
    #
    # p is the phantom
    # r is the reconstruction
    
    # flatten the arrays, ie. make them lists
    p = np.ravel(p)
    r = np.ravel(r)

    # find difference and only keep values where phantom greater than 0.1
    diff = abs(p - r)
    for i in range(len(p)-1, -1, -1):
        if p[i] < 0.1:
            diff = np.delete(diff, i)
            p = np.delete(p, i)
            
    # calculate relative error as a percentage (relative to phantom)
    rel_err = diff / p * 100
    return np.mean(rel_err) # return the mean so that it can be plotted




# create the original phantom
phant = phantoms.offset_jet(48, 55)
phant_centr = phantoms.offset_jet(0, 55)

# the range of number of projections to reconstruct for:
n_projections = [int(a) for a in np.linspace(3,90,9)]
n_iterations = 40


# all six types to plot
fbp_noise_err = []
sirt_noise_err = []
fbp_clean_err = []
sirt_clean_err = []
fbp_90_err = []
sirt_90_err = []
fbp_90_noise_err = []
sirt_90_noise_err = []

for n in n_projections:
    print(n,'projections')

    # find the different reconstructions of the phantom 
    
    print('Noise')
    sino_noise = astra1.sinogram(phant, np.pi, n, gaussian_noise=True)
    fbp_noise = astra1.reconstruct(sino_noise, 'FBP', n_iterations)
    sirt_noise = astra1.reconstruct(sino_noise, 'SIRT', n_iterations)
    
    print('Clean')
    sino_clean = astra1.sinogram(phant, np.pi, n)
    fbp_clean = astra1.reconstruct(sino_clean, 'FBP', n_iterations)
    sirt_clean = astra1.reconstruct(sino_clean, 'SIRT', n_iterations)
    
    print('90 Clean')
    sino_90 = astra1.sinogram(phant, np.pi/2, n)
    sino_90 = offset90_v2.centre_sino(sino_90)
    #graphs.colourmap(sino_90)
    sino_90 = offset90_v2.mirror_sinogram(sino_90)
    fbp_90 = astra1.reconstruct(sino_90, 'FBP', n_iterations, np.pi)
    sirt_90 = astra1.reconstruct(sino_90, 'SIRT', n_iterations, np.pi)

#    graphs.colourmap(fbp_90)
#    plt.title('fbp90 clean')
#    
#    graphs.colourmap(phant_centr-fbp_90)
#    plt.title('90deg fbp clean diff')
#    
#    graphs.colourmap(fbp_clean)
#    plt.title('fbp clean')
#    
#    graphs.colourmap(phant - fbp_clean)
#    plt.title('fbp clean diff')
    
    print('90 Noise')
    sino_90_noise = astra1.sinogram(phant, np.pi/2, n, gaussian_noise=True)
    sino_90_noise = offset90_v2.centre_sino(sino_90_noise)
    sino_90_noise = offset90_v2.mirror_sinogram(sino_90_noise)
    fbp_90_noise = astra1.reconstruct(sino_90_noise, 'FBP', n_iterations,
                                      np.pi)
    sirt_90_noise = astra1.reconstruct(sino_90_noise, 'SIRT', n_iterations,
                                       np.pi)


    # calculate the errors compared to the original phantom and append for plot
    print('Errors')
    fbp_noise_err.append(error(phant,fbp_noise))
    sirt_noise_err.append(error(phant,sirt_noise))
    fbp_clean_err.append(error(phant,fbp_clean))
    sirt_clean_err.append(error(phant,sirt_clean))
    fbp_90_err.append(error(phant_centr,fbp_90))
    sirt_90_err.append(error(phant_centr,sirt_90))
    fbp_90_noise_err.append(error(phant_centr,fbp_90_noise))
    sirt_90_noise_err.append(error(phant_centr,sirt_90_noise))
    print(' ')

plt.figure(1)
plt.plot(n_projections, fbp_noise_err, label='FBP over 180°')
plt.plot(n_projections, sirt_noise_err, label='SIRT over 180°')
plt.plot(n_projections, fbp_90_noise_err, label='FBP over 90°')
plt.plot(n_projections, sirt_90_noise_err, label='SIRT over 90°')
plt.legend()
plt.ylabel('Percentage error relative to original phantom')
plt.xlabel('Number of projections used')

plt.figure(2)
plt.plot(n_projections, fbp_clean_err, label='FBP over 180°')
plt.plot(n_projections, sirt_clean_err, label='SIRT over 180°')
plt.plot(n_projections, fbp_90_err, label='FBP over 90°')
plt.plot(n_projections, sirt_90_err, label='SIRT over 90°')
plt.legend()
plt.ylabel('Percentage error relative to original phantom')
plt.xlabel('Number of projections used')