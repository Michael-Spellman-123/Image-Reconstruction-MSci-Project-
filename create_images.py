"""
Creating png files of arrays (phantom, sinogram, reconstruction).
"""
import astra1
import imageio
import numpy as np
import real_units
import phantoms


#create phantom
jet = phantoms.shockjet(129,800,4,2000,6)

#create phantom with correct units
jet_correct_units = real_units.num_density(jet)

# above is commented out as messes with reconstruction scaling issues - FIXED
#above is commented out as messes with addition of noise

# create sinogram from phantom
sinogram_ = astra1.sinogram(jet, np.pi, 180,False,False,True)
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

