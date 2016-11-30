#!/usr/bin/python

'''Defines the Source class, which generates a payload given a
particular source type.  In the future, this class will also take care
of sources such as files, images, etc.'''

import random
import sys

class Source:

    ZEROS = 0
    ONES = 1
    RANDOM = 2
    U = 3
    TEXT = 4

    def __init__(self, config, channel_index, new_id):

        self.type = config.src_type
        self.n_bits = config.n_bits
        self.new_id = new_id

        print("In Source -> new_id: %s" % (self.new_id))

        # Create the payload
        if config.filenames is None:
            if self.type == Source.RANDOM: # random bits
                self.payload = [random.randint(0,1) for i in range(self.n_bits)]
            elif self.type == Source.ONES: # all ones
                self.payload = [1] * self.n_bits
            elif self.type == Source.ZEROS: # all zeros
                self.payload = [0] * self.n_bits
            else:
                sys.stderr.write("Payload type not supported\n")
                sys.exit(-1)
        else:
            filename = config.filenames[channel_index]
            self.type = Source.TEXT
            self.payload = self.get_bits(filename)
            self.n_bits = len(self.payload) # overwrite nbits

        # For outputting data types
        self._str_map = {Source.RANDOM: "random", Source.ONES : "all ones", Source.ZEROS : "all zeros", Source.U : "unit step response", Source.TEXT : "text file"}


    def __str__(self):
        s = "Data type: %s\n" % (self._str_map[self.type])
        s += "\tData size: %d bits\n" % (len(self.payload))
        return s

    def get_bits(self, filename):
        '''Returns the bit representation of this file (ASCII encoding).'''
        bits = []
        if self.new_id:
            for c in str(self.new_id):
                bits.extend(self.int2bits(ord(c), 8))

        string = "%s" % (self.new_id)

        with open(filename, 'r') as f:
            for line in f:
                for c in line:
                    bits.extend(self.int2bits(ord(c), 8))
                    string += c


        print("String to send: %s" % (string))
        return bits

    def int2bits(self, x, width): 
        '''Returns a list of bits that represent this byte.'''
        return tuple((0,1)[x>>j & 1] for j in range(width-1,-1,-1)) 
