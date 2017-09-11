"""
Download GOES LST, using the id 
download_GOES_LST(id, year=2009, source='GENHEM')
Need to order data first
"""
import ftplib
import os

def download_GOES_LST(id, year=2009, source='GENHEM'):
   # id = '2584218284'
    print('download for Year=%d, source=%s'%(year, source))
    os.chdir('data/' + source)
    currdir=os.getcwd()
    
    # Create year folder
    if not os.path.exists(str(year)):
        os.makedirs(str(year))
    os.chdir(str(year))

    ftp = ftplib.FTP('ftp.class.ngdc.noaa.gov') 
    ftp.login()

    ftp.cwd(id + '/001')

    fn_list = ftp.nlst()
    fn_list.sort()

    for fn in fn_list:
        print(fn)
        ftp.retrbinary("RETR " + fn, open(fn, 'wb').write)

    print('Download task complete, close FTP connection')
    ftp.quit()  
    os.chdir('../../../')
