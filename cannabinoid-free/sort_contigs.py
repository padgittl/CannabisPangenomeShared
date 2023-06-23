import numpy as np
import pandas as pd
import sys
from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser(description='sort contigs')
    parser.add_argument('counts')
    parser.add_argument('sizes')
    return parser.parse_args()


def main():
    args = parse_arguments()
    counts = pd.read_table(args.counts, header=None, index_col=1)
    sizes = pd.read_table(args.sizes, header=None, index_col=0)
    df = pd.concat((counts, sizes.loc[counts.index,:]), axis=1)
    df[2] = df[0]/np.log(df[1])
    df.columns = 'kmers_bp', 'total_bp', 'relevance'
    df.index.name = 'contig'
    df.sort_values('relevance', ascending=False, inplace=True)
    df.loc[:,('kmers_bp', 'total_bp')].to_csv(sys.stdout, sep='\t')

if __name__  == '__main__':
    main()
  