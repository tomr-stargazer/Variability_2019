"""
Basic script to transform data from its raw, downloaded state (.fits) to something I can work with.

"""

# WSERV 8 = IC 348

import numpy as np
import matplotlib.pyplot as plt

from astropy.table import Table
dat = Table.read('WSERV11_results6_23_31_38_30286.fits', format='fits')
name = 'WSERV11'

null = -999999488.0

# this is the so-called error correction of Hodgkin 2009, which makes the 
# error bar estimates more grounded in reality (they are otherwise unrealistically
# low for bright stars) — there's a 2% (0.02 mag) noise floor in practice that 
# is not captured in the pipeline-produced error estimates.
dat['JAPERMAG3ERR'] = (1.082 * dat['JAPERMAG3ERR']**2 + 0.021**2)**0.5
dat['HAPERMAG3ERR'] = (1.082 * dat['HAPERMAG3ERR']**2 + 0.021**2)**0.5
dat['KAPERMAG3ERR'] = (1.082 * dat['KAPERMAG3ERR']**2 + 0.021**2)**0.5

# we are turning nulls to nans
dat['JAPERMAG3'][dat['JAPERMAG3'] == null] = np.nan
dat['HAPERMAG3'][dat['HAPERMAG3'] == null] = np.nan
dat['KAPERMAG3'][dat['KAPERMAG3'] == null] = np.nan
dat['JAPERMAG3ERR'][dat['JAPERMAG3ERR'] == null] = np.nan
dat['HAPERMAG3ERR'][dat['HAPERMAG3ERR'] == null] = np.nan
dat['KAPERMAG3ERR'][dat['KAPERMAG3ERR'] == null] = np.nan
dat['JMHPNT'][dat['JMHPNT'] == null] = np.nan
dat['JMHPNTERR'][dat['JMHPNTERR'] == null] = np.nan
dat['HMKPNT'][dat['HMKPNT'] == null] = np.nan
dat['HMKPNTERR'][dat['HMKPNTERR'] == null] = np.nan

df = dat.to_pandas() 



