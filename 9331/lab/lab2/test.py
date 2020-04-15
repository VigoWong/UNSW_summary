# import socket
#
# UDP_IP = "127.0.0.1"
# UDP_PORT = 5005
# MESSAGE = "Hello, World!"
#
# print("UDP target IP:", UDP_IP)
# print("UDP target port:", UDP_PORT)
# print("message:", MESSAGE)
#
# sock = socket.socket(socket.AF_INET,  # Internet
#                      socket.SOCK_DGRAM)  # UDP
# sock.sendto(MESSAGE.encode(encoding='utf_8', errors='strict'), (UDP_IP, UDP_PORT))

import time

def getMS():
    """get millisecond of now in string of length 3"""
    a = str(int(time.time()*1000)%1000)
    if len(a) == 1: return '00'+a
    if len(a) == 2: return '0'+a
    return a

def getTime():
    """get time in format HH:MM:SS:MS"""
    now = time.strftime('%S', time.localtime())
    return now + getMS()

print(getTime())