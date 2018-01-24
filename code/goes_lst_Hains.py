from __future__ import division
import os.path
import numpy as np
import pandas as pd
import xarray as xr


def compute_scale_and_offset(min, max, n):
    # stretch/compress data to the available packed range
    scale_factor = (max - min) / (2 ** n - 2) # reserve for missing value
    # translate the range to be symmetric about zero
    add_offset = min + 2 ** (n - 1) * scale_factor
    return (scale_factor, add_offset)

def set_global_parameter():
    global save_dir_txt, res, lat, lon, attrs, scale_factor, add_offset
    save_dir_txt = '../data/hains_lst/processed_lst/'
    res = 0.04
    lat = np.arange(0.04*1515 - res/2, -0.02, -res)
    lon = np.arange(-120+res/2, -120+0.04*1775 + res/2, res)
    
    # Get scale_factor and add_offset
    scale_factor, add_offset = compute_scale_and_offset(240, 340, 16)
    
    attrs = {'scale_factor': scale_factor, 'add_offset':add_offset, '_FillValue': np.int16((2**16)/2 - 1), 
             'long_name': "Mean surface temperature"}    

# fn = 'test_data/LST_2014192_1215.dat'
def load_hourly_goes_lst_dat(year,day,h=0):
    dir_txt = '../data/hains_lst/' + str(year) + '/'
    head_txt = 'LST_'

    fn = dir_txt + head_txt + str(year)+ '%03d'%day + '_%02d'%h + '15.dat'

    if os.path.isfile(fn):
        myarray = np.fromfile(fn, dtype=np.float32)
        myarray = np.flipud(myarray.reshape(1515,1775))

        # Convert array to int16
        myarray[myarray==-9999]=np.nan
        myarray = np.floor((myarray - add_offset) / scale_factor)
        myarray[np.isnan(myarray)] = (2**16)/2 - 1
    else:
        print('%s is missing'%fn)
        myarray = np.array([False, False]) 
    return myarray

def save_to_netcdf_monthly(year, month):
    # Create a dataframe to save time index
    date = pd.date_range(start='2009/04/01/00:15',end='20170101', freq='h')
    df_time=pd.DataFrame(range(len(date)),index=date)
    time_month = df_time['%d/%02d'%(year,month)]

    lst_array = np.zeros([time_month.shape[0],len(lat),len(lon)], dtype=np.int16) + np.int16((2**16)/2 - 1)
    
    for i,t in enumerate(time_month.index):
        print('processing %s'%t)
        
        d = load_hourly_goes_lst_dat(t.year, t.dayofyear, h=t.hour)
        if d.any():
            lst_array[i,:,:] = d

    foo = xr.DataArray(lst_array, coords=[time_month.index, lat, lon],
                       dims=['time','latitude','longitude'],
                       attrs=attrs, name='lst')

    foo.sel(latitude=slice(50,20),longitude=slice(-125,-70)). \
        to_netcdf('%s/LST_%d_%02d.nc'%(save_dir_txt,year,month))
    print('Netcdf file LST_%d_%02d.nc saved'%(year,month))

def task_save_monthly_mean(year=2014):
    for m in range(1, 13):
        ds = xr.open_dataset('%s/LST_%d_%02d.nc'%(save_dir_txt, year, m))
        ds.lst.mean(dim='time').to_netcdf('%s/LST_%d_%02d_mean.nc'%(save_dir_txt,year,m))
        print('LST_%d_%02d_mean.nc saved'%(year,m))


def main():
    year = 2014
#    t = load_hourly_goes_lst_dat(year,1,h=7)
    for m in range(1,13):
        save_to_netcdf_monthly(year, m)

if __name__ == "__main__":
    set_global_parameter()
    main()
#    task_save_monthly(year=2010)
#    task_save_monthly_mean()
