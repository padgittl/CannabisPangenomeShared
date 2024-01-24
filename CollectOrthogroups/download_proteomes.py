import urllib3
import shutil
import gzip
import os.path

DEST_DIR = 'proteomes/'

PROTEOMES = {
    'Corylus_avellana.CavTom2PMs-1.0.': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/corylus_avellana/pep/Corylus_avellana.CavTom2PMs-1.0.pep.all.fa.gz',
    'Cucumis_sativus.ASM407v2.': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/cucumis_sativus/pep/Cucumis_sativus.ASM407v2.pep.all.fa.gz',
    'Ficus_carica.UNIPI_FiCari_1.0.': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/ficus_carica/pep/Ficus_carica.UNIPI_FiCari_1.0.pep.all.fa.gz',
    'Glycine_max.Glycine_max_v2.1.': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/glycine_max/pep/Glycine_max.Glycine_max_v2.1.pep.all.fa.gz',
    'Glycine_soja.ASM419377v2.': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/glycine_soja/pep/Glycine_soja.ASM419377v2.pep.all.fa.gz',
    'Malus_domestica_golden.ASM211411v1.': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/malus_domestica_golden/pep/Malus_domestica_golden.ASM211411v1.pep.all.fa.gz',
    'Medicago_truncatula.MedtrA17_4.0.': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/medicago_truncatula/pep/Medicago_truncatula.MedtrA17_4.0.pep.all.fa.gz',
    'Phaseolus_vulgaris.PhaVulg1_0.': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/phaseolus_vulgaris/pep/Phaseolus_vulgaris.PhaVulg1_0.pep.all.fa.gz',
    'Prunus_persica.Prunus_persica_NCBIv2': 'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-58/fasta/prunus_persica/pep/Prunus_persica.Prunus_persica_NCBIv2.pep.all.fa.gz'
}

def download_proteome(url, dest_file):
    http = urllib3.PoolManager()
    with http.request('GET', url, preload_content=False) as r, open(f'{dest_file}.gz', 'wb') as f:
        shutil.copyfileobj(r, f)
    with gzip.open(f'{dest_file}.gz', 'rb') as f_in:
        with open(dest_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(f'{dest_file}.gz')


def main():
    for proteome, url in PROTEOMES.items():
        download_proteome(url, os.path.join(DEST_DIR, f'{proteome}.fa'))
        

if __name__ == '__main__':
    main()
