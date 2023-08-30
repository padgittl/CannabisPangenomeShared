from collections import Counter
import pandas as pd
import seaborn as sns
import numpy as np
from math import prod, floor
from scipy.stats import hypergeom

COL_COLOR_PALETTE = 'rocket_r'

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
            'core'
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

    ax = sns.lineplot(x='n_genomes', y='n_orthogroups', hue='sequence',
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


def main():
    contours = None
    palette = COL_COLOR_PALETTE
    ortho = pd.read_table('Phylogenetic_Hierarchical_Orthogroups/N3.tsv',
                      index_col=0, dtype=str).iloc[:,2:].notna()
    ortho = ortho.drop(
        ['FragariaVesca', 'LotusJaponicus', 'MalusDomestica', 'PrunusPersica', 'RosaChinensis'],
        axis=1
    )
    col_df = pd.DataFrame(col_values(ortho, contours=contours),
                              columns=('n_genomes', 'n_orthogroups', 'sequence'))
    col_df.to_csv('Csativa-collect-orthogroups.tsv', index=False, sep='\t')
    col_plot(col_df, 'Csativa-collect-orthogroups.svg',
                 palette=(palette if contours else sns.color_palette(palette, n_colors=2)))
    col_plot(col_df, 'Csativa-collect-orthogroups.pdf',
                 palette=(palette if contours else sns.color_palette(palette, n_colors=2)))

if __name__ == '__main__':
    main()
