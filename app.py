import os, time
import wget
import csv
from stat import * # ST_SIZE etc

file_url  = 'http://datosabiertos.miraflores.gob.pe/rest/datastreams/220665/data.csv'
file_name = wget.download(file_url)

try:
    st = os.stat(file_name)
except IOError:
    print "failed to get information about", file_name
else:
    print "file size:", st[ST_SIZE]
    print "file modified:", time.asctime(time.localtime(st[ST_MTIME]))

with open('veterinarias.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['CODIGO'], row['NOMBRE-O-RAZON-SOCIAL'], row['NOMBRE-DE-VIA'], row['NRO'], row['LETRA'], row['INTERIOR'], row['GIRO'], row['NOMBRE-COMERCIAL'], row['FEC-INICIO'])
