mkdir genomes
aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/ genomes/ \
  --recursive --exclude "*" --include "*.softmasked.fasta.gz"
aws s3 cp s3://salk-tm-shared/csat/releases/notscaffolded/ genomes/ \
  --recursive --exclude "*" --include "*.softmasked.fasta.gz"
