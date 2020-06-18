import numpy as np

phase = np.pi
L = 5.51E-3
wavelength = 633E-9
m = 6.63E-26
alpha = 1.83E-40
epsilon = 8.85E-12
k = 2*np.pi / wavelength
print('k',k)



eta = phase/(k*L) + 1

print('eta', eta)

n = 3* epsilon * ((eta)**2-1) / (alpha * ((eta)**2+2))

rho = m * n

print('rho', rho, 'kgm-3')

rho_cgs = rho / 1000 

print('rho_cgs', rho_cgs, 'gcm-3')

print('n', n, 'm-3')

n_cgs = n * 1E-6

print('n_cgs', n_cgs, 'cm-3')