import json

class CONFIGURATION:
    def __init__(self, contentType, accept):
        self.authorization = ''
        self.contentType = contentType
        self.accept = accept

    def __str__(self):
        return json.dumps({
          'authorization': self.authorization,
          'contentType': self.contentType,
          'accept': self.accept
        })

MAINCONFIGURATION = CONFIGURATION(
  'application/json',
  'application/json'
)