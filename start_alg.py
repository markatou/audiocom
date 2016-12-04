from config import Config  
from socket import *
import argparse
import playMusic


host = ""
port = 13000
buf = 1024

def start_alg(alg, config):
    print("Listening for start signal...")
    start = False

    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    while not start:
        (data, addr) = UDPSock.recvfrom(buf)
        print("Received message", data)
        if data == b"Start":
            start = True
    UDPSock.close()

    print('Calling alg')
    alg(config)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # Source and Sink options
    parser.add_argument("-S", "--src", type=str, default='1', help="payload (0, 1, step, random)")
    parser.add_argument("-n", "--nbits", type=int, default=512, help="number of data bits")

    # Phy-layer Transmitter and Receiver options
    parser.add_argument("-r", "--samplerate", type=int, default=48000, help="sample rate (Hz)")
    parser.add_argument("-i", "--chunksize", type=int, default=256, help="samples per chunk (transmitter)")
    parser.add_argument("-p", "--prefill", type=int, default=60, help="write buffer prefill (transmitter)")
    parser.add_argument("-s", "--spb", type=int, default=512, help="samples per bit")
    parser.add_argument("-c", "--channel", type=int, default=1000, help="lowest carrier frequency (Hz)")
    parser.add_argument("-c2", "--channel2", type=int, help="second carrier frequency (Hz)")
    parser.add_argument("-G", "--gap", type=int, default=500, help="channel gap (Hz)") # not used in PS5
    parser.add_argument("-q", "--silence", type=int, default=80, help="#samples of silence at start of preamble")
    parser.add_argument("-T", "--tone", action="store_true", help="don't use preamble")
    parser.add_argument("-t", "--threshold", type=float, help="threshold value")
    parser.add_argument("-w", "--window", type=float, default=.5, help="window for subsample")
    parser.add_argument("-L", "--avgwindow", type=int, help="window for averaging filter")

    parser.add_argument("--file", type=str, action="append", help="filename(s)")

    # Modulation (signaling) and Demodulation options
    parser.add_argument("-k", "--keytype", type=str, default="on_off", help="keying (signaling) scheme")
    parser.add_argument("-d", "--demod", type=str, default="quad", help="demodulation scheme (envelope, het, quad)")
    parser.add_argument("-f", "--filter", type=str, default="lp", help="filter type (avg)")
    parser.add_argument("-o", "--one", type=float, default=1.0, help="voltage level for bit 1")
    parser.add_argument("-z", "--zero", type=float, default=0.0, help="voltage level for bit 0 (ignored unless key type is custom)")

    # AbstractChannel options
    parser.add_argument("-a", "--abstract", action="store_true", help="use bypass channel instead of audio")
    parser.add_argument("-v", type=float, default=0.00, help="noise variance (for bypass channel)")
    parser.add_argument("-u", "--usr", type=str, default='1', help="unit step & sample response (h)")
    parser.add_argument("-l", "--lag", type=int, default=0, help="lag (for bypass channel)")

    # Miscellaneous
    parser.add_argument("-g", "--graph", type=str, choices=['time', 'freq', 'usr'], help="show graphs")
    parser.add_argument("--verbose", action="store_true", help="verbose debugging")

    # Options for which algorithm to start
    parser.add_argument('--log', action='store_true')
    parser.add_argument('--sync', action='store_true')
    parser.add_argument('--music', action='store_true')

    args = parser.parse_args()
    args.file = ["testfiles/A"]

    config = Config(args)

    if args.log:
        import log_log
        start_alg(log_log.run, config)

    elif args.sync:
        import sync_audiocom
        start_alg(sync_audiocom.run, config)
    
    elif args.music:
        import playMusic
        start_alg(playMusic.playM, "SomebodyInstrumental.wav")
