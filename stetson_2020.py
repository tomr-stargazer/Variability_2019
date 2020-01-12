"""
I am coding up a refreshed Stetson index for this Mon R2 and IC348 project,
specifically with pandas compatibility in mind.

"""

import numpy as np

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

    d_j = delta(j, sigma_j, j.mean(), n)
    d_h = delta(h, sigma_h, h.mean(), n)
    d_k = delta(k, sigma_k, k.mean(), n)

    P_i = np.array( [d_j * d_h,
                     d_h * d_k,
                     d_j * d_k] )

    # I originally had two sums going: one over P_i, and one over all the 
    # elements of n, but then I realized that a single sum over all axes
    # did the exact same thing (I tested it) so now it's back to one sum.
    s = np.sum( np.sign( P_i ) * np.sqrt( np.abs( P_i ))) /(n*1.)

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

# q2_chisq = q2_groupby.apply(chisq)
# q2_stetson = q2_groupby.apply(threeband_stetson_pandas)