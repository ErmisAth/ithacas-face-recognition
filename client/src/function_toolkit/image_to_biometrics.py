import face_recognition
import json

def image_to_biometrics(image):

    # get image encodings
    image_encodings = face_recognition.face_encodings(image)

    # no faces in the pictures
    if not image_encodings:
        biometrics = {}
        biometrics['face_vector'] = []
        biometrics['success'] = False
        return json.dumps(biometrics)

    # more than one faces in the pictures
    if len(image_encodings) > 1:
        biometrics = {}
        biometrics['face_vector'] = []
        biometrics['success'] = False
        return json.dumps(biometrics)

    # get the encoding from the list
    image_encoding = image_encodings[0]

    biometrics = {}
    biometrics['face_vector'] = image_encoding.tolist()
    biometrics['success'] = True
    return json.dumps(biometrics)
