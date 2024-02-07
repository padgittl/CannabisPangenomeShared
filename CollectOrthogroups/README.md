# Orthogroup-based collection curves

conda environment
```sh
conda create -n CollectOrthogroups -c conda-forge -c bioconda python=3.10 awscli biopython cigar minimap2 pyarrow pandas seaborn seqkit tabix pyfaidx pybedtools
```

Steps to generate orthogroup-based collection curves (scaffolded only)
```sh
sh download_genomes_scaffolded.sh
sh download_primary_cds_scaffolded.sh
sh download_orthogroups_scaffolded.sh
sh merge_cds_scaffolded.sh
python align_cds.py --genomes genomes_scaffolded/*.fasta.gz \
  --cds primary_high_confidence_cds_merged/primary_high_confidence.cds.fasta.gz \
  --processes 2 \
  aligned_cds_scaffolded/
python filter_aligned_cds.py \
  --cigar \
  --match-percent 80 \
  --paf aligned_cds_scaffolded/*.paf \
  --bed primary_high_confidence_scaffolded/*.bed.gz \
  --processes 64 \
  filtered_cds_scaffolded/
python collect_orthogroups_scaffolded.py --rescue filtered_cds_scaffolded/
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

# Analysis of gene-based pangenome
We define the gene-based pangenome as the set of all genes present in at least one genome of the pangenome. For each of 78 _C. sativa_ genomes, the primary transcript of each high-confidence gene prediction was chosen as a representative. Among primary transcripts, likely contaminants were determined by [...] and removed. To mitigate the problem of unannotated genes, we aligned coding sequences of all primary transcripts to each of the 78 _Cannabis_ genomes using `minimap2` [ref] with parameters ... to generate a PAF file with CIGAR strings for each genome. For each genome, if an aligned CDS sequence had a mapping quality of at least 60, a number of CIGAR matches at least 80% of the query length, and did not overlap a directly annotated gene, it was considered an unannotated gene and its orthogroup was marked as present in the target genome.

1. coding sequences merged to a single file
2. duplicate sequences removed with seqkig
3. all sequences aligned to all genomes
