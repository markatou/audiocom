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
    s = "active"
    modulated_samples, channel, sources  = makeChannel(config)
    time = datetime.datetime.now()
    
    while s == "active":
        if (datetime.datetime.now() - time).total_seconds() > 10:
            time = datetime.datetime.now()
            if random.random() > 0.5:
                send(config,modulated_samples,channel,sources)
            else:
                s = listen(config,modulated_samples,channel,sources)
            print( "s= " + s)

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

    
        
def send(config,modulated_samples, channel,sources):

    # Transmit and receive data on the channel.  The received samples
    # (samples_rx) have not been processed in any way.

    samples_rx = channel.xmit(modulated_samples)
    print('Sent the samples')

def listen(config,modulated_samples,channel,sources):
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
    
