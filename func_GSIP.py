import numpy as np
import pandas as pd
import xarray as xr


"""
Load hourly raw GSIP data
"""
def load_hourly_data_for_day(year, day, h=0, head_txt='gsipL3_g13_GENHEM_'):
    dir_txt = 'data/GENHEM/' + str(year) + '/'
#     dir_txt = 'test_data/'
    fn = dir_txt + head_txt + str(year)+ '%03d'%day + '_%02d'%h + '45.nc'
    try:
        ds = xr.open_dataset(fn)
        return ds
    except:
        print('%s is missing'%fn)
        return False
