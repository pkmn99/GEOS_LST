import xarray as xr
from affine import Affine

fn = 'gsipL3_g13_GENHEM_2012359_1245.nc'
ds = xr.open_dataset(fn)


a = Affine(0.125,0,-132.0625,0,-0.125,59.9375)
# get col and row number
ds['col'], ds['row'] = ~a * (ds['lon_cell'], ds['lat_cell'])
# need to floor to get integer col and row
ds[['row','col']].to_netcdf('row_col.nc')
print('row and col saved to file')
