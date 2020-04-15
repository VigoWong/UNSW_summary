from socket import *
import sys
import datetime
import time


def UDPPingClient():
    # check the validity of the arguments
    if (len(sys.argv) != 3):
        print("Required arguments: host and port")
        sys.exit(1)
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except ValueError:
        print("Incorrect port!")
        sys.exit(1)

    i = 0
    ls = []
    for i in range(10):
        sock = socket(AF_INET, SOCK_DGRAM)
        # AF_INET is the socket of IPv4 protocol and SOCK_DGRAM is socket datagram

        sock.settimeout(1)
        # set the timeout criterion to 1 second

        try:
            begin = datetime.datetime.now()
            # record the time stamp of the start off of the packet
            message = "PING {0} {1} \r\n".format(str(i + 1), begin)
            # defind the ping message
            sock.sendto(message.encode(encoding='utf-8', errors='strict'),
                        (host, port))
            # sending request
            data, address = sock.recvfrom(1024)
            # receiving replies
            end = datetime.datetime.now()
            # record the end time stamp
            diff = '%.1f' % ((end - begin).microseconds / 1000.0)
            ls.append((end - begin).microseconds / 1000.0)
            # format the recv message
            recv = 'ping to {0}, seq = {1}, rtt = {2} ms'.format(
                host,
                str(i),
                diff
            )
        except timeout:
            # format the recv message
            recv = 'ping to {0}, seq = {1}, rtt = time out'.format(host, str(i))

        sock.close()
        # print the output
        print(recv)
        time.sleep(1)
    print(f"the maximum rtt: %.1f ms" % max(ls))
    print(f"the minimum rtt: %.1f ms" % min(ls))
    print(f"the average rtt: %.1f ms" % (sum(ls)/len(ls)))


if __name__ == '__main__':
    UDPPingClient()
