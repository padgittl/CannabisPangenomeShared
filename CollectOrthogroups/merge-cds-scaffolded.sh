mkdir primary_high_confidence_cds_merged_scaffolded
cat primary_high_confidence_cds_scaffolded/*.fasta.gz | seqkit rmdup -s | bgzip -c > primary_high_confidence_cds_merged_scaffolded/primary_high_confidence.cds.fasta.gz
