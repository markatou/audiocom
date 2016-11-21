#!/usr/bin/python

'''Defines main() for Audiocom, which parses arguments and calls
run().  run() constructs an array of bits, which are pre-pended with a
preamble, converted to samples, modulated, and sent across the
channel.  On the receiving end, samples are demodulated and filtered,
digitized, and converted back to their original source.'''

import argparse
import numpy
import sys
import random
import graphs
import util
import time
from audio_channel import AudioChannel
from abstract_channel import AbstractChannel
from config import Config
from preamble import Preamble
from receiver import Receiver
from sender import Sender
from sink import Sink
from source import Source
import datetime

def run(config):
    modulated_samples, channel, sources  = makeChannel(config)

    # Listen for start signal
    print("Listening for start signal...")
    start = False
    while not start:
        start = listen(config, 20*modulated_samples, channel, sources, "Mens et manus.\n")

    print("Starting leader election")

    active = True
    round_number = 0
    time = datetime.datetime.now()

    while active and round_number < 20:
        # Round are ~10 seconds each
        if (datetime.datetime.now() - time).total_seconds() > 10:
            time = datetime.datetime.now()
            if random.random() > 0.5:
                print("Sending message")
                send(config, modulated_samples, channel, sources)
            else:
                print("Listening for message")
                active = not listen(config, modulated_samples, channel, sources, "Mens et manus.\n")

            print("Active ? : <%s>" % (active))
            print("Round Number : <%d>" % (round_number))
            round_number += 1

def send_start(config):
    modulated_samples, channel, sources  = makeChannel(config)
    print("Sending start signal!!")

    for i in range(5):
        time.sleep(5)
        send(config, modulated_samples, channel, sources)

def makeChannel(config):
    # Create the preamble to pre-pend to the transmission
    preamble = Preamble(config)

    # Create the sources
    sources = {}
    for i in range(len(config.channels)):
        frequency = config.channels[i]
        source = Source(config, i)
        print("Channel: %d Hz" % frequency)
        print("\n".join(["\t%s" % source]))
        sources[frequency] = source

    # Create a sender for each source, so we can process the bits to
    # get the modulated samples.  We combine all of the modulated
    # samples into a single array by adding them.

    baseband_samples = []
    modulated_samples = []

    for frequency in sources:
        src = sources[frequency]
        sender = Sender(frequency, preamble, config)
        sender.set_source(src)

        modulated_samples = util.add_arrays(sender.modulated_samples(), modulated_samples)
        baseband_samples = util.add_arrays(sender.bits_to_samples(src.payload), baseband_samples)

    # Create the channel
    if config.bypass:
        channel = AbstractChannel(config.bypass_noise, config.bypass_h, config.bypass_lag)
    else:
        channel = AudioChannel(config)
    return modulated_samples, channel, sources

    
        
def send(config, modulated_samples, channel, sources):

    # Transmit and receive data on the channel.  The received samples
    # (samples_rx) have not been processed in any way.

    samples_rx = channel.xmit(modulated_samples)
    print('Sent the samples')

def listen(config, modulated_samples, channel, sources, message):
    ''' Listen for message and return True if message was recieved. '''

    preamble = Preamble(config)
    samples_rx = channel.recv(4*modulated_samples)
    print('Received', len(samples_rx), 'samples')

    for frequency in config.channels:
        r = Receiver(frequency, preamble, config)
        try:
            # Call the main receiver function.  The returned array of bits
            # EXCLUDES the preamble.
            bits  = r.process(samples_rx)
    
            # Push into a Sink so we can convert back to a useful payload
            # (this step will become more useful when we're transmitting
            # files or images instead of just bit arrays)
            src = sources[frequency]
            sink = Sink(src)
            received_payload = sink.process(bits)
            print("Received %d data bits" % len(received_payload))

            if src.type == Source.TEXT:
                print("Received text was:", sink.received_text)
                if ((str(sink.received_text)) == message):
                    return True
 
            if len(received_payload) > 0:
                # Output BER
                hd = util.hamming(received_payload, src.payload)
                ber = float(hd)/len(received_payload)
                print('BER:', ber)
            else:
                print('Could not recover transmission.')

        except Exception as e:
            print(repr(e))
    return False

def elect(config):
    '''Primary Audiocom functionality.'''

    # Create the preamble to pre-pend to the transmission
    preamble = Preamble(config)

    # Create the sources
    sources = {}
    for i in range(len(config.channels)):
        frequency = config.channels[i]
        source = Source(config, i)
        print("Channel: %d Hz" % frequency)
        print("\n".join(["\t%s" % source]))
        sources[frequency] = source

    # Create a sender for each source, so we can process the bits to
    # get the modulated samples.  We combine all of the modulated
    # samples into a single array by adding them.

    baseband_samples = []
    modulated_samples = []

    for frequency in sources:
        src = sources[frequency]
        sender = Sender(frequency, preamble, config)
        sender.set_source(src)

        modulated_samples = util.add_arrays(sender.modulated_samples(), modulated_samples)
        baseband_samples = util.add_arrays(sender.bits_to_samples(src.payload), baseband_samples)

    # Create the channel
    if config.bypass:
        channel = AbstractChannel(config.bypass_noise, config.bypass_h, config.bypass_lag)
    else:
        channel = AudioChannel(config)

    # Transmit and receive data on the channel.  The received samples
    # (samples_rx) have not been processed in any way.

    if random.random() > 0.5:
        samples_rx = channel.xmit(modulated_samples)
        print('Sent', len(samples_rx), 'samples')
    else:
    
        samples_rx = channel.recv(4*modulated_samples)
        print('Received', len(samples_rx), 'samples')

        for frequency in config.channels:
            r = Receiver(frequency, preamble, config)
            try:
                # Call the main receiver function.  The returned array of bits
                # EXCLUDES the preamble.
                bits  = r.process(samples_rx)
    
                # Push into a Sink so we can convert back to a useful payload
                # (this step will become more useful when we're transmitting
                # files or images instead of just bit arrays)
                src = sources[frequency]
                sink = Sink(src)
                received_payload = sink.process(bits)
                print("Received %d data bits" % len(received_payload))
                if src.type == Source.TEXT:
                    print("Received text was:", sink.received_text)
                    if ((str(sink.received_text)) == "Mens et manus.\n"):
                        return "inactive"
 
                if len(received_payload) > 0:
                    # Output BER
                    hd = util.hamming(received_payload, src.payload)
                    ber = float(hd)/len(received_payload)
                    print('BER:', ber)
                else:
                    print('Could not recover transmission.')

            except Exception as e:
                print(repr(e))
    return "active"
    
if __name__ == '__main__':

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
    parser.add_argument("--start", action='store_true', help="send only start signal")

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

    args = parser.parse_args()
    args.file = ["testfiles/A"]

    config = Config(args)
    print(config) # useful output

    if args.start:
        send_start(config)
    else:
        # Go!
        run(config)
