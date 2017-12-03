import mysql.connector as mariadb
import os
from ml.verification import cnn_predict
from ml.ocr import OCR
import json
import time

IMAGE_DIR = '/home/vyas/images/'


def decode(var):
    if isinstance(var, int) or isinstance(var, str):
        return var


def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], map(decode, row)))
            for row in cursor.fetchall()]


if __name__ == '__main__':
    status = 'Uploaded'

    while True:
        mariadb_connection = mariadb.connect(host="128.199.81.127",
                                             user='sree',
                                             password='asdf1234asdf',
                                             database='deepauth')

        cursor = mariadb_connection.cursor()
        cursor.execute('select c_id, type from documents where status = %s',
                       (status,))
        data = dictfetchall(cursor)
        cursor.close()
        for image in data:
            c_id = image['c_id']
            doc_type = image['type']
            filename = os.path.join(IMAGE_DIR, c_id + "_" + doc_type)
            # CNN shit
            val = cnn_predict(filename)
            # OCR shit
            ocr = OCR(filename, "AIzaSyBdkJThmnTQ_DpX-mR6Q0O8a8xRNIVCaDw")
            ocr.request_ocr()
            doc = ocr.parse_ocr(doc_type)
            json_doc = json.dumps(doc.__dict__)
            cursor = mariadb_connection.cursor()
            if ocr.validate(c_id) and val > 0.3:
                cursor.execute('update documents set content = ? and status\
                        = ? where c_id = ?', [json_doc, 'Approved', c_id])
            else:
                cursor.execute('update documents set content = ? and status\
                        = ? where c_id = ?', [json_doc, 'Rejected', c_id])
        mariadb_connection.commit()
        time.sleep(1000)
