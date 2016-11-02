#!/usr/bin/python
import os, time
import wget
import csv
import MySQLdb
from stat import * # ST_SIZE etc
from datetime import datetime

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
    d = datetime.strptime(time.asctime(time.localtime(st[ST_MTIME])), '%a  %b  %d %H:%M:%S %Y')
    day_string = d.strftime('%d/%m/%Y')
    print "file name: ", file_name
    print "file size: ", st[ST_SIZE]
    print "file modified: ", day_string

existe = False

sqlBuscarPorFecha = "select * from archivo \
                     where fecha = '%s'" % (day_string)

try:
   results = cursor.execute(sqlBuscarPorFecha)
   if results > 0:
       existe = True
   db.commit()
except:
   db.rollback()

if existe is False:
    sqlArchivo = "insert into archivo(nombre, tamanio, fecha) \
              values ('%s', '%s', '%s')" % \
              (file_name, str(st[ST_SIZE]), day_string)

    try:
       cursor.execute(sqlArchivo)
       db.commit()
    except:
       db.rollback()

sqlLastID = "SELECT LAST_INSERT_ID()"

try:
   lastID = cursor.execute(sqlLastID)
   print "last id  ", lastID
   db.commit()
except:
   db.rollback()

if existe is False:
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['CODIGO'], row['NOMBRE-O-RAZON-SOCIAL'], row['NOMBRE-DE-VIA'], row['NRO'], row['LETRA'], row['INTERIOR'], row['GIRO'], row['FEC-INICIO'])
            # crear la  sentencia sql
            sqlLocal = "insert into local(CODIGO, NOMBREORAZONSOCIAL, NOMBREDEVIA, NRO, LETRA, INTERIOR, GIRO, FECINICIO, archivo_id) \
                        values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
                        (row['CODIGO'], row['NOMBRE-O-RAZON-SOCIAL'], row['NOMBRE-DE-VIA'], row['NRO'], row['LETRA'], row['INTERIOR'], row['GIRO'], row['FEC-INICIO'], lastID)
            try:
               cursor.execute(sqlLocal)
               db.commit()
            except:
               db.rollback()

# se desconecta con el servidor
db.close()

# retira el archivo original *.csv
if os.path.exists(file_name):
    os.remove(file_name)
