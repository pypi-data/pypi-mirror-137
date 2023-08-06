
import os
import generate
# import generateDistributions
from math import exp
from scipy.special import zeta
import numpy as np
from scipy.stats import zipf
import time


def in_dist(k):
    return k**(-2) / zeta(2)


def out_dist(k):
    return k**(-3) / zeta(3)

# def out_dist(k):
#     return zipf.pmf(k, 3)


if __name__ == "__main__":

    start = time.time()

    generate.models(

        # group_name='none_800_ma_mp_1',
        # group_name='inPLa2_800_ma_mp_1',
        group_name='bench',
        n_models=10,
        n_species=100,
        out_dist=out_dist,
        in_dist=in_dist,
        # kinetics=['mass_action', 'loguniform', ['kf', 'kr', 'kc'], [[0.01, 100], [0.01, 100], [0.01, 100]]],
        overwrite=True,
        # ic_params=['uniform', 0, 10],
        dist_plots=True,
        net_plots=True

    )

    finish = time.time()
    elapsed = finish-start
    # print(elapsed)
