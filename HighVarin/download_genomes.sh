mkdir varin_genomes non_varin_genomes
for varin in COFBa COSVb DPFBb DPSVb MBFBb MBSVb OFBb PPFBb SDFBb SKFBb SVA12a SVA6a TKFBb TWFBb TWSVb UFBb WCFBb; do
  aws s3 cp s3://salk-tm-shared/csat/releases/${varin}/${varin}.softmasked.fasta.gz varin_genomes/${varin}.softmasked.fasta.gz
done

for non_varin in COFBb COSVa DPFBa DPSVa MBFBa MBSVa OFBa PPFBa SDFBa SKFBa SVA12b SVA6b TKFBa TWFBa TWSVa UFBa WCFBa; do
  aws s3 cp s3://salk-tm-shared/csat/releases/${non_varin}/${non_varin}.softmasked.fasta.gz non_varin_genomes/${non_varin}.softmasked.fasta.gz
done