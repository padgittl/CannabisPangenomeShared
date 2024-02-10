# Orthogroup-based collection curves

conda environment
```sh
conda create -n CollectKmers -c conda-forge -c bioconda cython \
  gff2bed more-itertools pybedtools python-newick pyfaidx \
  rust seaborn upsetplot urllib3
conda activate CollectKmers
pip install pankmer
```

Steps to generate k-mer-based collection curves (scaffolded only)
```sh
sh download_genomes_scaffolded.sh
sh index_kmers_scaffolded.sh
sh collect_kmers_scaffolded.sh
```

Steps to generate k-mer-based collection curves (all genomes)
```sh
sh download_genomes.sh
sh index_kmers.sh
sh collect_kmers.sh
```
