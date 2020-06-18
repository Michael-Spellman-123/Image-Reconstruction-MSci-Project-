"""
To reconstruct a phantom whose line of symmetry passes through the axis of 
rotation from a sinogram that uses a range of just 90 degrees. Because the line
of symmetry passes through the axis of rotation the sinogram just has to be 
mirrored. However this is unlikely to happen in experiment - see offset90.py
"""
import astra1
import numpy as np
import imageio
import graphs
import matplotlib.pyplot as plt
import phantoms

def mirror_sinogram(s):
    # takes 90 degrees of sinogram and flips it and adds it to get 180deg
    num_angles = s.shape[0]
    print(num_angles)
    sino_mirr = np.zeros((2*num_angles,s.shape[1]))
    sino_mirr[0:num_angles, 0:s.shape[1]] += s
    sinogram2 = np.flip(s,0)
    sino_mirr[num_angles:2*num_angles, 0:s.shape[1]] += sinogram2[0:]
    return sino_mirr



if __name__ == '__main__':

    #create phantom
    jet = phantoms.shockjet(129,800,4,2000,6)
    
    # create sinogram from phantom
    num_angles =  90
    sinogram90 = astra1.sinogram(jet, np.pi/2, num_angles)
    
    
    
    sino_mirr = mirror_sinogram(sinogram90)
    
    # image of sinogram
    imageio.imwrite('sino_mirr.png', sino_mirr)
    graphs.colourmap(sino_mirr)
    sinogram180 = astra1.sinogram(jet, np.pi, 2*num_angles)
    ## image of the full proper sinogram
    imageio.imwrite('sinogram180.png', sinogram180)
    
    # difference of sinogram from 90 and the normal 180
    sino_diff = sinogram180 - sino_mirr
    
    
    graphs.colourmap(sino_diff)
    plt.title('Difference in sinograms.')
    
    # do reconstructions
    reconstruction90 = astra1.reconstruct(sino_mirr,'FBP', 100)
    reconstruction180 = astra1.reconstruct(sinogram180,'FBP', 100)
    
    # difference between reconstruction from 90 degrees and 180 degrees
    reconstruct_diff = reconstruction180 - reconstruction90
    graphs.colourmap(reconstruct_diff)






