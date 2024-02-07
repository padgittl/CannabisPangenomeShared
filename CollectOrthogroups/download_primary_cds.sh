mkdir primary_high_confidence
aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/ primary_high_confidence/ \
  --recursive --exclude "*" --include "*.primary_high_confidence.cds.fasta.gz" --include "*.primary_high_confidence.bed.gz"
aws s3 cp s3://salk-tm-shared/csat/releases/not_scaffolded/ primary_high_confidence/ \
  --recursive --exclude "*" --include "*.primary_high_confidence.cds.fasta.gz" --include "*.primary_high_confidence.bed.gz"
aws s3 cp s3://salk-tm-shared/csat/releases/publics/ primary_high_confidence/ \
  --recursive --exclude "*" --include "*.primary_high_confidence.cds.fasta.gz" --include "*.primary_high_confidence.bed.gz"
gunzip primary_high_confidence/*/*.primary_high_confidence.cds.fasta.gz
