"""face-recognition service"""

import face_recognition

class FaceRecognitionService:

    "This is a generic class containing all face-recognition provided by the server"

    def does_face_match(self, image_filename_1, image_filename_2):

        """
        Determines if two images contain a face that belongs to the same person


        Parameters:


        Returns:
          Boolean: Pictures contain same person (true). Pictures contain different people (false).
          None: Pictures contain 0 or multiple faces.
        """
        # load images
        image1 = face_recognition.load_image_file(image_filename_1)
        image2 = face_recognition.load_image_file(image_filename_2)

        # get image encodings
        image_encodings_1 = face_recognition.face_encodings(image1)
        image_encodings_2 = face_recognition.face_encodings(image2)

        # no faces in the pictures
        if not image_encodings_1 or not image_encodings_2:
            return

        # more than one faces in the pictures
        if len(image_encodings_1) > 1 or len(image_encodings_2) > 1:
            return

        # get the encoding from the list
        image_encoding_1 = image_encodings_1[0]
        image_encoding_2 = image_encodings_2[0]

        results = face_recognition.compare_faces([image_encoding_1], image_encoding_2)

        return results[0]
