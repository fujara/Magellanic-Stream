import pandas as pd
import numpy as np
from astropy.io import fits
import os
import matplotlib.pyplot as plt
from skimage import data, img_as_float
from skimage import exposure
from astropy import wcs
import warnings
from astropy.coordinates import angular_separation
import seaborn as sns
import itertools
import astropy.units as u
import astropy.constants as c
import tqdm
from reproject.mosaicking import find_optimal_celestial_wcs
from reproject import reproject_interp
from reproject.mosaicking import reproject_and_coadd 
import warnings
warnings.filterwarnings("ignore")

directory = '/Users/mncavieres/Documents/2022-1/Investigacion/Test Data'
files = os.listdir(directory)
tile = [obs for obs in files if 'v20180602' in  obs]
tile_dir = ['/Users/mncavieres/Documents/2022-1/Investigacion/Test Data/'+t for t in tile]

for obs in tqdm.tqdm(tile):
    print(f'working on: {obs}')
    with fits.open(f'/Users/mncavieres/Documents/2022-1/Investigacion/Test Data/{obs}' ) as f2: #open fits
        wcs_out, shape_out = find_optimal_celestial_wcs(f2[1:18]) #get wcs object for mosaic
        array, footprint = reproject_and_coadd(f2[1:18], wcs_out, shape_out=shape_out, reproject_function=reproject_interp) #reproject and co add chips to build the mosaic
        hdu_new = fits.PrimaryHDU(array, header = wcs_out)
        hdu.writeto(f'{obs}_mosaic.fits')
        #p2, p98 = np.percentile(array, (2, 98))
        #img_rescale = exposure.rescale_intensity(array, in_range=(p2, p98))


        #fig = plt.figure(figsize=(10,10))
        #ax = fig.add_subplot( projection=wcs_out)
        #ax.imshow(array, cmap= 'gray')
        #ax.set_ylabel('dec')
        #ax.set_xlabel('ra')


        #plt.savefig(f'/Users/mncavieres/Documents/2022-1/Investigacion/plots/mosaics/mosaic_{obs}.png', dpi = 1000, bbox_inches = 'tight')
