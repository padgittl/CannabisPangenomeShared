mkdir varin_genomes non_varin_genomes
for varin in EH23a EH23b COFBa DPFBb MBFBb OFBb PPFBb SDFBb SKFBb TKFBb TWFBb UFBb WCFBb SVA12a SVA6a TWSVa COSVb DPSVb MBSVb; do
  aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${varin}/${varin}.softmasked.fasta.gz varin_genomes/${varin}.softmasked.fasta.gz
done
for varin in HO40 FB191 USV WCSV SKSV ACBD SHH24 SSV SV2 SSHS WH106; do
  aws s3 cp s3://salk-tm-shared/csat/releases/not_scaffolded/${varin}/${varin}.softmasked.fasta.gz varin_genomes/${varin}.softmasked.fasta.gz
done

for non_varin in COFBb DPFBa MBFBa OFBa PPFBa SDFBa SKFBa TKFBa TWFBa UFBa WCFBa; do
  aws s3 cp s3://salk-tm-shared/csat/releases/scaffolded/${non_varin}/${non_varin}.softmasked.fasta.gz non_varin_genomes/${non_varin}.softmasked.fasta.gz
done
