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
    """
    Handles command line input of start-up command 

    Parameters:
      argv[1:] command line inputs

    Returns:
      CONFIGURATION: Object containing the server configuration
    """

    # initialise args
    username = ''
    password = ''
    outputFile = 'server.log'

    # parse args
    try:
        (opts,_) = getopt(argv, 'u:p:o:', ['username=', 'password=', 'outputFile='])
    except GetoptError:
        print('app.py -u <username> -p <password> -o <outputFile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-u', '--username'):
            username = arg
        elif opt in ('-p', '--password'):
            password = arg
        elif opt in ('-o', '--outputFile'):
            outputFile = arg

    # base64 encoding for credentials
    output = b64encode(bytes(username + ':' + password, 'utf-8'))
    
    # load configuration
    config = MAINCONFIGURATION
    config.authorization = 'Basic ' + output.decode()
    config.outputFile = outputFile

    return config

def main(argv):

    """
    Handles command line input of start-up command 

    Parameters:
      argv[1:] command line inputs

    Returns:
      CONFIGURATION: Object containing the server configuration
    """

    # create flask app and configuration

    ### see if I need configs
    app = Flask(__name__)
    config = handleInput(argv)

    # create FaceRecognitionController
    fRController = FaceRecognitionController(
        app,
        config,
        prefix='/api/face-recognition'
    )
    fRController.createRoutes()

    # create a file to store weblogs and delete old content
    log = open(config.outputFile, 'w')
    log.seek(0)
    log.truncate()
    log.write("Python Server for Interational Travel CSC Log\n")
    log.close()

    # set loghandling and formatting on the log file
    log_handler = RotatingFileHandler(config.outputFile, maxBytes =1000000, backupCount=1)
    formatter = logging.Formatter("%(message)s")
    log_handler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(log_handler)

    @app.route('/serverAlive', methods=['GET'])
    def amIAlive():
        return json.dumps({'message': 'I am alive'}), 200
    
    return app

if __name__ == "__main__":
    app = main(sys.argv[1:])
    http_server = WSGIServer(('', 5000), app, log = app.logger)
    print('server running on localhost:5000 in a moment!')
    http_server.serve_forever()