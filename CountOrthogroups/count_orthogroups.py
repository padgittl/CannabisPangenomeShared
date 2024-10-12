import pandas as pd
import sys
from argparse import ArgumentParser
from collections import Counter
from scipy.stats import hypergeom
from math import prod, floor


def parse_arguments():
    parser = ArgumentParser(description = "count orthogroups")
    parser.add_argument('orthogroup_table')
    parser.add_argument('-c', '--contours', type=int, nargs='+', default=[])
    parser.add_argument('-f', '--contours-float', type=float, nargs='+', default=[])
    return parser.parse_args()


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
        yield (
            n_genomes,
            sum(
                (1-prod((g-s-n)/(g-n) for n in range(n_genomes)))*score_dist[s]
                for s in range(1, g+1)
            ),
            'Pan'
        )
        if contours:
            for c in contours:
                yield (
                    n_genomes,
                    sum(
                        (
                            hypergeom.sf(floor(c/100*n_genomes), g, s, n_genomes)
                        )*score_dist[s]
                        for s in range(1, g+1)
                    ),
                    f'{c}%'
                )
        yield (
            n_genomes,
            sum(
                prod((s-n)/(g-n) for n in range(n_genomes))*score_dist[s]
                for s in range(1, g+1)
            ),
            'Core'
        )


def main():
    args = parse_arguments()
    ortho = pd.read_table(args.orthogroup_table, index_col=0)
    contours = args.contours + args.contours_float
    col_df = pd.DataFrame(
        col_values(ortho, contours=contours),
        columns=('Genomes', 'Orthogroups', 'Level')
    )
    col_df.to_csv(sys.stdout, index=False, sep='\t')


if __name__ == '__main__':
    main()
