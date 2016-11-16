#!/usr/bin/python

'''Defines the AudioChannel class, derived from Channel.  Transmits
and receives a signal over audio via a lot of pyaudio nonsense.'''

import numpy
import pyaudio
import struct
import sys

from channel import Channel

class AudioChannel(Channel):

    FORMAT = pyaudio.paFloat32
    CHANNELS = 1

    def __init__(self, config):
        self.p = pyaudio.PyAudio()
        self.sample_rate = config.sample_rate
        self.SAMPLES_PER_CHUNK = config.chunk_size
        self.WRITE_BUFFER_PREFILL = config.prefill
        self.verbose = config.verbose

    def xmit(self, samples_tx):
        # Create the payload chunks
        sample_count = 0
        total_sample_count = 0
        chunk_data = []

        for i in range(0, len(samples_tx), self.SAMPLES_PER_CHUNK):
            this_chunk = samples_tx[i:i+self.SAMPLES_PER_CHUNK]
            chunk_data.append(bytes())
            for c in this_chunk:
                chunk_data[-1] += struct.pack('f', c)
            
        total_sample_count = len(chunk_data)*self.SAMPLES_PER_CHUNK
        samples_rx = []
        max_recv_samples = total_sample_count + 4000
        nsamples = 0

        # open soundcard channel
        self.soundcard_inout = self.p.open(format = AudioChannel.FORMAT,
                                           channels = AudioChannel.CHANNELS,
                                           rate = self.sample_rate,
                                           input = True,
                                           output = True,
                                           frames_per_buffer = self.SAMPLES_PER_CHUNK)

        do_exceptions = True

        # Transmit the prefill chunks
        for chunk in chunk_data[:self.WRITE_BUFFER_PREFILL]:
            self.soundcard_inout.write(chunk, exception_on_underflow=not do_exceptions)

        # Transmit the actual data
        for chunk in chunk_data[self.WRITE_BUFFER_PREFILL:]:
            # Transmit
            self.soundcard_inout.write(chunk, exception_on_underflow=not do_exceptions)
        return samples_rx

    def recv(self, samples_tx):
        '''Transmit and receive samples over an Audio channel.  Return an
        array of received samples.'''

        # Create the payload chunks
        sample_count = 0
        total_sample_count = 0
        chunk_data = []

        for i in range(0, len(samples_tx), self.SAMPLES_PER_CHUNK):
            this_chunk = samples_tx[i:i+self.SAMPLES_PER_CHUNK]
            chunk_data.append(bytes())
            for c in this_chunk:
                chunk_data[-1] += struct.pack('f', c)
            
        total_sample_count = len(chunk_data)*self.SAMPLES_PER_CHUNK
        samples_rx = []
        max_recv_samples = total_sample_count + 4000
        nsamples = 0

        # open soundcard channel
        self.soundcard_inout = self.p.open(format = AudioChannel.FORMAT,
                                           channels = AudioChannel.CHANNELS,
                                           rate = self.sample_rate,
                                           input = True,
                                           output = True,
                                           frames_per_buffer = self.SAMPLES_PER_CHUNK)

        do_exceptions = True

        # Transmit the prefill chunks
        for chunk in chunk_data[:self.WRITE_BUFFER_PREFILL]:
            self.soundcard_inout.write(chunk, exception_on_underflow=not do_exceptions)

        # Receive the actual data
        for chunk in chunk_data[self.WRITE_BUFFER_PREFILL:]:
            # Receive
            rx_sample_count = 0
            sample_chunk_rx = []

            try:
                x = struct.unpack('f' * self.SAMPLES_PER_CHUNK, self.soundcard_inout.read(self.SAMPLES_PER_CHUNK, exception_on_overflow=not do_exceptions))
                sample_chunk_rx.extend(x)
                nsamples += self.SAMPLES_PER_CHUNK
                samples_rx.extend(sample_chunk_rx)

            except IOError as e:
                if self.verbose:
                    sys.stderr.write( "IOError %s\n" % e )

        # Receive any remaining chunks
        while nsamples < max_recv_samples:
            rx_sample_count = 0
            sample_chunk_rx = []
            try:
                x = self.soundcard_inout.read(self.SAMPLES_PER_CHUNK, exception_on_overflow = not do_exceptions)
                x = struct.unpack('f' * self.SAMPLES_PER_CHUNK, x)

                sample_chunk_rx.extend(x)
                nsamples += self.SAMPLES_PER_CHUNK
                samples_rx.extend(sample_chunk_rx)
            except IOError as e:
                print(e)
                if self.verbose:
                    sys.stderr.write( "IOError %s\n" % e )

        self.soundcard_inout.close()

        return samples_rx


    def xmit_and_recv(self, samples_tx):
        '''Transmit and receive samples over an Audio channel.  Return an
        array of received samples.'''

        # Create the payload chunks
        sample_count = 0
        total_sample_count = 0
        chunk_data = []

        for i in range(0, len(samples_tx), self.SAMPLES_PER_CHUNK):
            this_chunk = samples_tx[i:i+self.SAMPLES_PER_CHUNK]
            chunk_data.append(bytes())
            for c in this_chunk:
                chunk_data[-1] += struct.pack('f', c)
            
        total_sample_count = len(chunk_data)*self.SAMPLES_PER_CHUNK
        samples_rx = []
        max_recv_samples = total_sample_count + 4000
        nsamples = 0

        # open soundcard channel
        self.soundcard_inout = self.p.open(format = AudioChannel.FORMAT,
                                           channels = AudioChannel.CHANNELS,
                                           rate = self.sample_rate,
                                           input = True,
                                           output = True,
                                           frames_per_buffer = self.SAMPLES_PER_CHUNK)

        do_exceptions = True

        # Transmit the prefill chunks
        for chunk in chunk_data[:self.WRITE_BUFFER_PREFILL]:
            self.soundcard_inout.write(chunk, exception_on_underflow=not do_exceptions)

        # Transmit and receive the actual data
        for chunk in chunk_data[self.WRITE_BUFFER_PREFILL:]:

            # Transmit
            self.soundcard_inout.write(chunk, exception_on_underflow=not do_exceptions)

            # Receive
            rx_sample_count = 0
            sample_chunk_rx = []

            try:
                x = struct.unpack('f' * self.SAMPLES_PER_CHUNK, self.soundcard_inout.read(self.SAMPLES_PER_CHUNK, exception_on_overflow=not do_exceptions))
                sample_chunk_rx.extend(x)
                nsamples += self.SAMPLES_PER_CHUNK
                samples_rx.extend(sample_chunk_rx)

            except IOError as e:
                if self.verbose:
                    sys.stderr.write( "IOError %s\n" % e )

        # Receive any remaining chunks
        while nsamples < max_recv_samples:
            rx_sample_count = 0
            sample_chunk_rx = []
            try:
                x = self.soundcard_inout.read(self.SAMPLES_PER_CHUNK, exception_on_overflow = not do_exceptions)
                x = struct.unpack('f' * self.SAMPLES_PER_CHUNK, x)

                sample_chunk_rx.extend(x)
                nsamples += self.SAMPLES_PER_CHUNK
                samples_rx.extend(sample_chunk_rx)
            except IOError as e:
                print(e)
                if self.verbose:
                    sys.stderr.write( "IOError %s\n" % e )

        self.soundcard_inout.close()

        return samples_rx
