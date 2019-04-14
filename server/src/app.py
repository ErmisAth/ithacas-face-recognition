#!flask/bin/python
import sys
from base64 import b64encode
from getopt import getopt
from getopt import GetoptError
import json
from flask import Flask
from gevent.pywsgi import WSGIServer
from logging.handlers import RotatingFileHandler
import logging

from services.FaceRecognitionService import FaceRecognitionService
from controllers.FaceRecognitionController import FaceRecognitionController
from config import MAINCONFIGURATION

def handleInput(argv):
    outputFile = 'server.log'
    try:
        (opts,_) = getopt(argv, 'o:', ['outputFile='])
    except GetoptError:
        print('app.py -o <outputFile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-o', '--outputFile'):
            outputFile = arg
    output = b64encode(bytes(username + ':' + password, 'utf-8'))
    config = MAINCONFIGURATION
    config.authorization = 'Basic ' + output.decode()
    config.outputFile = outputFile
    return config

def main(argv):
    app = Flask(__name__)
    config = handleInput(argv)
    # create FaceRecognitionController
    fRController = FaceRecognitionController(app, config, prefix='/api/face-recognition')
    fRController.createRoutes()
    # create a file to store weblogs and delete old content
    log = open(config.outputFile, 'w'); log.seek(0); log.truncate()
    log.write("Python Server for Interational Travel CSC Log\n"); log.close()
    # set loghandling and formatting on the log file
    log_handler = RotatingFileHandler(config.outputFile, maxBytes =1000000, backupCount=1)
    formatter = logging.Formatter("%(message)s")
    log_handler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)
    # create server alive route
    @app.route('/serverAlive', methods=['GET'])
    def amIAlive():
        return json.dumps({'message': 'I am alive'}), 200
    
    return app

if __name__ == "__main__":
    app = main(sys.argv[1:])
    http_server = WSGIServer(('', 5000), app, log = app.logger)
    print('server running on localhost:5000 in a moment!')
    http_server.serve_forever()
