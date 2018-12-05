import os
import sys
import json
import logging

import Auth
import Settings
from API import AOIS, Exports

logging.basicConfig(level=logging.INFO, format=Settings.LOG_FORMAT)

class Grid():

    session = None

    def __init__(self):
        if not self.session:
            logging.info('Starting GRiD Service')
            session = Auth.Connection().getSession()
            self.aoi_endpoint = AOIS(session)
            self.export_endpoint = Exports(session)

    def getAOIList(self, aois_json):
        aois = json.loads(aois_json)
        
        aoi_list = []
        for aoi in aois['aois']:
            data = {'pk': aoi['pk'], 'name': aoi['name'], 'exports': aoi['exports'], 'rasters': []}
            for raster in aoi['raster_intersects']:
                raster_info = {'pk': str(raster['pk']), 'name': str(raster['name'])}
                data['rasters'].append(raster_info)
            aoi_list.append(data)
        logging.info('Total AOIS: {}'.format(len(aoi_list)))
        return aoi_list

    def getExportList(self, export_json):
        exports = json.loads(export_json)
        
        export_list = []
        for export in exports['exports']:
            data = {'pk': export['pk'], 'name': export['name'], 'status': export['status'], 'url': export['url'], 'files': []}
            logging.debug('Found Export: {}'.format(data))
            
            for export_file in export['exportfiles']:
                file_info = {'name': str(export_file['name']), 'url': str(export_file['url'])}
                data['files'].append(file_info)
            export_list.append(data)
        logging.info('Total Exports {}'.format(len(export_list)))
        return export_list
    

    def getExportFiles(self, export_list):
        file_paths = []

        for export in export_list:
            for file_info in export['files']:
                url = file_info['url']
                path = os.path.join('data', file_info['name'])
                logging.info("Downloading from URL {} to {}".format(url, path))

                file_path = self.export_endpoint.download(url, path)
                file_paths.append(file_path)
        logging.info("Download: {} files".format(len(file_paths)))
        return file_paths


if __name__ == '__main__':
    try:
        grid = Grid()
        geom = "POLYGON ((-76.72709941864009 37.4840533121707, -76.5827322006226 36.942963620815, -75.3535079956055 37.0357212778916, -75.47491550445559 37.6097439561546, -76.72709941864009 37.4840533121707))"
        response = grid.aoi_endpoint.create('api_test', geom, 'raster')
        aoi_list = grid.getAOIList(response.text)

        for aoi in aoi_list:
            for raster in aoi['rasters']:
                response = grid.export_endpoint.create(aoi['pk'], raster['pk'])

        #export_list = grid.getExportList(response.text)
        #export = grid.getExportFiles(export_list)
    except Exception as exc:
        exc_type, exc_obj, exc_trace = sys.exc_info()
        logging.error('Error Type: {}, Line: {}, Message: {}'.format(exc_type.__name__, exc_trace.tb_lineno, exc_obj.message))