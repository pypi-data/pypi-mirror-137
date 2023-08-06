#===============================================================================
# specivar.py
#===============================================================================

"""Filter VCF to variants that are specific to a sample group"""

# Imports ======================================================================

from argparse import ArgumentParser
from pysam import VariantFile



# Functions ====================================================================

def parse_arguments():
    parser = ArgumentParser(
        description='Filter VCF to variants that are specific to a sample group')
    parser.add_argument('vcf', metavar='<input.vcf>', help='input VCF file')
    parser.add_argument('--groups', metavar='<"GROUP">', nargs='+',
                        help='specify a subset of sample groups')
    parser.add_argument('--remove-bnd', action='store_true',
                        help='remove "BND" calls')
    return parser.parse_args()


def main():
    args = parse_arguments()
    vcf_in = VariantFile(args.vcf)
    vcf_out = VariantFile('-', 'w', header=vcf_in.header)
    for rec in vcf_in.fetch():
        if args.remove_bnd:
            if rec.info['SVTYPE'] == 'BND':
                continue
        groups = {s.split('_')[0] for s in rec.samples
                  if not any(a is None for a in rec.samples[s].allele_indices)
                  if sum(rec.samples[s].allele_indices) > 0}
        if (len(groups) == 1) and (args.groups is None or groups.pop() in args.groups):
                vcf_out.write(rec)
