import socket
from database import session_factory, Articolo, Articoli, Ordine, engine
from PyQt5 import QtCore
import selectors
import types


def make_query(data):
    session = session_factory()
    data = str(data, 'utf-8')
    codice_ean = int(data)
    print(data)
    query = ''

    articolo = session.query(Articolo).get(codice_ean)

    query = articolo.__repr__()
    session.close()
    print(query)

    return query


class ConnectionThread(QtCore.QThread):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    cancel = False
    sel = selectors.DefaultSelector()

    progressChanged = QtCore.pyqtSignal(str)

    def __init__(self, MAX_CONN=1):
        super().__init__()
        self.MAX_CONN = MAX_CONN
        self.server.bind(("192.168.1.191", 57891))
        self.server.listen()
        print("Listening on 192.168.1.116:57891...")
        self.server.setblocking(False)
        self.sel.register(self.server, selectors.EVENT_READ, data=None)

    def run(self):
        while not self.cancel:
            events = self.sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept_wrapper(key.fileobj)
                else:
                    self.service_connection(key, mask)

    def accept_wrapper(self, sock):
        conn, addr = sock.accept()  # Should be ready to read
        self.connections.append(addr)
        print('accepted connection from', addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        self.progressChanged.emit(f"conn {addr}")

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
                print(recv_data)
                self.progressChanged.emit(f"scan {str(recv_data, 'utf-8')}")
            else:
                print('closing connection to', data.addr)
                self.sel.unregister(sock)
                sock.close()
                self.progressChanged.emit("disconnection")
                self.connections.remove(data.addr)
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                return
                # send to device

    def get_connections(self):
        return self.connections


class ScannerThread(QtCore.QThread):
    cancel = False
    progressChanged = QtCore.pyqtSignal(str)
    progressEnded = QtCore.pyqtSignal(int)
    conn = None

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self):
        with self.conn:
            print('Connected by', addr)
            self.progressChanged.emit(f"conn {addr}")
            while not self.cancel:
                try:
                    data = self.conn.recv(512)
                except Exception as e:
                    return

                if not data:
                    break
                res = str(data, 'utf-8')
                res = "scan " + res

                self.conn.send(bytes(res, 'utf-8'))
                self.progressChanged.emit(res)

        self.progressEnded.emit(-1)

    def stop(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            print("closed")
        except Exception as e:
            pass
        if self.conn:
            self.conn.close()
        self.cancel = True

        self.sock.close()

        # self.progressEnded.emit(-1)


if __name__ == '__main__':
    ct = ConnectionThread()
    ct.start()
