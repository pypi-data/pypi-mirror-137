#!/usr/bin/env python3
#===============================================================================
# pysmoove.py
#===============================================================================

"""Execute the population-level SV calling workflow for smoove"""

# Imports ======================================================================

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from multiprocessing import Pool
from subprocess import run
from functools import partial
from math import floor
from os import mkdir, remove

import os.path




# Functions ====================================================================

def smoove_call_cohort(*bams, name, fasta, exclude=None, processes: int = 1,
                       outdir='./', overwrite: bool = False):
    calls_vcf = os.path.join(outdir, f'{name}-smoove.genotyped.vcf.gz')
    if overwrite or not os.path.isfile(calls_vcf):
        run(('smoove', 'call', '--removepr', '--outdir', outdir,
             '--name', name, '--fasta', fasta, '--processes', str(processes),
             '--genotype', *bams) + bool(exclude) * ('--exclude', exclude))
    return calls_vcf


def smoove_call(bam, fasta, exclude=None, processes: int = 1,
                outdir=os.path.join('./', 'smoove-call'),
                overwrite: bool = False):
    sample_name = str(os.path.basename(bam))[:-4]
    calls_vcf = os.path.join(outdir, f'{sample_name}-smoove.genotyped.vcf.gz')
    if overwrite or not os.path.isfile(calls_vcf):
        run(('smoove', 'call', '--outdir', outdir, '--name', sample_name,
            '--fasta', fasta, '--processes', str(processes),
            '--genotype', bam) + bool(exclude) * ('--exclude', exclude))
    return calls_vcf


def smoove_merge(*vcfs, name, fasta, outdir=os.path.join('./', 'smoove-merge'),
                 overwrite: bool = False):
    merged_vcf = os.path.join(outdir, f'{name}.sites.vcf.gz')
    if overwrite or not os.path.isfile(merged_vcf):
        run(('smoove', 'merge','--name', name, '--fasta', fasta,
            '--outdir', outdir, *vcfs))
    return merged_vcf


def smoove_genotype(bam, fasta, vcf, processes: int = 1,
                    outdir=os.path.join('./', 'smoove-genotype'),
                    overwrite: bool = False):
    sample_name = str(os.path.basename(bam))[:-4]
    genotyped_vcf = os.path.join(outdir,
                                 f'{sample_name}-joint-smoove.genotyped.vcf.gz')
    if overwrite or not os.path.isfile(genotyped_vcf):
        run(('smoove', 'genotype', '--duphold', '--removepr',
            '--processes', str(processes),
            '--name', f'{sample_name}-joint',
            '--outdir', outdir, '--fasta', fasta, '--vcf', vcf, bam))
    return genotyped_vcf


def smoove_paste(*vcfs, name, outdir=os.path.join('./', 'smoove-paste'),
                 overwrite: bool = False):
    square_vcf = os.path.join(outdir, f'{name}.smoove.square.vcf.gz')
    if overwrite or not os.path.isfile(square_vcf):
        run(('smoove', 'paste', '--name', name, '--outdir', outdir, *vcfs))
    return square_vcf


def smoove_annotate(vcf, gff, overwrite: bool = False):
    vcf_dir = os.path.dirname(vcf)
    vcf_base = f'{str(os.path.basename(vcf))[:-7]}.anno.vcf'
    annotated_vcf = os.path.join(vcf_dir, vcf_base)
    annotated_vcf_gz = os.path.join(vcf_dir, f'{vcf_base}.gz')
    if overwrite or not os.path.isfile(annotated_vcf_gz):
        if os.path.isfile(annotated_vcf_gz):
            remove(annotated_vcf_gz)
        with open(annotated_vcf, 'w') as f:
            run(('smoove', 'annotate', '--gff', gff, vcf), stdout=f)
        run(('bgzip', annotated_vcf))
    return annotated_vcf_gz


def parse_arguments():
    parser = ArgumentParser(
        description='Execute the population-level SV calling workflow for smoove',
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('bams', nargs='+', help='path(s) to BAM file(s)')
    parser.add_argument('--name', required=True, help='project name used in output files')
    parser.add_argument('--fasta', required=True, help='reference fasta file')
    parser.add_argument('--exclude', help='BED of excluded regions (usually repeats)')
    parser.add_argument('--processes', type=int, default=1, help='number of processes')
    parser.add_argument('--outdir', default='./', help='output directory')
    parser.add_argument('--gff', help='GFF file of gene annotations')
    parser.add_argument('--overwrite', action='store_true',
        help='overwrite existing results files')
    workflow_group = parser.add_mutually_exclusive_group()
    workflow_group.add_argument('--population', action='store_true',
        help='use the large-population workflow, even if the number of bams is <20')
    workflow_group.add_argument('--cohort', action='store_true',
        help='use the small-cohort workflow, even if the number of bams is >=20')
    return parser.parse_args()


def main():
    args = parse_arguments()
    n_bams = len(args.bams)
    if (n_bams < 20 and not args.population) or args.cohort:
        square_vcf = smoove_call_cohort(*args.bams, name=args.name,
            fasta=args.fasta, exclude=args.exclude, outdir=args.outdir,
            processes=args.processes, overwrite=args.overwrite)
    elif n_bams >= 20 or args.population:
        for dirname in ('smoove-call', 'smoove-merge', 'smoove-genotype',
                        'smoove-paste'):
            if not os.path.isdir(os.path.join(args.outdir, dirname)):
                mkdir(os.path.join(args.outdir, dirname))
        with Pool(processes=min(args.processes, n_bams)) as pool:
            calls = pool.map(partial(smoove_call, fasta=args.fasta,
                    exclude=args.exclude,
                    processes=max(floor(args.processes/n_bams), 1),
                    outdir=os.path.join(args.outdir, 'smoove-call'),
                    overwrite=args.overwrite),
                args.bams)
        merged_vcf = smoove_merge(*calls, name=f'{args.name}-merged',
                    fasta=args.fasta,
                    outdir=os.path.join(args.outdir, 'smoove-merge'),
                    overwrite=args.overwrite)
        with Pool(processes=min(args.processes, n_bams)) as pool:
            genotypes = pool.map(partial(smoove_genotype, fasta=args.fasta,
                    vcf=merged_vcf,
                    processes=max(floor(args.processes/n_bams), 1),
                    outdir=os.path.join(args.outdir, 'smoove-genotype'),
                    overwrite=args.overwrite),
                args.bams)
        square_vcf = smoove_paste(*genotypes, name=args.name,
            outdir=os.path.join(args.outdir, 'smoove-paste'),
            overwrite=args.overwrite)
    if args.gff:
        smoove_annotate(square_vcf, args.gff, overwrite=args.overwrite)




# Execute ======================================================================

if __name__ == '__main__':
    main()
