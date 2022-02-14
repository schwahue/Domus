from ctypes import addressof
from app import app
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb
 
app = Flask(__name__)
         
app.config['SECRET_KEY'] = 'super secret key'

app.config['MYSQL_HOST'] = 'ecp-db-instance.cnsgbbbzr71l.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin1234'
app.config['MYSQL_DB'] = 'ECP_DB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app) 
 
@app.route('/')
def index(): 
    return render_template('index.html')
 
@app.route("/fetchrecords",methods=["POST","GET"])
def fetchrecords():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        query = request.form['action']
        minimum_price = request.form['minimum_price']
        maximum_price = request.form['maximum_price']
        property_type = request.form['property_type']
        district = request.form['district']
        bedroom = request.form['bedroom']

        #print(query)
        if query == '':
            cur.execute("SELECT * FROM listing ORDER BY id ASC")
            propertylist = cur.fetchall()
            print('all list')

        elif query == 'property_type':
            cur.execute("SELECT * FROM ECP_DB.listing WHERE property_type = '(%s)';", property_type)
            propertylist = cur.fetchall()
            print('Property type list')

        elif query == 'district':
            cur.execute("SELECT * FROM ECP_DB.listing WHERE district = '(%s)';", district)
            propertylist = cur.fetchall()
            print('District list')

        elif query == 'bedroom':
            cur.execute("SELECT * FROM ECP_DB.listing WHERE bedroom = '(%s)';", bedroom)
            propertylist = cur.fetchall()
            print('Bedroom list')

        else:
            cur.execute("SELECT * FROM listing WHERE price BETWEEN (%s) AND (%s)", [minimum_price, maximum_price])
            propertylist = cur.fetchall()  
    return jsonify({'htmlresponse': render_template('response.html', propertylist=propertylist)})

if __name__ == '__main__':
    app.run(debug=True)
 
