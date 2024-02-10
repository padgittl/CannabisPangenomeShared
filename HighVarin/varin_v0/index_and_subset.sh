pankmer index -g varin_genomes/ non_varin_genomes/ -o varin_non_varin_index.tar
pankmer subset -x -i varin_non_varin_index.tar -o varin_x_subset.tar \
  -g EH23a.softmasked EH23b.softmasked COFBa.softmasked DPFBb.softmasked \
     MBFBb.softmasked OFBb.softmasked PPFBb.softmasked SDFBb.softmasked \
     SKFBb.softmasked TKFBb.softmasked TWFBb.softmasked UFBb.softmasked \
     WCFBb.softmasked SVA12a.softmasked SVA6a.softmasked TWSVa.softmasked \
     COSVb.softmasked DPSVb.softmasked MBSVb.softmasked HO40.softmasked \
     FB191.softmasked USV.softmasked WCSV.softmasked SKSV.softmasked \
     ACBD.softmasked SHH24.softmasked SSV.softmasked SV2.softmasked \
     SSHS.softmasked WH106.softmasked
