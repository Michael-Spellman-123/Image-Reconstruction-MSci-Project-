# -*- coding: utf-8 -*-
"""
Comparing error for different types of noise and different number of iterations
"""

import astra1
import phantoms
import real_units
import imageio
import matplotlib.pyplot as plt
import numpy as np
import pylab
#create phantom
jet = phantoms.shockjet(129,800,4,2000,6)

#create phantom with correct units

jet_correct_units = real_units.num_density(jet)
# above is unused further out as messes with reconstruction scaling issues - FIXED
#above is unused further as messes with addition of noise


# reconstruct for different amount of angles and plot the average discrepancy..
# .. from the phantom jet
ang_discrepancy_no_noise = []
ang_discrepancy_poisson_noise = []
ang_discrepancy_sandp_noise = []
ang_discrepancy_gaussian_noise = []

angles = range(1,90)#range of different number of angles to take projections at
num_iterations = 15
alg ='FBP'
poi =   False 
sandp = False
gauss = True
for a in angles:
    # a is number of angles used to get sinogram
    #print(a, 'angles')

    sinogram_ = astra1.sinogram(jet, np.pi, a, poi, sandp, gauss)
    sinogram_correct_units = real_units.num_density(sinogram_)
    reconstruction = astra1.reconstruct(sinogram_correct_units, alg, num_iterations)
    d = (np.mean(abs(jet_correct_units - reconstruction)) / np.mean(jet_correct_units)) *100 
    
    
    if poi == True:
        ang_discrepancy_poisson_noise.append(d)

    if sandp == True:
        ang_discrepancy_sandp_noise.append(d)
    if gauss == True:
        ang_discrepancy_gaussian_noise.append(d)

        
    if [poi,gauss,sandp] == [False,False,False]:
        ang_discrepancy_no_noise.append(d)

fig = plt.figure()
#fig.suptitle(alg 'with poisson noise, fontsize=20)

if poi == True:
    plt.plot(angles,ang_discrepancy_poisson_noise)
    plt.xlabel('Number of angles in sinogram')
    plt.ylabel('Average discrepancy relative to average phantom value (%)')
    #pylab.ylim(0, 150) 
    fig.suptitle(f'{alg} with poisson noise, {num_iterations} iterations', fontsize=16)
    #plt.show()

if sandp == True:
    plt.plot(angles,ang_discrepancy_sandp_noise)
    plt.xlabel('Number of angles in sinogram')
    plt.ylabel('Average discrepancy relative to average phantom value (%)')
    fig.suptitle(f'{alg} with sandp noise, {num_iterations} iterations', fontsize=16)
    #plt.show()
if gauss == True:
    plt.plot(angles, ang_discrepancy_gaussian_noise)
    plt.xlabel('Number of angles in sinogram')
    plt.ylabel('Average discrepancy relative to average phantom value (%)')
    #pylab.ylim(0,50)
    fig.suptitle(f'{alg} with gaussian noise,{num_iterations} iterations', fontsize=16)
    #plt.show

if [poi,gauss,sandp] == [False,False,False]:
    plt.plot(angles,ang_discrepancy_no_noise)
    plt.xlabel('Number of angles in sinogram')
    plt.ylabel('Average discrepancy relative to average phantom value (%)')
    fig.suptitle(f'{alg} with no noise, {num_iterations} iterations', fontsize=16)

plt.show()
"""
fig2 = plt.figure()
plt.plot(angles, ang_discrepancy_no_noise)
plt.plot(angles, ang_discrepancy_gaussian_noise)
plt.plot(angles, ang_discrepancy_poisson_noise)
plt.plot(angles, ang_discrepancy_sandp_noise)
plt.xlabel('Number of angles in sinogram')
plt.ylabel('Average discrepancy relative to average phantom value (%)')
fig2.suptitle(f'{alg} with no noise', fontsize=20)
plt.show()

"""
# birds eye view of phantom
imageio.imwrite("shockjet_phantom.png", jet_correct_units)

# image of sinogram
imageio.imwrite('sinogram.png', sinogram_correct_units)

# reconstruction
imageio.imwrite('reconstruction.png', reconstruction)

