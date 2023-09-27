mkdir primary_high_confidence_cds
for line in `python scaffolded.py`;
  do aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${line}/${line}.primary_high_confidence.cds.fasta.gz primary_high_confidence_cds/${line}.primary_high_confidence.cds.fasta.gz;
done
