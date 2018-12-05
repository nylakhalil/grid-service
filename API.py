import os
import logging

import requests
import argparse

import Settings

logging.basicConfig(level=logging.INFO, format=Settings.LOG_FORMAT)

class AOIS:

    def __init__(self, session):
        logging.debug("Starting AOIS Session")
        self.session = session

    def getAll(self):
        return self.session.get(Settings.API_AOI_ENDPOINT)

    def getByPK(self, pk, intersection_geoms=False):
        payload = {'pk': pk, 'intersection_types': 'raster', 'intersection_geoms': intersection_geoms}
        return self.session.get(Settings.API_AOI_ENDPOINT, params=payload)

    def create(self, name, geom, intersection_types):
        payload = {'name': name, 'geom': geom, 'intersection_types': intersection_types}
        return self.session.post(Settings.API_AOI_ENDPOINT, data=payload)

class Exports:

    def __init__(self, session):
        logging.debug('Starting AOIS Session')
        self.session = session

    def getByPK(self, pk):
        return self.session.get(Settings.API_EXPORTS_ENDPOINT + pk)

    def create(self, name, products):
        payload = {'aoi': name, 'products': products}
        return self.session.post(Settings.API_EXPORTS_ENDPOINT, data=payload)

    def download(self, url, save_path):
        response = self.session.get(url, stream=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
        return save_path
