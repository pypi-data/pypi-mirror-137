# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 10:55:37 2014

@author: jundurraga-ucl
"""
from peegy.processing.tools import epochs_processing_tools as ept
import numpy as np
import matplotlib.pyplot as plt
# create synthetic data
fs = 1000.0
nsamples = np.round(1 * fs).astype(np.int)
nchans = 36
ntrials = 130
noise_dim = 36  # dimensionality of noise
f1 = 40
source = np.expand_dims(np.sin(2 * np.pi * f1 * np.arange(nsamples) / fs), axis=1)
coeff = np.ones(nchans//2) * 0.5 / (nchans / 2)
coeff = np.expand_dims(np.hstack((coeff, coeff)), 0)

s = source * coeff
s_std = np.std(s, axis=0)
s = np.tile(np.expand_dims(s, axis=2), (1, 1, ntrials))

desired_snr = 5.0
ini_std = 10.0 ** (-desired_snr / 20.0) * s_std * ntrials ** 0.5
theoretical_rn = ini_std / ntrials ** 0.5

noise = np.random.normal(0, ini_std[0], size=(nsamples, nchans, ntrials))
s[:, 0] = s[:, 0] * 0.5
data = noise + s
w_ave, w, rn, cumulative_rn, w_fft, n = ept.et_mean(epochs=data,
                                                    block_size=10,
                                                    samples_distance=10)

snr, s_var = ept.et_snr_in_rois(data=w_ave, rn=rn)
print('snr in dB = {:}'.format(10 * np.log10(snr)))
across_channels_ave, total_rn, total_snr, t_s_var = \
    ept.et_snr_weighted_mean(averaged_epochs=w_ave, rn=rn, snr=np.max(snr, axis=1))

fig = plt.figure()
ax = fig.add_subplot(131)
ax.plot(np.mean(s, axis=2))
ax = fig.add_subplot(132)
ax.plot(w_ave)
ax = fig.add_subplot(133)
ax.plot(across_channels_ave)
plt.show()
