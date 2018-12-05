import logging

import requests

import Settings

logging.basicConfig(level=logging.INFO, format=Settings.LOG_FORMAT)

class Connection:
    session = None
    headers = None
    
    def __init__(self):
        if not self.session:
            logging.info("Creating GRiD Session")
            self.headers = { "Authorization": "Bearer " + Settings.API_TOKEN, "Accept": "application/json" }
            self.session = requests.Session()
            self.session.headers.update(self.headers)

    def getSession(self):
        return self.session