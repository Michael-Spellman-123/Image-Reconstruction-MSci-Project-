"""
To reconstruct a phantom whose line of symmetry does not pass through the 
axis of rotation from a sinogram with a range of 90 degrees.
Has to adjust the sinogram before mirroring it.
Need to know the offset of the phantom!

"""
import astra1
import numpy as np
import graphs
import matplotlib.pyplot as plt
import phantoms


def centre(s, h, r=np.pi/2, v=10E-99):
    # makes sinogram mirrorable (puts line of symmetry in reconstruction...
    # ... through the axis of rotation)
    # s is the sinogram
    # r is the range of angle the projection is over eg pi/2    
    # h is the horizontal distance to the centre of the object from the...
    # ... axis of rotation 
    # v is the vertical distance to the center of the object from the...
    # ... axis of rotation. DON'T NEED TO KNOW v TO CORRECT SINOGRAM, CAN BE...
    # ... LEFT AS 0
    sinogram = np.zeros((s.shape[0], 2*s.shape[1]))
    R = np.sqrt(v * v + h * h) # distance between centre of object to axis of rotation
    angle = np.arctan(h / v)
    interval = r / s.shape[0] # interval between projections in radians
    for y in range(s.shape[0]):
        sinogram[y, int(round(s.shape[1]/2-R*np.sin(y*interval+angle))):
            int(round(s.shape[1]/2-R*np.sin(y*interval+angle)+s.shape[1]))]\
            = s[y,]
    # remove edges that were added to allow the sinogram to be shifted:
    sinogram = np.zeros((s.shape[0], s.shape[1]))[0:, 0:]\
    = sinogram[0:, round(s.shape[1]/2):round(3*s.shape[1]/2)]
    return sinogram


def mirror_sinogram(s):
    # takes 90 degrees of sinogram and flips it and adds it to get 180deg
    num_angles = s.shape[0]
    sino_mirr = np.zeros((2*num_angles, s.shape[1]))
    sino_mirr[0:num_angles, 0:s.shape[1]] += s
    sinogram2 = np.flip(s, 0)
    sino_mirr[num_angles:2*num_angles, 0:s.shape[1]] += sinogram2[0:]
    return sino_mirr


if __name__ == "__main__":

    # make offset jet
    ofsj = phantoms.offset_jet(48, 55)
    graphs.colourmap(ofsj)
    plt.title('Original phantom')
    
    # take projections and make sinogram
    offsino = astra1.sinogram(ofsj, np.pi/2, 90)
    graphs.colourmap(offsino)
    plt.title('90 degrees sinogram')
    
    # straighten
    offsino = centre(offsino, np.pi/2, 48, 55)
    graphs.colourmap(offsino)
    plt.title('Line of symmetry through axis of rotation')
    
    # mirror
    offsino = mirror_sinogram(offsino)
    graphs.colourmap(offsino)
    plt.title('Mirrored to 180 degrees')
    
    # reconstruction
    off_recon = astra1.reconstruct(offsino, 'FBP', 100, np.pi)
    graphs.colourmap(off_recon)
    plt.title('Reconstruction')