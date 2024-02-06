import pandas as pd
import os.path
from argparse import ArgumentParser
from itertools import chain
from scaffolded import SCAFFOLDED
from pyfaidx import Fasta

PAF_DIR = 'filtered_cds_cigar'
CDS_DIR = 'primary_high_confidence_cds'
HOG_TSV = 'nolans-orthofinder/Phylogenetic_Hierarchical_Orthogroups/N30.tsv'
SINGLETONS_TSV = 'nolans-orthofinder/Orthogroups/Orthogroups_UnassignedGenes.tsv'
LIKELY_CONTAMINANTS = 'csat.likely_contaminants.tsv'

def hap_to_genes(cds_file, paf_file, contam, rescue: bool = True):
    with open(paf_file, 'r') as f:
        genes = set(chain(
            Fasta(cds_file).keys(),
            (l.split()[0] for l in f.readlines()) if rescue else ()
        ))
    return genes - contam

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('-r', '--rescue', action='store_true')
    return parser.parse_args()

def main():
    args = parse_arguments()
    hogs = tuple(pd.read_table(HOG_TSV, index_col=0)[SCAFFOLDED].dropna(how='all').index)
    gene_to_og = {
        gene: hog for hog, gene_list in pd.read_table(HOG_TSV, index_col=0)[SCAFFOLDED].dropna(how='all').iterrows()
        for gene in ', '.join(g for g in gene_list if (not pd.isna(g))).split(', ')
    }
    # singletons = {
    #     gene: og for og, gene_list in pd.read_table(SINGLETONS_TSV, index_col=0, dtype=str)[SCAFFOLDED].dropna(how='all').iterrows()
    #     for gene in (g for g in gene_list if (not pd.isna(g)))
    # }
    # gene_to_og.update(singletons)
    ogs = hogs #+ tuple(singletons.values())
    haps_to_ogs = {hap: {gene_to_og[g]
                            for g in hap_to_genes(
                                os.path.join(CDS_DIR, f'{hap}.primary_high_confidence.cds.fasta'),
                                os.path.join(PAF_DIR, f'{hap}.paf'),
                                set(pd.read_table(LIKELY_CONTAMINANTS)['GID']),
                                rescue=args.rescue
                            )
                            if gene_to_og.get(g)}
                    for hap in SCAFFOLDED}
    og_tab = pd.DataFrame({hap: [og in haps_to_ogs[hap] for og in ogs] for hap in SCAFFOLDED}, index=ogs)
    og_tab.loc[~(og_tab==False).all(axis=1)].to_csv('orthogroup_table.tsv', sep='\t')

if __name__ == '__main__':
    main()
