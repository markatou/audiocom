#!/usr/bin/python

'''Defines functions for making particular plots.'''

import platform
import math
import numpy
import warnings
import matplotlib

if platform.uname()[0] == 'Darwin':
    matplotlib.use('macosx')

import matplotlib.pyplot as p

def get_spec(samples):
    P = len(samples)
    omega1 = 2*math.pi/P
    omegak = omega1*P*numpy.fft.fftfreq(P)
    X = numpy.fft.fft(samples)
    return omegak, X

def plot_sig_spectrum(modulated_samples, demodulated_samples, show=False):
    p.figure()

    p.subplot(211)
    omegas, Xs = get_spec(modulated_samples)
    p.plot(omegas, abs(Xs))
    p.title("Modulated Samples")
    p.xlabel("Omega")
    p.xlim((-math.pi, math.pi))

    y_min = min(abs(Xs))
    y_max = max(abs(Xs))

    p.subplot(212)
    omegas, Xs = get_spec(demodulated_samples)
    p.plot(omegas, abs(Xs))
    p.title("Demodulated + Filtered Samples")
    p.xlabel("Omega")
    p.xlim((-math.pi, math.pi))
    p.ylim([y_min, y_max])

    warnings.filterwarnings("ignore")
    p.tight_layout()
    if show:
        p.show()

def plot_usr(samples,show=False):
    p.figure()

    p.xlabel('Sample number')
    p.ylabel('Voltage')
    p.title('Demodulated Samples')
    p.plot(range(len(samples)), samples)
    p.xlim(-len(samples), len(samples))

    warnings.filterwarnings("ignore")
    p.tight_layout()

    if show:
        p.show()
    
def plot_samples(baseband_samples, modulated_samples, received_samples, stems=False, show=False):
    '''Plot an array of samples.

    Arguments:
    samples -- samples to plot
    name -- title for graph
    show -- if true, displays the graph (if false, usually there is a
    separate call to p.show() in a later function)
    '''

    p.figure()
    p.subplot(311)

    p.xlabel('Sample number')
    p.ylabel('Voltage')
    p.title('Baseband Samples')
    if stems:
        p.stem(range(len(baseband_samples)), baseband_samples)
    else:
        p.plot(range(len(baseband_samples)), baseband_samples)

    p.subplot(312)
    p.xlabel('Sample number')
    p.ylabel('Voltage')
    p.title('Modulated Samples')
    if stems:
        p.stem(range(len(modulated_samples)), modulated_samples)
    else:
        p.plot(range(len(modulated_samples)), modulated_samples)

    p.subplot(313)
    p.xlabel('Sample number')
    p.ylabel('Voltage')
    p.title('Received Samples')
    if stems:
        p.stem(range(len(received_samples)), received_samples)
    else:
        p.plot(range(len(received_samples)), received_samples)

    warnings.filterwarnings("ignore")
    p.tight_layout()
    if show:
        p.show()
