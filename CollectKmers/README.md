# *k*-mer-based collection curves

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
pankmer index -t 2 -g genomes_scaffolded/ -o csativa_index_scaffolded.tar
pankmer collect -i csativa_index_scaffolded.tar -o csativa_collect_scaffolded.svg \
  -t csativa_collect_scaffolded.tsv  --title "" --color-palette "#1E90FF" "#FFA500"
```

Steps to generate k-mer-based collection curves (all genomes)
```sh
sh download_genomes.sh
pankmer index -t 2 -g genomes/ -o csativa_index.tar
pankmer collect -i csativa_index.tar -o csativa_collect.svg \
  -t csativa_collect.tsv  --title "" --color-palette "#1E90FF" "#FFA500"
```
