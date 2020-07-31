"""
This is a quick module to grab data and plot a three-band light curve.

"""

import numpy as np
import matplotlib.pyplot as plt


def quickplot(dataset, sourceid, set_title=True):
    """
    Grabs one star's data from a dataset and plots it in a SIMPLE, one-panel plot.
    """

    fig, ax = plt.subplots(1, figsize=(9, 4))
    stardata = dataset[dataset["SOURCEID"] == sourceid]

    times = stardata["MEANMJDOBS"]
    j_mags = stardata["JAPERMAG3"]
    h_mags = stardata["HAPERMAG3"]
    k_mags = stardata["KAPERMAG3"]

    ax.plot(times, j_mags, "b.")
    ax.plot(times, h_mags, "g.")
    ax.plot(times, k_mags, "r.")

    ax.invert_yaxis()
    ax.set_xlabel("Modified Julian Date (JD - 2400000.5)")
    ax.set_ylabel("J, H, K magnitude")

    if set_title:
        ax.set_title(f"Source ID: {sourceid}")

    return fig


def three_plot(dataset, sourceid, set_title=True):
    """
    Grabs one star's data from a dataset and plots it in a three-panel plot.
    """

    fig, axes = plt.subplots(nrows=3, figsize=(9, 4))
    stardata = dataset[dataset["SOURCEID"] == sourceid]

    times = stardata["MEANMJDOBS"]
    j_mags = stardata["JAPERMAG3"]
    h_mags = stardata["HAPERMAG3"]
    k_mags = stardata["KAPERMAG3"]

    j_errs = stardata["JAPERMAG3ERR"]
    h_errs = stardata["HAPERMAG3ERR"]
    k_errs = stardata["KAPERMAG3ERR"]

    axes[0].errorbar(times, j_mags, yerr=j_errs, fmt="b.")
    axes[1].errorbar(times, h_mags, yerr=h_errs, fmt="g.")
    axes[2].errorbar(times, k_mags, yerr=k_errs, fmt="r.")

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


def phase_plot(df, sid, period, offset, set_title=True):
    """
    Period-folded light curve.
    """

    fig, axes = plt.subplots(nrows=3)
    stardata = df[df["SOURCEID"] == sid]

    times = stardata["MEANMJDOBS"]
    phase = ((times % period) / period + offset) % 1.0

    j_mags = stardata["JAPERMAG3"]
    h_mags = stardata["HAPERMAG3"]
    k_mags = stardata["KAPERMAG3"]

    j_errs = stardata["JAPERMAG3ERR"]
    h_errs = stardata["HAPERMAG3ERR"]
    k_errs = stardata["KAPERMAG3ERR"]

    axes[0].errorbar(phase, j_mags, yerr=j_errs, fmt="b.")
    axes[1].errorbar(phase, h_mags, yerr=h_errs, fmt="g.")
    axes[2].errorbar(phase, k_mags, yerr=k_errs, fmt="r.")

    sym = "."
    ms = 5

    for ax, x, xerr in zip(axes, [j_mags, h_mags, k_mags], [j_errs, h_errs, k_errs]):

        ax.errorbar(
            phase - 1, x, yerr=xerr, fmt=sym, mfc="0.7", mec="0.7", ecolor="0.7", ms=ms
        )
        ax.errorbar(
            phase + 1, x, yerr=xerr, fmt=sym, mfc="0.7", mec="0.7", ecolor="0.7", ms=ms
        )

        ax.set_xticks([0, 0.5, 1])
        ax.set_xticks(np.arange(-0.5, 1.5, 0.1), minor=True)

        ax.set_xlim(-0.25, 1.25)

    axes[0].invert_yaxis()
    axes[1].invert_yaxis()
    axes[2].invert_yaxis()

    axes[0].set_ylabel("J mag")
    axes[1].set_ylabel("H mag")
    axes[2].set_ylabel("K mag")
    axes[2].set_xlabel(f"Phase, Period={period:.2f}d")

    if set_title:
        axes[0].set_title(f"Source ID: {sid}")

    return fig


def plot_phase_core(
    ax, t, x, xerr, period, offset=0, sym="o", color="k", ms=6, hide=False
):
    """ 
    Plots a pretty period-folded lightcurve on a given axes object.

    Doesn't assume anything about your data (e.g., that it's in magnitudes)
    
    Parameters
    ----------
    ax : plt.Axes
    t, x, xerr : array_like
    period : float
    offset : float, optional
        How much to shift the phase by. Default is zero.
    sym : str, optional
        Default 'o'. (circles)
    color : str, optional
        Default 'k'. (black)
    ms : float
        Default 6.
        
    Returns
    -------
    period : float
        The input period.
    
    """

    phase = ((t % period) / period + offset) % 1.0

    if not hide:
        ax.errorbar(phase, x, yerr=xerr, fmt=color + sym, ms=ms)
    ax.errorbar(
        phase - 1, x, yerr=xerr, fmt=sym, mfc="0.7", mec="0.7", ecolor="0.7", ms=ms
    )
    ax.errorbar(
        phase + 1, x, yerr=xerr, fmt=sym, mfc="0.7", mec="0.7", ecolor="0.7", ms=ms
    )

    ax.set_xticks([0, 0.5, 1])
    ax.set_xticks(np.arange(-0.5, 1.5, 0.1), minor=True)

    ax.set_xlim(-0.25, 1.25)


def plot_five_cmcc(df, sid, set_title=True):

    fig = plt.figure(figsize=(10, 6), dpi=80, facecolor="w", edgecolor="k")

    bottom = 0.1
    height = 0.25
    left = 0.075
    width = 0.5

    ax_k = fig.add_axes((left, bottom, width, height))
    ax_h = fig.add_axes((left, bottom + 0.3, width, height), sharex=ax_k)
    ax_j = fig.add_axes((left, bottom + 0.6, width, height), sharex=ax_k)

    ax_jhk = fig.add_axes((0.65, bottom, 0.23, 0.375))
    ax_khk = fig.add_axes((0.65, bottom + 0.475, 0.23, 0.375))

    stardata = df[df["SOURCEID"] == sid]

    times = stardata["MEANMJDOBS"]
    j_mags = stardata["JAPERMAG3"]
    h_mags = stardata["HAPERMAG3"]
    k_mags = stardata["KAPERMAG3"]

    j_errs = stardata["JAPERMAG3ERR"]
    h_errs = stardata["HAPERMAG3ERR"]
    k_errs = stardata["KAPERMAG3ERR"]

    jmh = stardata["JMHPNT"]
    hmk = stardata["HMKPNT"]
    jmh_errs = stardata["JMHPNTERR"]
    hmk_errs = stardata["HMKPNTERR"]

    ax_j.errorbar(times, j_mags, yerr=j_errs, fmt="b.")
    ax_h.errorbar(times, h_mags, yerr=h_errs, fmt="g.")
    ax_k.errorbar(times, k_mags, yerr=k_errs, fmt="r.")

    ax_j.invert_yaxis()
    ax_h.invert_yaxis()
    ax_k.invert_yaxis()

    ax_jhk.errorbar(hmk, jmh, xerr=hmk_errs, yerr=jmh_errs, fmt='k.', elinewidth=0.3, ms=2)
    ax_khk.errorbar(hmk, k_mags, xerr=hmk_errs, yerr=k_errs, fmt='k.', elinewidth=0.3, ms=2)

    ax_khk.invert_yaxis()

    ax_j.set_ylabel("J mag")
    ax_h.set_ylabel("H mag")
    ax_k.set_ylabel("K mag")
    ax_k.set_xlabel("Modified Julian Date (JD - 2400000.5)")
    ax_jhk.set_xlabel( "H-K" )
    ax_jhk.set_ylabel( "J-H")#, {'rotation':'horizontal'})
    ax_khk.set_xlabel( "H-K" )
    ax_khk.set_ylabel( "K")#, {'rotation':'horizontal'})

    if set_title:
        ax_j.set_title(f"Source ID: {sid}")

    return fig

