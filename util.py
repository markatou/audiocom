#!/usr/bin/python

'''Various utility functions, including modulate.'''

import math
import numpy
import operator
import sys

def add_arrays(s1, s2):
    '''Adds two numpy arrays together.  If the arrays are of different
    sizes, the sum is performed as if the smaller array were padded
    with 0's at the end.'''
    L = max(len(s1), len(s2))
    a = numpy.append(s1, [0]*(L-len(s1)))
    b = numpy.append(s2, [0]*(L-len(s2)))
    return a + b

def modulate(fc, samples, sample_rate):
    '''Modulate a series of samples using a given frequency and sample rate.'''
    # TODO: Your code here
    #args = numpy.arange(0, len(samples)) * fc * 2 * math.pi / sample_rate  
    res = []
    Om = fc*2.0*math.pi/sample_rate
    for i in range(len(samples)):
       res.append(samples[i]*math.cos(Om * i))
    
    # You will need to return something different than what we are
    # returning here (i.e., do not leave the below line in your code;
    # it's here only so Audiocom doesn't throw exceptions)
    return  res  

def recover_h(x, y, n_samples=40):
    '''Recovers h such that x * h = y.'''
    # TODO: Your code here
    # You will need to return something different than what we are
    # returning here (i.e., do not leave the below line in your code;
    # it's here only so Audiocom doesn't throw exceptions)
    
    k = 0
    while x[k] == 0:
        if k + 1 < len(x):
            k += 1
        else:
            break
    xl =[]
    yl = []     
    for i in x:
        xl.append(i)

    for i in y:
        yl.append(i)

    x = xl
    y = yl
      
    for i in range(n_samples):
        x.append(0)
        y.append(0) 
    x = x[k:]
    y = y[k:]
    
    h = [] 
    for i in range(n_samples):
        summ = 0 
        for z in range(i):
            summ += h[z]*x[i-z]       
        h.append((y[i] - summ) / x[0])
    
    return h

def bits_to_samples(bits, spb, v0, v1):
    '''Convert an array of bits to samples by expanding each bit to spb
    samples.  v0 and v1 define the voltage levels for 0 and 1,
    respectively.'''
    samples = [0.0]*len(bits)*spb
    for i in range(len(bits)):
        v = v1 if bits[i] == 1 else v0
        samples[i*spb:(i+1)*spb] = [v] * spb
    return samples

def hamming(s1, s2):
    '''Return the Hamming distance between two bit strings.  If one is
    shorter than the other, return the HD between the first n bits (n =
    length of shorter string) + difference in their length.'''
    l = min(len(s1), len(s2))
    d = abs(len(s1) - len(s2))
    hd = sum(map(operator.xor,s1[:l],s2[:l]))
    return hd + d

