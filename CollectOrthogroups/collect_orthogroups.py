import pandas as pd
import os.path
from argparse import ArgumentParser
from csativa_genomes import CSATIVA_GENOMES
from pyfaidx import Fasta
from collections import Counter
import seaborn as sns
from math import prod, floor
from scipy.stats import hypergeom

PAF_DIR = 'filtered_cds'
CDS_DIR = 'primary_high_confidence'
HOG_TSV = 'nolans-orthofinder/Phylogenetic_Hierarchical_Orthogroups/N30.tsv'
SINGLETONS_TSV = 'nolans-orthofinder/Orthogroups/Orthogroups_UnassignedGenes.tsv'
LIKELY_CONTAMINANTS = 'csat.likely_contaminants.tsv'
COL_COLOR_PALETTE = 'magma_r'
COL_TWO_COLORS = "#1E90FF", "#FFA500"

def hap_to_genes(cds_file, contam, rescue_alignment=None):
    directly_predicted_genes = set(Fasta(cds_file).keys()) - contam
    if rescue_alignment:
        with open(rescue_alignment, 'r') as f:
            rescued_genes = set(l.split()[0] for l in f.readlines()) - contam
    else:
        rescued_genes = set()
    return directly_predicted_genes.union(rescued_genes)


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
            'pan'
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


def col_plot(plotting_data, output, title: str = 'Collection curve',
             linewidth: int = 3, palette=COL_COLOR_PALETTE, alpha: float = 1.0,
             width: float = 4.0, height: float = 3.0, legend_loc='best'):
    """Draw a plot of the collection curve

    Parameters
    ----------
    plotting_data : DataFrame
        data frame of plotting data to be passed to sns.lineplot
    output
        path to output file
    title : str
        plot title [Collection curve]
    linewidth : int
        line width [3]
    palette
        argument sent to seaborn to be used as color palette [mako_r]
    alpha : float
        opacity of plot lines [1.0]
    width : float
        width of plot in inches [4.0]
    height : float
        height of plot in inches [3.0]
    legend_loc : str
        location of plot legend, e.g. 'upper left', 'best', or 'outside' [best]
    """

    ax = sns.lineplot(x='Genomes', y='Orthogroups', hue='sequence',
                      data=plotting_data, linewidth=linewidth,
                      palette=palette, alpha=alpha)
    ax.set_title(title)
    ax.set_ylim(bottom=0)
    if legend_loc == 'outside':
        leg = ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left',
                        borderaxespad=0)
    else:
        leg = ax.legend(loc=legend_loc)
    for line in leg.get_lines():
        line.set_linewidth(linewidth)
        line.set_alpha(alpha)
    fig = ax.get_figure()
    fig.set_figwidth(width)
    fig.set_figheight(height)
    fig.tight_layout()
    fig.savefig(output)
    fig.clf()

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-r', '--rescue')
    parser.add_argument('-c', '--contours', type=int, nargs='+')
    return parser.parse_args()

def main():
    args = parse_arguments()
    hogs = tuple(pd.read_table(HOG_TSV, index_col=0)[CSATIVA_GENOMES].dropna(how='all').index)
    gene_to_og = {
        gene: hog for hog, gene_list in pd.read_table(HOG_TSV, index_col=0)[CSATIVA_GENOMES].dropna(how='all').iterrows()
        for gene in ', '.join(g for g in gene_list if (not pd.isna(g))).split(', ')
    }
    # singletons = {
    #     gene: og for og, gene_list in pd.read_table(SINGLETONS_TSV, index_col=0, dtype=str)[CSATIVA_GENOMES].dropna(how='all').iterrows()
    #     for gene in (g for g in gene_list if (not pd.isna(g)))
    # }
    # gene_to_og.update(singletons)
    ogs = hogs #+ tuple(singletons.values())
    haps_to_ogs = {hap: {gene_to_og[g]
                            for g in hap_to_genes(
                                os.path.join(CDS_DIR, f'{hap}.primary_high_confidence.cds.fasta'),
                                set(pd.read_table(LIKELY_CONTAMINANTS)['GID']),
                                rescue_alignment=os.path.join(PAF_DIR, f'{hap}.paf') if args.rescue else None
                            )
                            if gene_to_og.get(g)}
                    for hap in CSATIVA_GENOMES}
    ortho = pd.DataFrame(
        {hap: [og in haps_to_ogs[hap] for og in ogs] for hap in CSATIVA_GENOMES},
        index=ogs
    )
    ortho = ortho.loc[~(ortho==False).all(axis=1)]
    ortho.to_csv('orthogroup_table.tsv', sep='\t')

    contours = args.contours
    col_df = pd.DataFrame(
        col_values(ortho, contours=contours),
        columns=('Genomes', 'Orthogroups', 'sequence')
    )
    col_df.to_csv('Csativa-collect-orthogroups.tsv', index=False, sep='\t')
    col_plot(col_df, 'Csativa-collect-orthogroups.svg', title='',
                 palette=(COL_COLOR_PALETTE if contours else COL_TWO_COLORS))
    col_plot(col_df, 'Csativa-collect-orthogroups.pdf', title='',
                 palette=(COL_COLOR_PALETTE if contours else COL_TWO_COLORS))


if __name__ == '__main__':
    main()
