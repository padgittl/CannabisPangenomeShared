mkdir primary_high_confidence_scaffolded
for genome in `python scaffolded.py`; do
  aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${genome}/${genome}.primary_high_confidence.cds.fasta.gz primary_high_confidence_scaffolded/${genome}.primary_high_confidence.cds.fasta.gz;
  gunzip primary_high_confidence_scaffolded/${genome}.primary_high_confidence.cds.fasta.gz
  aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${genome}/${genome}.primary_high_confidence.bed.gz primary_high_confidence_scaffolded/${genome}.primary_high_confidence.bed.gz;
done
