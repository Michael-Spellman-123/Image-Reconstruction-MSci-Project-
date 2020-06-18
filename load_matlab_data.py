# -*- coding: utf-8 -*-


import scipy.io as sio
import glob
import numpy as np 

directory1 = r'C:\my stuff\Imperial\4th Year\MSci Project\experimental_reconstruction\Experimental_reconstruction\28-2-20'
directory2 = r'C:\my stuff\Imperial\4th Year\MSci Project\experimental_reconstruction\Experimental_reconstruction\28-2-20(2)'
x1= glob.glob(directory1 + "/*.mat")
x2 = glob.glob(directory2 + "/*.mat")

y1 = []
y2 = []

"""
for a in range(len(x2)):
    y2.append(sio.loadmat(x2[a]))
    print(y2[a]['InterpretData']['phase'])
"""
#print(y['phase'])

x = sio.loadmat('3619.mat')
print(np.shape((x['InterpretData']['phase'])))

"""
y2.append(sio.loadmat(x2[0]))
print(np.shape(((y2[0])['InterpretData']['phase'])))
"""