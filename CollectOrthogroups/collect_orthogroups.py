from collections import Counter
import pandas as pd
import seaborn as sns
import numpy as np
from math import prod, floor
from scipy.stats import hypergeom

COL_COLOR_PALETTE = 'mako_r'

def col_values(orthogroup_df, contours=None):
    """Calculate collection curve

    Parameters
    ----------
    orthogroup_df
        df of orthogroups
    contours
        if not None, an iterable of integers between 0 and 100

    Yields
    -------
        collection curve values
    """

    g = len(orthogroup_df.columns)
    score_dist = Counter(sum(score) for _, score in orthogroup_df.iterrows())
    for n_genomes in range(1, g+1):
        yield n_genomes, sum((1-prod((g-s-n)/(g-n) for n in range(n_genomes)))*score_dist[s]
            for s in range(1, g+1)), 'pan'
        if contours:
            for c in contours:
                yield n_genomes, sum((hypergeom.sf(floor(c/100*n_genomes), g, s, n_genomes))*score_dist[s]
                    for s in range(1, g+1)), f'{c}%'
        yield n_genomes, sum(prod((s-n)/(g-n) for n in range(n_genomes))*score_dist[s]
            for s in range(1, g+1)), 'core'

def main():
    ortho = pd.read_table('Phylogenetic_Hierarchical_Orthogroups/N3.tsv',
                      index_col=0, dtype=str).iloc[:,2:].notna()
    col_df = pd.DataFrame(col_values(ortho, contours=None),
                              columns=('n_genomes', 'n_kmers', 'sequence'))
    print(col_df)
