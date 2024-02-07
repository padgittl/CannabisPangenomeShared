mkdir primary_high_confidence_cds_merged_scaffolded
cat primary_high_confidence_scaffolded/*.fasta | seqkit rmdup -s | bgzip -c > primary_high_confidence_cds_merged_scaffolded/primary_high_confidence.cds.fasta.gz
