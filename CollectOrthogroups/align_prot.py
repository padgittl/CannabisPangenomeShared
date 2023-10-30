#===============================================================================
# align_prot.py
#===============================================================================

"""splice-aware alignment protein sequences to scaffolded genomes with miniprot"""

# Imports ======================================================================

import shutil
import os.path
from argparse import ArgumentParser
from multiprocessing import Pool
from functools import partial
from subprocess import run

# Functions ====================================================================

def check_miniprot():
    path = shutil.which('miniprot')
    if path:
        print(f'miniprot found at {path}')
    else:
        raise RuntimeError('miniprot not found')


def splice_align(genome, proteins, outdir='.'):
    with open(os.path.join(
        outdir, os.path.basename(genome).replace('softmasked.fasta.gz', 'paf')
    )) as f:
        run((shutil.which('miniprot'), '-t', '1', genome, proteins), stdout=f)


def parse_arguments():
    parser = ArgumentParser(description='align protein sequences to scaffolded genomes')
    parser.add_argument('outdir', help='directory for output files')
    parser.add_argument('--genomes', nargs='+', required=True)
    parser.add_argument('--proteins', required=True)
    parser.add_argument('--processes', type=int, help='number of processes')
    return parser.parse_args()


def main():
    args = parse_arguments()
    check_miniprot()
    with Pool(processes=args.processes) as pool:
        pool.map(partial(splice_align, proteins=args.proteins, outdir=args.outdir), args.genomes)


# Execute ======================================================================

if __name__ == '__main__':
    main()
