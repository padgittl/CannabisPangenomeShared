#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

mkdir primary_high_confidence_proteins
for genome in `python scaffolded.py`;
  do aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${genome}/${genome}.primary_high_confidence.proteins.fasta.gz primary_high_confidence_proteins/${genome}.primary_high_confidence.proteins.fasta.gz;
done
