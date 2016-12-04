#!/usr/bin/env python
import pyaudio
import wave
from config import Config
from socket import *


host = ""
port = 13000
buf = 1024

def start_alg():
    print("Listening for start signal...")
    start = False

    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    filename = " "
    while not start:
        (data, addr) = UDPSock.recvfrom(buf)
        print("Received message", data)
        if data == b"voice":
            filename = "beatles_submarine/voix.wav"
    UDPSock.close()

    print('Calling alg')
    start_alg(filename)





def playM(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True)
    data = wf.readframes(chunk)

    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    p.terminate()
