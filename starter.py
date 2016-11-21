import os
from socket import *


def start(listOfIPs):
  for host in listOfIPs:
    #host = "127.0.0.1" # set to IP address of target computer
    port = 13000
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    print("Sending")
    while True:
      data = "Start"
      UDPSock.sendto(data, addr)
      if data == "Start":
        break
    UDPSock.close()
    os._exit(0)
  return "Done"  

start(["18.62.27.147"])
