"""face-recognition service"""

import face_recognition

class FaceRecognitionService():

    "This is a generic class containing all face-recognition provided by the server"

    def does_face_match(self, biometrics):
        """
        Determines if two face encodings represent the same person

        Parameters:
          

        Returns:
          Boolean: Pictures contain same person (true). Pictures contain different people (false).
          None: Pictures contain 0 or multiple faces. File is not in allowed extensions
        """
        print(biometrics)
        # data format validation
        image_encoding_1 = biometrics['biometrics'][0]['vector']
        image_encoding_2 = biometrics['biometrics'][1]['vector']

        results = face_recognition.compare_faces([image_encoding_1], image_encoding_2)

        return results[0]
