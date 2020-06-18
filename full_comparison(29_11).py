# -*- coding: utf-8 -*-
"""
Aim to compare SIRT and FBP over a range of angles both with and without noise.
"""

import astra1
import phantoms
import graphs
import numpy as np
import offset90_v2_29_11
import matplotlib.pyplot as plt


def error(p, r):
    # Finds the error relative to the value of the phantom in that same cell...
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
#phant_centr = phantoms.shockjet(129, 800, 4, 2000, 6) 
phant_centr = phantoms.shockjet(129, 800, 4, 2000, 6) 
#phant_centr2 = phantoms.shockjet(128, 800, 4, 1000, 12) 
#sino_noise = astra1.sinogram(phant_centr, np.pi, 180, gaussian_noise=True, s_and_p_noise=True)
#reconstruction_noise = astra1.reconstruct(sino_noise,'SIRT', 100)


"""
sino_clean = astra1.sinogram(phant_centr, np.pi, 180)
sino_noise = astra1.sinogram(phant_centr, np.pi, 180, gaussian_noise=True, s_and_p_noise=True)



graphs.colourmap(phant_centr)
graphs.colourmap(sino_clean)


graphs.colourmap(sino_noise)


# do reconstruction
reconstruction_clean  = astra1.reconstruct(sino_clean,'SIRT', 100)
reconstruction_noise = astra1.reconstruct(sino_noise,'SIRT', 100)

graphs.colourmap(reconstruction_clean)
graphs.colourmap(reconstruction_noise)




# compare lineouts
plt.figure(1)
graphs.lineout(phant_centr)
graphs.lineout(reconstruction_clean)
graphs.lineout(reconstruction_noise)

plt.title('Comparison of lineouts from the phantom and the reconstruction.')

plt.figure(2)

# relative difference between phantom and reconstruction
diff_phant_clean = (phant_centr - reconstruction_clean) 
diff_phant_noise = (phant_centr - reconstruction_noise) 
plt.title('Lineout of the difference between the phantom and the reconstruction.')
graphs.lineout(diff_phant_clean)
graphs.lineout(diff_phant_noise)



graphs.plot3d(diff_phant)
graphs.plot3d(diff_phant_centr)
graphs.plot3d(diff_phant3)
graphs.plot3d(diff_phant_noise)

plt.title('3D plot of the difference between the phantom and the reconstruction.')

"""

"""
# the range of number of projections to reconstruct for:
n_projections = [int(a) for a in np.linspace(2,90,88)]

n_iterations = 50

"""

#the range of number of iterations to reconstruct for@
n_iterations = [int(a) for a in np.linspace(1,90,90)]
n_projections = 90


#comment out one of the two above as appropriate

# all six types to plot
fbp_noise_err = []
sirt_noise_err = []
fbp_clean_err = []
sirt_clean_err = []
fbp_90_err = []
sirt_90_err = []
fbp_90_noise_err = []
sirt_90_noise_err = []
"""
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
    sino_90 = offset90_v2_29_11.centre_sino(sino_90)
    sino_90 = offset90_v2_29_11.mirror_sinogram(sino_90)
    fbp_90 = astra1.reconstruct(sino_90, 'FBP', n_iterations, np.pi)
    fbp_90 = offset90_v2_29_11.resize(fbp_90, 129)
    sirt_90 = astra1.reconstruct(sino_90, 'SIRT', n_iterations, np.pi)
    sirt_90 = offset90_v2_29_11.resize(sirt_90, 129)

    print('90 Noise')
    sino_90_noise = astra1.sinogram(phant, np.pi/2, n, gaussian_noise=True)
    sino_90_noise = offset90_v2_29_11.centre_sino(sino_90_noise)
    sino_90_noise = offset90_v2_29_11.mirror_sinogram(sino_90_noise)
    fbp_90_noise = astra1.reconstruct(sino_90_noise, 'FBP', n_iterations, np.pi)
    fbp_90_noise = offset90_v2_29_11.resize(fbp_90_noise, 129)
    sirt_90_noise = astra1.reconstruct(sino_90_noise, 'SIRT', n_iterations, np.pi)
    sirt_90_noise = offset90_v2_29_11.resize(sirt_90_noise, 129)

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

plt.figure(2)
plt.plot(n_projections, fbp_noise_err, 'b', label='FBP - 180° range')
plt.plot(n_projections, fbp_90_noise_err, 'b--', label='FBP - 90° range')
plt.plot(n_projections, sirt_noise_err, 'r', label='SIRT - 180° range')
plt.plot(n_projections, sirt_90_noise_err, 'r--', label='SIRT - 90° range')
plt.yticks(np.arange(0, 51, 5))
plt.ylim(0,50)
plt.xticks(np.arange(0, 91, 10))
plt.xlim(0,90)
plt.grid()
plt.legend()
plt.ylabel('Reconstruction error (%)', fontsize=15)
plt.xlabel('Number of projections used', fontsize=15)

plt.figure(3)
plt.plot(n_projections, fbp_clean_err,'b', label='FBP - 180° range')
plt.plot(n_projections, fbp_90_err, 'b--', label='FBP - 90° range')
plt.plot(n_projections, sirt_clean_err, 'r', label='SIRT - 180° range')
plt.plot(n_projections, sirt_90_err, 'r--', label='SIRT - 90° range')
plt.yticks(np.arange(0, 51, 5))
plt.ylim(0,50)
plt.xticks(np.arange(0, 91, 10))
plt.xlim(0,90)
plt.grid()
plt.legend()
plt.ylabel('Reconstruction error (%)', fontsize=15)
plt.xlabel('Number of projections used', fontsize=15)
"""
"""
for n in n_projections:
    print(n,'projections')

    # find the different reconstructions of the phantom 
    
    print('Noise')
    sino_noise = astra1.sinogram(phant_centr, np.pi, n, gaussian_noise=True, s_and_p_noise=True)
    fbp_noise = astra1.reconstruct(sino_noise, 'FBP', n_iterations)
    sirt_noise = astra1.reconstruct(sino_noise, 'SIRT', n_iterations)
    
    print('Clean')
    sino_clean = astra1.sinogram(phant_centr, np.pi, n)
    fbp_clean = astra1.reconstruct(sino_clean, 'FBP', n_iterations)
    sirt_clean = astra1.reconstruct(sino_clean, 'SIRT', n_iterations)
    
    print('90 Clean')
    sino_90 = astra1.sinogram(phant_centr, np.pi/2, n)
    #sino_90 = offset90_v2_29_11.centre_sino(sino_90)
    sino_90 = offset90_v2_29_11.mirror_sinogram(sino_90)
    fbp_90 = astra1.reconstruct(sino_90, 'FBP', n_iterations, np.pi)
    #fbp_90 = offset90_v2_29_11.resize(fbp_90, 129)
    sirt_90 = astra1.reconstruct(sino_90, 'SIRT', n_iterations, np.pi)
    #sirt_90 = offset90_v2_29_11.resize(sirt_90, 129)
    
    print('90 Noise')
    sino_90_noise = astra1.sinogram(phant_centr, np.pi/2, n, gaussian_noise=True, s_and_p_noise=True)
    #sino_90_noise = offset90_v2_29_11.centre_sino(sino_90_noise)
    sino_90_noise = offset90_v2_29_11.mirror_sinogram(sino_90_noise)
    fbp_90_noise = astra1.reconstruct(sino_90_noise, 'FBP', n_iterations, np.pi)
    #fbp_90_noise = offset90_v2_29_11.resize(fbp_90_noise, 129)
    sirt_90_noise = astra1.reconstruct(sino_90_noise, 'SIRT', n_iterations, np.pi)
    #sirt_90_noise = offset90_v2_29_11.resize(sirt_90_noise, 129)

    # calculate the errors compared to the original phantom and append for plot
    print('Errors')
    fbp_noise_err.append(error(phant_centr,fbp_noise))
    sirt_noise_err.append(error(phant_centr,sirt_noise))
    fbp_clean_err.append(error(phant_centr,fbp_clean))
    sirt_clean_err.append(error(phant_centr,sirt_clean))
    fbp_90_err.append(error(phant_centr,fbp_90))
    sirt_90_err.append(error(phant_centr,sirt_90))
    fbp_90_noise_err.append(error(phant_centr,fbp_90_noise))
    sirt_90_noise_err.append(error(phant_centr,sirt_90_noise))
    print(' ')

plt.figure(4)
plt.plot(n_projections, fbp_noise_err, 'b', label='FBP - 180° range')
plt.plot(n_projections, fbp_90_noise_err, 'c--', label='FBP - 90° range')
plt.yticks(np.arange(0, 51, 5))
plt.ylim(0,50)
plt.xticks(np.arange(0, 91, 10))
plt.xlim(0,90)
plt.grid()
plt.legend()
plt.ylabel('Reconstruction error (%)', fontsize=15)
plt.xlabel('Number of projections used', fontsize=15)


plt.figure(5)
plt.plot(n_projections, sirt_noise_err, 'r', label='SIRT - 180° range')
plt.plot(n_projections, sirt_90_noise_err, 'r--', label='SIRT - 90° range')
plt.yticks(np.arange(0, 51, 5))
plt.ylim(0,50)
plt.xticks(np.arange(0, 91, 10))
plt.xlim(0,90)
plt.grid()
plt.legend()
plt.ylabel('Reconstruction error (%)', fontsize=15)
plt.xlabel('Number of projections used', fontsize=15)


plt.figure(6)
plt.plot(n_projections, fbp_clean_err,'b', label='FBP - 180° range')
plt.plot(n_projections, fbp_90_err, 'b--', label='FBP - 90° range')
plt.plot(n_projections, sirt_clean_err, 'r', label='SIRT - 180° range')
plt.plot(n_projections, sirt_90_err, 'r--', label='SIRT - 90° range')
plt.yticks(np.arange(0, 51, 5))
plt.ylim(0,50)
plt.xticks(np.arange(0, 91, 10))
plt.xlim(0,90)
plt.grid()
plt.legend()
plt.ylabel('Reconstruction error (%)', fontsize=15)
plt.xlabel('Number of projections used', fontsize=15)



# compare lineouts

plt.figure(7)
graphs.lineout(phant_centr, 'original')
graphs.lineout(fbp_noise, 'FBP - 180° range')
graphs.lineout(fbp_clean, 'FBP - 180° range' )
graphs.lineout(fbp_90, 'FBP - 90° range')
graphs.lineout(fbp_90_noise, 'FBP - 90° range')
plt.grid()
plt.legend()
plt.title('Comparison of lineouts from the phantom and the reconstruction.')


plt.figure(8)
graphs.lineout(phant_centr, 'original')
graphs.lineout(sirt_noise, 'SIRT - 180° range')
graphs.lineout(sirt_clean, 'SIRT - 180° range')
graphs.lineout(sirt_90, 'SIRT - 90° range')
graphs.lineout(sirt_90_noise, 'SIRT - 90° range')
plt.grid()
plt.legend()
plt.title('Comparison of lineouts from the phantom and the reconstruction.')


plt.figure(9)
graphs.lineout(phant_centr, 'original')
graphs.lineout(sirt_noise, 'SIRT - 180° range')
graphs.lineout(fbp_noise, 'FBP - 180° range')
plt.grid()
plt.legend()
plt.title('Comparison of lineouts from the phantom and the reconstruction.')


plt.figure(9)
graphs.lineout(phant_centr, 'original')
graphs.lineout(sirt_clean, 'SIRT - 180° range')
graphs.lineout(fbp_clean, 'FBP - 180° range' )
plt.grid()
plt.legend()
plt.title('Comparison of lineouts from the phantom and the reconstruction.')


# relative difference between phantom and reconstruction

plt.figure(10)

diff_phant_clean = (phant_centr - reconstruction_clean) 
diff_phant_noise = (phant_centr - reconstruction_noise) 
plt.title('Lineout of the difference between the phantom and the reconstruction.')
graphs.lineout(diff_phant_clean)
graphs.lineout(diff_phant_noise)

"""
for n in n_iterations:
    print(n,'iterations')

    # find the different reconstructions of the phantom 
    
    print('Noise')
    sino_noise = astra1.sinogram(phant_centr, np.pi, n_projections, gaussian_noise=True, s_and_p_noise=True)
    fbp_noise = astra1.reconstruct(sino_noise, 'FBP', n)
    sirt_noise = astra1.reconstruct(sino_noise, 'SIRT', n)
    
    print('Clean')
    sino_clean = astra1.sinogram(phant_centr, np.pi, n_projections)
    fbp_clean = astra1.reconstruct(sino_clean, 'FBP', n)
    sirt_clean = astra1.reconstruct(sino_clean, 'SIRT', n)
    
    print('90 Clean')
    sino_90 = astra1.sinogram(phant_centr, np.pi/2, n_projections)
    #sino_90 = offset90_v2_29_11.centre_sino(sino_90)
    sino_90 = offset90_v2_29_11.mirror_sinogram(sino_90)
    fbp_90 = astra1.reconstruct(sino_90, 'FBP', n, np.pi)
    #fbp_90 = offset90_v2_29_11.resize(fbp_90, 129)
    sirt_90 = astra1.reconstruct(sino_90, 'SIRT', n, np.pi)
    #sirt_90 = offset90_v2_29_11.resize(sirt_90, 129)

    print('90 Noise')
    sino_90_noise = astra1.sinogram(phant_centr, np.pi/2, n_projections, gaussian_noise=True, s_and_p_noise = True)
    #sino_90_noise = offset90_v2_29_11.centre_sino(sino_90_noise)
    sino_90_noise = offset90_v2_29_11.mirror_sinogram(sino_90_noise)
    fbp_90_noise = astra1.reconstruct(sino_90_noise, 'FBP', n, np.pi)
    #fbp_90_noise = offset90_v2_29_11.resize(fbp_90_noise, 129)
    sirt_90_noise = astra1.reconstruct(sino_90_noise, 'SIRT', n, np.pi)
    #sirt_90_noise = offset90_v2_29_11.resize(sirt_90_noise, 129)

    # calculate the errors compared to the original phantom and append for plot
    print('Errors')
    fbp_noise_err.append(error(phant_centr,fbp_noise))
    sirt_noise_err.append(error(phant_centr,sirt_noise))
    fbp_clean_err.append(error(phant_centr,fbp_clean))
    sirt_clean_err.append(error(phant_centr,sirt_clean))
    fbp_90_err.append(error(phant_centr,fbp_90))
    sirt_90_err.append(error(phant_centr,sirt_90))
    fbp_90_noise_err.append(error(phant_centr,fbp_90_noise))
    sirt_90_noise_err.append(error(phant_centr,sirt_90_noise))
    print(' ')

plt.figure(7)
plt.plot(n_iterations, fbp_noise_err, 'b', label='FBP - 180° range')
plt.plot(n_iterations, fbp_90_noise_err, 'b--', label='FBP - 90° range')
plt.plot(n_iterations, sirt_noise_err, 'r', label='SIRT - 180° range')
plt.plot(n_iterations, sirt_90_noise_err, 'r--', label='SIRT - 90° range')
plt.yticks(np.arange(0, 51, 5))
plt.ylim(0,50)
plt.xticks(np.arange(0, 91, 10))
plt.xlim(0,90)
plt.grid()
plt.legend()
plt.ylabel('Reconstruction error (%)', fontsize=15)
plt.xlabel('Number of iterations used', fontsize=15)

plt.figure(8)
plt.plot(n_iterations, fbp_clean_err,'b', label='FBP - 180° range')
plt.plot(n_iterations, fbp_90_err, 'b--', label='FBP - 90° range')
plt.plot(n_iterations, sirt_clean_err, 'r', label='SIRT - 180° range')
plt.plot(n_iterations, sirt_90_err, 'r--', label='SIRT - 90° range')
plt.yticks(np.arange(0, 51, 5))
plt.ylim(0,50)
plt.xticks(np.arange(0, 91, 10))
plt.xlim(0,90)
plt.grid()
plt.legend()
plt.ylabel('Reconstruction error (%)', fontsize=15)
plt.xlabel('Number of iterations used', fontsize=15)

