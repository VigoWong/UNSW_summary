# (i) create a connection socket when contacted by a client (browser).
#
# (ii) receive HTTP request from this connection. Your server should only process GET request. You may assume that only GET requests will be received.
#
# (iii) parse the request to determine the specific file being requested.
#
# (iv) get the requested file from the server's file system.
#
# (v) create an HTTP response message consisting of the requested file preceded by header lines.
#
# (vi) send the response over the TCP connection to the requesting browser.
#
# (vii) If the requested file is not present on the server, the server should send an HTTP “404 Not Found” message back to the client.
#
# (viii) the server should listen in a loop, waiting for next request from the browser.

# created by Haowei Huang on March 8th, 2020
import re
from socket import *
import sys
import os

HOST = '127.0.0.1'

resonse_pic = '''
HTTP/1.1 200 ok
Content-Type: image/png

'''

resonse_html = '''
HTTP/1.1 200 ok
Content-Type: text/html

'''

response_404 = '''
HTTP/1.1 404 Not Found
Content-Type: text/html

'''



def TCPservice():
    # check the validity of the arguments
    if (len(sys.argv) != 2):
        print("Required arguments: port")
        sys.exit(1)
    try:
        POST = int(sys.argv[1])
    except ValueError:
        print("Incorrect port!")
        sys.exit(1)

    # configuration
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((HOST, POST))
    server.listen(5)

    while True:
        connection, addr = server.accept()
        request = connection.recv(1024).decode()

        # in case of sudden abortion
        if not request:
            continue

        # extraction of request
        method = request.split(' ')[0]
        src = request.split(' ')[1]
        content = ''

        # deal wiht GET request
        if method == 'GET':
            src = src[1:]
            # check if the requested sorce exist in the server path
            if os.path.exists('./' + src):
                # deal with html request
                if re.match('^\w*.html$', src):
                    content = resonse_html.encode()
                    file = open(src, 'rb')
                    content += file.read()
                    file.close()
                # deal with picture request
                elif re.match('^\w*.png$', src):
                    content = resonse_pic.encode()
                    file = open(src, 'rb')
                    content += file.read()
                    file.close()
            else:
                # the requested file is not present on the server, then return a 404 response
                content = response_404.encode()
        else:
            continue

        # send the source for client
        connection.sendall(content)


if __name__ == '__main__':
    TCPservice()
