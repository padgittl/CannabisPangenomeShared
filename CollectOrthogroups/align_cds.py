#===============================================================================
# align_cds.py
#===============================================================================

"""splice-aware alignment CDS sequences to scaffolded genomes with minimap2"""

# Imports ======================================================================

import shutil
from argparse import ArgumentParser

# Functions ====================================================================

def check_minimap2():
    path = shutil.which('minimap2')
    if path:
        print(f'minimap2 found at {path}')
    else:
        raise RuntimeError('minimap2 not found')



def parse_arguments():
    parser = ArgumentParser(description='align CDS sequences to scaffolded genomes')
    parser.add_argument('outdir', help='directory for output files')
    parser.add_argument('--genomes', nargs='+', required=True)
    parser.add_argument('--cds', nargs='+', required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()

# Execute ======================================================================

if __name__ == '__main__':
    main()
