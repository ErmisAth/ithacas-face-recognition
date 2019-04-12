import json
from flask import abort, make_response, request
from services.FaceRecognitionService import FaceRecognitionService

class FaceRecognitionController:
    def __init__(self, app, config, prefix):
        self.app = app
        self.prefix = prefix
        self.fRService = FaceRecognitionService()
        self.contentType = config.contentType

    def createRoutes(self):
        @self.app.route(self.prefix, methods=['POST'])
        def recogniseFace():
            self.app.logger.info('=> start of face-recognition endpoint')
            self.app.logger.info('---> run post command')
            try:
                data = request.get_data()
                data = data.decode('utf-8')
                data = json.loads(data)
            except:
                return 'request failed: post body did not match requirements', 422
            try:
                response = self.fRService.does_face_match(data)
                if (not response):
                    abort(500, 'empty response: face-recognition failed')
            except ValueError:
                abort(500, 'error response: face-recognition failed')
            
            response = make_response(json.dumps(response), 200)
            response.headers['content-type'] = self.contentType

            return response
