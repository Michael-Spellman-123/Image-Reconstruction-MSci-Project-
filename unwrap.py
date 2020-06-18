from PIL import Image
import numpy as np
import glob
import scipy.io as sio
import graphs
import matplotlib.pyplot as plt


def stack_projs(directory):
    """
    directory is directory with all .mat phase map files in
    returns 3d array: all the projections stacked up:
    
    stack[projection number, sinogram number (height), width (coord perp. to direction of flow)]
    
    """
    files = glob.glob(glob.glob(directory + '*')[0] + '/*.mat')
    n = 0 # n=projection number
    firstfile = sio.loadmat(files[0])['InterpretData']['phase'][0][0]
    dimx = firstfile.shape[0]
    dimy = firstfile.shape[1]
    
    stack = np.zeros((len(files), dimy, dimx))
    for f in files:
        imarray = np.flip(sio.loadmat(f)['InterpretData']['phase'][0][0],0)
        print(imarray)
        for y in range(imarray.shape[1]):
            stack[n,-y,:] += imarray[:,y]
        n += 1
    
    return stack

    
#projs_2_sinos(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\27_2_20\tomo_phasemaps')
stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\11-3-20\180_phasemaps')


def first_projection(directory):
    files = glob.glob(glob.glob(directory + '*')[0] + '/*.mat')
    firstfile = sio.loadmat(files[0])['InterpretData']['phase'][0][0]
    #return firstfile
    flipped_firstfile = np.zeros((np.shape(firstfile)[1],np.shape(firstfile)[0]))
    for y in range(np.shape(firstfile)[1]):
        flipped_firstfile[-y,:] = firstfile[:,y]
    return flipped_firstfile


#if __name__ == "__main__":
#    s10 = projs_2sinos(r'C:\my stuff\Imperial\4th Year\MSci Project\experimental_reconstruction\Experimental_reconstruction\projections10')
#   # s10 = open_batch(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Experimental_reconstruction\projections90')
#
#    s10 = projs_2_sinos(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Experimental_reconstruction\projections10')
#    
#    #s90 = open_batch(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Experimental_reconstruction\projections90')
#    #s90 = open_batch(r'C:\my stuff\Imperial\4th Year\MSci Project\experimental_reconstruction\Experimental_reconstruction\projections90')
#
#    graphs.colourmap(s10[0:,0:,0], equal=False)
#    plt.ylabel('Theta')
#    plt.xlabel('r')
#    plt.title('p(r,theta)')

