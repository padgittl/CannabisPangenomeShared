# Calculation of collection/rarefaction curves

In a pangenome with haplotypes H and gene familes / orthogroups X, some orthogroups are unique to a single haplotype, some are shared across multiple haplotypes, and some are present in all haploytpes (the core genome). 

In pangenomics, collection or rarefaction curves show the relationship of the number of haplotypes (here *|H|*) to the number of gene families or orthogroups (here *|X|*). 

Given the table P(|X|,|H|) with |X| orthogroups and |H| haplotypes, let the _score_ s_x in [0,H] of an orthogroup x be the number of haplotypes *h* in which x is present. Let s_h in [0,X] be |s_x such that s_x = h| 

```python
S(x) [0,H] -> [0,X] = sum(s_x == s for x in range(0,X))
```

For each number of haplotypes h, we estimate the total number of orthogroups in the pangenome:
```python
sum(
    (1-prod((H-s-n)/(H-n) for n in range(h)))*score_dist[s]
    for s in range(1, H+1)
)
```
and the likewise the size of the core genome:
```python
sum(
    prod((s-n)/(g-n) for n in range(n_genomes))*score_dist[s]
    for s in range(1, g+1)
)
```

Each is a special case of a general formula for estimating the number of orthogroups that will have a sco, based on the hypergeometric survival function:
```python
sum(
    hypergeom.sf(k, g, s, n_genomes)*score_dist[s]
    for s in range(1, g+1)
)
```
in the pangenome case, k=1. In the core genome case k=n_genomes.
