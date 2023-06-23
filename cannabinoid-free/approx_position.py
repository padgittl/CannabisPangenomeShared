import pysam
from argparse import ArgumentParser
from statistics import mean, median

def parse_arguments():
    parser = ArgumentParser(description='approx position')
    parser.add_argument('contig')
    parser.add_argument('chrom')
    parser.add_argument('alignment')
    return parser.parse_args()


def main():
    args = parse_arguments()
    with pysam.AlignmentFile(args.alignment) as af:
        print(median(int(a.reference_start + len(a.query_sequence)/2)
            for a in af if all(
            (a.query_name==args.contig,
             af.getrname(a.reference_id)==args.chrom,
             a.mapping_quality>=60))))

if __name__ == '__main__':
    main()
