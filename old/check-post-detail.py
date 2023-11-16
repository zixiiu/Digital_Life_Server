#!/usr/bin/env python3
"""
License: MIT License
Copyright (c) 2023 Miel Donkers
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("----->GET request:\n---->Path:\n %s\n---->Headers:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        print("--->write")
        self.wfile.write("-->GET request for {}".format(self.path).encode('utf-8'))
        print("--->do_GET end")

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print("----->POST request:\n----->Path: %s\n----->Headers:\n%s\n----->Body:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        print("--->write")
        self._set_response()
        self.wfile.write("-->POST request for {}".format(self.path).encode('utf-8'))
        print("--->do_POST end")


def run(server_class=HTTPServer, handler_class=S, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...Port Number:' + str(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

run()
