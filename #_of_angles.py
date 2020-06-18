"""
To investigate the accuracy of the reconstruction with different numbers of 
projections.
"""
import astra1
import matplotlib.pyplot as plt
import numpy as np
import phantoms
import pylab
import graphs


def error(p, r):
    # Finds the error relative to the value of the phantom in that same cell...
    # ... rather than relative to the mean of the phantom as done before....
    # ... Returns the mean of these errors.
    #
    # p is the phantom
    # r is the reconstruction
    
    # flatten the arrays, ie. make them lists
    p = np.ravel(p)
    r = np.ravel(r)

    # find difference and only keep values where phantom greater than 10^-4
    diff = abs(p - r)
    for i in range(len(p)-1, -1, -1):
        if p[i] < 1E-4:
            diff = np.delete(diff, i)
            p = np.delete(p, i)

    # calculate relative error as a percentage (relative to phantom)
    rel_err = diff / p * 100
    return np.mean(rel_err) # return the mean so that it can be plotted
    
    

#create phantom
jet = phantoms.shockjet(129,800,4,2000,6)


# reconstruct for different amount of angles and plot the average discrepancy..
# .. from the phantom jet
ang_discrepancy = []
angles = range(2,90,5) # range of different number of angles to take projections at
alg = 'SIRT'
for a in angles:
    # a is number of angles used to get sinogram
    print(a, 'angles')
    s = astra1.sinogram(jet, np.pi, a)
    r = astra1.reconstruct(s,alg,100)
    err = error(jet, r)
    #graphs.colourmap(r)
    ang_discrepancy.append(err)
    
plt.figure()
plt.plot(angles, ang_discrepancy)
plt.xlabel('Number of projections in sinogram')
plt.ylabel('Average discrepancy relative to average phantom value (%)')
plt.title(alg)
#pylab.ylim(0,6.5)
