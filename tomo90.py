# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 12:51:52 2019

@author: Elliot Ray
"""

import tomopy_prep_alignment as tpa
import astra1
import numpy as np
import graphs
import matplotlib.pyplot as plt
import phantoms

# make offset jet
ofsj = phantoms.offset_jet(48, 55)


# take projections and make sinogram
offsino = astra1.sinogram(ofsj, np.pi/2, 90)

offsino = np.array([offsino])


aligned = tpa.align_seq(offsino, np.linspace(0, np.pi/2, 90, endpoint=False))
#graphs.colourmap(aligned)
