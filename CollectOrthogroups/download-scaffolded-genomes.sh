mkdir scaffolded_genomes
for genome in `python scaffolded.py`;
  do aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${genome}/${genome}.softmasked.fasta.gz scaffolded_genomes/${genome}.softmasked.fasta.gz;
done
