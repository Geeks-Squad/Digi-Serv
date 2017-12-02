import sys
import logging
import json
import os
from flask import Flask, send_file
from flask import request
from flask_httpauth import HTTPBasicAuth
from flaskext.mysql import MySQL

logger = logging.getLogger(__name__)

debug = 0

app = Flask(__name__)

# MySQL Connection
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'sree'
app.config['MYSQL_DATABASE_PASSWORD'] = 'asdf1234asdf'
app.config['MYSQL_DATABASE_DB'] = 'deepauth'
app.config['MYSQL_DATABASE_HOST'] = '128.199.81.127'
app.config['UPLOAD_FOLDER'] = '/home/vyas/images/'
mysql.init_app(app)

lformat = logging.Formatter('%(asctime)s %(name)s:%(levelname)s: %(message)s')

# Logging
lsh = logging.StreamHandler(sys.stdout)
lsh.setFormatter(lformat)
lsh.setLevel(logging.WARNING)
logger.addHandler(lsh)

auth = HTTPBasicAuth()


def convert(cur, one=False):
    r = [dict((cur.description[i][0], value) for i, value in enumerate(row))
            for row in cur.fetchall()]
    data = (r[0] if r else None) if one else r
    return json.dumps(data)


@auth.get_password
def get_pw(username):
    return True


@app.route('/user/<int:id>/get', methods=['GET'])
# @auth.login_required()
def login(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Customer WHERE id = %d", [id])
    return convert(cur)


@app.route('/user/signup', methods=['POST'])
def signup():
    data = json.loads(request.get_json(force=True))
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Customers values (%s, %s, %d, %s, %s)",
                [data['name'], data['mobile'], data['aadhaar'], data['email'],
                    data['pass']])
    return "300"


@app.route('/user/<int:id>/upload', methods=['POST'])
# @auth.login_required
def get_image(name):
    data = json.loads(request.get_json(force=True))
    cur = mysql.connection.cursor()
    if (data['c_id'] + 'pancard') not in request.files and (data['c_id'] +
                                                            'DriverLicense') not in request.files:
        return "400"
    if data['type'] == 'pancard':
        image = request.files[data['c_id']] + '_PanCard'
        filename = data['c_id'] + '_PanCard'
    else:
        image = request.files[data['c_id']] + '_DriverLicense'
        filename = data['c_id'] + '_DriverLicense'
    loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(loc)
    cur.execute("INSERT INTO Documents values (%s, %d, %s, %s)", [data['type'],
                data['c_id'], loc, 'Submited'])
    return 200


@app.route('/user/<int:id>/docs', methods=['GET'])
def get_user_docs(name):
    cur = mysql.connection.cursor()
    cur.execute("select * from documents where c_id = %d", [id])
    return convert(cur)


@app.route('/user/<int:id>/<int:doc>/status', methods=['GET'])
# @auth.login_required
def get_doc_status(name, doc):
    cur = mysql.connection.cursor()
    cur.execute('select status from documents where id = %d and d_id = %d',
                [id, doc])
    return convert(cur)


@app.route('/user/<int:c_id>/<string:doc_type>', methods=['GET'])
# @auth.login_required
def get_user_doc(c_id, doc_type):
    cur = mysql.connection.cursor()
    cur.execute('select * from document where type = %d and c_id = %d',
                [doc_type, c_id])
    return convert(cur)


@app.route('/user/<int:c_id>/<string:doc_type>/image', methods=['GET'])
def get_user_doc_image(c_id, doc_type):
    return send_file(app.config['UPLOAD_FOLDER'] + c_id + '_' + doc_type,
                     as_attachment=False)


@app.route('/user/<int:c_id>/<int:doc_id>/send/<int:o_id>', methods=['POST'])
# @auth.login_required
def send_user_docs_to(c_id, doc_id, o_id):
    cur = mysql.connection.cursor()
    cur.execute('insert into transaction values (%d, %d, %d, %s)', [c_id,
                doc_id, o_id, 'Submitted'])
    return "200"


@app.route('/user/<c_id>/sent', methods=['GET'])
# @auth.login_required
def get_user_sent_to(c_id):
    cur = mysql.connection.cursor()
    cur.execute('select * from transaction where c_id = %d', [c_id])
    return convert(cur)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
