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
python align_cds.py --genomes genomes_scaffolded/*.fasta \
  --cds primary_high_confidence_cds_merged_scaffolded/primary_high_confidence.cds.fasta.gz \
  --processes 2 \
  aligned_cds_scaffolded/
python filter_aligned_cds.py \
  --cigar \
  --match-percent 80 \
  --paf aligned_cds_scaffolded/*.paf \
  --bed primary_high_confidence_scaffolded/*.bed.gz \
  --processes 2 \
  filtered_cds_scaffolded/
python collect_orthogroups_scaffolded.py --rescue
```

Steps to generate orthogroup-based collection curves (all genomes)
```sh
sh download_genomes.sh
sh download_primary_cds.sh
sh download_orthogroups.sh
sh merge_cds.sh
python align_cds.py --genomes genomes/*/*.fasta.gz \
  --cds primary_high_confidence_cds_merged/primary_high_confidence.cds.fasta.gz \
  --processes 2 \
  aligned_cds/
python filter_aligned_cds.py \
  --cigar \
  --match-percent 80 \
  --paf aligned_cds/*.paf \
  --bed primary_high_confidence/*/*.bed.gz \
  --processes 64 \
  filtered_cds/
python collect_orthogroups.py --rescue
```

# Analysis of gene-based pangenome
We define the gene-based pangenome as the set of all gene families (orthogroups) with a representative in at least one genome of the pangenome. For each of 78/193 _C. sativa_ genomes, the primary transcript of each high-confidence gene prediction was chosen as a representative. The proteins corresponding to each primary transcript were clustered into orthogroups using Orthofinder (v.2.5.5) [^1] (parameters in supplementary data X). The set of primary transcripts CDS were merged into a single FASTA file, and exact duplicates were removed with SeqKit (2.7.0) [^2]. Among primary transcripts, likely contaminants were determined by identifying transcripts predicted on contigs where fewer than 90% of predictions were annotated as either "viridiplantae" or "eukaryote" according to eggNOG-mapper (v2.1.12) [^3], and were removed. To mitigate the problem of unannotated genes, we aligned coding sequences of all primary transcripts to each of the 78/193 _Cannabis_ genomes using `minimap2` (v2.26) [^2] with parameters `minimap2 -c -x splice` to generate a PAF file with CIGAR strings for each genome. For each genome, if an aligned CDS sequence had a mapping quality of at least 60, had a number of CIGAR matches at least 80% of the query length, and did not overlap a directly annotated gene, it was considered an unannotated gene and its orthogroup was marked as present in the target genome. The set of orthogroups that had at least one representative present in all 78/193 genomes were considered to be the core genome, the remaining orthogroups were considered to be the variable genome. The presence or absence of each orthogroup in each genome was recorded in a table (supplemental data X). This table was used to compute the collection/rarefaction curves (supplemental note X).

[^1]: OrthoFinder: phylogenetic orthology inference for comparative genomics
[^2]: SeqKit: A Cross-Platform and Ultrafast Toolkit for FASTA/Q File Manipulation
[^3]: eggNOG-mapper v2: Functional Annotation, Orthology Assignments, and Domain Prediction at the Metagenomic Scale 
[^4]: Minimap2: pairwise alignment for nucleotide sequences
