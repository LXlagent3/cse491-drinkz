
import sys
import socket

def main(args):

    address = args[1]
    port = args[2]

    #create the socket
    mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    mSocket.connect((address, int(port)))

    mSocket.send("GET / HTTP/1.0\r\n\r\n")
    text = ""
    while True:
        buf = mSocket.recv(1000)
        if not buf:
            break
        text+=buf
    #end the socket
    mSocket.close()

def form(args):

    address = args[1]
    port = args[2]

    mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    mSocket.connect((address, int(port)))

    mSocket.send("GET /recv?add=4&to=6 HTTP/1.0\r\n\r\n")
    text = ""
    while 1:
        buf = mSocket.recv(1000)
        if not buf:
            break
        text+=buf

    mSocket.close()

def image(args):

    address = args[1]
    port = args[2]

    mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    mSocket.connect((address, int(port)))

    mSocket.send("GET /helmet HTTP/1.0\r\n\r\n")
    fp = mSocket.makefile("request_image")
    for line in fp:
        if "Content-Length: " in line:
           length = int(line.strip("Content-Length: "))
           break
        
    fp2 = open("Spartan-helmet-Black-150-pxls.gif","r")
    text2 = ""
    for line in fp2:
        text2+=line
    
    mSocket.close()
   
if __name__ == '__main__':
    form(sys.argv)
    image(sys.argv)
    main(sys.argv)
        
        
    
       
   
