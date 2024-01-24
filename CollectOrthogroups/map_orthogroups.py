import pandas as pd

gene_to_hog = {
    gene: hog for hog, gene_list in pd.read_table(
        'orthofinder-proteomes/primary_transcripts/OrthoFinder/Results_Jan21/Phylogenetic_Hierarchical_Orthogroups/N0.tsv',
        index_col=0)['Cannabis_sativa_high_confidence_prot_merged'].dropna().items()
    for gene in gene_list.split(', ')
  }
