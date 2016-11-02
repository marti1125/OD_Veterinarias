#!/usr/bin/python
import os, time
import wget
import csv
import MySQLdb
from stat import * # ST_SIZE etc

file_url  = 'http://datosabiertos.miraflores.gob.pe/rest/datastreams/220665/data.csv'
file_name = wget.download(file_url)

# Se abre la conexion a la base de datos
db = MySQLdb.connect("localhost","root","","veterinaria")

# prepara el objeto cursor()
cursor = db.cursor()

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
        print(row['CODIGO'], row['NOMBRE-O-RAZON-SOCIAL'], row['NOMBRE-DE-VIA'], row['NRO'], row['LETRA'], row['INTERIOR'], row['GIRO'], row['FEC-INICIO'])
        # crear la  sentencia sql
        sql = "insert into local(CODIGO, NOMBREORAZONSOCIAL, NOMBREDEVIA, NRO, LETRA, INTERIOR, GIRO, FECINICIO) \
               values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
               (row['CODIGO'], row['NOMBRE-O-RAZON-SOCIAL'], row['NOMBRE-DE-VIA'], row['NRO'], row['LETRA'], row['INTERIOR'], row['GIRO'], row['FEC-INICIO'])
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()

# se desconecta con el servidor
db.close()

# retira el archivo original *.csv
if os.path.exists('veterinarias.csv'):
    os.remove('veterinarias.csv')
