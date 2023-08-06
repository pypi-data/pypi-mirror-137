#===============================================================================
# specivar.py
#===============================================================================

"""Filter VCF to variants that are specific to a sample group"""

# Imports ======================================================================

from argparse import ArgumentParser
from collections import defaultdict
from pysam import VariantFile
import pandas as pd
import numpy as np



# Constants ====================================================================

DEFAULT_TOLERANCE = 1




# Functions ====================================================================

def count_samples_per_group(groups):
    occurrence = defaultdict(lambda: 0)
    for g in groups:
        occurrence[g] += 1
    return pd.Series(occurrence, dtype=np.int64)

def parse_arguments():
    parser = ArgumentParser(
        description='Filter VCF to variants that are specific to a sample group')
    parser.add_argument('vcf', metavar='<input.vcf>', help='input VCF file')
    parser.add_argument('--tolerance', metavar='<int>', type=int,
        default=DEFAULT_TOLERANCE,
        help=f'number of samples allowed to break specificity [{DEFAULT_TOLERANCE}]')
    parser.add_argument('--groups', metavar='<"GROUP">', nargs='+',
        help='specify a subset of sample groups')
    parser.add_argument('--remove-bnd', action='store_true',
        help='remove "BND" calls')
    args = parser.parse_args()
    args.groups = set(args.groups)
    return args


def main():
    args = parse_arguments()
    vcf_in = VariantFile(args.vcf)
    vcf_out = VariantFile('-', 'w', header=vcf_in.header)
    for rec in vcf_in.fetch():
        if args.remove_bnd:
            if rec.info['SVTYPE'] == 'BND':
                continue
        groups = tuple(s.split('_')[0] for s in rec.samples
                  if not any(a is None for a in rec.samples[s].allele_indices)
                  if sum(rec.samples[s].allele_indices) > 0)
        counts = count_samples_per_group(groups)
        if len(counts.values) == 0:
            continue
        max_val = counts.values.max()
        argmax = counts[counts.values == max_val].index
        nonmax = counts[counts.values < max_val].values
        if len(argmax) == 1:
            if (args.groups is None) or (argmax[0] in args.groups):
                if len(nonmax) == 0 or sum(nonmax) <= args.tolerance:
                    vcf_out.write(rec)
