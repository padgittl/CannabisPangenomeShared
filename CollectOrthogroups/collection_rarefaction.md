# Calculation of collection/rarefaction curves

Given the table X(r,g) with r orthogroups and g genomes, let the _score_ s_r in [0,g] of orthogroup r be the number of genomes in which r is present. let S be the distribution of scores, where S_s is the number of orthogroups with score s.

For each number of genomes g, we estimate the total number of orthogroups in the pangenome:
```python
sum(
    (1-prod((g-s-n)/(g-n) for n in range(n_genomes)))*score_dist[s]
    for s in range(1, g+1)
)
```
and the likewise the size of the core genome:
```python
sum(
    prod((s-n)/(g-n) for n in range(n_genomes))*score_dist[s]
    for s in range(1, g+1)
)
```

Each is a special case of a general formula for estimating the number of orthogroups that will be found in at least *k* genomes, based on the hypergeometric survival function:
```python
sum(
    (
        hypergeom.sf(k, g, s, n_genomes)
    )*score_dist[s]
    for s in range(1, g+1)
)
```
in the pangenome case k=1, in the core genome case k=n_genomes