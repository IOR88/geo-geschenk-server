from flask import (Flask, request, jsonify, make_response)
from flask_socketio import (SocketIO, emit)
from flask import make_response
from bson.json_util import dumps, loads
import json
import threading
import multiprocessing

from upload_service import (UploadService, MongoDBService)
from utils import (random_charts_generator, encode_mongo_data)
from views import view_geosquizzy_listening


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)

doc_session = ''


@app.route('/', methods=['GET'])
def main():
    return "MR. MIAU TEST PAGE :)"


@socket_io.on('connect')
def connect():
    print('connected')
    pass


@app.route('/upload', methods=['POST'])
def upload():
    global doc_session
    doc_session = random_charts_generator()
    try:
        # TODO
        # multiprocessing here
        # if not (request.files.get('file', None) is None):
        #     UploadService(request=request, session=doc_session)
        # else:
        socket_thread = threading.Thread(target=view_geosquizzy_listening, args=(app, socket_io, 5))
        upload_params = {'url': 'https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/'
                                'master/build_big_data/test_data/ExampleDataPoint.json',
                         'session': doc_session}
        upload_process = multiprocessing.Process(target=UploadService,
                                                 kwargs=upload_params)

        socket_thread.start()
        upload_process.start()

        # TODO geo-squizzy has to add ending signal
        # upload_process.join()
        # socket_thread.join()

        # upload_service = UploadService(url='https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/'
        #                                    'master/build_big_data/test_data/ExampleDataPoint.json',
        #                                session=doc_session)

        # data = upload_service.response()
        res = {'status': 200}
    except Exception as e:
        print(e)
        res = {'status': 401}

    return jsonify(res)


# @app.route('/search', methods=['POST'])
# def search():
#     global doc_session
#     print(doc_session)
#     try:
#         mongo = MongoDBService(port=27017, url='localhost', db='test', collection=doc_session)
#         cur = mongo.make_search_query(query=request.get_json()['query'])
#         data = [x for x in cur]
#         res = {'status': 200, 'data': data}
#     except Exception as e:
#         print(e)
#         res = {'status': 401, 'data': []}
#     mongo_translation = encode_mongo_data(res)
#     return make_response(jsonify(mongo_translation))

if __name__ == '__main__':
    # socket_io.run(app, port=8000)
    # app.run()
    pass