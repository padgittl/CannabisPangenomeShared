for line in `python scaffolded.py`;
  do aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${line}/${line}.primary_high_confidence.proteins.fasta.gz ${line}.primary_high_confidence.proteins.fasta.gz;
done
