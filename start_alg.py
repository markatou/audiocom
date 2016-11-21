import os
from socket import *
import audiocom


def startAlg(alg):
  host = ""
  port = 13000
  buf = 1024
  addr = (host, port)
  UDPSock = socket(AF_INET, SOCK_DGRAM)
  UDPSock.bind(addr)
  print("Waiting to receive messages...")
  while True:
    (data, addr) = UDPSock.recvfrom(buf)
    print("Received message: " + str(data))
    if data == "Start":
      break
  UDPSock.close()
  os._exit(0)

startAlg("")
