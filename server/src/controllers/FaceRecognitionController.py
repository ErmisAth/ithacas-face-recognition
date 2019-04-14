import json
from flask import abort, make_response, request
from jsonschema import validate
from services.FaceRecognitionService import FaceRecognitionService
from schemas.BiometricsSchema import Biometrics

class FaceRecognitionController:
    def __init__(self, app, config, prefix):
        self.app = app
        self.prefix = prefix
        self.fRService = FaceRecognitionService()
        self.contentType = config.contentType

    def createRoutes(self):
        @self.app.route(self.prefix, methods=['POST'])
        def recogniseFace():
            try:
                data = json.loads(request.get_data()); validate(data, schema=Biometrics)
                if not data['success']:
                    abort(500, 'error response: face-recognition failed')
                response = self.fRService.does_face_match(data)
                if (not response):
                    abort(500, 'empty response: face-recognition failed')
            except:
                abort(500, 'error response: face-recognition failed')
            response = make_response(json.dumps(response), 200)
            response.headers['content-type'] = self.contentType
            return response
