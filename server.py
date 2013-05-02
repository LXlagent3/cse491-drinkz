#!/usr/bin/env python
import random
import socket
import time
from drinkz.app import SimpleApp
from StringIO import StringIO
import json

the_app = SimpleApp()

sock = socket.socket()        
host = socket.gethostname()  
port = random.randint(8000, 9999)
sock.bind((host, port))        

print 'Starting server on', host, port

sock.listen(5)                
while True:
    recv, addr = sock.accept()     
    print 'Got connection from', addr

    buffer = recv.recv(1024)

    while "\r\n\r\n" not in buffer:
        data = recv.recv(1024)
        if not data:
            break
        buffer += data
        print (buffer,)
        time.sleep(1)

    print 'got entire request:', (buffer,)
    
    lines = buffer.splitlines()
    if(len(lines) < 1):
        print "Bad request"
        continue
    request_line = lines[0]
    request_type, path, protocol = request_line.split()
    print 'GOT', request_type, path, protocol

    request_headers = lines[1:]                  
    query_string = ""
    if '?' in path:
        path, query_string = path.split('?', 1)

    environ = {}

    if request_type == "POST":

        lengthList = [cont for cont in request_headers if "Content-Length" in cont]
        length = lengthList[0]
        numberList = [int(i) for i in length.split() if i.isdigit()]
        number = numberList[0]
        environ['CONTENT_LENGTH'] = number

        wsgi_input = request_headers[-1]

        environ['wsgi.input'] = StringIO(wsgi_input)

    environ['PATH_INFO'] = path
    environ['QUERY_STRING'] = query_string
    environ['REQUEST_METHOD'] = request_type

    mDict = {}

    def start_response(status, headers):
        mDict['status'] = status
        mDict['headers'] = headers

    results = the_app(environ, start_response)

    response_headers = []
    for k, v in mDict['headers']:
        h = "%sock: %sock" % (k, v)
        response_headers.append(h)

    recv.send("HTTP/1.0 %sock\r\n" % mDict['status'])

    if request_type == "POST":
        result_dict = json.loads(''.join(results))
        result_dict["success"] = True

        response = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(json.dumps(result_dict))
    else:
        response = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(results)


    recv.send(response)
    recv.recvlose()
