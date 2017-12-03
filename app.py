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

# MySQL get_db()
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


@app.route('/user/<id>/get', methods=['GET'])
# @auth.login_required()
def login(id):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM customer WHERE mobile_no = %s", [int(id)])
    return convert(cur)


@app.route('/user/signup', methods=['POST'])
def signup():
    print(request.json)
    print(request.get_json(force=True))
    data = json.loads(request.get_json(force=True))
    con = mysql.connect()
    cur = con.cursor()
    cur.execute("INSERT INTO customer(name, email, a_no, pwd, location, \
                mobile_no) values(%s, %s, %s, %s, %s, %s)",
                [data['name'], data['email'], data['aadhaar'],
                    data['pass'], data['loc'], data['mobile']])
    con.commit()
    return "200"


@app.route('/user/rama/<id>/upload', methods=['POST'])
# @auth.login_required
def get_rama_image(id):
    con = mysql.connect()
    cur = con.cursor()
    image1 = request.files['PanCard']
    filename1 = id + '_PanCard'
    image2 = request.files['DrivingLicense']
    filename2 = id + '_DriverLicense'
    loc1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
    loc2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
    image1.save(loc1)
    image2.save(loc2)
    print("Done")
    cur.execute("insert into documents(type, c_id, status) values(%s,\
                %s, %s)", ['PanCard', id, 'Uploaded'])
    cur.execute("insert into documents(type, c_id, status) values(%s,\
                %s, %s)", ['DrivingLicense', id, 'Uploaded'])
    con.commit()
    return "200"


@app.route('/user/<id>/upload', methods=['POST'])
# @auth.login_required
def get_image(id):
    doc_type = request.headers['doctype']
    con = mysql.connect()
    cur = con.cursor()
    print(request.files)
    if doc_type == 'pancard':
        image = request.files[id]
        filename = id + '_PanCard'
    else:
        image = request.files[id]
        filename = id + '_DriverLicense'
    loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(loc)
    print("Done")
    cur.execute("insert into documents(type, c_id, status) values(%s,\
                %s, %s)", [doc_type, id, 'Uploaded'])
    cur.execute('insert into transac values (%s, %s, %s, %s, %s)', [id,
                1, 12, 'Submitted', 'Pending'])
    con.commit()
    return "200"


@app.route('/user/<id>/docs', methods=['GET'])
def get_user_docs(id):
    cur = mysql.get_db().cursor()
    cur.execute("select * from documents where c_id = %s", [id])
    return convert(cur)


@app.route('/user/<id>/<doc>/status', methods=['GET'])
# @auth.login_required
def get_doc_status(name, doc):
    cur = mysql.get_db().cursor()
    cur.execute('select status from documents where id = %s and d_id = %s',
                [int(id), int(doc)])
    return convert(cur)


@app.route('/user/<c_id>/<doc_type>', methods=['GET'])
# @auth.login_required
def get_user_doc(c_id, doc_type):
    cur = mysql.get_db().cursor()
    cur.execute('select * from document where type = %s and c_id = %s',
                [doc_type, c_id])
    return convert(cur)


@app.route('/user/<c_id>/<doc_type>/image', methods=['GET'])
def get_user_doc_image(c_id, doc_type):
    return send_file(app.config['UPLOAD_FOLDER'] + c_id + '_' + doc_type,
                     as_attachment=False)


@app.route('/user/<c_id>/<doc_id>/send/<o_id>', methods=['POST'])
# @auth.login_required
def send_user_docs_to(c_id, doc_id, o_id):
    con = mysql.connect()
    cur = con.cursor()
    cur.execute('insert into transaction values (%s, %s, %s, %s)', [c_id,
                doc_id, o_id, 'Submitted'])
    con.commit()
    return "200"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
