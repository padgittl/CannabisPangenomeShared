# Counting orthogroups

This directory contains a method to count orthogroups (representing "pan-genes") from the included tables:

| File | Description |
| ---- | ----------- |
| `orthogroup_table.tsv` | Presence-absence table of genomes x orthogroups for the full pangenome |
| `orthogroup_table_scaffolded.tsv` | Table for the set of scaffolded genomes only |

Running `count_orthogroups.py` will produce a table with estimated count of "Pan" (total) and "Core" (universal) genes for each genome size. This is the underlying data for the collection cuve plot. For example:

```sh
python count_orthogroups.py orthogroup_table_scaffolded.tsv
```
```
Genomes Orthogroups     Level
1       30456.4358974359        Pan
1       30456.4358974359        Core
2       35920.41158841159       Pan
2       24992.460206460208      Core
...
78      60661.0 Pan
78      9010.0  Core
```

This means the estimate for the number of genes in a single genome is about 30456, for a pangenome of 2 samples 35920 pan-genes and 24992 core genes, etc, until listing the final count of observed pan- (60661) and core (9010) genes in the 78-sample pangenome. If you only want to see the final result, you can use `tail`

```sh
python count_orthogroups.py orthogroup_table_scaffolded.tsv | tail -n 2
```
```
78      60661.0 Pan
78      9010.0  Core
```

To address questions of "shell," "cloud," "dispensable," and "private", you can use the `--contours` argument. For example, to see how many orthogroups are present in *at least 50% of the samples:

```sh
python count_orthogroups.py orthogroup_table_scaffolded.tsv --contours 50 | tail -n 3
```
```
78      60661.0 Pan
78      28728.0 50%
78      9010.0  Core
```
So, of the 60661 pan-genes, 9010 are present in all 78 samples, and 28728 are in at least 39 samples. One interpretation of core/shell/cloud could be:

| Level | N. genes |
| ----- | -------- |
| Core | 9010 |
| Shell | 19718 |
| Cloud | 31933 |

You can use as many contours as you want:

```sh
python count_orthogroups.py orthogroup_table_scaffolded.tsv --contours 25 50 75 | tail -n 5
```
```
78      60661.0 Pan
78      35867.0 25%
78      28728.0 50%
78      23571.0 75%
78      9010.0  Core
```

If you need the contours to be floats there is a `--contours-float` argument. For example, if we want the "private" genes to be those that are in exactly one genome we can find it by counting how many genes are in *at least two* genomes. We set a contour of `2 / 78 = 2.56%`.

```sh
python count_orthogroups.py orthogroup_table_scaffolded.tsv --contours-float 2.56 | tail -n 3
```
```
78      60661.0 Pan
78      57239.0 2.56%
78      9010.0  Core
```

Hence, the number of genes in exactly one genome is `60661 - 57239 = 3422`, and another interpretation of gene counts can be:

| Level | N. genes |
| ----- | -------- |
| Core | 9010 |
| Dispensable | 48229 |
| Private | 3422 |