import threading
import multiprocessing
from flask import (Flask, request, jsonify, make_response)
from flask_socketio import (SocketIO, emit)


from upload_service import (UploadService, MongoDBService)
from utils import (random_charts_generator, encode_mongo_data)
from views import (view_geosquizzy_listening,)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)

doc_session = ''


@socket_io.on('connect')
def connect():
    """
    First connection with web-socket client we set doc_session
    which will be used latter to reference mongodb collection
    """
    print('connected')
    global doc_session
    doc_session = random_charts_generator()

@socket_io.on('upload')
def upload(data):
    # TODO file upload
    pass

@socket_io.on('demo')
def demo():
    """
    starts one new socket_thread which connect with GsDemon and
    listen for its broadcasts and emit it by socket to client

    when socket is ready and listening it start concurrent process
    which consider uploading GeoJSON do mongodb and starting geosquizzy
    algorithm execution
    """
    global doc_session
    try:
        socket_thread = threading.Thread(target=view_geosquizzy_listening, args=(app, socket_io, 5))
        upload_params = {'url': 'https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/'
                                'master/build_big_data/test_data/ExampleDataPoint.json',
                         'session': doc_session}
        upload_process = multiprocessing.Process(target=UploadService,
                                                 kwargs=upload_params)

        socket_thread.start()
        upload_process.start()

        socket_thread.join()
        upload_process.join()

    except (Exception,) as e:
        print(e)
        socket_io.emit('demo', {'code': 1501, 'message': 'Server Error'})


@socket_io.on('search')
def search(data):
    """
    @global doc_session is set when connect socket is emitted from client web-socket
    """
    global doc_session
    try:
        mongo = MongoDBService(port=27017, url='localhost', db='test', collection=doc_session)
        cur = mongo.make_search_query(query=data['query'])
        data = [x for x in cur]
        if data:
            mongo_translation = encode_mongo_data(data)
            """ code 1000 results for search query """
            socket_io.emit('data', {'code': 1000, 'data': mongo_translation})
        else:
            """ code 1401 no results for search query """
            socket_io.emit('data', {'code': 1401, 'data': []})
    except (Exception,) as err:
            """ code 1501 internal app error """
            socket_io.emit('data', {'code': 1501, 'message': 'Server Error'})

if __name__ == '__main__':
    # socket_io.run(app, port=8000)
    # app.run()
    pass