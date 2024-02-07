Steps to generate orthogroup-based collection curves (scaffolded only)
```sh
sh download-scaffolded-genomes.sh
sh download-scaffolded-primary-cds.sh
sh merge-cds.sh
python align_cds.py --genomes scaffolded_genomes/*.fasta.gz \
  --cds primary_high_confidence_cds_merged/primary_high_confidence.cds.fasta.gz \
  --processes 2 \
  aligned_cds_scaffolded/
python filter_aligned_cds.py --paf aligned_cds_scaffolded/*.paf \
  --cigar \
  --match-percent 80 \
  --paf aligned_cds/*.paf \
  --processes 2 \
  filtered_cds_scaffolded/
sh download-orthogroups-scaffolded.sh
python collect_orthogroups.py --rescue filtered_cds_scaffolded/
```

Steps to generate orthogroup-based collection curves (all genomes)
```sh
sh download-genomes.sh
sh download-primary-cds.sh
sh merge-cds.sh
python align_cds.py --genomes genomes/*.fasta.gz \
  --cds primary_high_confidence_cds_merged/primary_high_confidence.cds.fasta.gz \
  --processes 2 \
  aligned_cds/
python filter_aligned_cds.py --paf aligned_cds/*.paf \
  --cigar \
  --match-percent 80 \
  --paf aligned_cds/*.paf \
  --processes 2 \
  filtered_cds/
sh download-orthogroups.sh
python collect_orthogroups.py --rescue filtered_cds/
```

1. coding sequences merged to a single file
2. duplicate sequences removed with seqkig
3. all sequences aligned to all genomes
