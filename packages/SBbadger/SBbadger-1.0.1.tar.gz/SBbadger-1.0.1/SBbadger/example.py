
import generate
from scipy.stats import zipf


def in_dist(k):
    return k ** (-2)


def out_dist(k):
    return zipf.pmf(k, 3)


if __name__ == "__main__":

    generate.models(
        group_name="test",
        n_models=100,
        n_species=100,
        # rxn_prob=[0.3, 0.2, 0.2, 0.3],
        out_dist=out_dist,
        in_dist=in_dist,
        min_freq=1.0,
        # edge_type='metabolic',
        n_cpus=1
        )

