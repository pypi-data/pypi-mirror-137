from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from time import sleep
from threading import Thread
from socketserver import ThreadingMixIn
import uuid
import requests


class Connection:

    def __init__(self, handle):
        self.id = str(uuid.uuid4())
        self.creation_date = datetime.now()
        self.handle = handle

    def close(self):
        self.handle.close()

    def __hash__(self):
        return self.id.__hash__()

    def __str__(self):
        return self.creation_date.isoformat() + " " +  str(self.handle.client_address[0]) + ":" + str(self.handle.client_address[1])

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.creation_date < other.creation_date

    def __eq__(self, other):
        return self.creation_date == other.creation_date


class ThreadingServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

    def __init__(self, server_address, target_url: str, max_lifetime_sec: int = 60, verify: bool = True):
        self.target_url = target_url
        self.verify = verify
        self.max_lifetime_sec = max_lifetime_sec
        self.running_connections = list()
        HTTPServer.__init__(self, server_address, RequestHandler, True)
        Thread(target=self.__run_housekeeping, daemon=True).start()

    def on_connected(self, connection: Connection):
        self.running_connections.append(connection)
        print("Connection "  + str(connection) + " established (running connections " + str(len(self.running_connections)) + ")")

    def on_disconnected(self, connection: Connection):
        try:
            self.running_connections.remove(connection)
        except Exception as e:
            print(e)
        print("Connection "  + str(connection) + " terminated (running connections " + str(len(self.running_connections)) + ")")

    def __run_housekeeping(self):
        sleep(self.max_lifetime_sec / 2)
        while True:
            try:
                connections = set(self.running_connections)
                if len(connections) > 0:
                    for connection in connections:
                        if (datetime.now() - connection.creation_date).total_seconds() > self.max_lifetime_sec:
                            connection.close()

            except Exception as e:
                print("error occurred while housekeeping " + str(e))


class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server: ThreadingServer):
        self.is_running = True
        self.server = server
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def close(self):
        self.is_running = False

    def do_GET(self):
        print("Connection " + str(self.client_address[0]) + ":" + str(self.client_address[1]) + " established")
        connection = Connection(self)
        self.server.on_connected(connection)
        resp = None
        try:
            resp = requests.get(self.server.target_url, stream=True, verify=self.server.verify)
            self.send_response(200)
            self.send_header('Content-type', resp.headers['Content-Type'])
            self.end_headers()
            for chunk in resp.iter_content(chunk_size=10 * 1024):
                if self.is_running:
                    self.wfile.write(chunk)
                else:
                    return
        except Exception as e:
            print(e)
        finally:
            if resp is not None:
                try:
                    resp.close()
                except Exception as e:
                    print(e)
            try:
                self.wfile.close()
            except Exception as e:
                print(e)
            self.server.on_disconnected(connection)


def run_server(port: int, target_url: str, verify: bool = True, max_lifetime_sec: int = 45 * 60):
    server = ThreadingServer(('0.0.0.0', port), target_url, max_lifetime_sec, verify)
    print(f"Starting httpd server on {port}")
    server.serve_forever()


#run_server(9070, 'https://10.1.66.20/anonymous/jpeg/stream=0', False, max_lifetime_sec=10)