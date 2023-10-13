#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

mkdir primary_high_confidence_cds
for genome in `python scaffolded.py`;
  do aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${genome}/${genome}.primary_high_confidence.cds.fasta.gz primary_high_confidence_cds/${genome}.primary_high_confidence.cds.fasta.gz;
done
