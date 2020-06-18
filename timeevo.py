import graphs
import unwrap
import matplotlib.pyplot as plt
import numpy as np
import improve_data
import real_units

#phase_map_stack = unwrap.stack_projs(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\6-3-20\2.3mm_time_evo')
#phase_map_stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\27-2-20\tomo_phasemaps2')
#phase_map_stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\6-3-20\6-3-20-phase_2.3mm')
phase_map_stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\6-3-20\6-3-20-1.3mm-phase')

grad_sub_stack =  np.array([improve_data.gradsub(proj, 45, 180) for proj in phase_map_stack])
smooth_bckgnd_stack = np.array([improve_data.smooth_background(proj, 45, 180) for proj in grad_sub_stack])
n_stack = real_units.num_density(smooth_bckgnd_stack)
smooth_n_stack = improve_data.smooth_sinos(n_stack)



#smooth_n_stack = improve_data.smooth_sinos(smooth_bckgnd_stack)


flipped_stack = np.copy(smooth_n_stack)
temp_stack = np.copy(smooth_n_stack)
for y in range(np.shape(smooth_n_stack)[1]):
    temp_stack[:,-y,:] = smooth_n_stack[:,y,:] 
for x in range(np.shape(smooth_n_stack)[2]):
    flipped_stack[:,:,-x] = temp_stack[:,:,x] 
    
smooth_n_stack = np.copy(flipped_stack)


lineouts = []
for n in range(len(smooth_n_stack)):
    p = smooth_n_stack[n]
    if sum(p[100,:]) < 0:
        p = -p
        smooth_n_stack[n] = p
    lineouts.append(p[100,:])
    
frame = 1
for p in smooth_n_stack:
    graphs.colourmap(p)
    #plt.clim(0,9) # set colourmap range
    plt.title('Frame %i' % frame)
    #plt.clim(0,2E18)
    plt.savefig(str(frame))
    frame += 1

#for n in range(len(lineouts)): 
    
plt.figure()
for n in range(6):
    colour = str((len(lineouts)+0.2)/(n+0.2))
    plt.plot(range(np.shape(smooth_n_stack)[2]),lineouts[n], label = 'Frame:' + str(n))
    
plt.ylabel('Density (cm$^3$)', fontsize=15)
plt.xlabel('x')
plt.title('Lineouts over time')
plt.legend()

plt.figure()
for n in range(6,13):
    colour = str((len(lineouts)+0.2)/(n+0.2))
    plt.plot(range(np.shape(smooth_n_stack)[2]),lineouts[n], label = 'Frame:' + str(n))
    
plt.ylabel('Density (cm$^3$)', fontsize=15)
plt.xlabel('x')
plt.title('Lineouts over time')
plt.legend()

plt.figure()
for n in range(13,19):
    colour = str((len(lineouts)+0.2)/(n+0.2))
    plt.plot(range(np.shape(smooth_n_stack)[2]),lineouts[n], label = 'Frame:' + str(n))
    
plt.ylabel('Density (cm$^3$)', fontsize=15)
plt.xlabel('x')
plt.title('Lineouts over time')
plt.legend()
    
"""
plt.figure()
rows = np.linspace(0, np.shape(smooth_n_stack)[1]-1,5, dtype=int)
for row in rows:
    lineouts = []
    for p in smooth_n_stack:
        lineouts.append(p[row,50:150])
    integratedlo = []
    for lo in lineouts:
        integratedlo.append(sum(lo))
    plt.plot(range(len(lineouts)), integratedlo, label=str(row))
plt.title('Integrated lineouts over time')
plt.legend()
"""