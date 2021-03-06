from base64 import b64encode
import json
import requests
from ml.pancard import PanCard
from ml.drivingl import DrivingLicense


class OCR:
    def __init__(self, image, key):
        self.image = image
        self.api_key = key
        self.endpoint = 'https://vision.googleapis.com/v1/images:annotate'

    def make_image_request(self, image):
        with open(image, 'rb') as f:
            ctxt = b64encode(f.read()).decode()
            return ({
                    'image': {'content': ctxt},
                    'features': [{
                        'type': 'TEXT_DETECTION',
                        'maxResults': 1
                    }]
                    })

    def make_image_data(self, image):
        """Returns the image data lists as bytes"""
        imgdict = self.make_image_request(image)
        return json.dumps({"requests": imgdict}).encode()

    def request_ocr(self):
        response = requests.post(self.endpoint,
                                 data=self.make_image_data(self.image),
                                 params={'key': self.api_key},
                                 headers={'Content-Type': 'application/json'})
        if response.status_code != 200 or response.json().get('error'):
            self.status = response.text
        self.response = response

    def parse_ocr(self, doc_type):
        resp = self.response.json()['responses']
        if doc_type == "PanDoc":
            panDoc = PanCard(self.image)
            data = resp['textAnnotations'][0]['description'].split('\n')
            panDoc.store_info(data[3], data[5], data[7], data[9])
            return panDoc
        elif doc_type == "DrivingLicense":
            drivl = DrivingLicense(self.image)
            print(resp)
            data = resp[0]['textAnnotations'][0]['description'].split('\n')
            drivl.store_info(data[0].split(" ")[1], data[1].split(" ")[1:],
                             data[2].split(" ")[1:], data[3].split("of ")[1],
                             data[-1])
            return drivl

    def validate(self, c_id):
        return True


if __name__ == '__main__':
    ocr = OCR('/home/vyas/Downloads/IMG_20171201_085752.jpg',
              'AIzaSyBdkJThmnTQ_DpX-mR6Q0O8a8xRNIVCaDw')
    ocr.request_ocr()
    ocr.parse_ocr("DrivingLicense")

