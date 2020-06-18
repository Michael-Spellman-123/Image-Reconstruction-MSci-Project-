# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 15:31:56 2020

@author: MS XPS
"""

import astra1
import unwrap
import graphs
import numpy as np 
import matplotlib.pyplot as plt
import real_units

# create sinograms
#s10 = unwrap.projs_2_sinos(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Experimental_reconstruction\projections10')
s10 = unwrap.projs_2_sinos(r'C:\my stuff\Imperial\4th Year\MSci Project\experimental_reconstruction\Experimental_reconstruction\projections10')

reconstructions = []
density = []
# set height step:
row_step_size = 200


for n in range(0, s10.shape[2], row_step_size):
    r = astra1.reconstruct(s10[0:,0:,n], 'FBP', 1, np.pi)
    reconstructions.append(r)
    real_units.phase2ref_ind(r)
    real_units.ref_ind2num_density(r)
    density.append(real_units.num_density(r))
    
    
def density_map(density):
    
    for a in range(len(density)):
        graphs.colourmap(density[a])
        plt.title('Image i' % a)
        plt.show()
    
density_map(density)

