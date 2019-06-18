import numpy as np
import pandas as pd
from affine import Affine

"""
Save US lat/lon boundary and the corresponding row and col number
to a csv file, which can be used for other functions 
"""
def US_boundary_table(type):
    res = 0.125
    if type=='US':
        lat_north = 50
        lat_south = 20
        lon_west = -125
        lon_east = -70

    if type=='global':
        lat_north = 90
        lat_south = -90
        lon_west = -180
        lon_east = 180

    if type=='GENHEM':
        lat_north = 60
        lat_south = -30
        lon_west = -140
        lon_east = -30
    
    lat = np.arange(lat_north-res/2, lat_south-res/2, -res)
    lon = np.arange(lon_west+res/2, lon_east + res/2, res)
    
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
#    df.to_csv('result/US_row_col_0125deg.csv')
    df.to_csv('../result/%s_row_col_0125deg.csv'%type)
    print('File saved as result/%s_row_col_0125deg'%type)

if __name__=="__main__":
    US_boundary_table('GENHEM')
