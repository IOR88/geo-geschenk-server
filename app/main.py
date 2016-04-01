from flask import Flask, request, jsonify
from upload_service import UploadService, MongoDBService
from utils import random_charts_generator, encode_mongo_data
from flask import make_response
from bson.json_util import dumps, loads
import json

import logging
from logging.handlers import RotatingFileHandler
# from tests import test_fetching_data_via_urllib

app = Flask(__name__)
doc_session = ''

@app.route('/', methods=['GET'])
def main():
    # TODO we should generate some unique ID, does Flask support session ?
    print(doc_session)
    return "MR. MIAU TEST PAGE :)"


@app.route('/upload', methods=['POST'])
def upload():
    global doc_session
    doc_session = random_charts_generator()
    try:
        if not (request.files.get('file', None) is None):
            upload_service = UploadService(request=request, session=doc_session)
        else:
            upload_service = UploadService(url='https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/ExampleDataPoint.json',
                                           session=doc_session)
        data = upload_service.response()
        res = {'status': 200, 'data': data}
    except Exception as e:
        print(e)
        res = {'status': 401, 'data': []}

    return jsonify(res)


@app.route('/search', methods=['POST'])
def search():
    global doc_session
    print(doc_session)
    try:
        mongo = MongoDBService(port=27017, url='localhost', db='test', collection=doc_session)
        cur = mongo.make_search_query(query=request.get_json()['query'])
        data = [x for x in cur]
        res = {'status': 200, 'data': data}
    except Exception as e:
        print(e)
        res = {'status': 401, 'data': []}
    mongo_translation = encode_mongo_data(res)
    return make_response(jsonify(mongo_translation))

if __name__ == '__main__':
    app.run()