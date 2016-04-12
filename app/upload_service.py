from geosquizzy.geosquizzy import GeoSquizzy
from utils import get_data

import json
from pymongo import MongoClient
from socket import (AF_INET, SOCK_STREAM)


# TODO TEMP
geojson_options = {'mode': 'static', 'geojson_type': 'FeatureCollection'}
outcome_options = {}
optimization_options = {'batch': 1, 'loss': 1.0}
socket_options = {'HOST': 'localhost',
                  'PORT': 6004,
                  'FAMILY': AF_INET,
                  'TYPE': SOCK_STREAM}


class UploadService:
    def __init__(self, request=None, session=None, url=None):
        self.data = self.__get__file(request=request, url=url)
        self.file_raw = self.__read__data__(data=self.data)
        self.file = self.__decode_file__(file=self.file_raw)
        self.mongo = MongoDBService(port=27017, url='localhost', db='test')
        self.mongo.save_doc(name=session, doc=self.file)
        self.geojson = GeoJSONService(geojson_options=geojson_options,
                                      outcome_options=outcome_options,
                                      socket_options=socket_options,
                                      optim=optimization_options,
                                      data=self.file)

    @staticmethod
    def __get__file(**kwargs):
        # TODO
        # file = kwargs.get('request', None)
        # if file is not None:
        #     return kwargs['request'].files['file']
        # else:
        return get_data(url=kwargs['url'])

    @staticmethod
    def __read__data__(data=None):
        return data.read()

    @staticmethod
    def __decode_file__(file=None):
        return file.decode('utf-8')

    def response(self):
        return self.geojson.get_data()


class GeoJSONService:
    def __init__(self, geojson_options=None,
                       outcome_options=None,
                       optim=None,
                       data=None,
                       socket_options=None):
        self.geo_squizzy = GeoSquizzy(geojson_options=geojson_options,
                                      outcome_options=outcome_options,
                                      optim=optim,
                                      socket_options=socket_options)
        self.geo_squizzy.start(geojson=data)

    @staticmethod
    def __update_mongo__(key=None):
        key['keys'] = [x for x in key['keys'] if x != 'features']
        return key

    def get_data(self):
        # we have to adjust keys to mongoDB features query
        return [self.__update_mongo__(key=x) for x in self.geo_squizzy.get_results()]


class MongoDBService:
    def __init__(self, port=None, url=None, db=None, collection=None):
        self.client = MongoClient(url, port)
        self.db = self.client[db]
        if not (collection is None):
            self.collection = self.db[collection]

    def create_collection(self, name=None):
        return self.db[name]

    def convert_into_object(self, string=None):
        return json.loads(string)

    def make_search_query(self, query=None):
        query = {str.join('.', x['keys'][::-1]): x.get('search') for x in query if x.get('search', None) is not None}
        return self.__search__(query=query)

    def save_doc(self, name=None, doc=None):
        collection = self.create_collection(name=name)
        mongo_data = self.convert_into_object(string=doc)
        [collection.insert_one(x) for x in mongo_data['features']]

    def __search__(self, query=None):
        res = self.collection.find(query)
        return res
