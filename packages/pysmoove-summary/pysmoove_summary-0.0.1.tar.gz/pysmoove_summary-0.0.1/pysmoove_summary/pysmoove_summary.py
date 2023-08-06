#===============================================================================
# pysmoove_summary.py
#===============================================================================

from argparse import ArgumentParser
from pysam import VariantFile

DHFFC_DEL = 0.7
DHFFC_DUP = 1.25
MSHQ = 3.0

def parse_arguments():
    parser = ArgumentParser(description='generate summary BED from VCF of SVs')
    parser.add_argument('vcf', metavar='<vcf>', help='VCF containing SVs')
    parser.add_argument('--dhffc-del', metavar='<float>', type=float,
        default=DHFFC_DEL, help=f'filter out deletions with DHFFC above this value [{DHFFC_DEL}]')
    parser.add_argument('--dhffc-dup', metavar='<float>', type=float,
        default=DHFFC_DUP, help=f'filter out deletions with DHFFC below this value [{DHFFC_DUP}]')
    parser.add_argument('--mshq', metavar='<float>', type=float,
        default=MSHQ, help=f'filter out hets with MSHQ below this value [{MSHQ}]')
    parser.add_argument('--header', action='store_true',
        help='include a header in output')
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.header:
        print('chrom', 'start', 'stop', 'type', 'size', 'samples',
                'genotypes', 'genes',  sep='\t')
    vcf_in = VariantFile(args.vcf)
    for rec in vcf_in.fetch():
        if rec.info['SVTYPE'] == 'BND':
            continue
        samples = tuple(s for s in rec.samples
                        if not any(a is None for a in rec.samples[s].allele_indices)
                        if  sum(rec.samples[s].allele_indices) > 0)
        genotypes = tuple('/'.join(str(i) for i in rec.samples[s].allele_indices) for s in samples)
        if rec.info['SVTYPE'] == 'DEL':
            if all(rec.samples[s]['DHFFC'] > args.dhffc_del for s in samples):
                continue
        if rec.info['SVTYPE'] == 'DUP':
            if all(rec.samples[s]['DHFFC'] < args.dhffc_dup for s in samples):
                continue
        if '0/1' in genotypes:
            if rec.info['MSHQ'] < args.mshq:
                continue
        genes = tuple(g.split('|')[0] for g in rec.info.get('smoove_gene', ())
                        if g.split('|')[1].startswith('gene'))
        if len(genes) == 0:
            genes = ('NA',)
        elif len(genes) > 4:
            genes = ('MANY',)
        print(rec.chrom, rec.pos-1, rec.stop, rec.info['SVTYPE'],
                abs(rec.info['SVLEN'][0]), ','.join(samples),
                ','.join(genotypes), ','.join(genes), sep='\t')


if __name__ == '__main__':
    main()
