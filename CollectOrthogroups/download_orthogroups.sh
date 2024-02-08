aws s3 cp s3://salk-tm-shared/csat/releases/orthofinder/csat_prots.full_small.orthofinder/Phylogenetic_Hierarchical_Orthogroups.tar.gz Phylogenetic_Hierarchical_Orthogroups.tar.gz
aws s3 cp s3://salk-tm-shared/csat/releases/orthofinder/csat_prots.full_small.orthofinder/Orthogroups.tar.gz Orthogroups.tar.gz
tar -zxvf Phylogenetic_Hierarchical_Orthogroups.tar.gz Phylogenetic_Hierarchical_Orthogroups/N3.tsv
tar -zxvf Orthogroups.tar.gz Orthogroups/Orthogroups_UnassignedGenes.tsv
rm Phylogenetic_Hierarchical_Orthogroups.tar.gz
rm Orthogroups.tar.gz