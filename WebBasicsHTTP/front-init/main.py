import mimetypes
import urllib.parse
import socket
#import os
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import logging
import json

BASE_DIR = Path()
BUFFER_SIZE = 1024
PORT_HTTP = 3000
HOST_HTTP = '0.0.0.0'
HOST_SOCKET = '127.0.0.1' #ALSO POSIBLE localhost
SOCKET_PORT = 5000

class GoitFramework(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        #print(route.query) 
        match route.path:
            case '/':
                self.send_html('index.html')
            case '/message':
                self.send_html('message.html')
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html('error.html', 404)
            
    def do_POST(self):
        size = self.headers.get('Content-Length')
        data = self.rfile.read(int(size))
        #Create a socket and work with it
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data, (HOST_SOCKET, SOCKET_PORT))
        client_socket.close()
        self.send_response(302)
        self.send_header('Location', '/message')
        self.end_headers()

    # Prepare and send HTTP response for serving HTML content
    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())
    
    # Work with static resources - png, css
    def send_static(self, filename, status_code=200):
        # Send the HTTP response status code
        self.send_response(status_code)
        # Guess the MIME type of the file based on its extension
        mime_type, *_ = mimetypes.guess_type(filename)
        # Set the 'Content-Type' header in the HTTP response
        if mime_type:
            self.send_header('Content-Type', mime_type)
        else:
            # If MIME type cannot be guessed, set a default 'text/plain' content type
            self.send_header('Content-Type', 'text/plain')
        # End the HTTP headers section
        self.end_headers()
        # Open the file in binary mode and send its content as the response body
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

# Save received data from site to file data.json    
def save_data_from_site_form(data):
    parse_data = urllib.parse.unquote_plus(data.decode())
    try:
        parse_dict = {str(datetime.now()): {key: value for key, value in [el.split('=') for el in parse_data.split('&')]} }
        print(parse_dict)
        # Read existing data from the file
        file_path = Path('storage/data.json')
        existing_data = {}
        if file_path.exists():
            with open('storage/data.json', 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        
        # Append new data to existing data
        existing_data.update(parse_dict)
        # write 
        with open('storage/data.json', 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
    except ValueError as err:
        logging.error(err)
    except OSError as err:
        logging.error(err)

def run_server_socket(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    #server_socket.listen()
    logging.info("Start the socket server")
    try:
        while True:
            message, address = server_socket.recvfrom(BUFFER_SIZE)
            save_data_from_site_form(message)
    except KeyboardInterrupt:
        pass 
    finally:
        server_socket.close()

def run_server_http(host, port):
    address = (host, port)
    http_server = HTTPServer(address, GoitFramework)
    print(f"Server running on http://localhost:{PORT_HTTP}")
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass 
    finally:
        http_server.server_close()

def check_exist_of_storage_data():
    storage_dir = Path('storage')
    data_file = storage_dir/'data.json'
    if not storage_dir.exists():
        storage_dir.mkdir(parents=True, exist_ok=True)
    if not data_file.exists():
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    check_exist_of_storage_data()

    server = Thread(target=run_server_http, args=(HOST_HTTP, PORT_HTTP))
    server.start()

    server_socket = Thread(target=run_server_socket, args=(HOST_SOCKET, SOCKET_PORT))
    server_socket.start()
    