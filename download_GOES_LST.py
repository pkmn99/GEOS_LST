"""
Download GOES LST, using the id 
download_GOES_LST(id, year=2009, source='GENHEM')
Need to order data first
"""
import ftplib
import os

def download_GOES_LST(id, year=2009, source='GENHEM',test=False):
    print('download for Year=%d, source=%s'%(year, source))
    os.chdir('data/' + source)
    currdir=os.getcwd()
    
    # Create year folder
    if not os.path.exists(str(year)):
        os.makedirs(str(year))
    os.chdir(str(year))
    try:
        ftp = ftplib.FTP('ftp.class.ngdc.noaa.gov') 
        ftp.login()

        ftp.cwd(id + '/001')
        print('enter OK')
        if not test:
            fn_list = ftp.nlst()
            fn_list.sort()

            for fn in fn_list:
                print(fn)
                ftp.retrbinary("RETR " + fn, open(fn, 'wb').write)

            print('Download task complete, close FTP connection')
        ftp.quit()  
    except:
        print ('%s Error'%id)
    os.chdir('../../../')

import urllib2
import shutil
import pandas as pd 
def get_file(url):
    req = urllib2.urlopen(url)
    file = s.split('/')[-1]
    with open(file, 'wb') as fp:
        shutil.copyfileobj(req, fp)

def get_file_urllib2(id, year=2009, source='GENHEM')
    ftp_name = 'ftp://ftp.class.ncdc.noaa.gov/'
   # id = '2585819234'
    fn = pd.read_csv(id + '.txt', sep=' ', header=None)

    if not os.path.exists(str(year)):
        os.makedirs(str(year))
    os.chdir(str(year))
    
    for i in range(fn.shape[0]):
        s = ftp_name + id + fn[1][i]
        print('dowloading %s'%s)
        get_file(s)
