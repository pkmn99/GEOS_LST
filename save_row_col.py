import numpy as np
import pandas as pd
from affine import Affine

#def US_boundary_table():
# US lat/lon boundary
lat_north = 50
lat_south = 20
lon_west = -125
lon_east = -70
res = 0.125

lat = np.arange(lat_north-res/2, lat_south-res/2 -0.001, -res)
lon = np.arange(lon_west+res/2, lon_east + res/2 + 0.001, res)

lon_mesh, lat_mesh = np.meshgrid(lon, lat)

a = Affine(0.125,0,lon_west,0,-0.125,lat_north)

# get col and row number
col, row = ~a * (lon_mesh.flatten(), lat_mesh.flatten())

d = {'lat' : lat_mesh.flatten(),
     'lon' : lon_mesh.flatten(),
     'row' : np.int16(row),
     'col' : np.int16(col),
     'ind_1d': np.arange(len(row))}

df = pd.DataFrame(d, columns=['lat','lon','row','col','ind_1d'])
df.to_csv('result/US_row_col_0125deg.csv')
print('File saved as result/US_row_col_0125deg')
