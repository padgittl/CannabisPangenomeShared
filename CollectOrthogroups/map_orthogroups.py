import pandas as pd
import os.path
from scaffolded import SCAFFOLDED

PAF_DIR = 'filtered_cds_cigar'

hogs = tuple(pd.read_table(
        'orthofinder-proteomes/primary_transcripts/OrthoFinder/Results_Jan21/Phylogenetic_Hierarchical_Orthogroups/N7.tsv',
        index_col=0)['Cannabis_sativa_high_confidence_prot_merged'].dropna().index)

gene_to_hog = {
    gene: hog for hog, gene_list in pd.read_table(
        'orthofinder-proteomes/primary_transcripts/OrthoFinder/Results_Jan21/Phylogenetic_Hierarchical_Orthogroups/N7.tsv',
        index_col=0)['Cannabis_sativa_high_confidence_prot_merged'].dropna().items()
    for gene in gene_list.split(', ')
}

def hap_to_genes(paf_file):
    return tuple(pd.read_table(paf_file, index_col=0).index)

haps_to_hogs = {hap: {gene_to_hog[g]
                      for g in hap_to_genes(os.path.join(PAF_DIR, f'{hap}.paf'))
                      if gene_to_hog.get(g)}
                 for hap in SCAFFOLDED}

pd.DataFrame({hap: [h in haps_to_hogs[hap] for h in hogs] for hap in SCAFFOLDED}, index=hogs).to_csv('orthogroup_table.tsv', sep='\t')
