from download_GOES_LST import download_GOES_LST, get_file_urllib2


#id = ['2584679704', 
#      '2584679714', '2584679724', '2584679734', '2584681064',
#      '2584681144', '2584681154', '2584681164']

#id = ['2585806374', '2585807544', '2585807554', '2585807564',
#     '2585807574', '2585807884', '2585807894', '2585807904',
#     '2585807914', '2585808024', '2585808484', '2585808494',
#     '2585808504', '2585808514', '2585808554', '2585810574',
#     '2585814614', '2585819234']

#id  = ['2587449984', '2587449574', '2587449584', '2587450364',
#       '2587449994', '2587450394', '2587454224', '2587454234']

#       '2587449594', '2587449604', '2587449714', '2587450004',
#       '2587447174', '2587454244', '2587450284', '2587450404',
#       '2587450904', '2587454214']

year = 2017
id  = ['2600213704','2600213714','2600213724','2600213734',
       '2600214574','2600214594','2600214614','2600214624',
       '2600214634','2600214644','2600214794','2600214804',
       '2600214814']
       

for n, i in enumerate(id):
    print('Task %d of %s'%(n,i))
    download_GOES_LST(i, year=year, test=False)


#for n, i in enumerate(id):
#    print('Task %d of %s'%(n,i))
#    get_file_urllib2(i, year=year, source='GENHEM')
