# Functions for processing the county level GOES LST data
import numpy as np 
import pandas as pd

"""
Load county daily goes lst for one year
df = load_goes_lst_county_year(year, lst_type='max', freq='1d')
"""
def load_goes_lst_county_year(year, lst_type='max', freq='1d'):
    fn_path = '../data/county_level_lst/'
    fn = 'goes_lst_%s_daily_%d_county.csv'%(lst_type,year)
    df = pd.read_csv(fn_path + fn, index_col=[0], parse_dates=[0])
    if freq!='1d':
        return df.resample(freq).mean()
    else:
        return df


""" 
Load county goes lst data for several years
df = load_goes_lst_county_year_range(start_year, end_year, lst_type='max', freq='1d')
"""    
def load_goes_lst_county_year_range(start_year, end_year, lst_type='max', freq='1d'):
    df = [load_goes_lst_county_year(i,freq=freq) for i in range(start_year,end_year+1)]
    df_all = pd.concat(df)
    return df_all.dropna(axis='columns', how='all')

"""
Save the growing season montly goes lst to a csv file in crop model data format
df = save_goes_lst_gs_to_csv()
"""
def save_goes_lst_gs_to_csv():
    # load processed daily county level data
    lst_mon = load_goes_lst_county_year_range(2010, 2014, lst_type='max', freq='M')

    # Select growing season
    lst_gs = lst_mon[(lst_mon.index.month>4)&(lst_mon.index.month<10)]

    # make some rearrangement of the data layout 
    lst_gs_1 = lst_gs.stack().to_frame('lst').reset_index()
    lst_gs_1.rename(columns={'level_1':'FIPS'}, inplace=True)

    # Add year and month as column
    lst_gs_1['year'] = lst_gs_1['level_0'].apply(lambda x: x.year)
    lst_gs_1['mon'] = lst_gs_1['level_0'].apply(lambda x: x.month)

    # Seperate monthly lst as column by mutle-index and pivot
    lst_gs_2 = lst_gs_1.iloc[:,1::].set_index(['year','FIPS']).pivot(columns='mon')

    # drop multi-index of columns
    lst_gs_2.columns = lst_gs_2.columns.droplevel(0)

    # rename lst column
    lst_gs_2 = lst_gs_2.reset_index().rename(columns={5:'maxlst5',6:'maxlst6',7:'maxlst7',8:'maxlst8',9:'maxlst9'})
    
    lst_gs_2.to_csv('../data/county_level_lst/goes_lst_max_month_5_9_2010_2014_county.csv')
    print('goes_lst_max_month_5_9_2010_2014_county.csv saved')
    return lst_gs_2


if __name__ == '__main__':
    save_goes_lst_gs_to_csv()
