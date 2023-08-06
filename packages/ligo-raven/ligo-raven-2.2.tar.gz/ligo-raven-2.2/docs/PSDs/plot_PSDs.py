#!/usr/bin/env python

# Imports.
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import matplotlib.pyplot as plt


# Read in AdVirgo PSDs.
with open('AdV_refsens_100512.txt') as f: f1 = np.float64(f.read().split()[0::2])
with open('AdV_refsens_100512.txt') as f: S1 = np.float64(f.read().split()[1::2])

# Read in aLIGO PSDs.
with open('ZERO_DET_high_P.txt') as f: f2 = np.float64(f.read().split()[0::2])
with open('ZERO_DET_high_P.txt') as f: S2 = np.float64(f.read().split()[1::2])


# Produce a plot.
plt.figure(figsize=(5.5, 5.5))
plt.plot(f1, S1, 'g-', label='Advanced Virgo')
plt.plot(f2, S2, 'r-', label='Advanced LIGO (ZERO\_DET\_high\_P)')
plt.plot([10, 1000], [1.5e-22/2, 7e-24/2], 'k', linewidth=1.1)
plt.text(40, 3.4e-23, 'NS-NS inspiral at 60 Mpc', size=8, rotation=-27.5)
plt.legend()
plt.xlim( [min(f1.min(), f2.min()), max(f1.max(), f2.max())] )
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylim([1e-24, 1e-20])
plt.yscale('log')
plt.ylabel(r'Amplitude Spectral Density $(1/\sqrt{\mathrm{Hz}})$')
plt.savefig('PSDs.pdf')
