import pandas as pd

ortho = pd.read_table('Phylogenetic_Hierarchical_Orthogroups/N3.tsv',
                      index_col=0, dtype=str)
ortho['YMv2b'] = ortho['YMv2b'].map(lambda s: s != 'NaN')
print(ortho)
