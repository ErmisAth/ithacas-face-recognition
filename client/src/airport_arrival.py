import cv2
import json
import requests as rq
from jsonschema import validate
from function_toolkit.image_to_biometrics import image_to_biometrics
from schemas.BiometricsSchema import Biometrics
from PIL import Image
window_name = "smile-for-me-please :)"
url = 'http://localhost:5000/api/face-recognition'
cam = cv2.VideoCapture(0)
cv2.namedWindow(window_name)
while True:
    ret, frame = cam.read()
    cv2.imshow(window_name, frame)
    if not ret:
        break
    k = cv2.waitKey(1)
    if k%256 == 27:
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        captured_frame = frame
        biometrics_json = image_to_biometrics(frame)
        try:
            validate(biometrics_json, schema=Biometrics)
            r = rq.post(url, data=biometrics_json)
            r_json = json.loads(r.text)
            if r_json['face_match']:
                print('\033[1m' + '\033[92m' + 'APPROVED!')
            else:
                print('\033[1m' + '\033[1;31m' + 'REJECTED!')
            if r.status_code != 200:
                raise Exception('bad http response code')
        except Exception as e:
            print(str(e))
cam.release()
cv2.destroyAllWindows() 
