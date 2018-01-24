# zonal statistics to covert goes LST data to US county mean 
import numpy as np
import pandas as pd
import xarray as xr
from rasterstats import zonal_stats
import rasterio
import cartopy.io.shapereader as shpreader

global source_dir, save_dir
source_dir = '../data/hains_lst/processed_lst/'
save_dir = '../data/hains_lst/county_level_lst/'

# Get affine from one data file
def get_affine():
    dataset = rasterio.open('%s/LST_2014_04.nc'%source_dir, driver='netcdf')
    return dataset.transform

"""
Aggregate hourly data to daily, by year and month 
Usage: df = zonal_county_value(year, mon, lst_type='max')
lst_type is the aggregation method of the lst data
"""
def zonal_county_value(year, mon, lst_type='max'):
    affine = get_affine()
    ds = xr.open_dataset('%s/LST_%d_%02d.nc'%(source_dir, year, mon))
    ds_daily = ds.resample(freq='D', dim='time', how=lst_type)

    # Load shapefile and construct pandas frame 
    shape_fn = '../../data/US_county_gis/counties.shp'
    shapes = shpreader.Reader(shape_fn)
    county_fips = [i.attributes['FIPS'] for i in shapes.records()]
    if mon <12:
        time_range = pd.period_range(start='%d-%02d'%(year, mon),
                     end='%d-%02d'%(year, mon+1), freq='D')[:-1]
    else:
        time_range = pd.period_range(start='%d-%02d'%(year, mon),
                     end='%d-%02d'%(year+1, 1), freq='D')[:-1]

    df = pd.DataFrame(np.zeros([len(time_range), len(county_fips)]).fill(np.nan),
                      index=time_range, columns=county_fips)

    # zonal statistics for each day 
    for i, t in enumerate(time_range):
        
        print(t)
        zs = zonal_stats(shape_fn, ds_daily.lst[i].values, affine=affine)
    
        # save zonal results
        df.loc[t]=[i['mean'] for i in zs]
       # # Save to csv at the end of each year
       # if (t.dayofyear == 365) | (t.dayofyear == 366):
       #     print('save file at the end of year %s'%t.strftime('%Y'))
#        df[t.strftime('%Y')].to_csv('./result/goes_lst_%s_daily_%d%02d_county.csv'%(lst_type,year,mon))
    return df

def main():
    lst_type = 'max'
    for year in range(2010, 2015):
#    year = 2014
#    mon = 4
        frame = [zonal_county_value(year, mon, lst_type=lst_type) for mon in range(1,13)]
        df = pd.concat(frame)
        df.to_csv('%sgoes_lst_%s_daily_%d_county.csv'%(save_dir, lst_type, year))
        print('county level daily %s lst for %d saved'%(lst_type, year))

if __name__ == '__main__':
    main()
