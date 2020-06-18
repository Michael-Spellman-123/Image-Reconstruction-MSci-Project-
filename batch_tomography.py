import unwrap
import astra1
import numpy as np
import graphs
import matplotlib.pyplot as plt
import improve_data
import real_units
import offset90_v2_29_11
import warnings
warnings.simplefilter('ignore', np.RankWarning)

#s10 = unwrap.open_batch(r'C:\my stuff\Imperial\4th Year\MSci Project\Experimental_reconstruction\projections10')
#s10 = unwrap.projs_2_sinos(r'C:\my stuff\Imperial\4th Year\MSci Project\experimental_reconstruction\Experimental_reconstruction\projections10')
#s10 = unwrap.open_batch(r'C:\my stuff\Imperial\4th Year\MSci Project\experimental_reconstruction\Experimental_reconstruction\projections10')

# create sinograms
#stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\6-3-20\30 angles\2.3mm_100bar\phase_maps')
#stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\6-3-20\30 angles\1.3mm_100bar\phase_maps')

#stack = unwrap.stack_projs(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\180test_Temp')
#stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\11-3-20\180_phasemaps')
#stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\27-2-20\tomo_phasemaps2')
#stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\17-3-20-2-no_mount_phases')

stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\17-3-20-2-no_blade_interferograms/phase')

#stack = stack[:, 1:130, 5:190] #17-3-20 no blade
stack = stack[:,5:195, 2:200] #11-3-20 data
#stack = stack[:,1:200, 1:240] #27-2-20 data
#stack = stack[:,1:200, 1:240] #17-3-20 no mount not done yet

grad_sub_stack = np.array([improve_data.gradsub(proj, 15, 180) for proj in stack])
#smooth_bckgnd_stack = np.array([improve_data.smooth_background(proj, 20, 210) for proj in stack])

smooth_bckgnd_stack = np.array([improve_data.smooth_background(proj, 15, 180) for proj in grad_sub_stack])
n_stack = real_units.num_density(smooth_bckgnd_stack)
#n_stack = real_units.num_density(stack)


#smooth_n_stack = improve_data.smooth_sinos(n_stack)
####### does reconstructions at different heights #######
number_of_slices = np.shape(n_stack)[1]
reconstructions = []

for x in np.linspace(0, np.shape(n_stack)[1]-1, number_of_slices, dtype=int):
    print(x)
    #sino_90 = offset90_v2_29_11.centre_sino(smooth_n_stack[0:90,x,0:])
    #sino_180 = offset90_v2_29_11.mirror_sinogram(sino_90)

    #sino_180 = offset90_v2_29_11.centre_sino(smooth_n_stack[0:180,x,0:])
    sino_180 = offset90_v2_29_11.centre_sino(n_stack[0:180,x,0:])


    reconstructions.append(astra1.reconstruct(sino_180,
                                              'SIRT', 30, np.pi))

for n in range(len(reconstructions)):    
    graphs.colourmap(reconstructions[n])
    #row_num = int((n+1)*np.shape(n_stack)[1]/number_of_slices)
    row_num = int((np.shape(n_stack)[1]-n)*np.shape(n_stack)[1]/number_of_slices)
    plt.title('Row %i' % row_num)
    #plt.clim(0,8E18) # set constant colourmap
    plt.savefig(str(row_num))
    #plt.close()
    
    



################ show improvement process:   ##############################
############## as improvement in the sinogram #############################
# choose a height:
height = 120

sino = stack[0:,height,0:]
grad_subsino = grad_sub_stack[0:,height,0:]
smth_bckgnd_sino = smooth_bckgnd_stack[0:,height,0:]
#smoothsino = smooth_n_stack[0:,height,0:]

graphs.colourmap(sino, equal=False)
plt.title('Raw')
graphs.colourmap(astra1.reconstruct(stack[0:,height,0:],'SIRT', 50, np.pi))
plt.title('Raw')

graphs.colourmap(grad_subsino, equal=False)
plt.title('Gradient subtracted')
graphs.colourmap(astra1.reconstruct(grad_sub_stack[0:,height,0:],'SIRT', 50, np.pi))
plt.title('Gradient subtracted')

graphs.colourmap(smth_bckgnd_sino, equal=False)
plt.title('Background smoothed')
graphs.colourmap(astra1.reconstruct(smooth_bckgnd_stack[0:,height,0:],'SIRT', 50, np.pi))
plt.title('Background smoothed')
"""
graphs.colourmap(smoothsino, equal=False)
plt.title('Sinogram smoothed')
graphs.colourmap(astra1.reconstruct(smooth_n_stack[0:,height,0:],'SIRT', 50, np.pi))
plt.title('Sinogram smoothed')



for y in np.linspace(0,np.shape(sino)[0]-1,7, dtype=int):
    plt.figure(41)
    plt.title('Raw')
    plt.plot(range(np.shape(sino)[1]),sino[y,0:])
    plt.figure(42)
    plt.title('Gradient subtracted')
    plt.plot(range(np.shape(sino)[1]),grad_subsino[y,0:])    
    plt.figure(43)
    plt.title('Background smoothed')
    plt.plot(range(np.shape(sino)[1]),smth_bckgnd_sino[y,0:])    
    plt.figure(44)
    plt.title('Sinogram smoothed')
    plt.plot(range(np.shape(sino)[1]),smoothsino[y,0:])


################ show improvement process:   ##############################
############## as improvement in the projection #############################
# choose a projection:

proj_no = 0

flipped_stack = np.copy(smooth_n_stack)
temp_stack = np.copy(smooth_n_stack)
for y in range(np.shape(smooth_n_stack)[1]):
    temp_stack[:,-y,:] = smooth_n_stack[:,y,:] 
for x in range(np.shape(smooth_n_stack)[2]):
    flipped_stack[:,:,-x] = temp_stack[:,:,x] 
    
smooth_n_stack = np.copy(flipped_stack)


proj = stack[proj_no,0:,0:]
grad_subproj = grad_sub_stack[proj_no,0:,0:]
smth_bckgnd_proj = smooth_bckgnd_stack[proj_no,0:,0:]
smoothproj = smooth_n_stack[proj_no,0:,0:]

graphs.colourmap(proj, equal=False)
plt.title('Raw')

graphs.colourmap(grad_subproj, equal=False)
plt.title('Gradient subtracted')

graphs.colourmap(smth_bckgnd_proj, equal=False)
plt.title('Background smoothed')

graphs.colourmap(smoothproj, equal=False)
plt.title('Sinogram smoothed')
"""


    