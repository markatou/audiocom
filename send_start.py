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

start(["18.62.19.207", "18.62.31.229", "18.62.22.204", "18.62.23.44", "18.62.23.47","18.62.23.48"])
