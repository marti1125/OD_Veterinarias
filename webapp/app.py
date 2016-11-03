from flask import Flask
from flask import jsonify
from flask import render_template
import MySQLdb
import collections
app = Flask(__name__)

class MyClass(object):
    def __init__(self, number, d):
        self.number = number
        self.d = d


@app.route("/locales")
def local():
    db = MySQLdb.connect("localhost","root","","veterinaria")
    cursor = db.cursor()
    sqlBuscarPorFecha = "select * from local"

    rows = []

    try:
       cursor.execute(sqlBuscarPorFecha)
       results = cursor.fetchall()
       for row in results:
           d = collections.OrderedDict()
           d['id'] = row[0]
           d['codigo'] = row[1]
           d['razonsocial'] = row[2]
           d['direccion'] = row[3] + " " + row[4]
           d['giro'] = row[7]
           d['latitud'] = row[10]
           d['longitud'] = row[11]
           rows.append(d)
       db.commit()
    except:
       db.rollback()

    return jsonify(rows)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
