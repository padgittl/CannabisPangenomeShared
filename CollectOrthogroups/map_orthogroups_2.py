import pandas as pd
import os.path
from itertools import chain
from scaffolded import SCAFFOLDED
from pyfaidx import Fasta

PAF_DIR = 'filtered_cds_cigar'
CDS_DIR = 'primary_high_confidence_cds'
HOG_TSV = 'nolans-orthofinder/Phylogenetic_Hierarchical_Orthogroups/N30.tsv'
SINGLETONS_TSV = 'nolans-orthofinder/Orthogroups/Orthogroups_UnassignedGenes.tsv'
hogs = tuple(pd.read_table(HOG_TSV, index_col=0)[SCAFFOLDED].dropna(how='all').index)
singletons = {
    gene[:-3]: og for og, gene_list in pd.read_table(SINGLETONS_TSV, index_col=0, dtype=str)[SCAFFOLDED].dropna(how='all').iterrows()
    for gene in (g for g in gene_list if (not pd.isna(g)))
}
gene_to_og = {
    gene[:-3]: hog for hog, gene_list in pd.read_table(HOG_TSV, index_col=0)[SCAFFOLDED].dropna(how='all').iterrows()
    for gene in ', '.join(g for g in gene_list if (not pd.isna(g))).split(', ')
}
ogs = hogs #+ tuple(singletons.values())
# gene_to_og.update(singletons)

def hap_to_genes(paf_file, cds_file):
    with open(paf_file, 'r') as f:
        genes = set(l.split()[0] for l in f.readlines())
        # genes = set(chain((l.split()[0] for l in f.readlines()), Fasta(cds_file).keys()))
    return genes

haps_to_ogs = {hap: {gene_to_og[g[:-3]]
                        for g in hap_to_genes(
                            os.path.join(PAF_DIR, f'{hap}.paf'),
                            os.path.join(CDS_DIR, f'{hap}.primary_high_confidence.cds.fasta')
                        )
                        if gene_to_og.get(g[:-3])}
                 for hap in SCAFFOLDED}

og_tab = pd.DataFrame({hap: [og in haps_to_ogs[hap] for og in ogs] for hap in SCAFFOLDED}, index=ogs)
og_tab.loc[~(og_tab==False).all(axis=1)].to_csv('orthogroup_table.tsv', sep='\t')
