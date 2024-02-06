#===============================================================================
# filter_aligned_cds.py
#===============================================================================

"""filter CDS alignments"""

# Imports ======================================================================

import os.path
from argparse import ArgumentParser
from multiprocessing import Pool
from functools import partial
from cigar import Cigar

# Functions ====================================================================

def filter_aligned_cds(
        paf,
        outdir: str = '.' ,
        use_cigar: bool = False,
        match_percent: int = 80
    ):
    with open(paf, 'r') as f_in, open(os.path.join(outdir, os.path.basename(paf)), 'w') as f_out:
        for line in f_in:
            _, q_len, _, _, _, _, _, _, _, match, _, qual, *_, cig = line.split()
            if use_cigar:
                match = {op: val for val, op in Cigar(cig.split(':')[-1]).merge_like_ops().items()}.get('M', 0)
            if qual == '60' and int(match) / int(q_len) > match_percent / 100:
                f_out.write(line)


def parse_arguments():
    parser = ArgumentParser(description='filter CDS alignments')
    parser.add_argument('outdir', help='directory for output files')
    parser.add_argument('--paf', nargs='+', required=True)
    parser.add_argument('--processes', type=int, help='number of processes')
    parser.add_argument('--cigar', action='store_true', help='use CIGAR to calculate matches')
    parser.add_argument('--match-percent', type=int, default=80,
                        help='minimum percent matches for an alignment to pass')
    return parser.parse_args()


def main():
    args = parse_arguments()
    with Pool(processes=args.processes) as pool:
        pool.map(
            partial(filter_aligned_cds, outdir=args.outdir, cigar=args.cigar, match=args.match),
            args.paf
        )


# Execute ======================================================================

if __name__ == '__main__':
    main()
