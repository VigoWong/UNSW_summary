# Created by Vigo on 20th March, 2020

# coding: utf-8
from socket import *
import sys
from threading import *
import time
import datetime as dt
import re

IP_ADDRESS = "127.0.0.1"
BASE_PORT = 12000
BUFFERSIZE = 1024


class Peer():
    # initialization of a peer class
    def __init__(self, peer_arr, ifinit=True):
        if ifinit:
            self.peerID = peer_arr[0]
            self.firSucc = peer_arr[1]
            self.secSucc = peer_arr[2]
            self.pingInterval = peer_arr[3]
        else:
            self.peerID = peer_arr[0]
            self.pingInterval = peer_arr[2]
            # acquire the corresponding first and second successor
            self.acquireSucc(peer_arr[1])

        self.firSuccCount = 0
        self.secSuccCount = 0
        self.firPred = None  # it would be specified after ping command
        self.secPred = None  # it would be specified after receiving ping command

        self.displaymessages = {
            "PingRequestSend": "Ping requests sent to Peers %d and %d",
            "PingRequestReceive": "Ping request message received from Peer %d",
            "PingResponse": "Ping response received from Peer %d",
            "PingTimeOut": "Peer %d is no longer alive.",
            "SuccessorRequest": "Peer %d Join request forwarded to my successor",
            "JoinReceive": "Peer %d Join request received",
            "SuccessorChanged": "Successor Change request received",
            "FirSuccchange": "My new first successor is Peer %d",
            "SecSuccchange": "My new second successor is Peer %d",
            "JoinAccepted": "Successor Change request received",
            "FirstInit": "My first successor is Peer %d",
            "SecondInit": "My second successor is Peer %d",
            "DepartureNotice": "Peer %d will depart from the network",
            "StoreRequest": "Store %s request forwarded to my successor",
            "StoreAccepted": "Store %s request accepted",
            "FileFound": "File %s is stored here",
            "FileLocation": "Peer %d had File %s",
            "FileSending": "Sending file %s to Peer %d",
            "FileSendingFinish": "The file has been sent",
            "FileRequest": "File request for %s has been sent to my successor",
            "FileNotFound": "Request for File %s has been received, but the file is not stored here",
            "FileReceiving": "Receiving File %s from Peer %d",
            "FileReceived": "File %s received",
        }

        # threads for backend and frontend
        # terminal input
        Thread(target=self.clientInput, daemon=False).start()
        # process UDP request
        Thread(target=self.UDPlistener, daemon=True).start()
        # process TCP request
        Thread(target=self.TCPlistener, daemon=True).start()
        # sending ping request for first successor regularly
        Thread(target=self.pingManager, args=(True,), daemon=True).start()
        # sending ping request for second successor regularly
        Thread(target=self.pingManager, args=(False,), daemon=True).start()

    # listening to the possible UDP message
    def UDPlistener(self):
        con = socket(AF_INET, SOCK_DGRAM)
        local_addr = (IP_ADDRESS, BASE_PORT + self.peerID)
        con.bind(local_addr)

        while True:
            data, addr = con.recvfrom(BUFFERSIZE)
            Thread(target=self.UDPHandler, args=(addr, data.decode(), con)).start()

    # process UDP request
    def UDPHandler(self, addr, data, con):
        # possible requests or messages:
        # 1. ping
        if re.match(r"first successor: ping request from \d+", data):
            peer_sender = re.findall(r'\d+', data)
            # declaration of receiving a ping request
            print(self.displaymessages["PingRequestReceive"] % int(peer_sender[0]))
            self.firPred = int(peer_sender[0])
            reply = 'ping reply'
            con.sendto(reply.encode(), addr)
        elif re.match(r"second successor: ping request from \d+", data):
            peer_sender = re.findall(r'\d+', data)
            # declaration of receiving a ping request
            print(self.displaymessages["PingRequestReceive"] % int(peer_sender[0]))
            self.secPred = int(peer_sender[0])
            reply = 'ping reply'
            con.sendto(reply.encode(), addr)

        else:
            pass

    # listening to the possible TCP connection request
    def TCPlistener(self):
        con = socket(AF_INET, SOCK_STREAM)
        local_addr = (IP_ADDRESS, BASE_PORT + self.peerID)
        con.bind(local_addr)
        con.listen(5)

        while True:
            sock, addr = con.accept()
            Thread(target=self.TCPHandler, args=(sock,)).start()

    # process the TCP connection
    def TCPHandler(self, sock):
        data = sock.recv(BUFFERSIZE).decode()
        # possible TCP requests or messages:
        # 1. peer join 2. peer departure 3. data retrieval
        if re.match(r'Joining Request from \d+', data):
            peer = re.findall(r'\d+', data)
            self.joinRequest(peer[0])
        elif re.match(r'successor changed: your first successor is \d+, second successor is \d+', data):
            fir, sec = re.findall(r'\d+', data)
            print(self.displaymessages["SuccessorChanged"])
            self.firSucc = int(fir)
            self.secSucc = int(sec)
            print(self.displaymessages["FirSuccchange"] % self.firSucc)
            print(self.displaymessages["SecSuccchange"] % self.secSucc)
        elif re.match(r'joining response: your first successor is \d+, second successor is \d+', data):
            fir, sec = re.findall(r'\d+', data)
            print(self.displaymessages["JoinAccepted"])
            self.firSucc = int(fir)
            self.secSucc = int(sec)
            print(self.displaymessages["FirstInit"] % self.firSucc)
            print(self.displaymessages["SecondInit"] % self.secSucc)
        elif re.match(r'departure notice(\d+): your first successor is \d+, second successor is \d+', data):
            peer, fir, sec = re.findall(r'\d+', data)
            print(self.displaymessages["DepartureNotice"] % peer)
            self.firSucc = int(fir)
            self.secSucc = int(sec)
            print(self.displaymessages["FirSuccchange"] % self.firSucc)
            print(self.displaymessages["SecSuccchange"] % self.secSucc)
        elif re.match(r'abrupt departure detected: \d+', data):
            msg = "accepted, my first successor is %d, my second successor is %d" % (self.firSucc, self.secSucc)
            sock.send(msg.encode())
        elif re.match(r'Store \d+', data):
            self.storeRequest(data)
        elif re.match(r'Request \d+ from \d+', data):
            self.requestFile(data)
        elif re.match(r'file \d+ from peer \d+', data):
            self.fileReceiving(data, sock)
        else:
            pass

    # process file transfer request
    def fileReceiving(self, data, sock):
        # get ready to receive the file
        file_name, sender = re.findall(r'\d+', data)
        print(self.displaymessages['FileLocation'] % (int(sender), file_name))
        print(self.displaymessages['FileReceiving'] % (file_name, int(sender)))
        file = 'received_' + file_name + '.pdf'
        try:
            with open(file, 'wb') as f:
                sock.send('agree')
                while True:
                    # receiving data
                    file_data = sock.recv(BUFFERSIZE)
                    if file_data:
                        f.write(file_data)
                    else:
                        # finish
                        break
        except Exception as e:
            print('error', e)  # bug
            return
        else:
            print(self.displaymessages["FileReceived"] % file_name)
            # bug

    # process file store request
    def storeRequest(self, data):
        file = str(re.findall(r'\d+', data)[0])
        if file.isalnum() and len(file) == 4:
            index = int(file) % 256
            if index == self.peerID or (self.firPred < index and self.peerID > index):
                print(self.displaymessages["StoreAccepted"] % file)
                pass  # bug
            else:
                # sending store request to successor
                print(self.displaymessages["StoreRequest"] % file)
                con = socket(AF_INET, SOCK_STREAM)
                addr = (IP_ADDRESS, BASE_PORT + self.firSucc)
                con.connect(addr)
                con.send(data.encode())
                con.close()
                pass  # bug

    # sending joining request
    def acquireSucc(self, known_peer):
        # acquire the first and second successor by sending TCP request to the known peer
        con = socket(AF_INET, SOCK_STREAM)
        addr = (IP_ADDRESS, BASE_PORT + known_peer)
        con.connect(addr)
        msg = 'Joining Request from ' + str(self.peerID)
        con.send(msg.encode())
        con.close()

    def gracefulDeparture(self):
        # notifying the departure to first predecessor by TCP message
        msg = 'departure notice(%d): your first successor is %d, second successor is %d' % (
            self.peerID, self.firSucc, self.secSucc)
        con = socket(AF_INET, SOCK_STREAM)
        addr = (IP_ADDRESS, BASE_PORT + self.firPred)
        con.connect(addr)
        con.send(msg.encode())
        con.close()

        # notifying the departure to second predecessor by TCP message
        msg = 'departure notice(%d): your first successor is %d, second successor is %d' % (
            self.peerID, self.firPred, self.firSucc)
        con = socket(AF_INET, SOCK_STREAM)
        addr = (IP_ADDRESS, BASE_PORT + self.secPred)
        con.connect(addr)
        con.send(msg.encode())
        con.close()

    def requestFile(self, data):
        file, requester = re.findall(r'\d+', data)
        requester = int(requester)
        if file.isalnum() and len(file) == 4:
            index = int(file) % 256
            if index == self.peerID or (self.firPred < index and self.peerID > index):
                # file founded
                file_name = file + '.pdf'
                print(self.displaymessages["FileFound"] % file)
                # begin to build connection with requester
                msg = 'file %s from peer %d' % (file, self.peerID)  # connection request
                con = socket(AF_INET, SOCK_STREAM)
                addr = (IP_ADDRESS, BASE_PORT + requester)
                con.connect(addr)
                con.send(msg.encode())
                response, addr = con.recvfrom(BUFFERSIZE)
                # connection is built
                if response.decode() == 'agree':
                    # begin to send file
                    print(self.displaymessages["FileSending"] % (file, requester))
                    try:
                        with open(file_name, 'rb') as f:
                            while True:
                                file_data = f.read(BUFFERSIZE)
                                if file_data:
                                    con.send(file_data)
                                else:
                                    # finish
                                    print(self.displaymessages["FileSendingFinish"])
                    except Exception as e:
                        print("sending error:", e)#bug
                    con.close()
                else:
                    return  # connection request is rejected

            else:
                # sending store request to successor
                print(self.displaymessages["FileNotFound"] % file)
                con = socket(AF_INET, SOCK_STREAM)
                addr = (IP_ADDRESS, BASE_PORT + self.firSucc)
                con.connect(addr)
                con.send(data.encode())
                con.close()
                pass  # bug

    # process screen/terminal input(departure, etc.)
    def clientInput(self):
        while True:
            command = input()
            if command == 'Quit':
                t = Thread(target=self.gracefulDeparture, args=())
                t.start()
                t.join()
                sys.exit(0)
            if re.match(r'Store \d+', command):
                self.storeRequest(command)
            if re.match(r'Request \d+', command):
                file = re.findall(r'\d+', command)[0]
                if file.isalnum() and len(file) == 4:
                    index = int(file) % 256
                    if index == self.peerID or (self.firPred < index and self.peerID > index):
                        print(self.displaymessages["FileFound"] % file)
                        pass  # bug
                    else:
                        # sending file request to successor
                        print(self.displaymessages["FileRequest"] % file)
                        # msg format: 'Request <file> from <peer>'
                        msg = command + ' from %d' % (self.peerID)
                        con = socket(AF_INET, SOCK_STREAM)
                        addr = (IP_ADDRESS, BASE_PORT + self.firSucc)
                        con.connect(addr)
                        con.send(msg.encode())
                        con.close()
                        pass  # bug
                else:
                    continue  # file format is invalid(bug)



            else:
                continue

    # process joining request
    def joinRequest(self, newpeer):
        if (newpeer < self.firSucc and newpeer > self.peerID) or \
                (newpeer > self.firSucc and self.firSucc < self.peerID):  # reach the start point of the circle
            # if the new peer number greater than the current peer,
            # simply change the successor and declare it and response to the sender
            print(self.displaymessages["JoinReceive"] % (newpeer))
            print(self.displaymessages["FirSuccchange"] % (newpeer))
            print(self.displaymessages["SecSuccchange"] % (self.secSucc))
            self.secSucc = self.firSucc
            self.firSucc = newpeer

            # send details to predecessor and new peer
            response_fornew = "joining response: your first successor is %d, second successor is %d" % (
                self.firSucc, self.secSucc)
            response_forpre = "successor changed: your first successor is %d, second successor is %d" % (
                self.peerID, newpeer)

            # for new peer
            con = socket(AF_INET, SOCK_STREAM)
            addr = (IP_ADDRESS, BASE_PORT + newpeer)
            con.connect(addr)
            con.send(response_fornew.encode())
            con.close()

            # for predecessor
            con = socket(AF_INET, SOCK_STREAM)
            addr = (IP_ADDRESS, BASE_PORT + self.firPred)
            con.connect(addr)
            con.send(response_forpre.encode())
            con.close()

        else:
            # if the new peer number greater than the first successor,
            # send request to the first successor, and declare it
            print(self.displaymessages["SuccessorRequest"] % (newpeer))
            con = socket(AF_INET, SOCK_STREAM)
            addr = (IP_ADDRESS, BASE_PORT + self.firSucc)
            con.connect(addr)
            msg = 'Successor Request from ' + str(newpeer)
            con.send(msg.encode())

            # # receiving response and response to predecessor
            # data = con.recv(BUFFERSIZE)
            # sock.send(data)

            # terminate the connection with successor
            con.close()

    # sending ping request to successors
    def pingManager(self, isFirst):
        # use UDP for pinging
        con = socket(AF_INET, SOCK_DGRAM)
        # by default, the timeout criteria is set to 5.0s
        con.settimeout(1.5 * self.pingInterval)

        # ping successors regularly
        while True:
            succ = self.firSucc if isFirst else self.secSucc  # the current successor
            port = BASE_PORT + succ  # corresponding port
            addr = (IP_ADDRESS, port)  # address of the ping receiver

            if isFirst:
                print(self.displaymessages["PingRequestSend"] % (self.firSucc, self.secSucc))
                msg = 'first successor: ping request from %d' % (self.peerID)  # ping message
            else:
                msg = 'second successor: ping request from %d' % (self.peerID)  # ping message

            con.sendto(msg.encode(), addr)  # sending

            try:
                response, addr_from = con.recvfrom(BUFFERSIZE)

                # if receiving a response
                # reset the count of timeout
                if isFirst:
                    self.firSuccCount = 0
                else:
                    self.secSuccCount = 0

                # declaration of the ping request
                print(self.displaymessages["PingResponse"] % (succ))

            except timeout:
                if isFirst:
                    self.firSuccCount += 1
                    if self.firSuccCount > 1:
                        self.detectedDeparture(succ, isFirst)

                else:
                    self.secSuccCount += 1
                    if self.secSuccCount > 1:
                        self.detectedDeparture(succ, isFirst)

            except ConnectionResetError:
                continue

            # set the frequency to send a ping command
            time.sleep(self.pingInterval)

        # close the connection when finished
        con.close()

    def detectedDeparture(self, departPeer, isFirst):
        # declare that the successor no longer exist
        print(self.displaymessages["PingTimeOut"] % (departPeer))
        if isFirst:
            msg = 'abrupt departure detected: %d' % departPeer
            con = socket(AF_INET, SOCK_STREAM)
            addr = (IP_ADDRESS, BASE_PORT + self.secSucc)
            con.connect(addr)
            con.send(msg.encode())

            # data format: "accepted, my first successor is %d, my second successor is %d"
            data, addr_1 = con.recvfrom(BUFFERSIZE)
            fir, sec = re.findall(r"\d+", data.decode())
            con.close()

            self.firSucc = self.secSucc
            self.secSucc = int(fir)
            print(self.displaymessages["FirSuccchange"] % (self.firSucc))
            print(self.displaymessages["SecSuccchange"] % (self.secSucc))
        else:
            msg = 'abrupt departure detected: %d' % departPeer
            con = socket(AF_INET, SOCK_STREAM)
            addr = (IP_ADDRESS, BASE_PORT + self.firSucc)
            con.connect(addr)
            con.send(msg.encode())

            # data format: "accepted, my first successor is %d, my second successor is %d"
            data, addr_1 = con.recvfrom(BUFFERSIZE)
            fir, sec = re.findall(r"\d+", data.decode())
            con.close()

            if fir != departPeer:
                self.secSucc = int(fir)
            else:
                self.secSucc = int(sec)
            print(self.displaymessages["FirSuccchange"] % (self.firSucc))
            print(self.displaymessages["SecSuccchange"] % (self.secSucc))


if __name__ == '__main__':
    # check parameters
    try:
        if (len(sys.argv) < 2):
            raise TypeError
        if sys.argv[1] == 'init':
            if (len(sys.argv) != 6):
                raise TypeError
            if (int(sys.argv[2]) < 0 or int(sys.argv[2]) > 255
                    or int(sys.argv[3]) < 0 or int(sys.argv[4]) < 0
                    or int(sys.argv[5]) < 0):
                raise ValueError

        elif sys.argv[1] == 'join':
            if (len(sys.argv) != 5):
                raise TypeError
            if (int(sys.argv[2]) < 0 or int(sys.argv[2]) > 255
                    or int(sys.argv[3]) < 0 or int(sys.argv[4]) < 0):
                raise ValueError
        else:
            raise ValueError

    except ValueError:
        print("Parameter Errors !")
        sys.exit(-1)

    except TypeError:
        print("TypeError: missing required positional argument...")
        sys.exit(-1)

    peer_arr = [int(sys.argv[i]) for i in range(2, len(sys.argv))]
    if sys.argv[1] == 'init':
        process = Peer(peer_arr, ifinit=True)

    if sys.argv[1] == 'join':
        process = Peer(peer_arr, ifinit=False)
