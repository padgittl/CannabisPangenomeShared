#===============================================================================
# filter_aligned_cds.py
#===============================================================================

"""filter CDS alignments"""

# Imports ======================================================================

import os.path
import tempfile
from argparse import ArgumentParser
from multiprocessing import Pool
from functools import partial
from cigar import Cigar
from pybedtools import BedTool

# Functions ====================================================================

def filter_aligned_cds(
        paf,
        bed,
        outdir: str = '.' ,
        use_cigar: bool = False,
        match_percent: int = 80
    ):
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(paf, 'r') as f_in, open(os.path.join(temp_dir, f'{os.path.basename(paf)}.bed'), 'w') as f_out:
            for line in f_in:
                q_name, q_len, q_start, q_end, strand, t_name, t_len, t_start, t_end, *rest = line.split()
                f_out.write('\t'.join((t_name, t_start, t_end, strand, q_name, ','.join((q_len, q_start, q_end, t_len, *rest))))+'\n')
        BedTool(os.path.join(temp_dir, f'{os.path.basename(paf)}.bed')).intersect(
           BedTool(bed), v=True
        ).saveas(os.path.join(temp_dir, f'{os.path.basename(paf)}.non_overlapping.bed'))
        with open(os.path.join(temp_dir, f'{os.path.basename(paf)}.non_overlapping.bed'), 'r') as f_in, open(os.path.join(outdir, os.path.basename(paf)), 'w') as f_out:
            for line in f_in:
                t_name, t_start, t_end, strand, q_name, other = line.split()
                q_len, q_start, q_end, t_len, match, block_len, qual, *rest, cig = other.split(',')
                if use_cigar:
                    match = {op: val for val, op in Cigar(cig.split(':')[-1]).merge_like_ops().items()}.get('M', 0)
                if qual >= '60' and int(match) / int(q_len) > match_percent / 100:
                    f_out.write('\t'.join((q_name, q_len, q_start, q_end, strand, t_name, t_len, t_start, t_end, str(match), block_len, qual, *rest, cig))+'\n')
    # with open(paf, 'r') as f_in, open(os.path.join(outdir, os.path.basename(paf)), 'w') as f_out:
    #     for line in f_in:
    #         _, q_len, _, _, _, _, _, _, _, match, _, qual, *_, cig = line.split()
    #         if use_cigar:
    #             match = {op: val for val, op in Cigar(cig.split(':')[-1]).merge_like_ops().items()}.get('M', 0)
    #         if qual >= '60' and int(match) / int(q_len) > match_percent / 100:
    #             f_out.write(line)


def parse_arguments():
    parser = ArgumentParser(description='filter CDS alignments')
    parser.add_argument('outdir', help='directory for output files')
    parser.add_argument('--paf', nargs='+', required=True)
    parser.add_argument('--bed', nargs='+', required=True)
    parser.add_argument('--cigar', action='store_true', help='use CIGAR to calculate matches')
    parser.add_argument('--match-percent', type=int, default=80,
                        help='minimum percent matches for an alignment to pass')
    parser.add_argument('--processes', type=int, help='number of processes')
    return parser.parse_args()


def main():
    args = parse_arguments()
    with Pool(processes=args.processes) as pool:
        pool.starmap(
            partial(filter_aligned_cds, outdir=args.outdir, use_cigar=args.cigar,
                    match_percent=args.match_percent),
            zip(args.paf, args.bed)
        )


# Execute ======================================================================

if __name__ == '__main__':
    main()
