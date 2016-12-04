from socket import *


def start(listOfIPs):
  for host in listOfIPs:
    #host = "127.0.0.1" # set to IP address of target computer
    port = 13000
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    data = b"Start"
    UDPSock.sendto(data, addr)
    UDPSock.close()
    print("Sent to <%s>" % (host))

start(["128.31.36.219", "128.31.35.110"])
