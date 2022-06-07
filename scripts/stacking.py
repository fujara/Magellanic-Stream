import pandas as pd
import numpy as np
from astropy.io import fits
import seaborn as sns
import astropy.units as u
import astropy.constants as c
import sys
from astropy.io import ascii
from astropy.table import Table
import os





def maketable(dir): #creates an ASCI table containing file_names, filter, tile, dither, zp, FWHM, MJD-OBS, EXPTIME, NCHIP
    file_names = os.listdir(dir) #creates list with file names
    RA = [] #RA in primary
    DEC = [] #DEC in primary
    MJD = [] #MJD-OBS in primary
    FWHM_start = [] #ESO TEL AMBI FWHM START in primary
    FWHM_end = [] #ESO TEL AMBI FWHM END in primary
    AG_FWHM =[] #ESO TEL GUID FWHM in primary
    EXPTIME = []# EXPTIME in primary
    NCHIP = [] # ESO DET CHIP NO in primary
    GAIN = [] #GAINCOR in secondary
    DIT = [] #HIERARCH ESO DET DIT dither om primary



    #read files and extract header information
    for file in file_names:
        with fits.open(f'{dir}/{file}') as hdul:  # open a FITS file
            hdr_p = hdul[0].header
            hdr_s = hdul[1].header
            #append cuerrent file info to lists
            RA.append(hdr_p['RA'])
            DEC.append(hdr_p['DEC'])
            MJD.append(hdr_p['MJD-OBS'])
            FWHM_start.append(hdr_p['ESO TEL AMBI FWHM START'])
            FWHM_end.append(hdr_p['ESO TEL AMBI FWHM END'])
            AG_FWHM.append(hdr_p['ESO TEL GUID FWHM'])
            EXPTIME.append(hdr_p['EXPTIME'])
            NCHIP.append(hdr_s['ESO DET CHIP NO'])
            GAIN.append(hdr_s['GAINCOR'])
            DIT.append(hdr_p['HIERARCH ESO DET DIT'])

    #add lists to dataframe
    dat = np.array([file_names, RA, DEC, MJD, FWHM_start, FWHM_end, AG_FWHM, EXPTIME, NCHIP, GAIN, DIT])
    col = ['file_names', 'RA', 'DEC', 'MJD', 'FWHM_start', 'FWHM_end', 'AG_FWHM', 'EXPTIME', 'NCHIP', 'GAIN', 'DIT']
    df = pd.DataFrame(columns=  col, data = dat.transpose() )
    t2 = Table.from_pandas(df)
    ascii.write(t2, 'table.dat', overwrite=True)


def test(dir): #given a dir it will just create an ascii table with the file_names
    
    file_names = os.listdir(dir) #creates list with file names
    df = pd.DataFrame( )
    df['file_names'] = file_names
    t2 = Table.from_pandas(df)
    tab_dir = '/home/mcavieres/MS/Magellanic-Stream/tables'
    ascii.write(t2, f'{tab_dir}/table_test.dat', overwrite=True)

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])

