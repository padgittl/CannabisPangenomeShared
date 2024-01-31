import pandas as pd
import os.path
from scaffolded import SCAFFOLDED

PAF_DIR = 'filtered_cds_cigar'
HOG_TSV = 'nolans-orthofinder/Phylogenetic_Hierarchical_Orthogroups/N30.tsv'
SINGLETONS_TSV = 'nolans-orthofinder/Orthogroups/Orthogroups_UnassignedGenes.tsv'
hogs = tuple(pd.read_table(HOG_TSV, index_col=0)[SCAFFOLDED].dropna().index)
singletons = {
    gene: og for og, gene_list in pd.read_table(SINGLETONS_TSV, index_col=0, dtype=str)[SCAFFOLDED].iterrows()
    for gene in (g for g in gene_list if (not pd.isna(g)))
}
gene_to_og = {
    gene: hog for hog, gene_list in pd.read_table(HOG_TSV, index_col=0)[SCAFFOLDED].iterrows()
    for gene in ', '.join(g for g in gene_list if (not pd.isna(g))).split(', ')
}
ogs = hogs + tuple(singletons.values())
gene_to_og.update(singletons)

def hap_to_genes(paf_file):
    return tuple(pd.read_table(paf_file, index_col=0).index)

haps_to_ogs = {hap: {gene_to_og[g]
                      for g in hap_to_genes(os.path.join(PAF_DIR, f'{hap}.paf'))
                      if gene_to_og.get(g)}
                 for hap in SCAFFOLDED}

pd.DataFrame({hap: [og in haps_to_ogs[hap] for og in ogs] for hap in SCAFFOLDED}, index=ogs).to_csv('orthogroup_table.tsv', sep='\t')
