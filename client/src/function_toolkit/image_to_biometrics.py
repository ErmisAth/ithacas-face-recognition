import face_recognition
import json

def image_to_biometrics(image):
    image_encodings = face_recognition.face_encodings(image)
    if not image_encodings:
        biometrics = {}
        biometrics['face_vector'] = []
        biometrics['success'] = False
        return json.dumps(biometrics)
    if len(image_encodings) > 1:
        biometrics = {}
        biometrics['face_vector'] = []
        biometrics['success'] = False
        return json.dumps(biometrics)
    image_encoding = image_encodings[0]
    biometrics = {}
    biometrics['face_vector'] = image_encoding.tolist()
    biometrics['success'] = True
    return json.dumps(biometrics)
