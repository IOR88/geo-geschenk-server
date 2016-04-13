import time
from socket import AF_INET, SOCK_STREAM

from geosquizzy.gs_socket.gs_client import GsSocketClient


def view_geosquizzy_listening(app, socket_io, timeout):
    # with app.app_context():
    # http://kronosapiens.github.io/blog/2014/08/14/understanding-contexts-in-flask.html
    with app.test_request_context('geosquizzy'):
        socket_io.emit('geosquizzy', {'status': 1, 'data': None})

        try:
            client = GsSocketClient(HOST='localhost',
                                    PORT=6004,
                                    FAMILY=AF_INET,
                                    TYPE=SOCK_STREAM)
            client.connect()
            # start = time.time()
            while True:
                data = client.socket.recv(1024)
                if data:
                    # TODO some error occurred - > unexpected EOF while parsing (<string>, line 1)
                    res = eval(str(data, 'utf-8'))
                    if res == 0:
                        socket_io.emit('geosquizzy', {'status': 0, 'data': None})
                        break
                    else:
                        socket_io.emit('geosquizzy', {'status': 2, 'data': res})

        except (Exception,) as err:
            print(err)