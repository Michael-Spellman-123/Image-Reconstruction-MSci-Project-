"""
To investigate the accuracy of the reconstruction with different numbers of 
iterations.
"""
import astra1
import matplotlib.pyplot as plt
import numpy as np
import phantoms
import pylab
#create phantom
jet = phantoms.shockjet(129,800,4,2000,6)


# reconstruct for different number of iterations and plot the average discrepancy..
# .. from the phantom jet
iterations = range(1,40) # range of different number of iterations to reconstruct with
iter_discrepancy = []
alg = 'SIRT'
for i in iterations:
    # i is number of iterations used to get reconstruction
    print(i,'iterations')
    s = astra1.sinogram(jet, np.pi, 90)
    r = astra1.reconstruct(s,alg,i)
    e = np.mean(abs(jet - r)) / np.mean(jet) * 100
    iter_discrepancy.append(e)
    
plt.figure()
plt.plot(iterations,iter_discrepancy)
plt.xlabel('Number of iterations for reconstruction')
plt.ylabel('Average discrepancy relative to average phantom value (%)')
#pylab.ylim(0,50)
