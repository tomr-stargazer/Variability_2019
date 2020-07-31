"""
Basic script to transform data from its raw, downloaded state (.fits) to something I can work with.

"""

# WSERV 8 = IC 348

import numpy as np
import matplotlib.pyplot as plt
from stetson_2020 import (
    threeband_stetson_pandas,
    j_chisq_red,
    h_chisq_red,
    k_chisq_red,
    j_period_fap,
    h_period_fap,
    k_period_fap,
)

from astropy.table import Table

dat = Table.read("WSERV8_results6_23_50_28_30335.fits", format="fits")
name = "WSERV8"

null = -999999488.0

# this is the so-called error correction of Hodgkin 2009, which makes the
# error bar estimates more grounded in reality (they are otherwise unrealistically
# low for bright stars) — there's a 2% (0.02 mag) noise floor in practice that
# is not captured in the pipeline-produced error estimates.
dat["JAPERMAG3ERR"] = (1.082 * dat["JAPERMAG3ERR"] ** 2 + 0.021 ** 2) ** 0.5
dat["HAPERMAG3ERR"] = (1.082 * dat["HAPERMAG3ERR"] ** 2 + 0.021 ** 2) ** 0.5
dat["KAPERMAG3ERR"] = (1.082 * dat["KAPERMAG3ERR"] ** 2 + 0.021 ** 2) ** 0.5

# we are turning nulls to nans
dat["JAPERMAG3"][dat["JAPERMAG3"] == null] = np.nan
dat["HAPERMAG3"][dat["HAPERMAG3"] == null] = np.nan
dat["KAPERMAG3"][dat["KAPERMAG3"] == null] = np.nan
dat["JAPERMAG3ERR"][dat["JAPERMAG3ERR"] == null] = np.nan
dat["HAPERMAG3ERR"][dat["HAPERMAG3ERR"] == null] = np.nan
dat["KAPERMAG3ERR"][dat["KAPERMAG3ERR"] == null] = np.nan
dat["JMHPNT"][dat["JMHPNT"] == null] = np.nan
dat["JMHPNTERR"][dat["JMHPNTERR"] == null] = np.nan
dat["HMKPNT"][dat["HMKPNT"] == null] = np.nan
dat["HMKPNTERR"][dat["HMKPNTERR"] == null] = np.nan

df = dat.to_pandas()

df_groupby = df.groupby("SOURCEID")

# intermediate spreadsheets!
df_maxes = df_groupby.aggregate(np.nanmax)
df_mins = df_groupby.aggregate(np.nanmin)
df_medians = df_groupby.aggregate(np.nanmedian)
df_j_counts = df_groupby["JAPERMAG3"].aggregate("count")
df_h_counts = df_groupby["HAPERMAG3"].aggregate("count")
df_k_counts = df_groupby["KAPERMAG3"].aggregate("count")

qj = (
    (df_maxes["JPPERRBITS"] == 0)
    & (df_j_counts > 60)
    & (df_j_counts < 130)
    & (df_mins["JAPERMAG3"] > 10)
    & (df_maxes["JAPERMAG3"] < 19)
    & ((df_medians["MERGEDCLASS"] == -1) | (df_medians["MERGEDCLASS"] == -2))
)

qh = (
    (df_maxes["HPPERRBITS"] == 0)
    & (df_h_counts > 60)
    & (df_h_counts < 130)
    & (df_mins["HAPERMAG3"] > 10)
    & (df_maxes["HAPERMAG3"] < 18)
    & ((df_medians["MERGEDCLASS"] == -1) | (df_medians["MERGEDCLASS"] == -2))
)

qk = (
    (df_maxes["KPPERRBITS"] == 0)
    & (df_k_counts > 60)
    & (df_k_counts < 130)
    & (df_mins["KAPERMAG3"] > 10)
    & (df_maxes["KAPERMAG3"] < 18)
    & ((df_medians["MERGEDCLASS"] == -1) | (df_medians["MERGEDCLASS"] == -2))
)

# anyone who is all 3 is a Q2 source!
q2 = qj & qh & qk
# anyone who is any of the 3 (but not all!) is a Q1 source!
q1 = (qj | qh | qk) & ~q2

q0 = (df_j_counts > 60) | (df_h_counts > 60) | (df_k_counts > 60)

q2_sourceids = df_medians[q2].index
q1_sourceids = df_medians[q1].index
qj_sourceids = df_medians[qj].index
qh_sourceids = df_medians[qh].index
qk_sourceids = df_medians[qk].index

df_q2 = df[np.in1d(df["SOURCEID"], q2_sourceids)]
df_q2_stetson = df_q2.groupby("SOURCEID").apply(threeband_stetson_pandas)

q2_variables = df_q2_stetson.index[df_q2_stetson > 2.5]


df_qj = df[np.in1d(df["SOURCEID"], qj_sourceids)]
df_qh = df[np.in1d(df["SOURCEID"], qh_sourceids)]
df_qk = df[np.in1d(df["SOURCEID"], qk_sourceids)]

qj_j_chisq_red = df_qj.groupby("SOURCEID").apply(j_chisq_red)
qh_h_chisq_red = df_qh.groupby("SOURCEID").apply(h_chisq_red)
qk_k_chisq_red = df_qk.groupby("SOURCEID").apply(k_chisq_red)

qj_variables = qj_j_chisq_red.index[qj_j_chisq_red > 3]
qh_variables = qh_h_chisq_red.index[qh_h_chisq_red > 3]
qk_variables = qk_k_chisq_red.index[qk_k_chisq_red > 3]

q1_variables = list(
    set.union(set(qj_variables), qh_variables, qk_variables) - set(q2_variables)
)

q1and2_variables = list(q1_variables) + list(q2_variables)

q12var_df = df[np.in1d(df["SOURCEID"], q1and2_variables)]
q12var_df_grouped = q12var_df.groupby("SOURCEID")

J_periods = q12var_df_grouped.apply(j_period_fap)
H_periods = q12var_df_grouped.apply(h_period_fap)
K_periods = q12var_df_grouped.apply(k_period_fap)

variable_means = q12var_df_grouped.aggregate(np.nanmean)
variable_means["J_periods"] = J_periods
variable_means["H_periods"] = H_periods
variable_means["K_periods"] = K_periods
