"""
DOES NOT WORK (Shift CoM to middle which isnt correct)
To do what offset90.py does but without knowing the offset of the phantom 
(has to be found from the sinogram).
To reconstruct a phantom whose line of symmetry does not pass through the 
axis of rotation from a sinogram with a range of 90 degrees.
Has to adjust the sinogram before mirroring it.
"""
import astra1
import numpy as np
import graphs
import matplotlib.pyplot as plt
import phantoms


def com(s, y):
    # finds 'centre of mass' of a projection
    # s is sinogram
    # y # projection in the sinogram
    x = np.arange(s.shape[1])
    integrand = s[y] * x
    integral = sum(integrand)
    total = sum(s[y])
    return integral / total


def centre_sino(s):
    # straightens sinogram using the position of the mean in the projections
    sinogram = np.zeros((s.shape[0], 2*s.shape[1]))
    for y in range(s.shape[0]):
        start = int(s.shape[1] - com(s, y))
        sinogram[y, start:start + s.shape[1]] = s[y,]
    # remove edges that were added to allow the sinogram to be shifted:
    sinogram = np.zeros((s.shape[0], s.shape[1]))[0:, 0:]\
    = sinogram[0:, int(s.shape[1]/2):int(3*s.shape[1]/2)]
    return sinogram


def mirror_sinogram(s):
    # takes 90 degrees of sinogram and flips it and adds it to get 180deg
    num_angles = s.shape[0]
    sino_mirr = np.zeros((2*num_angles, s.shape[1]))
    sino_mirr[0:num_angles, 0:s.shape[1]] += s
    sinogram2 = np.flip(s, 0)
    sino_mirr[num_angles:2*num_angles, 0:s.shape[1]] = sinogram2[0:]
    return sino_mirr

def resize(r, d):
    # resizes the reconstruction to the desired size
    # r is the reconstruction
    # d is the desired size
    resized = np.zeros((d,d))
    start = int((r.shape[0] - d) / 2)
    resized = r[start + 2:start + d + 2, start:start + d]
    return resized

if __name__ == "__main__":
     
    j = phantoms.offset_jet(0, 0)
    sino = astra1.sinogram(j, np.pi/2, 180)
    
    
    
    # make offset jet
    ofsj = phantoms.offset_jet(48, 55)
    graphs.colourmap(ofsj)
    plt.title('Original phantom')

    # take projections and make sinogram
    offsino = astra1.sinogram(ofsj, np.pi/2, 180)
    graphs.colourmap(offsino)
    plt.title('90 degrees sinogram')

    # straighten
    offsino = centre_sino(offsino)#, np.pi/2, 48, 55)
    graphs.colourmap(offsino)
    plt.title('Line of symmetry through axis of rotation')

    graphs.colourmap(sino - offsino)



    # mirror
    offsino = mirror_sinogram(offsino)
    graphs.colourmap(offsino)
    plt.title('Mirrored to 180 degrees')
    
    # reconstruction
    off_recon = astra1.reconstruct(offsino, 'FBP', 100, np.pi)
    graphs.colourmap(off_recon)
    plt.title('Reconstruction')
    

"""
    # testing resizing works
    testoff = phantoms.offset_jet(0, 0)
    graphs.colourmap(testoff)
    resized = resize(testoff, 129)

    
    test = phantoms.shockjet(129, 800, 4, 2000, 6)
    graphs.colourmap(resized-test)
    plt.title('Difference')
"""
