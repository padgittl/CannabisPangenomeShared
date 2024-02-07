mkdir primary_high_confidence_cds
aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${genome}/ primary_high_confidence_cds/ \
  --recursive --exclude "*" --include "*.primary_high_confidence.cds.fasta.gz"
aws s3 cp s3://salk-tm-shared/csat/releases/not-scaffolded/${genome}/ primary_high_confidence_cds/ \
  --recursive --exclude "*" --include "*.primary_high_confidence.cds.fasta.gz"
