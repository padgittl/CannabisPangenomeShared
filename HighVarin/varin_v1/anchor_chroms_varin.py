#===============================================================================
# anchor_chroms_varin.py
#===============================================================================

import pankmer
import os
import os.path
from argparse import ArgumentParser
from itertools import islice

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('sample')
    parser.add_argument('-t', '--threads', type=int, default=1)
    return parser.parse_args()

args = parse_arguments()
sizes = pankmer.anchor.get_chromosome_sizes_from_anchor(
    os.path.join('varin_genomes', f'{args.sample}.softmasked.fasta.gz')
)
os.mkdir(os.path.join('anchor', args.sample))
for _, (chrom, size) in islice(sizes.iterrows(), 10):
    print(chrom, size)
    pankmer.anchor_region(
        'varin_x_subset',
        anchor=os.path.join('varin_genomes', f'{args.sample}.softmasked.fasta'),
        coords=f'{chrom}:1-{size}',
        output_file=os.path.join('anchor', args.sample, f'{chrom}.bdg.gz'),
        bgzip=True,
        threads=args.threads
    )

    # import seaborn as sns
    # COLOR_PALETTE = sns.color_palette("husl", 4)
    # pankmer.anchor_genome(
    #     eh23a, ho40, parent0, parent1,
    #     output=os.path.join('anchor', args.sample, f'{chrom}.svg'),
    #     anchor=os.path.join('genomes-crosses', f'{args.sample}.softmasked.fasta.gz'),
    #     chromosomes=[chrom],
    #     output_table=os.path.join('anchor', args.sample, f'{chrom}.tsv'),
    #     groups=['EH23a', 'HO40'] + args.parent,
    #     legend=True,
    #     title=None,
    #     legend_title='Ancestor',
    #     legend_loc='outside',
    #     x_label=f'{chrom} (Mb)',
    #     color_palette=COLOR_PALETTE,
    #     processes=args.processes
    # )
