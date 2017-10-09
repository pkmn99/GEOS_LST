import xarray as xr

from __future__ import division
def compute_scale_and_offset(min, max, n):
    # stretch/compress data to the available packed range
    scale_factor = (max - min) / (2 ** n - 2) # reserve for missing value
    # translate the range to be symmetric about zero
    add_offset = min + 2 ** (n - 1) * scale_factor
    return (scale_factor, add_offset)


# fn = 'test_data/LST_2014192_1215.dat'
def load_hourly_goes_lst_dat(fn):
    dir_txt = 'data/GOES_LST_Hain/data/' + str(year) + '/'
    head_txt = 'LST_'

    fn = dir_txt + head_txt + str(year)+ '%03d'%day + '_%02d'%h + '15.dat'

    myarray = np.fromfile(fn, dtype=np.float32)
    myarray = np.flipud(myarray.reshape(1515,1775))

    # Convert array to int16
    myarray[myarray==-9999]=nan
    myarray = floor((myarray - add_offset) / scale_factor)
    myarray[np.isnan(myarray)] = (2**16)/2 - 1
    return myarray

def save_to_netcdf_monthly(year, month):
    # Create a dataframe to save time index
    date = pd.date_range(start='2009/04/01/00:45',end='20170101', freq='h')
    df_time=pd.DataFrame(range(len(date)),index=date)
    time_month = df_time['%d/%02d'%(year,month)]

    lst_array = np.zeros([time_month.shape[0],len(lat),len(lon)], dtype=np.int16) + np.int16((2**16)/2 - 1)
    
    for i,t in enumerate(time_month.index):
        print('processing %s'%t)
        try:
            lst_array[i,:,:] = load_hourly_goes_lst_dat(t.year, t.dayofyear, h=t.hour)

    foo = xr.DataArray(lst_array, coords=[time_month.index, lat, lon], dims=['time','latitude','longitude'], 
                       attrs=attrs, name='lst')
    foo.sel(latitude=slice(50,20),longitude=slice(-125,-70)). \
        to_netcdf('result/LST_%d_%02d.nc'%(year,month))
    print('Netcdf file LST_%d_%02d.nc saved'%(year,month))

if __name__ == "__main__":
    attrs = {'scale_factor': scale_factor, 'add_offset':add_offset, '_FillValue' : int16((2**16)/2 - 1), 
             'long_name': "Mean surface temperature"}    

    # Get scale_factor and add_offset
    scale_factor, add_offset = compute_scale_and_offset(240, 340, 16)

    year = 2014
    save_to_netcdf_monthly(year, 1)