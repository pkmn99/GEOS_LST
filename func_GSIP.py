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

# Define US lat/lon boundary
def US_latlon_boundary():
    lat_north = 50
    lat_south = 20
    lon_west = -125
    lon_east = -70
    res = 0.125
    lat = np.arange(lat_north-res/2, lat_south-res/2-0.001, -res)
    lon = np.arange(lon_west+res/2, lon_east + res/2+0.001, res)
    return lat, lon

"""
Convert the GSIP LST data to 2d map
array = convert_to_map(ds)
""" 
def convert_to_map(ds):
    c = (ds['lon_cell']>=lon[0]) & (ds['lon_cell']<=lon[-1]) \
        &(ds['lat_cell']>=lat[-1]) & (ds['lat_cell']<=lat[0])
    
    # Make a dataframe to save points within the US lat/lon boundary
    df_data = pd.DataFrame({'lat': ds['lat_cell'].values[c.values],
                            'lon': ds['lon_cell'].values[c.values],
                            'lst': ds['lst'].values[c.values]
                             })
    # Link it with the references US data frame
    df_data = df_data.merge(US_table, on=['lat','lon'])
        
    map_array = np.zeros([len(lat), len(lon)],dtype=np.int8).flatten() + np.int8(-128)
    map_array[df_data['ind_1d'].values] = df_data['lst'].values
    
    return map_array.reshape(len(lat), len(lon))    

"""
Save GSIP hourly data to netcdf, one month for one file 
Usage: save_to_netcdf_monthly(year, month)
"""
def save_to_netcdf_monthly(year, month):
    # Create a dataframe to save time index
    date = pd.date_range(start='2009/04/01/00:45',end='20170101', freq='h')
    df_time=pd.DataFrame(range(len(date)),index=date)
    time_month = df_time['%d/%02d'%(year,month)]
    lst_array = np.zeros([time_month.shape[0],len(lat),len(lon)], dtype=np.int8) + np.int8(-128)
    
    for i,t in enumerate(time_month.index):
        print('processing %s'%t)
        ds = load_hourly_data_for_day(t.year, t.dayofyear, h=t.hour, head_txt='gsipL3_g13_GENHEM_')
        if ds:
            lst_array[i,:,:] = convert_to_map(ds)
    # Load a sample data to get attribute 
    ds_sample = load_hourly_data_for_day(2012, 1, h=0, head_txt='gsipL3_g13_GENHEM_')

    foo = xr.DataArray(lst_array, coords=[time_month.index, lat, lon], dims=['time','latitude','longitude'], 
                       attrs=ds_sample.lst.attrs, name='lst')
    foo.to_netcdf('result/gsipL3_g13_GENHEM_%d_%02d.nc'%(year,month))
    print('Netcdf file gsipL3_g13_GENHEM_%d_%02d.nc saved'%(year,month))

if __name__ == '__main__':
    lat, lon = US_latlon_boundary()
    US_table = pd.read_csv('result/US_row_col_0125deg.csv')
    year = 2012
    for month in range(9, 13):
        save_to_netcdf_monthly(year, month)
