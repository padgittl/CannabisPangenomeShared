import pandas as pd
import os.path
from scaffolded import SCAFFOLDED

PAF_DIR = 'filtered_cds_cigar'
HOG_TSV = 'nolans-proteomes/primary_transcripts/OrthoFinder/Results_Jan30/WorkingDirectory/OrthoFinder/Results_Jan31/Phylogenetic_Hierarchical_Orthogroups/N1.tsv'
SINGLETONS_TSV = 'nolans-proteomes/primary_transcripts/OrthoFinder/Results_Jan30/WorkingDirectory/OrthoFinder/Results_Jan31/Orthogroups/Orthogroups_UnassignedGenes.tsv'
CSAT_COLNAME = 'Cannabis_sativa_high_confidence_prot_merged'
hogs = tuple(pd.read_table(HOG_TSV, index_col=0)[CSAT_COLNAME].dropna().index)
singletons = {gene: og for og, gene in pd.read_table(SINGLETONS_TSV, index_col=0)[CSAT_COLNAME].dropna().items()}
gene_to_hog = {
    gene: hog for hog, gene_list in pd.read_table(HOG_TSV, index_col=0)[CSAT_COLNAME].dropna().items()
    for gene in gene_list.split(', ')
}
gene_to_og = gene_to_hog.update(singletons)

def hap_to_genes(paf_file):
    return tuple(pd.read_table(paf_file, index_col=0).index)

haps_to_ogs = {hap: {gene_to_og[g]
                      for g in hap_to_genes(os.path.join(PAF_DIR, f'{hap}.paf'))
                      if gene_to_og.get(g)}
                 for hap in SCAFFOLDED}

pd.DataFrame({hap: [h in haps_to_ogs[hap] for h in hogs] for hap in SCAFFOLDED}, index=hogs).to_csv('orthogroup_table.tsv', sep='\t')
