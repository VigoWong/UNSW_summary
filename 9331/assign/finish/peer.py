# Created by Haowei Huang on 6th April, 2020

from socket import *
import sys
from threading import *
import time
import re


# GlobalParameter inferred by the whole program
class GlobalParameter():
    timeout = 10
    IP_ADDRESS = "127.0.0.1"
    BASE_PORT = 12000
    BUFFERSIZE = 1024
    displaymessages = {
        "PingRequestSend": "Ping requests sent to Peers %d and %d",
        "PingRequestReceive": "Ping request message received from Peer %d",
        "PingResponse": "Ping response received from Peer %d",
        "PingTimeOut": "Peer %d is no longer alive.",
        "SuccessorRequest": "Peer %d Join request forwarded to my successor",
        "JoinReceive": "Peer %d Join request received",
        "SuccessorChanged": "Successor Change request received",
        "FirSuccchange": "My new first successor is Peer %d",
        "SecSuccchange": "My new second successor is Peer %d",
        "JoinAccepted": "Join request has been accepted ",
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


# UDP manager for peers
class UDPManager():
    def __init__(self, address, peer):
        '''
        manager initialization
        :param address: peer address
        :param peer: the peer object
        '''
        self.address = address
        self.peer = peer
        self.pingInterval = peer.pingInterval  # ping interval
        self.firSucctimeoutCount = 0  # counting of timeout times for first successor
        self.secSucctimeoutCount = 0  # counting of timeout times for second successor

    def pingSetup(self, msg, recv_address):
        '''
        init a thread to send ping message
        :param msg: the msg to be sent
        :param recv_address: the receiver address
        '''
        ping_sender = Thread(target=self.sendMessage, args=(msg.encode(), recv_address,), daemon=True)
        ping_sender.start()

    def sendMessage(self, msg, recv_address):
        '''
        udp socket set up and sending message
        :param msg: the msg to be sent
        :param recv_address: the receiver address
        '''
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.sendto(msg, recv_address)
        sock.close()

    def sendSetup(self, msg, recv_address):
        '''
        init a thread to send udp message
        :param msg: the msg to be sent
        :param recv_address: the receiver address
        '''
        udp_sender = Thread(target=self.sendMessage, args=(msg.encode(), recv_address,), daemon=True)
        udp_sender.start()

    def UDPListener(self):
        '''
        udp messages listener, initializing threads to handle msg
        '''
        sock = socket(AF_INET, SOCK_DGRAM)
        # bind the local address
        sock.bind(self.address)
        while True:
            # init a process for the udp message
            data, sender_addr = sock.recvfrom(GlobalParameter.BUFFERSIZE)
            # once receive a message, then init a thread to handle it
            Thread(target=self.UDPMessageHandler, args=(data.decode(), sender_addr, sock,), daemon=True).start()

    def UDPMessageHandler(self, data, sender_addr, sock):
        '''
        processing udp message
        :param data: data received from listener
        :param sender_addr: the address of the msg sender
        :param sock: socket of the listener
        :return:
        '''
        # ping request from first predsessor
        if re.match(r"first successor: ping request from \d+", data):
            # declaration of receiving a ping request
            sender_id = int(re.findall(r'\d+', data)[0])
            print(GlobalParameter.displaymessages["PingRequestReceive"] % sender_id)
            self.peer.firPred = sender_id
            reply = 'ping reply'
            sock.sendto(reply.encode(), sender_addr)
        # ping request from second predsessor
        elif re.match(r"second successor: ping request from \d+", data):
            # declaration of receiving a ping request
            sender_id = int(re.findall(r'\d+', data)[0])
            print(GlobalParameter.displaymessages["PingRequestReceive"] % sender_id)
            self.peer.secPred = sender_id
            reply = 'ping reply'
            sock.sendto(reply.encode(), sender_addr)
        else:
            pass

    def pingBeginner(self):
        '''
        ping beginner. it would be triggered once a peer join or being initialized
        '''
        while True:
            # check if a peer is still alive. If not, simply exit with code 0
            if self.peer.isAlive:
                print(GlobalParameter.displaymessages["PingRequestSend"] % (self.peer.firSucc, self.peer.secSucc))
                Thread(target=self.pingSending, args=(1,), daemon=True).start()
                Thread(target=self.pingSending, args=(0,), daemon=True).start()
                time.sleep(self.pingInterval)
            else:
                sys.exit(0)

    def pingSending(self, isFirst):
        '''
        sending ping request over UDP, receiving response and process timeout
        :param isFirst: determine which successor send ping request to
        '''
        con = socket(AF_INET, SOCK_DGRAM)
        con.settimeout(GlobalParameter.timeout)
        succ = self.peer.firSucc if isFirst else self.peer.secSucc  # the current successor
        port = GlobalParameter.BASE_PORT + succ  # corresponding port
        addr = (GlobalParameter.IP_ADDRESS, port)  # address of the ping receiver
        if isFirst:
            msg = 'first successor: ping request from %d' % (self.peer.peerID)  # ping message
        else:
            msg = 'second successor: ping request from %d' % (self.peer.peerID)  # ping message
        con.sendto(msg.encode(), addr)  # sending
        try:
            response, sender_addr = con.recvfrom(GlobalParameter.BUFFERSIZE)
            # if receiving a response reset the count of timeout
            if isFirst:
                self.firSucctimeoutCount = 0
            else:
                self.secSucctimeoutCount = 0
            # declaration of the ping request
            print(GlobalParameter.displaymessages["PingResponse"] % (succ))
            # close the connection when finished
            con.close()
        except timeout:
            if isFirst:
                self.firSucctimeoutCount += 1
                if self.firSucctimeoutCount > 2:
                    self.peer.detectedDeparture(succ, isFirst)
                # locking
            else:
                self.secSucctimeoutCount += 1
                if self.secSucctimeoutCount > 2:
                    self.peer.detectedDeparture(succ, isFirst)
                # locking
            # close the connection when finished
            con.close()


class TCPManager():
    def __init__(self, address, peer):
        '''
        manager initialization
        :param address: peer address
        :param peer: the peer object
        '''
        self.address = address
        self.peer = peer

    def sending(self, msg, recv_addr):
        '''
        sending TCP msg
        :param msg: msg to be sent
        :param recv_addr: the address of the receiver
        '''
        con = socket(AF_INET, SOCK_STREAM)
        con.connect(recv_addr)
        con.send(msg)
        con.close()

    def sendMessage(self, msg, recv_addr):
        '''
        initializing a thread to send msg
        :param msg: msg to be sent
        :param recv_addr: the address of the receiver
        '''
        Thread(target=self.sending, args=(msg.encode(), recv_addr,), daemon=True).start()

    def sendAndWait(self, msg, recv_addr):
        '''
        sending TCP msg and return the response
        :param msg: msg to be sent
        :param recv_addr: the address of the receiver
        :return: response from receiver
        '''
        con = socket(AF_INET, SOCK_STREAM)
        con.connect(recv_addr)
        con.send(msg.encode())
        response, addr = con.recvfrom(GlobalParameter.BUFFERSIZE)
        con.close()
        return response.decode()

    def TCPListener(self):
        '''
        initializing threads to listen to TCP communication request and process them
        '''
        con = socket(AF_INET, SOCK_STREAM)
        con.bind(self.peer.address)
        con.listen(5)
        while True:
            sock, sender_addr = con.accept()
            Thread(target=self.TCPMessageHandler, args=(sock,), daemon=True).start()

    def TCPMessageHandler(self, sock):
        '''
        processing TCP communication
        :param sock: the socket of listener
        '''

        # receiving msg from sender
        msg = sock.recv(GlobalParameter.BUFFERSIZE).decode()
        # possible TCP requests or messages:
        if re.match(r'Joining Request from \d+', msg):
            newpeer = int(re.findall(r'\d+', msg)[0])
            self.joinRequest(newpeer)
        elif re.match(r'successor changed: your first successor is \d+, second successor is \d+', msg):
            fir, sec = re.findall(r'\d+', msg)
            print(GlobalParameter.displaymessages["SuccessorChanged"])
            self.peer.firSucc = int(fir)
            self.peer.secSucc = int(sec)
            print(GlobalParameter.displaymessages["FirSuccchange"] % self.peer.firSucc)
            print(GlobalParameter.displaymessages["SecSuccchange"] % self.peer.secSucc)
        elif re.match(r'joining response: your first successor is \d+, second successor is \d+', msg):
            fir, sec = re.findall(r'\d+', msg)
            if fir == self.peer.peerID or sec == self.peer.peerID: pass  # duplicate notify
            print(GlobalParameter.displaymessages["JoinAccepted"])
            self.peer.firSucc = int(fir)
            self.peer.secSucc = int(sec)
            print(GlobalParameter.displaymessages["FirstInit"] % self.peer.firSucc)
            print(GlobalParameter.displaymessages["SecondInit"] % self.peer.secSucc)
        elif re.match(r'departure notice\(\d+\): your first successor is \d+, second successor is \d+', msg):
            departure_peer, fir, sec = re.findall(r'\d+', msg)
            print(GlobalParameter.displaymessages["DepartureNotice"] % int(departure_peer))
            self.peer.firSucc = int(fir)
            self.peer.secSucc = int(sec)
            print(GlobalParameter.displaymessages["FirSuccchange"] % self.peer.firSucc)
            print(GlobalParameter.displaymessages["SecSuccchange"] % self.peer.secSucc)
        elif re.match(r'abrupt departure detected: \d+', msg):
            msg = "accepted, my first successor is %d, my second successor is %d" % (
                self.peer.firSucc, self.peer.secSucc)
            sock.send(msg.encode())
        elif re.match(r'Store \d+', msg):
            self.peer.storeRequest(msg)
        elif re.match(r'Request \d+ from \d+', msg):
            self.peer.requestFileCommand(msg)
        elif re.match(r'destination: Request \d+ from \d+', msg):
            self.fileFoundAndSending(msg)
        elif re.match(r'file \d+ from peer \d+', msg):
            self.fileReceiving(msg, sock)
        else:
            pass

    def joinRequest(self, newpeer):
        '''
        procssing joining request from new peer
        :param newpeer: the new peer id of the joining requester
        '''

        if (newpeer < self.peer.firSucc and newpeer > self.peer.peerID) or (
                newpeer > self.peer.peerID and self.peer.firSucc < self.peer.peerID):  # reach the start point of the circle
            # if the new peer number greater than the current peer,
            # simply change the successor and declare it and response to the sender
            print(GlobalParameter.displaymessages["JoinReceive"] % (newpeer))
            print(GlobalParameter.displaymessages["FirSuccchange"] % (newpeer))
            print(GlobalParameter.displaymessages["SecSuccchange"] % (self.peer.firSucc))

            response_fornew = "joining response: your first successor is %d, second successor is %d" % (
                self.peer.firSucc, self.peer.secSucc)
            self.sendMessage(response_fornew, (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + newpeer))
            self.peer.secSucc = self.peer.firSucc
            self.peer.firSucc = newpeer

            while True:
                # send details to predecessor(if exist) and new peer
                if self.peer.firPred:
                    response_forpre = "successor changed: your first successor is %d, second successor is %d" % (
                        self.peer.peerID, newpeer)
                    self.sendMessage(response_forpre,
                                     (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + self.peer.firPred))
                    break
                else:
                    time.sleep(self.peer.pingInterval)

        else:
            # if the new peer number greater than the first successor,
            # send request to the first successor, and declare it
            print(GlobalParameter.displaymessages["SuccessorRequest"] % (newpeer))
            msg = 'Joining Request from ' + str(newpeer)
            self.sendMessage(msg, (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + self.peer.firSucc))

    def fileFoundAndSending(self, request):
        '''
        file request received and prepare to send the file to the requester
        :param request: file request
        '''

        # msg formatted 'destination: Request <FILE NO.> from <PEER>'
        if re.match(r'destination: Request \w+ from \w+', request):
            file, recv_peer = re.findall(r'\d+', request)
        else:
            file = re.findall(r'\d+', request)[0]
            recv_peer = self.peer.peerID
        print(GlobalParameter.displaymessages['FileFound'] % file)
        # file name formatted '<file>.pdf'
        file_name = file + '.pdf'
        recv_peer = int(recv_peer)

        # prepare to send the file
        con = socket(AF_INET, SOCK_STREAM)
        recv_addr = (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + recv_peer)
        # build a TCP connection
        con.connect(recv_addr)
        msg = 'file %s from peer %d' % (file, self.peer.peerID)  # connection request
        con.send(msg.encode())
        response, addr = con.recvfrom(GlobalParameter.BUFFERSIZE)
        # connection is ready
        if response.decode() == 'agree':
            # begin to send file
            print(GlobalParameter.displaymessages["FileSending"] % (file, recv_peer))
            try:
                with open(file_name, 'rb') as f:
                    while True:
                        file_data = f.read(GlobalParameter.BUFFERSIZE)
                        if file_data:
                            con.send(file_data)
                        else:
                            # finish
                            break
                print(GlobalParameter.displaymessages["FileSendingFinish"])
            except Exception as e:
                print("sending error:", e)  # bug
            con.close()

    def fileReceiving(self, msg, sock):
        '''
        # get ready to receive the file, msg formatted 'file <File_NO> from peer <Sender(peer)>'
        :param msg: the msg of file transmitting approval
        :param sock: the socket of the TCP connection
        '''
        file_name, sender = re.findall(r'\d+', msg)
        print(GlobalParameter.displaymessages['FileLocation'] % (int(sender), file_name))
        file = 'received_' + file_name + '.pdf'
        try:
            # create a file and ready to write in
            with open(file, 'wb') as f:
                sock.send('agree'.encode())
                print(GlobalParameter.displaymessages['FileReceiving'] % (file_name, int(sender)))
                while True:
                    # receiving data
                    file_data = sock.recv(GlobalParameter.BUFFERSIZE)
                    if file_data:
                        f.write(file_data)
                    else:
                        # finish
                        break
            # received the file
            print(GlobalParameter.displaymessages["FileReceived"] % file_name)
        except Exception as e:
            print('error', e)  # bug
            return


class Peer():

    def __init__(self):
        self.peerID = None
        self.address = None  # address is formatted ('localhost' , BASE_PORT + peerID)
        self.firSucc = None
        self.secSucc = None
        self.pingInterval = None

        self.firPred = None  # it would be specified after ping command
        self.secPred = None  # it would be specified after receiving ping command
        self.isAlive = True

    def InitPeer(self, peerID, firSucc, secSucc, pingInterval):
        '''
        initial request processing
        :param peerID: the id of the peer
        :param firSucc: the type in first successor
        :param secSucc: the type in second successor
        :param pingInterval: the interval of ping request
        '''
        self.peerID = peerID
        self.firSucc = firSucc
        self.secSucc = secSucc
        self.pingInterval = pingInterval
        self.address = (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + self.peerID)

        self.TCPManager = TCPManager(self.address, self)  # cope with tcp message sending and receiving
        self.UDPManager = UDPManager(self.address, self)  # cope with udp message sending and receiving

        # process UDP request
        Thread(target=self.UDPManager.UDPListener, daemon=True).start()
        # process TCP request
        Thread(target=self.TCPManager.TCPListener, daemon=True).start()
        # terminal input
        Thread(target=self.clientInput, daemon=False).start()

    def joinPeer(self, peerID, knownpeer, pingInterval):
        '''
        processing joining request
        :param peerID: the id of the peer
        :param knownpeer: the type in known peer
        :param pingInterval: the type in known peer
        :return:
        '''
        self.peerID = int(peerID)
        self.address = (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + self.peerID)
        self.pingInterval = int(pingInterval)

        self.TCPManager = TCPManager(self.address, self)  # cope with tcp message sending and receiving
        self.UDPManager = UDPManager(self.address, self)  # cope with udp message sending and receiving

        # process UDP request
        Thread(target=self.UDPManager.UDPListener, daemon=True).start()
        # process TCP request
        Thread(target=self.TCPManager.TCPListener, daemon=True).start()
        # terminal input
        Thread(target=self.clientInput, daemon=False).start()

        msg = 'Joining Request from %d' % self.peerID
        recv_addr = (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + knownpeer)

        self.TCPManager.sendMessage(msg, recv_addr)
        count = 0
        try:
            while True:
                if count > 2:
                    sys.exit(1)
                time.sleep(10)
                if self.firSucc and self.secSucc: break
                print("something happen, retransmitting the joining request")
                self.TCPManager.sendMessage(msg, recv_addr)
                count += 1
        except Exception:
            sys.exit(1)

    def detectedDeparture(self, succ, isFirst):
        '''
        processing abrupt departure of succsssor
        :param succ: the successor ip that left
        :param isFirst: verify which successor
        '''

        # declare that the successor no longer exist
        print(GlobalParameter.displaymessages["PingTimeOut"] % (succ))
        if isFirst:
            msg = 'abrupt departure detected: %d' % succ
            addr = (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + self.secSucc)
            reply = self.TCPManager.sendAndWait(msg, addr)
            fir, sec = re.findall(r'\d+', reply)
            self.firSucc = self.secSucc
            self.secSucc = int(fir)
            print(GlobalParameter.displaymessages['FirSuccchange'] % self.firSucc)
            print(GlobalParameter.displaymessages['SecSuccchange'] % self.secSucc)
        else:
            msg = 'abrupt departure detected: %d' % succ
            addr = (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + self.firSucc)
            reply = self.TCPManager.sendAndWait(msg, addr)
            fir, sec = re.findall(r'\d+', reply)
            if int(fir) == succ:
                self.secSucc = int(sec)
            else:
                self.secSucc = int(fir)
            print(GlobalParameter.displaymessages['FirSuccchange'] % self.firSucc)
            print(GlobalParameter.displaymessages['SecSuccchange'] % self.secSucc)

    def gracefulDeparture(self):
        '''
        processing graceful departure request
        '''
        # notifying the departure to first predecessor by TCP message
        if self.firPred:
            firPredAddr = (GlobalParameter.IP_ADDRESS, self.firPred + GlobalParameter.BASE_PORT)
            msg = 'departure notice(%d): your first successor is %d, second successor is %d' % (
                self.peerID, self.firSucc, self.secSucc)
            self.TCPManager.sendMessage(msg, firPredAddr)

        # notifying second predecessor of the departure by TCP message
        if self.secPred:
            secPreAddr = (GlobalParameter.IP_ADDRESS, self.secPred + GlobalParameter.BASE_PORT)
            msg = 'departure notice(%d): your first successor is %d, second successor is %d' % (
                self.peerID, self.firPred, self.firSucc)
            self.TCPManager.sendMessage(msg, secPreAddr)

        self.isAlive = False

    def clientInput(self):
        '''
        terminal input monitor
        '''

        while True:
            command = input()
            if command == 'Quit':
                self.gracefulDeparture()
                sys.exit(0)
            if re.match(r'Store \w+', command):
                self.storeRequest(command)
            if re.match(r'Request \w+', command):
                self.requestFileCommand(command)
            else:
                continue

    def storeRequest(self, storeRequest):
        '''
        processing file story request from terminal
        :param storeRequest: storing Request
        '''

        # store request is formatted "Store <file_NO.>"
        file_No = storeRequest.split()[1]
        if file_No.isalnum():
            index = int(file_No) % 256
            if index == self.peerID or (self.firPred < index and self.peerID > index) or \
                    (self.peerID < self.firPred and index > self.firPred):
                print(GlobalParameter.displaymessages["StoreAccepted"] % file_No)
                pass  # bug
            else:
                # sending store request to successor
                print(GlobalParameter.displaymessages["StoreRequest"] % file_No)
                firSuccAddr = (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + self.firSucc)
                self.TCPManager.sendMessage(storeRequest, firSuccAddr)
        else:
            print('incorrect input')

    def requestFileCommand(self, fileRequest):
        '''
        processing file transmission request from terminal or other peer
        :param fileRequest:
        '''
        file = fileRequest.split()[1]
        firSuccAddr = (GlobalParameter.IP_ADDRESS, GlobalParameter.BASE_PORT + self.firSucc)
        if file.isalnum():
            index = int(file) % 256
            # if index match the peer id
            if index == self.peerID:
                print(GlobalParameter.displaymessages["FileFound"] % file)
                self.TCPManager.fileFoundAndSending(fileRequest)
            # if index greater than first successor and less than peer id,
            # then first successor is the destination
            elif (index < self.firSucc and index > self.peerID) or \
                    (index > self.peerID and self.peerID > self.firSucc) or \
                    (index == self.firSucc):
                # sending file request to successor
                print(GlobalParameter.displaymessages["FileRequest"] % file)
                # msg format: 'destination: Request <file> from <peer>'
                if re.match(r'Request \w+ from \w+', fileRequest):
                    msg = 'destination: ' + fileRequest
                else:
                    msg = 'destination: ' + fileRequest + ' from %d' % (self.peerID)
                self.TCPManager.sendMessage(msg, firSuccAddr)
            else:
                # sending file request to successor
                print(GlobalParameter.displaymessages["FileRequest"] % file)
                if re.match(r'Request \w+ from \w+', fileRequest):
                    self.TCPManager.sendMessage(fileRequest, firSuccAddr)
                else:
                    # msg format: 'Request <file> from <peer>'
                    msg = fileRequest + ' from %d' % (self.peerID)
                    self.TCPManager.sendMessage(msg, firSuccAddr)
        else:
            # when file format is invalid(bug)
            print('incorrect input')


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

    # cope with initial request
    if sys.argv[1] == 'init':
        # init a peer for the process
        peer = Peer()
        peerID = int(sys.argv[2])
        firSucc = int(sys.argv[3])
        secSucc = int(sys.argv[4])
        pingInterval = int(sys.argv[5])
        # initialization
        peer.InitPeer(peerID, firSucc, secSucc, pingInterval)
        # begin to ping successor once initialized
        peer.UDPManager.pingBeginner()

    # cope with joining request
    if sys.argv[1] == 'join':
        peer = Peer()
        peerID = int(sys.argv[2])
        knownPeer = int(sys.argv[3])
        pingInterval = int(sys.argv[4])
        peer.joinPeer(peerID, knownPeer, pingInterval)
        # begin to ping successor once initialized
        peer.UDPManager.pingBeginner()
