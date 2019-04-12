import face_recognition
import numpy as np
import json

class FaceRecognitionService():

    def does_face_match(self, biometrics):

        # data format validation
        image_encoding_1 = np.array(biometrics['biometrics'][0]['vector'])
        image_encoding_2 = np.array(biometrics['biometrics'][1]['vector'])

        match = bool(face_recognition.compare_faces([image_encoding_1], image_encoding_2)[0])
        result = {"face_match": match}

        return result
