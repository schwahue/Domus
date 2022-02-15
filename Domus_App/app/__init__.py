from flask import Flask, render_template
# Need this with RDS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_dropzone import Dropzone


# Module to retrieve environment variables
import os



# Import helper functions module
from app.helpers import helper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config["SQLACHEMY_DATABASE_URI"] = 'mysql://username:password@localhost/db_name'

# Might change to use to retrieve from system manager instead
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
MYSQL_USER = app.config['MYSQL_USER']
MYSQL_PASSWORD = app.config['MYSQL_PASSWORD']
MYSQL_HOST = app.config['MYSQL_HOST']
MYSQL_DB = app.config['MYSQL_DB']


# DB for sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Store helper functions in jinjia's global environment variables
app.jinja_env.globals.update(
render_flash_msg_icon=helper.render_flash_msg_icon, 
format_currency = helper.format_currency, 
print_something = helper.print_something,
get_first_s3image_url = helper.get_first_s3image_url,
get_s3_imageurl_list = helper.get_s3_imageurl_list)


# Init Dropzone
dropzone = Dropzone(app)
# Init db (SQLAlchemy style)
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)



from ctypes import addressof
from app import app
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'ecp-db-instance.cnsgbbbzr71l.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin1234'
app.config['MYSQL_DB'] = 'ECP_DB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app) 
 
@app.route('/')
def listings(): 
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cur.execute("SELECT * FROM listing")
    # datas = cur.fetchall()
    # cur.close()
    # print(datas)
    return render_template('listings.html')
 
@app.route("/fetchrecords",methods=["POST","GET"])
def fetchrecords():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        query = request.form['action']
        minimum_price = request.form['minimum_price']
        maximum_price = request.form['maximum_price']
        #print(query)
        if query == '':
            cur.execute("SELECT * FROM listing ORDER BY id ASC")
            propertylist = cur.fetchall()
            print('all list')
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM listing WHERE price BETWEEN (%s) AND (%s)", [minimum_price, maximum_price])
            propertylist = cur.fetchall()  
            print("Filtered Data", propertylist)
    return jsonify({'htmlresponse': render_template('response.html', data=propertylist)})
 

if __name__ == '__main__':
    app.run(debug=True)
 

@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server_errer(e):
<<<<<<< HEAD
    return render_template("errors/500.html"), 500
=======
    return render_template("errors/500.html"), 500


from app.models.listing import ListingSchema
listing_schema = ListingSchema()
listings_schema = ListingSchema(many=True)

# Always put the router import, and blueprint registration after the db table schema init otherwise we get circular import error
from app import router
app.register_blueprint(router.router)


# TODO: refactor to factory pattern
>>>>>>> development
