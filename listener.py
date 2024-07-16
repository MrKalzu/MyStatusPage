import http.server
import socketserver
import json
import time
import threading

class Api:
    def __init__(self, config, db, logger) -> None:
        self.config = config
        self.db = db
        self.logger = logger
        self.server = None
        self.server_thread = None

    def create_handler(self):
        config = self.config
        db = self.db
        logger = self.logger

        class MyHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                logger.info("%s - - [%s] %s" %
                            (self.address_string(),
                             self.log_date_time_string(),
                             format%args))

            """Handle HTTP GET and POST requests."""
            def do_POST(self):
                if self.path == '/ping':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data)
        
                    server = data.get('server')
                    token = data.get('token')
        
                    tokens = config.get_tokens()
                    if server and token and tokens.get(server) == token:
                        connection_data = json.dumps({key: value for key, value in data.items() if key not in ['server', 'token']})
                        db.insert_ping(server, time.time(), connection_data)
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b"OK")
                    else:
                        self.send_response(404)
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()

        return MyHandler


    def start(self):
        settings = self.config.get_config()
        handler = self.create_handler()


        class ReusableTCPServer(socketserver.TCPServer):
            allow_reuse_address = True

        try:
            self.server = ReusableTCPServer((settings['listen'], int(settings['port'])), handler)
            self.logger.info(f"Serving HTTP on: {settings['listen']}:{settings['port']}")
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.start()
            self.logger.info(f"API server thread started successfully.")
        except Exception as e:
            self.logger.error(f"Failed to start the API server: {e}")

    def stop(self):
            if self.server:
                self.logger.info("Stopping server...")
                self.server.shutdown()
                self.server.server_close()
                self.server_thread.join()
                self.logger.info("Server stopped.")
