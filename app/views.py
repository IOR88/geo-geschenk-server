import time
from socket import AF_INET, SOCK_STREAM
from flask_socketio import emit

from geosquizzy.socket.gs_client import GsSocketClient


def view_geosquizzy_listening(app, timeout):
    with app.test_request_context('geosquizzy'):
        emit('geosquizzy', {'status': 1, 'data': None})

        try:
            client = GsSocketClient(HOST='localhost',
                                    PORT=8030,
                                    FAMILY=AF_INET,
                                    TYPE=SOCK_STREAM)
            client.connect()
            start = time.time()
            while True:
                if time.time() - start > timeout:
                    break
                try:
                    data = client.socket.recv(1024)
                    if data:
                        emit('geosquizzy', {'status': 2, 'data': str(data, 'utf-8')})
                except (Exception,) as err:
                    print(err)

        except (Exception,) as err:
            print(err)

        emit('geosquizzy', {'status': 0, 'data': None})