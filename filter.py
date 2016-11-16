#!/usr/bin/python

'''Defines different filters to use in the filtering step.'''

import math
import numpy

def averaging_filter(samples, window):
    '''Pass samples through an averaging filter.

    Arguments:
    samples -- samples to average
    window -- window size to use for averaging

    Returns: an array r that is the same size as samples.  r[x] =
    average of samples[x-window] to samples[x], inclusive.  When x <
    window, the averaging window is truncated.
    '''
    x = [0.0]*len(samples)
    for i in range(len(samples)):
        if i-window+1 < 0: # Beginning of the array
            x[i] = numpy.mean(samples[0:i+1])
        else:
            x[i] = numpy.mean(samples[i-window+1:i+1])
    return numpy.array(x)

def low_pass_filter(samples, channel_gap, sample_rate, L=50):
    # TODO: Your code here
    #print("\nWarning: Low-pass filter not implemented.\n")
    
    # a good choice for cutoff frequency is half of the channel gap.
    l = []
    O = (channel_gap*2*math.pi/sample_rate)/2.0
    for i in range(2*L+1):
        if i== L:
            l.append(O/math.pi)
        else:
            l.append(math.sin(O*(i-L))/(math.pi*(i-L)))
    return numpy.convolve(samples,numpy.array(l))

    
