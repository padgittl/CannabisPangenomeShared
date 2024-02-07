mkdir primary_high_confidence_cds_merged
cat primary_high_confidence/*/*.fasta | seqkit rmdup -s | bgzip -c > primary_high_confidence_cds_merged/primary_high_confidence.cds.fasta.gz
