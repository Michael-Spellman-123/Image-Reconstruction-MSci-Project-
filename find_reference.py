# -*- coding: utf-8 -*-


from PIL import Image
import numpy as np
import os
import glob
import graphs
from shutil import copyfile
import downsampling

#boo = np.array(Image.open('003604.tif'))
max_amp = [] 
new_images = []
#directory = r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\17-2-20_argon\10-2-20-100bar-narrow-1st-shot'
#directory = r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\27-2-20\density_of_one_shot_ref_files'
#directory = r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\6-3-20_2.3mm_off_axis\6-3-20-100bar-1st-half-shot-2nd-half-refs'

target_image = '000121.tif'


def open_images(directory):
    """
    Returns a list of np.arrays of all the .tif files in the specified directory
    and a list of the file names
    
    directory(string) =  location of folder containing references & target image 
    
    For example:
    images, names = open_images(directory)
    
    """
    return ([np.array(Image.open(f), dtype = np.int32) for f in 
            glob.glob(directory + '*' + '/*.tif')], 
            [n.replace(directory, "") for n in 
             glob.glob(directory + '*' + '/*.tif')])




def best_reference(directory, target_image):
    """
    directory(string) =  location of folder containing references & target image
    
    target_image(string) = name of .tif file of the target image
    """
    target = np.array(Image.open(glob.glob(directory + "*" + 
                                           '/*' + target_image)[0]), 
                                                            dtype = np.int32)
    images, names = open_images(directory)
    
    # remove target file from list of reference images:
    c = 0 
    for name in names:
        if name == "\\" + target_image:
            del images[c]
            del names[c]
            break
        c += 1
    
    # find reference that is closest match to target on the edges:
    c = 0

    lowest_diff = 10E99    
 
    for image in images:
        lhdiff = np.absolute((target[0:1500,:200] - image[0:1500,:200]))
        rhdiff = np.absolute((target[0:1500,-200:] - image[0:1500,-200:]))
        mean_diff = np.mean(lhdiff) + np.mean(rhdiff)
        if mean_diff < lowest_diff:
            lowest_diff = mean_diff
            best_ref = names[c]
        c += 1

        
    return best_ref


def batch_best_reference(reference_location, target_image_location,
                         make_folders = True, downsample = True):

    targets, target_names = open_images(target_image_location)
    refs, ref_names = open_images(reference_location)
    # find reference that is closest match to target on the edges:
    d=0
    for target in targets:
        c = 0
        lowest_diff = 10E99        
        for ref in refs:
            
            lhdiff = np.absolute((target[0:1500,:200] - ref[0:1500,:200]))
            rhdiff = np.absolute((target[0:1500,-200:] - ref[0:1500,-200:]))

            #lhdiff = np.absolute((target[0:188,:25] - ref[0:188,:25]))
            #rhdiff = np.absolute((target[0:188,-25:] - ref[0:188,-25:]))           
            

            mean_diff = np.mean(lhdiff) + np.mean(rhdiff)
            if mean_diff < lowest_diff:
                lowest_diff = mean_diff
                best_ref = ref_names[c]
          
            c += 1
        
        if make_folders:
            targ_n_ref_fol = target_image_location + str(target_names[d]) + '_w_ref'
            os.makedirs(targ_n_ref_fol)
            copyfile(target_image_location + '\\' + target_names[d],targ_n_ref_fol + str(target_names[d]))
            copyfile(reference_location + '\\' + best_ref, targ_n_ref_fol + best_ref)
         
        print('for', target_names[d], 'use', best_ref,'as reference')
        if downsample:
                downsampling.downsample(targ_n_ref_fol,8)
        print('for', target_names[d], 'use', best_ref,'as reference')
        d += 1
        
#batch_best_reference(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\Data_17_2\References-narrow_half',r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\Data_17_2\Targets-narrow')

#folder = "29-1-20"
#directory = os.getcwd() + "\\" + folder
# or can set directory outside of spyder project:
#directory = r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\Data_17_2\003662'
#fringe_visibility.delete_fuzzy_images
#best = batch_best_reference(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\6-3-20\30 angles\2.3mm_100bar\ref', r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\6-3-20\30 angles\2.3mm_100bar\shots')
batch_best_reference(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\17-3-20-2-no_mount_gas_jet_refs', r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\17-3-20-2-no_mount_gas_jet')

#batch_best_reference(r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\11-3-20\11-3-20-REF_files', r'C:\my stuff\Imperial\4th Year\MSci Project\Interpret\11-3-20\180_2ndhalf')

#batch_best_reference(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\6-3-20\refs', r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\6-3-20\1.3mm_targs\downsampled_files')

#best_reference(directory, target_image)


##############################################################################
##############################################################################

            #if downsample:
            #    downsampling.downsample(targ_n_ref_fol,8)
        #print('for', target_names[d], 'use', best_ref,'as reference')
        #d += 1
    
#batch_best_reference(r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\11-3-20\11-3-20-REF_files', r'C:\Users\Elliot Prestidge\Documents\4TH YEAR\Project\Data\11-3-20\1sthalf')













