"""
This is a quick module to grab data and plot a three-band light curve.

"""

import numpy as np
import matplotlib.pyplot as plt

def quickplot(dataset, sourceid, set_title=True):
    """
    Grabs one star's data from a dataset and plots it in a SIMPLE, one-panel plot.
    """

    fig, ax = plt.subplots(1, figsize=(9,4))
    stardata = dataset[dataset['SOURCEID'] == sourceid]

    times = stardata['MEANMJDOBS']
    j_mags = stardata['JAPERMAG3']
    h_mags = stardata['HAPERMAG3']
    k_mags = stardata['KAPERMAG3']

    ax.plot(times, j_mags, 'b.')
    ax.plot(times, h_mags, 'g.')
    ax.plot(times, k_mags, 'r.')

    ax.invert_yaxis()
    ax.set_xlabel("Modified Julian Date (JD - 2400000.5)")
    ax.set_ylabel("J, H, K magnitude")

    if set_title:
        ax.set_title(f"Source ID: {sourceid}")

    return fig


def three_plot(dataset, sourceid, set_title=True):
    """
    Grabs one star's data from a dataset and plots it in a SIMPLE, one-panel plot.
    """

    fig, axes = plt.subplots(nrows=3, figsize=(9,4))
    stardata = dataset[dataset['SOURCEID'] == sourceid]

    times = stardata['MEANMJDOBS']
    j_mags = stardata['JAPERMAG3']
    h_mags = stardata['HAPERMAG3']
    k_mags = stardata['KAPERMAG3']

    j_errs = stardata['JAPERMAG3ERR']
    h_errs = stardata['HAPERMAG3ERR']
    k_errs = stardata['KAPERMAG3ERR']

    axes[0].errorbar(times, j_mags, yerr=j_errs, fmt='b.')
    axes[1].errorbar(times, h_mags, yerr=h_errs, fmt='g.')
    axes[2].errorbar(times, k_mags, yerr=k_errs, fmt='r.')

    axes[0].invert_yaxis()
    axes[1].invert_yaxis()
    axes[2].invert_yaxis()

    axes[0].set_ylabel("J mag")
    axes[1].set_ylabel("H mag")
    axes[2].set_ylabel("K mag")
    axes[2].set_xlabel("Modified Julian Date (JD - 2400000.5)")

    if set_title:
        axes[0].set_title(f"Source ID: {sourceid}")

    return fig