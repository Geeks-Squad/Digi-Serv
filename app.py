import sys
import logging
from flask import Flask
from flask_restful import Resource, jsonify
from flask_httpauth import HTTPBasicAuth
from flaskext.mysql import MySQL

logger = logging.getLogger(__name__)

debug = 0

app = Flask(__name__)

# MySQL Connection
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

lformat = logging.Formatter('%(asctime)s %(name)s:%(levelname)s: %(message)s')

# Logging
lsh = logging.StreamHandler(sys.stdout)
lsh.setFormatter(lformat)
lsh.setLevel(logging.WARNING)
logger.addHandler(lsh)

auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    return None


@app.route('/user/get', method=['GET'])
@auth.login_required
def login():
    return "Hello, %s!" % auth.username()


@app.route('/user/signup', method=['POST'])
def signup():
    return


@app.route('/user/<int:name>/upload', method=['POST'])
@auth.login_required
def get_image(name):
    return


@app.route('/user/<int:name>/docs', method=['GET'])
@auth.login_required
def get_user_docs(name):
    return


@app.route('/user/<int:name>/<int:doc>/status', method=['GET'])
@auth.login_required
def get_doc_status(name, doc):
    return


@app.route('/user/<int:name>/<int:doc>', method=['GET'])
@auth.login_required
def get_user_doc(name, doc):
    return


@app.route('/user/<int:name>/<int:doc>/send/<int:cust>', method=['GET'])
@auth.login_required
def send_user_docs_to(name, doc, cust):
    return


@app.route('/user/<int:name>/<int:doc>/<int:cust>', method=['GET'])
@auth.login_required
def get_user_doc_customers(name, doc, cust):
    return


@app.route('/user/<int:name>/sent', method=['GET'])
@auth.login_required
def get_user_sent_to(name):
    return


@app.route('/cust/pending', method=['GET'])
@auth.login_required
def get_cust_pending():
    return


@app.route('/cust/approved', method=['GET'])
@auth.login_required
def get_cust_approved():
    return


@app.route('/cust/statistics', method=['GET'])
@auth.login_required
def get_cust_statistics():
    return


@app.route('/cust/recieved/<int:user>', method=['GET'])
@auth.login_required
def get_cust_recieved(user):
    return


@app.route('/cust/recieved/<int:user>/<int:doc>', method=['GET'])
@auth.login_required
def get_cust_user_doc(user, doc):
    return


if __name__ == '__main__':
    app.run()
