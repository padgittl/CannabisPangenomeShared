import numpy as np
import pandas as pd
import sys
import pysam
from argparse import ArgumentParser
from collections import Counter

EH23A_CHROMOSOMES = ['EH23a.chr1', 'EH23a.chr2', 'EH23a.chr3', 'EH23a.chr4',
                     'EH23a.chr5', 'EH23a.chr6', 'EH23a.chr7', 'EH23a.chr8',
                     'EH23a.chr9', 'EH23a.chrX']

EH23B_CHROMOSOMES = ['EH23b.chr1', 'EH23b.chr2', 'EH23b.chr3', 'EH23b.chr4',
                     'EH23b.chr5', 'EH23b.chr6', 'EH23b.chr7', 'EH23b.chr8',
                     'EH23b.chr9', 'EH23b.chrX']


def parse_arguments():
    parser = ArgumentParser(description='sort contigs')
    parser.add_argument('kmers')
    parser.add_argument('sizes')
    parser.add_argument('alignment')
    parser.add_argument('--hap', choices=('a', 'b'))
    return parser.parse_args()

def count_alignments(alignment_file):
    return Counter((a.query_name, alignment_file.getrname(a.reference_id))
                   for a in alignment_file if a.mapping_quality >= 60)


def main():
    args = parse_arguments()
    kmers = pd.read_table(args.kmers, header=None, index_col=1)
    sizes = pd.read_table(args.sizes, header=None, index_col=0)
    df = pd.concat((kmers, sizes.loc[kmers.index,:]), axis=1)
    df[2] = df[0]/np.log(df[1])
    df.columns = 'kmers_bp', 'total_bp', 'relevance'
    df.index.name = 'contig'
    df.sort_values('relevance', ascending=False, inplace=True)
    with pysam.AlignmentFile(args.alignment) as af:
        alignment_counts = count_alignments(af)
    if args.hap == 'a':
        chromosomes = EH23A_CHROMOSOMES
    elif args.hap == 'b':
        chromosomes = EH23B_CHROMOSOMES
    else:
        raise RuntimeError('invalid hap')
    df['chrom'] = tuple(sorted(((alignment_counts[(contig, chrom)], chrom)
                                for chrom in chromosomes), reverse=True)[0][1]
                                for contig in df.index)
    df.loc[:,['kmers_bp', 'total_bp', 'chrom']].to_csv(sys.stdout, sep='\t')

if __name__  == '__main__':
    main()
  