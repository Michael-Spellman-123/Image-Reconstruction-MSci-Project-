"""
For functions that use the AstraToolbox.
"""
import numpy as np
import astra


def geom_setup(w, r, n):
    # w is the dimensions of the detector/phantom eg 128
    # r is the range of angles used eg. pi
    # n is the number of angles used (number of projections)
    if r < np.pi:
        ep = True
    else:
        ep = False  
    angles = np.linspace(0, r, n, endpoint=ep) # r not included in angles
    vol_geom = astra.create_vol_geom(w, w)
    proj_geom = astra.create_proj_geom('parallel', 1., w, angles)
    projector_id = astra.create_projector('linear', proj_geom, vol_geom)
    
    return vol_geom, projector_id, proj_geom
"""
def add_gaussian(tomo, mean=0, std=None): #from tomopy
    
    Add Gaussian noise.

    Parameters
    ----------
    tomo : ndarray
        3D tomographic data.
    mean : float, optional
        Mean of the Gaussian distribution.
    std : float, optional
        Standard deviation of the Gaussian distribution.

    Returns
    -------
    ndarray
        3D tomographic data after Gaussian noise added.
    
    if std is None:
        std = tomo.max() * 100
    dx, dy, dz = tomo.shape
    tomo += std * np.random.randn(dx, dy, dz) + mean
    return tomo
"""
def sinogram(p, r, n, poisson_noise=False, s_and_p_noise = False, gaussian_noise = False, prob=10**-2, val=None, mean =0, std=None):
    # Create geometries and projector
    #adds noise to sinogram too 
    # p is phantom
    # r is range of angles eg pi
    # n is number of angles used
    #prob : float, optional
            #Independent probability that each element of a pixel might be
            #corrupted by the salt and pepper type noise.
    #val : float, optional
           #Value to be assigned to the corrupted pixels.
    
    projector_id = geom_setup(p.shape[0], r, n)[1]
    
    # Create sinogram.
    sinogram = astra.create_sino(p, projector_id)[1]
    #Noise section is 95% copied from tomopy 
    #https://tomopy.readthedocs.io/en/latest/_modules/tomopy/sim/project.html
    
    #if poisson_noise == True:
        #sinogram = np.random.poisson(sinogram)
    
        #return sinogram
    
        #sinogram = np.random.poisson(sinogram * 10000) / 10000
        #sinogram[sinogram > 1.1] = 1.1
        #sinogram /= 1.1

    
    if s_and_p_noise == True:
    
        dx, dy = sinogram.shape
        ind = np.random.rand(dx, dy) < prob
        if val is None:
            val = sinogram.max()
            sinogram[ind] = val
            return sinogram
        else:
            sinogram[ind] = val


    
    if gaussian_noise == True:
        #sinogram = np.ndarray.dtype.as_ndarray(sinogram)       
        
        if std is None:
            std = sinogram.max() * 0.5
        dx, dy = sinogram.shape
        sinogram += std * np.random.randn(dx, dy)  + mean
    return sinogram
        #add_gaussian(sinogram,mean=10**30, std =None)
        


def reconstruct(s, alg, iterations, rnge=np.pi):
    # Create reconstruction.
    # s is the sinogram to reconstruct
    # alg is the algorithm to use (string) eg 'SIRT' or 'FBP'
    # iterations is number of iterations
    # rnge is the range of angles used (if not set the default is pi)...
    # ... r should be >=pi for an accurate reconstruction
    if alg == 'FBP':
        iterations = 1
    vol_geom, projector_id, proj_geom = geom_setup(s.shape[1], rnge, s.shape[0])
    
    # create an astratoolbox id for the projections(sinogram)
    projections_id = astra.data2d.create('-sino', proj_geom, s)
    
    # set up reconstruction
    reconstruction_id = astra.data2d.create('-vol', vol_geom)
    cfg = astra.astra_dict(alg)
    cfg['ReconstructionDataId'] = reconstruction_id
    cfg['ProjectionDataId'] = projections_id 
    cfg['ProjectorId'] = projector_id
    cfg['option'] = {}
    cfg['option']['MinConstraint'] = 0.  # Force solution to be nonnegative.
    algorithm_id = astra.algorithm.create(cfg)
    astra.algorithm.run(algorithm_id, iterations) 
    
    return astra.data2d.get(reconstruction_id)


def full_reconstruct(p):
    # Create geometries and projector.
    vol_geom = astra.create_vol_geom(128, 128)
    angles = np.linspace(0, np.pi, 180, endpoint=False)
    proj_geom = astra.create_proj_geom('parallel', 1., 128, angles)
    projector_id = astra.create_projector('linear', proj_geom, vol_geom)
     
    # Create sinogram.
    sinogram_id, sinogram = astra.create_sino(p, projector_id)
     
    # Create reconstruction.
    reconstruction_id = astra.data2d.create('-vol', vol_geom)
    cfg = astra.astra_dict('FBP')
    cfg['ReconstructionDataId'] = reconstruction_id
    cfg['ProjectionDataId'] = sinogram_id
    cfg['ProjectorId'] = projector_id
    cfg['option'] = {}
    cfg['option']['MinConstraint'] = 0.  # Force solution to be nonnegative.
    algorithm_id = astra.algorithm.create(cfg)
    astra.algorithm.run(algorithm_id, 100)  # 100 iterations.
    reconstruction = astra.data2d.get(reconstruction_id)
    return reconstruction
    
    # Cleanup.
    astra.algorithm.delete(algorithm_id)
    astra.data2d.delete(reconstruction_id)
    astra.data2d.delete(sinogram_id)
    astra.projector.delete(projector_id)


