# Calculation of collection/rarefaction curves

Given the table X(r,g) with r orthogroups and g genomes, let the _score_ s_r in [0,g] of orthogroup r be the number of genomes in which r is present. let S be the distribution of scores, where S_s is the number of orthogroups with score s.

For each number of genomes g, we estimate the size of the pangenome:
```python
sum(
    (1-prod((g-s-n)/(g-n) for n in range(n_genomes)))*score_dist[s]
    for s in range(1, g+1)
)
```
and the size of the core genome:
```python
sum(
    prod((s-n)/(g-n) for n in range(n_genomes))*score_dist[s]
    for s in range(1, g+1)
)
```
