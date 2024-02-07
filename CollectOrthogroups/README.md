Steps to generate orthogroup-based collection curves (scaffolded only)
```sh
sh download-scaffolded-genomes.sh
sh download-scaffolded-primary-cds.sh
sh merge-cds.sh
python align_cds.py --genomes scaffolded_genomes/*.fasta.gz \
  --cds primary_high_confidence_cds_merged/primary_high_confidence.cds.fasta.gz \
  --processes 2 \
  aligned_cds_scaffolded/
python filter_aligned_cds.py --paf aligned_cds/*.paf \
  --cigar \
  --match-percent 80 \
  --paf aligned_cds/*.paf \
  filtered_cds_scaffolded/
sh download-orthogroups-scaffolded.sh
python collect_orthogroups.py --rescue filtered_cds_scaffolded/
```