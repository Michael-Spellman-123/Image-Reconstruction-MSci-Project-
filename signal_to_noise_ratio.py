# -*- coding: utf-8 -*-


import astra1
import numpy as np
import real_units

import imageio
import phantoms


#create phantom
jet = phantoms.shockjet(128,800,4,2000,6)

#create phantom with correct units
jet_correct_units = real_units.num_density(jet)

# above is commented out as messes with reconstruction scaling issues - FIXED
#above is commented out as messes with addition of noise

# create sinogram from phantom
sinogram_ = astra1.sinogram(jet, np.pi, 180,False,False)
#sinogram__= astra1.sinogram(jet_correct_units,np.pi,180,True)
sinogram_correct_units = real_units.num_density(sinogram_)
"""
# create sinogram with noise from phantom

sinogram_poisson_noise = astra1.sinogram_poisson(,sinogram,jet, np.pi, 180)
sinogram_poisson_s_and_p = astra1.add_salt_pepper(jet_correct_units,np.pi,180,0.01)
"""

# create reconstruction
reconstruction = astra1.reconstruct(sinogram_correct_units, 'FBP', 100)

# birds eye view of phantom
imageio.imwrite("shockjet_phantom.png", jet_correct_units)

# image of sinogram
imageio.imwrite('sinogram.png', sinogram_correct_units)

# reconstruction
imageio.imwrite('reconstruction.png', reconstruction)

#just practice arrays here
arrayarr1=np.array([[20, 2, 7, 1, 34], 
        [50, 12, 12, 34, 4]])
  
arrayarr2 = np.array([50, 12, 12, 34, 4]) 

def signaltonoise(a, axis=0, ddof =0):     

 #Parameters:	
            #a : array_like
            #An array_like object containing the sample data.

            #axis : int or None, optional

            #If axis is equal to None, the array is first ravel’d. 
            #If axis is an integer, this is the axis over which to operate. 

            #ddof : int, optional
                    #Degrees of freedom correction for standard deviation. 

 #Returns:	
         #s2n : ndarray
         #The mean to standard deviation ratio(s) along axis, or 0 where 
         #the standard deviation is 0.
    a = np.asanyarray(a)
    m = a.mean() #keep empty if no axis, setting axis =0 here ruins it
    sd = a.std() #keep empty if no axis, setting axis and ddof =0 here ruins it
    print(m)
    print(sd)
    
    return np.where(sd == 0, 0, m/sd) #says where in this array, entries 
                                      #satisfy a given condition".
                                      #m/sd is SNR calculation

print(signaltonoise(sinogram_correct_units))
