mkdir genomes_scaffolded
for genome in `python scaffolded.py`;
  do aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${genome}/${genome}.softmasked.fasta.gz genomes_scaffolded/${genome}.softmasked.fasta.gz;
done
