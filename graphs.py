"""
Functions that make useful graphs. Lineouts, 3d plots and colourmaps.
"""
import astra1
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d # needed
import phantoms

def lineout(p, label):
    # plots the lineout through middle of distribution
    #p is the data
    lineout=[]
    w = int(p.shape[0]/2) # finds middle
    for l in p:
        lineout.append(l[w]) # creates lineout
    plt.plot(range(-w,w+1), lineout, label = label)
    plt.xlabel('y', fontsize=15)
    plt.ylabel('Density (arb. units)', fontsize=15)

def lineout_horizontal(p, label):
    # plots the lineout through middle of distribution
    #p is the data
    lineout = []
    p = np.swapaxes(p,0,1)
    w = int(p.shape[0]/2) # finds middle
    for l in p:
        lineout.append(l[w]) # creates lineout
    plt.plot(range(-w,w+1), lineout, label = label)
    plt.xlabel('x', fontsize=15)
    plt.ylabel('Phase shift (radians)', fontsize=15)

def plot3d(p):
    # p is the 2D array to plot as a 3D surface
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    dim = max(p.shape)
    data = np.zeros((dim,dim))
    data[0:p.shape[0], 0:p.shape[1]] = p
    x, y = np.meshgrid(range(dim),range(dim)) # make coordinates
    ax.plot_surface(x,y,data, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    return ax


def colourmap(z,equal=True):
    # makes a colour map of a 2D array
    plt.figure()
    plt.pcolormesh(np.flip(z,0),cmap=plt.get_cmap('gray'))
    plt.colorbar()
    if equal:
        plt.axis('Equal')
    
    
#    
#if __name__ == "__main__": # when lineouts.py is imported it doesnt run the below
#
#    #create phantom
#    jet = phantoms.shockjet(128,800,4,2000,6)
#    
#    # create sinogram from phantom
#    sinogram_ = astra1.sinogram(jet, np.pi, 20)
#    
#    # do reconstruction
#    reconstruction = astra1.reconstruct(sinogram_,'SIRT', 100)
#    
#    
#    
#    # compare lineouts
#    plt.figure()
#    lineout(jet)
#    lineout(reconstruction)
#    plt.title('Comparison of lineouts from the phantom and the reconstruction.')
#    
#    
#    # relative difference between phantom and reconstruction
#    diff = (jet - reconstruction) 
#    plt.figure()
#    plt.title('Lineout of the difference between the phantom and the reconstruction.')
#    lineout(diff)
#    plot3d(diff)
#    plt.title('3D plot of the difference between the phantom and the reconstruction.')