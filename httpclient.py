#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = int(code)
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port="80"):
        # use sockets!
        if(port == None):
            port = 80
        print(host, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))  
        return s

    def get_code(self, data):
        parts = data.split()
        return parts[1]

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        parsed_url = urlparse(url)
        s = self.connect(parsed_url.hostname, parsed_url.port)
        print(parsed_url)

        path = parsed_url.path
        if(path == ""):
            path = "/"
        if(parsed_url.query != ""):
            path += "?" + parsed_url.query

        request = "GET " + path + " HTTP/1.1\r\n"
        request += "Host: " + parsed_url.hostname + "\r\n"
        request += "Accept: */*" + "\r\n" 
        request += "User-Agent: Custom\r\n"
        request += "Connection: close\r\n\r\n"

        print ("\n\n" + request + "\n\n")
        s.send(request)
        response = self.recvall(s)

        response_arr = response.splitlines()

        code = None
        reach_content = False
        body = ""
        for i, line in enumerate(response_arr):
            if(i == 0):
                code = self.get_code(line)
            elif(reach_content == False):
                self.get_headers(line)
                if(line == ""):
                    reach_content = True
            else:
                body += line + "\n"

        print "\n\n###########GOT RESPONSE" + code + " " + body+"\n############\n\n"

        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def command(self, command, url, args=None):
        print("COMMAND" , url, command)
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( sys.argv[1], sys.argv[2], sys.argv[3] )    
