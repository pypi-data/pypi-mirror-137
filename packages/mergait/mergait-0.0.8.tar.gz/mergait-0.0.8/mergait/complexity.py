""" Signal complexity related utility functions

These functions help attach signal complexity information to the running data
"""

import pandas as pd
import numpy as np
import neurokit2 as nk


def hurst(values):
    """
    Compute the Hurst complexity index

    Parameters
    ----------
    values : list
        data to compute the complexity for

    Returns
    -------
    float
        the Hurst index
    """
    if isinstance(values, pd.Series):
        values = values.values

    try:
        hurst = nk.complexity_hurst(values)[0]
    except:
        hurst = np.NaN

    return hurst


def dfa(values):
    """
    Compute the DFA (Detrended Fluatuation Analysis) number

    Parameters
    ----------
    values : list
        data to compute the complexity for

    Returns
    -------
    float
        the DFA index
    """
    if isinstance(values, pd.Series):
        values = values.values

    try:
        dfa = nk.complexity_dfa(values.values)[0]
    except:
        dfa = np.NaN

    return dfa


def xfen(u, v, m=10, r=0.2, n=2, N=False):
    """
    Cross Fuzzy Entropy

    :param u: first series of observations
    :param v: second series of observations
    :param m: fixed positive integer
    :param r: positiver real number
    :param N: length of series to handle
    :return:
    """
    import numpy as np

    if not N:
        N = np.min([len(u), len(v)])

    def Phi(m):
        u0 = [np.nanmean(u[i : i + m]) for i in range(N - m)]
        v0 = [np.nanmean(v[j : j + m]) for j in range(N - m)]

        try:
            d_map = np.max(
                np.abs(
                    np.array(
                        [
                            [
                                (u[i : i + m] - v[j : j + m] - u0[i] + v0[j])
                                for i in range(N - m)
                            ]
                            for j in range(N - m)
                        ]
                    )
                ),
                axis=2,
            )

            d_fuzzy_map = np.exp(-np.power(d_map, n) / r)

            B = np.sum(d_fuzzy_map, axis=0) / (N - m)
            return np.sum(B) / (N - m)
        except:
            return 0

    Phim = Phi(m)
    Phim1 = Phi(m + 1)

    if Phim == 0 or Phim1 == 0:
        return 0
    else:
        return np.log(Phi(m)) - np.log(Phi(m + 1))
