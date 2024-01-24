import urllib3
import gzip

proteomes = {
    'Corylus_avellana': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/corylus_avellana/pep/Corylus_avellana.CavTom2PMs-1.0.pep.all.fa.gz',
    'Cucumis_sativus': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/cucumis_sativus/pep/Cucumis_sativus.ASM407v2.pep.all.fa.gz',
    'Ficus_carica': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/ficus_carica/pep/Ficus_carica.UNIPI_FiCari_1.0.pep.all.fa.gz',
    'Glycine_max': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/glycine_max/pep/Glycine_max.Glycine_max_v2.1.pep.all.fa.gz',
    'Glycine_soja': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/glycine_soja/pep/Glycine_soja.ASM419377v2.pep.all.fa.gz',
    'Malus_domestica': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/malus_domestica_golden/pep/Malus_domestica_golden.ASM211411v1.pep.all.fa.gz',
    'Medicago_truncatula': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/medicago_truncatula/pep/Medicago_truncatula.MedtrA17_4.0.pep.all.fa.gz',
    'Phaseolus_vulgaris': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/phaseolus_vulgaris/pep/Phaseolus_vulgaris.PhaVulg1_0.pep.all.fa.gz',
    'Prunus_persica': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/prunus_persica/pep/Prunus_persica.Prunus_persica_NCBIv2.pep.all.fa.gz'
}

http = urllib3.PoolManager()
    with http.request('GET', PBCPG_URL, preload_content=False) as r, open(dest_tarfile, 'wb') as f:
        shutil.copyfileobj(r, f)
with gzip.open(f'{hg38_genome_local_path}.gz', 'rb') as f_in:
        with open(hg38_genome_local_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(f'{hg38_genome_local_path}.gz')

def main():
    for proteome, url in proteomes:

if __name__ == '__main__':
    main()
