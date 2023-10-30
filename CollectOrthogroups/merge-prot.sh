mkdir primary_high_confidence_prot_merged
cat primary_high_confidence_prot/*.fasta.gz | seqkit rmdup -s | bgzip -c > primary_high_confidence_prot_merged/primary_high_confidence.proteins.fasta.gz
