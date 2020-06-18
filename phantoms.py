"""
For functions that create phantoms.
"""
import numpy as np
import graphs
import astra1

def shockjet(n,s,p,S,P):
    # creates jet with shock phantom
    # n is dimenstions of array (128) -for phantom to be centered should be odd
    # s is the standard deviation of the gaussian
    # p is the power in the exponent of the super-gaussian
    # S, P are the corresponding shock supergaussian parameters
    
    # create gas jet
    x, y = np.meshgrid(range(int(-n/2),round(n/2+0.1),1),
                       range(int(-n/2),round(n/2+0.1),1)) # +0.1 to ensure rounds up
    rp = (x*x + y*y)**(p/2)
    superjet = np.array(np.exp(-rp/(2*s*s)))
    
    # puts shock near edge of gas jet:
    i = n/2
    for x in superjet[int(n/2)]:
        i -= 1
        if x > 0.5:
            whm = i # width at half maximum
            break
    shock_pos = int((2*whm / 3)) # can adjust this to adjust the position of... 
                                 # ... the shock relative to centre of jet
    
    # create shock super gaussian
    S2 = S*S
    X = np.arange(int(-n/2)+shock_pos,int(n/2)+shock_pos,1)
    RP = (2*X*X)**(P/2)
    shock = np.array(np.exp(-RP/(2*S2)))/2 + 1
    
    # multiply the 2 arrays
    n=0
    for x in shock:
        superjet[n] = shock[n]*superjet[n]
        n+=1
    
    return superjet



def offset_jet(h, v):
    # puts jet in array not at the centre
    jet = shockjet(129, 800, 4, 2000, 6)
    offset_jet = np.zeros((258, 258))
    offset_jet[int(offset_jet.shape[0]/2 - v - jet.shape[0]/2):
        int(offset_jet.shape[0]/2 - v + jet.shape[0]/2),
               int(offset_jet.shape[1]/2 + h - jet.shape[1]/2):
                   int(offset_jet.shape[1]/2+h+jet.shape[1]/2)] += jet
    return offset_jet

def offset_bar(h, v):
    # makes a rectangle in an array
    # makes 12x12 square because of the 5s below (5+5+2)
    w = 2
    l = 15
    offset_bar = np.zeros((256, 256))
    offset_bar[128-v-w:128-v+w, 128+h-l:128+h+l] += 1
    return offset_bar


def gaussianjet(n,s):
    # n is dimenstions of array (128)
    # s is the standard deviation of the gaussian
    s2 = s*s
    x, y = np.meshgrid(range(int(-n/2),int(n/2),1),range(int(-n/2),int(n/2),1))
    r2 = x*x + y*y
    return np.array(np.exp(-r2/(2*s2)))


def supergaussianjet(n,s,p):
    # n is dimenstions of array (128)
    # s is the standard deviation of the gaussian
    # p is the power in the exponent of the super-gaussian
    s2 = s*s
    x, y = np.meshgrid(range(int(-n/2),int(n/2),1),range(int(-n/2),int(n/2),1))
    rp = (x*x + y*y)**(p/2)
    return np.array(np.exp(-rp/(2*s2)))


if __name__ == "__main__":
    
    jet = shockjet(129, 800, 4, 2000, 6)
    graphs.colourmap(jet)
    sino = astra1.sinogram(jet, np.pi, 180)
    graphs.colourmap(sino)
    reconstruction = astra1.reconstruct(sino,'SIRT', 40, np.pi)
    graphs.colourmap(reconstruction)
    """
    offset = offset_bar(10,20)
    graphs.colourmap(offset)
    sino = astra1.sinogram(offset, np.pi, 180)
    #graphs.colourmap(sino)
    """
    #gaussian = gaussianjet(128,800)
    #graphs.colourmap(gaussian)
    #sino = astra1.sinogram(gaussian, np.pi, 180)
    #graphs.colourmap(sino)
    
    #graphs.plot3d(gaussian)
    
    
    