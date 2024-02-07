Steps to generate orthogroup-based collection curves
```sh
sh download-scaffolded-primary-cds.sh
sh merge-cds.sh
sh download-scaffolded-genomes.sh
python align_cds.py --genomes genomes/*.fasta.gz \
  --cds primary_high_confidence_cds_merged/primary_high_confidence.cds.fasta.gz \
  --processes 2 \
  aligned_cds/
python filter_aligned_cds.py --paf aligned_cds/*.paf \
  --cigar \
  --match-percent 80 \
  --paf aligned_cds/*.paf \
  filtered_cds/
python collect_orthogroups.py
```