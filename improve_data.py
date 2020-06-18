import unwrap
import astra1
import numpy as np
import graphs
import matplotlib.pyplot as plt

lower_lim =  15
upper_lim = 200

    
def gradsub(proj, lower_lim, upper_lim):
    """corrects projection data (gradient subtraction)
    proj = 2d projection (ie. phase map/density map)
    lower_lim & upper_lim are the cutoffs for data used for fitting line
    lower =45, upper=180 used for 27/2 data
    """
    # remove gradient    
    lhx = list(range(0,lower_lim))
    rhx = list(range(upper_lim, np.shape(proj)[1]))
    proj = np.array([
            row - np.poly1d(
                  np.polyfit(
                            lhx + rhx,
                            list(row[0:lower_lim])+list(row[upper_lim:]),
                            1))(range(0,np.shape(proj)[1])) for row in proj])

    if sum(proj[int(np.shape(proj)[0]/2)]) < 0:
        proj = -proj
    return proj
 
    

def smooth_background(proj, lower_lim, upper_lim):        
    # smooth background
    lhx = list(range(lower_lim))
    rhx = list(range(upper_lim, np.shape(proj)[1]))
    proj = proj.clip(min = 0)
    proj[:,0:lower_lim//2] = 0
    #proj[:,5-len(rhx)//2:] = 0 #codeasof13-4-20
    proj[:,(upper_lim+np.shape(proj)[1])//2:] = 0 #changed

    
    lhw = np.ones(lower_lim)
    lhw[[0, -1]] = 1E9
    rhw = np.ones(len(rhx))
    rhw[[0, -1]] = 1E9
        
    for n in range(np.shape(proj)[0]):
        lhparams = np.polyfit(lhx, proj[:,0:lower_lim][n], 3, w=lhw)
        rhparams = np.polyfit(rhx, proj[:,upper_lim:][n], 3, w=rhw)
        
        proj[:,0:lower_lim][n] = [np.poly1d(lhparams)(x) for x in lhx]
        proj[:,upper_lim:][n] = [np.poly1d(rhparams)(x) for x in rhx]
    
    return proj



def smooth_sinos(stack):
    smooth_stack = np.copy(stack)
    for n in range(3,np.shape(stack)[1]-3):
        sino = smooth_stack[0:,n,0:]
        avg = sum(sum(sino)) / len(sino)
        for m in range(len(sino)):
            smooth_stack[0:,n,0:][m] = sino[m] * avg / sum(sino[m])
    return smooth_stack




if __name__ == "__main__":
    
    #stack = unwrap.stack_projs(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\6-3-20\2.3mm_tomo\phase_maps')
    #stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\11-3-20\180_phasemaps')
    #stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\27-2-20\tomo_phasemaps2')
    #stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\17-3-20-2-no_mount_phases')
    #stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\6-3-20\6-3-20-1.3mm-phase')
    stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\6-3-20\30 angles\2.3mm_100bar\phase_maps')
    #stack = unwrap.stack_projs(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\17-3-20-2-no_blade_interferograms/phase')
    #stack = stack[:,1:100, 10:235]
    #stack = stack[:, 1:199, 5:246] #no blade
    #stack = stack[:, 0:209, 1:240] #no blade
    corrected_stack = np.array([gradsub(proj, lower_lim, upper_lim) for proj in stack])
    #stack = corrected_stack

    
    
    """
    
     #####plots difference between uncorrected and corrected sinograms #######
    for x in np.linspace(0,125,9, dtype=int):
        graphs.colourmap(stack[0:,x,0:] - corrected_stack[0:,x,0:], equal=False)
        plt.title(str(x))
        
    """
    """
    
    for x in range(0,np.shape(stack)[0]):    
        graphs.lineout(corrected_stack[x,0:,0:], 'lineouts')
    """
    """
    for x in range(0,np.shape(stack)[0]-10):    
        graphs.lineout_horizontal(corrected_stack[x,0:,0:], x)
        plt.title('Lineout of the phase maps')

        plt.legend()
    """
    """
    ####### plots the corrected phase maps #######
    for x in range(0,np.shape(stack)[0]-10):
        #graphs.colourmap(corrected_stack[x,0:,0:], equal=False)
        graphs.colourmap(stack[x,0:,0:], equal=False)


        #plt.clim(-4,5)
        #plt.savefig(str(x))
    
    #graphs.colourmap(corrected_stack[0,0:,0:], equal = False)
    #graphs.colourmap(stack[0,0:,0:], equal = False)
    """
    
    
    
    ####### does reconstructions at different heights and plots them & sinos#######
    for x in np.linspace(5,125,8, dtype=int):
        #graphs.colourmap(corrected_stack[0:,x,0:], equal=False)
        recon = astra1.reconstruct(corrected_stack[0:,x,0:], 'SIRT', 100, np.pi)
        graphs.colourmap(recon)
        plt.title(str(x))
    
    
    
    
    
    
    ####### plots a graph showing how the sinograms are corrected #######
    
    mean = np.zeros(np.shape(stack[0,0,0:]))
    for row in stack[0,0:,0:]:
        mean = mean + row
        print(row)
    mean = mean / np.shape(stack[0,0:,0:])[1]
    
    plt.figure()
    
    x1 = list(range(lower_lim))
    y1 = mean[0:lower_lim]
    plt.plot(x1, y1, label='Data used for fit', color='b')
    
    x2 = list(range(upper_lim,np.shape(stack)[2]))
    y2 = mean[upper_lim:np.shape(stack)[2]]
    plt.plot(x2, y2, color='b')
    
    plt.plot(range(lower_lim,upper_lim), mean[lower_lim:upper_lim], ls=':',label='Excluded from fit')
    
    fitx = x1+x2
    fity = list(y1)+list(y2)
    plt.plot(range(0,np.shape(stack)[2]), np.poly1d(np.polyfit(fitx, fity, 1))(range(0,np.shape(stack)[2])), ls= '--',label='Line of best fit')
    
    corrected = mean - np.poly1d(np.polyfit(fitx, fity, 1))(range(0,np.shape(stack)[2]))
    plt.plot(range(0,np.shape(stack)[2]),corrected, color = 'black', label='Corrected data')
    plt.legend()
    