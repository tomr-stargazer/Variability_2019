"""
I am coding up a refreshed Stetson index for this Mon R2 and IC348 project,
specifically with pandas compatibility in mind.

"""

import numpy as np
from astropy.timeseries import LombScargle

# From c. 2012.
def delta (m, sigma_m, mean_m, n):
    """ Normalized residual / "relative error" for one observation. 
    Used in Stetson's J variability index.

    INPUTS:
        m: a single magnitude measurement in a certain band
        sigma_m: the uncertainty on that measurement
        mean_m: the mean magnitude in that band
        n: the number of observations in that band

    OUTPUTS:
        d: the "relative error"
    """
    
    d = np.sqrt( n / (n-1) ) * (m - mean_m) / sigma_m
    
    return d

    
# From c. 2012.
def S (j, sigma_j, h, sigma_h, k, sigma_k) :
    """
    Computes the Stetson variability index for one star that has
    3 observations on each night. Uses Carpenter et al.'s notation.
    Simplified from the general expression assuming 3 observations every
      night.
    
    INPUTS:
        j: an array of J-band magnitudes
        sigma_j: an array of corresponding J-band uncertainties
        h: an array of H-band magnitudes
        sigma_h: an array of corresponding H-band uncertainties
        k: an array of K-band magnitudes
        sigma_k: an array of corresponding K-band uncertainties

    OUTPUTS:
        s: the Stetson variability index for 3 bands

    """

    n = j.size
    
    # Perhaps hackish
    if n < 2:
        return 0

    d_j = delta(j, sigma_j, np.nanmean(j), n)
    d_h = delta(h, sigma_h, np.nanmean(h), n)
    d_k = delta(k, sigma_k, np.nanmean(k), n)

    P_i = np.array( [d_j * d_h,
                     d_h * d_k,
                     d_j * d_k] )

    # I originally had two sums going: one over P_i, and one over all the 
    # elements of n, but then I realized that a single sum over all axes
    # did the exact same thing (I tested it) so now it's back to one sum.
    s = np.nansum( np.sign( P_i ) * np.sqrt( np.abs( P_i ))) /(n*1.)

    return s


# new. let's first see if we can manage to just shoehorn the old way into the new way.
def threeband_stetson_pandas(group):

    j = group['JAPERMAG3']
    sigma_j = group['JAPERMAG3ERR']
    h = group['HAPERMAG3']
    sigma_h = group['HAPERMAG3ERR']
    k = group['KAPERMAG3']
    sigma_k = group['KAPERMAG3ERR']

    # signature of S:
    return S (j, sigma_j, h, sigma_h, k, sigma_k) 


def chisq(group):
    d = group['JAPERMAG3']
    err = group['JAPERMAG3ERR']
    
    return ((d - d.mean())**2 / err**2).sum()


def j_chisq_red(group):
    d = group['JAPERMAG3']
    err = group['JAPERMAG3ERR']
    
    return ((d - d.mean())**2 / err**2).sum() / d.size


def h_chisq_red(group):
    d = group['HAPERMAG3']
    err = group['HAPERMAG3ERR']
    
    return ((d - d.mean())**2 / err**2).sum() / d.size


def k_chisq_red(group):
    d = group['KAPERMAG3']
    err = group['KAPERMAG3ERR']
    
    return ((d - d.mean())**2 / err**2).sum() / d.size

# q2_chisq = q2_groupby.apply(chisq)
# q2_stetson = q2_groupby.apply(threeband_stetson_pandas)

# def j_period_fap(group):
#     _t = group['MEANMJDOBS']
#     _y = group['JAPERMAG3']
#     _dy = group['JAPERMAG3ERR']

#     t = _t[~np.isnan(_y)]
#     y = _y[~np.isnan(_y)]
#     dy = _dy[~np.isnan(_y)]

#     ls = LombScargle(t, y, dy)
#     try:
#         frequency, power = ls.autopower()

#         best_period = 1/frequency[power==power.max()][0]
#         fap = ls.false_alarm_probability(power.max())

#         return best_period, fap
#     except ValueError:
#         return np.nan, np.nan


def period_fap(group, band):
    _t = group['MEANMJDOBS']
    _y = group[band.upper()+'APERMAG3']
    _dy = group[band.upper()+'APERMAG3ERR']

    t = _t[~np.isnan(_y)]
    y = _y[~np.isnan(_y)]
    dy = _dy[~np.isnan(_y)]

    ls = LombScargle(t, y, dy)
    try:
        frequency, power = ls.autopower()

        best_period = 1/frequency[power==power.max()][0]
        fap = ls.false_alarm_probability(power.max())

        return best_period, fap
    except ValueError:
        return np.nan, np.nan

def j_period_fap(group):
    return period_fap(group, 'J')
def h_period_fap(group):
    return period_fap(group, 'H')
def k_period_fap(group):
    return period_fap(group, 'K')

"""
def wavg(group):
    d = group['data']
    w = group['weights']
    return (d * w).sum() / w.sum()

def chisq(group):
    d = group['JAPERMAG3']
    err = group['JAPERMAG3ERR']
    
    return ((d - d.mean())**2 / err**2).sum()

q2_chisq = q2_groupby.apply(chisq)

"""