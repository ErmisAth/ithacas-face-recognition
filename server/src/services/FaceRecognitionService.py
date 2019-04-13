import face_recognition
import numpy as np
import json
import pymongo

class FaceRecognitionService():

    def does_face_match(self, biometrics):

        # data format validation
        image_encoding_1 = np.array(biometrics['face_vector'])
        
        client = pymongo.MongoClient('mongodb://localhost:27017/')

        db = client.odyssey
        collection = db.odysseyPassengers
        size = collection.count()
        face_vectors = collection.find({},{'face_vector' : 1, '_id' : 0})

        match = False
        for i in range(size):
            image_encoding_2 = face_vectors[i]['face_vector']
            if bool(face_recognition.compare_faces([image_encoding_1], np.array(image_encoding_2))[0]):
                match = True
        result = {"face_match": match}

        return result
