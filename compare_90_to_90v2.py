# -*- coding: utf-8 -*-
"""
Compare 90 to 90 v2
"""
import phantoms
import astra1
import numpy as np
import graphs
import matplotlib.pyplot as plt
import offset90
import offset90_v2

# make offset jet
ofsj = phantoms.offset_jet(48, 55)
graphs.colourmap(ofsj)
plt.title('Original phantom')

##############################################################################

# take projections and make sinogram
offsino1 = astra1.sinogram(ofsj, np.pi/2, 90)
graphs.colourmap(offsino1)
plt.title('90 degrees sinogram')

# straighten
offsino1 = offset90.centre(offsino1, np.pi/2, 48, 55)
graphs.colourmap(offsino1)
plt.title('Line of symmetry through axis of rotation')

# mirror
offsino1 = offset90.mirror_sinogram(offsino1)
graphs.colourmap(offsino1)
plt.title('Mirrored to 180 degrees')

# reconstruction
off_recon1 = astra1.reconstruct(offsino1, 'FBP', 100, np.pi)
graphs.colourmap(off_recon1)
plt.title('Reconstruction')

#############################################################################


# take projections and make sinogram
offsino2 = astra1.sinogram(ofsj, np.pi/2, 90)
graphs.colourmap(offsino2)
plt.title('90 degrees sinogram')

# straighten
offsino2 = offset90_v2.centre_sino(offsino2)#, np.pi/2, 48, 55)
graphs.colourmap(offsino2)
plt.title('Line of symmetry through axis of rotation')

# mirror
offsino2 = offset90_v2.mirror_sinogram(offsino2)
graphs.colourmap(offsino2)
plt.title('Mirrored to 180 degrees')

# reconstruction
off_recon2 = astra1.reconstruct(offsino2, 'FBP', 100, np.pi)
graphs.colourmap(off_recon2)
plt.title('Reconstruction')

#############################################################################
##################################COMPARE###################################

graphs.colourmap(offsino1-offsino2)
graphs.colourmap(off_recon1-off_recon2)












