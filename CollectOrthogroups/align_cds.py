#===============================================================================
# align_cds.py
#===============================================================================

"""splice-aware alignment CDS sequences to scaffolded genomes with minimap2"""

# Imports ======================================================================

import shutil
import os.path
from argparse import ArgumentParser
from multiprocessing import Pool
from functools import partial
from subprocess import run

# Functions ====================================================================

def check_minimap2():
    path = shutil.which('minimap2')
    if path:
        print(f'minimap2 found at {path}')
    else:
        raise RuntimeError('minimap2 not found')


def splice_align(genome, cds, outdir='.'):
    run(('minimap2', '-c', '-t', '1', '--splice',
         '-o', os.path.join(
             outdir,
            os.path.basename(genome).replace('softmasked.fasta.gz', 'paf')
         ),
         genome,
         cds
        )
    )


def parse_arguments():
    parser = ArgumentParser(description='align CDS sequences to scaffolded genomes')
    parser.add_argument('outdir', help='directory for output files')
    parser.add_argument('--genomes', nargs='+', required=True)
    parser.add_argument('--cds', required=True)
    parser.add_argument('--processes', type=int, help='number of processes')
    return parser.parse_args()


def main():
    args = parse_arguments()
    check_minimap2()
    with Pool(processes=args.processes) as pool:
        pool.map(partial(splice_align, cds=args.cds, outdir=args.outdir), args.genomes)


# Execute ======================================================================

if __name__ == '__main__':
    main()
