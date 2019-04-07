def doesFaceMatch(imageFile1, imageFile2):
  import face_recognition
  from PIL import Image

  # load images
  image1 = face_recognition.load_image_file(imageFile1)
  image2 = face_recognition.load_image_file(imageFile2)

  # get image encodings
  imageEncodings1 = face_recognition.face_encodings(image1)
  imageEncodings2 = face_recognition.face_encodings(image2)

  # no faces in the pictures
  if len(imageEncodings1) == 0 or len(imageEncodings2) == 0:
    print("No faces detected. Aborting...")
    exit()
  # more than one faces in the pictures
  if len(imageEncodings1) > 1 or len(imageEncodings2) > 1:
    print("Multiple faces detected. Aborting...")
    exit()

  imageEncoding1 = imageEncodings1[0]
  imageEncoding2 = imageEncodings2[0]

  results = face_recognition.compare_faces([imageEncoding1], imageEncoding2)

  return results[0]