import sys
import logging
import json
import os
from flask import Flask, send_file
from flask import request
from flask_httpauth import HTTPBasicAuth
from flaskext.mysql import MySQL

from docs.ocr import OCR

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


@app.route('/user/<id>/upload', methods=['POST'])
# @auth.login_required
def get_image(name):
    data = json.loads(request.get_json(force=True))
    con = mysql.connect()
    cur = con.cursor()
    if (data['c_id'] + 'pancard') not in request.files and (data['c_id'] +
                                                            'DriverLicense') not in request.files:
        return "400"
    if data['type'] == 'pancard':
        doc_type = 'PanCard'
        image = request.files[data['c_id']] + '_PanCard'
        filename = data['c_id'] + '_PanCard'
    else:
        doc_type = 'DriverLicense'
        image = request.files[data['c_id']] + '_DriverLicense'
        filename = data['c_id'] + '_DriverLicense'
    loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(loc)
    cur.execute("INSERT INTO documents values (%s, %s, %s)", [data['type'],
                data['c_id'], 'Submited'])
    ocr = OCR(loc, "AIzaSyBdkJThmnTQ_DpX-mR6Q0O8a8xRNIVCaDw")
    ocr.request_ocr()
    doc = ocr.parse_ocr(doc_type)
    json_doc = json.dumps(doc.__dict__)
    cur.execute("update documents set content = %s", [json_doc])
    con.commit()
    return "200"


@app.route('/user/<id>/docs', methods=['GET'])
def get_user_docs(name):
    cur = mysql.get_db().cursor()
    cur.execute("select * from documents where c_id = %s", [int(id)])
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
    cur = mysql.get_db().cursor()
    cur.execute('insert into transaction values (%s, %s, %s, %s)', [c_id,
                doc_id, o_id, 'Submitted'])
    return "200"


@app.route('/user/<c_id>/sent', methods=['GET'])
# @auth.login_required
def get_user_sent_to(c_id):
    cur = mysql.get_db().cursor()
    cur.execute('select * from transaction where c_id = %s', [c_id])
    return convert(cur)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
