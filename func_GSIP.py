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

# Check spatial boundary from all L3 data files
def check_data_boundary():
    # Save the unique boundary pattern of the GSIP data
    date = pd.date_range(start='2009/04/01/00:45',end='20170101', freq='h')
    df = pd.DataFrame(np.zeros([date.shape[0],5]), index=date,
                      columns=['west_lon','east_lon','north_lat','south_lat','n'])
    
    for i in range(df.shape[0]):
        ds = load_hourly_data_for_day(df.index[i].year, df.index[i].dayofyear, h=df.index[i].hour)
        if ds:
            df.iloc[i,:] = ds.west_lon.values,ds.east_lon.values,ds.north_lat.values, \
                           ds.south_lat.values, ds.dims['nlon_grid']
    
    df.to_csv('result/gsip_boundary.csv')
    
