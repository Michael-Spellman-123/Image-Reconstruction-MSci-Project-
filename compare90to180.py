"""
Compare the accuracy of reconstructions made from projections taken over 180
degrees with ones taken over 90 degrees.
"""

import astra1
import matplotlib.pyplot as plt
import numpy as np
import phantoms
import offset90_v2
import graphs

#create phantom
jet = phantoms.shockjet(129,800,4,2000,6)


s1 = astra1.sinogram(jet, np.pi, 180)
s2 = astra1.sinogram(jet, np.pi/2, 90)
s3 = offset90_v2.mirror_sinogram(s2)
graphs.colourmap(s1)
graphs.colourmap(s2)
graphs.colourmap(s3)
graphs.colourmap(s1-s3)


# reconstruct for different amount of angles and plot the average discrepancy..
# .. from the phantom jet
#ang_discrepancy = []
#angles = range(2,50,10) # range of different number of angles to take projections at


#for a in angles:
#    s1 = astra1.sinogram(jet, np.pi, a)
#    r1 = astra1.reconstruct(s1, 'SIRT', 100)
#    print(int(a/2))
#    s2 = astra1.sinogram(jet, np.pi/2, int(a/2))
#    #graphs.colourmap(s2)
#    s2 = offset90_v2.mirror_sinogram(s2)
#    r2 = astra1.reconstruct(s2, 'SIRT', 100)
#    d = s1 - s2
#    graphs.colourmap(d)

"""
for a in angles:
    # a is number of angles used to get sinogram
    print(a, 'angles')
    s = astra1.sinogram(jet, np.pi, a)
    r = astra1.reconstruct(s,'SIRT',100)
   # graphs.colourmap(r)
    d = np.mean(abs(jet - r)) / np.mean(jet) * 100
    ang_discrepancy.append(d)
    
plt.figure()
plt.plot(angles, ang_discrepancy, label='180 degrees')
plt.xlabel('Number of angles in sinogram')
plt.ylabel('Average discrepancy relative to average phantom value (%)')

ang_discrepancy2 = []
for a in angles:
    # a is number of angles used to get sinogram
    # same number of angles but over just 90 degrees
    print(a, 'angles')
    s = astra1.sinogram(jet, np.pi/2, a)
    s = offset90_v2.mirror_sinogram(s)
    r = astra1.reconstruct(s,'SIRT',100)
    #graphs.colourmap(r)
    d = np.mean(abs(jet - r)) / np.mean(jet) * 100
    ang_discrepancy2.append(d)
    
plt.plot(angles, ang_discrepancy2, label='90 degrees')
plt.xlabel('Number of angles in sinogram')
plt.ylabel('Average discrepancy relative to average phantom value (%)')
plt.legend()
"""