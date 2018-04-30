#!/usr/bin/env python3
import pysam
import string
import os
import random
import argparse
import enum
import itertools
from signal import signal, SIGPIPE, SIG_DFL

# Handle SIGPIPE so this pipes into `head` correctly
signal(SIGPIPE, SIG_DFL)


class GenotypeOption(enum.Enum):
    HOM_REF = 'hom-ref'
    HOM_ALT = 'hom-alt'
    HET = 'het'


def path_exists(arg: str):
    """
    Validates that the provided file exists, and returns it as a string
    """
    if not os.path.exists(arg):
        raise argparse.ArgumentTypeError('Path must exist!')
    else:
        return arg


def parse_args() -> argparse.Namespace:
    """
    Return the parsed args
    """
    parser = argparse.ArgumentParser(
        description="Generates a fake VCF based on another VCF's header")
    parser.add_argument('template_vcf', type=path_exists)
    parser.add_argument('--num-variants', '-n', type=int, required=False, default=1)
    parser.add_argument('--gt-opts', choices=['het', 'hom-ref', 'hom-alt'], type=GenotypeOption, required=False)
    parser.add_argument('--include-contig', type=str, required=False)
    parser.add_argument('--exclude-contig', type=str, required=False)
    return parser.parse_args()


def calc_multiplicity(key: str, record: pysam.VariantRecord, section: str = 'fmt') -> int:
    """
    Determines the multiplicity of a INFO or FMT field from a variant record
    """
    header_mult = record.header.formats[key].number if section == 'fmt' else record.header.info[
        key].number

    # If it's GT, it's always 1
    if key == 'GT':
        return 1
    elif isinstance(header_mult, int):
        return header_mult
    elif header_mult == 'A':
        return len(record.alts)
    elif header_mult == 'R':
        return len(record.alleles)
    elif header_mult == '.':
        return None
    else:
        raise NotImplementedError()


def data_from_vcf_type(key, record, section='fmt', gt_opts: GenotypeOption = None):
    """
    Generates a random value for a VCF field
    :param type: The VCF header type ("Integer", "Float", "Flag", "Character", or "String")
    """
    char_set = string.ascii_uppercase + string.ascii_lowercase
    multiplicity = calc_multiplicity(key, record, section)
    type = record.header.formats[key].type if section == 'fmt' else record.header.info[key].type

    # GT is an exception
    if section == 'fmt' and key == 'GT':
        if gt_opts == GenotypeOption.HET:
            # If it's a het, we always return the reference, and some number of alts, then shuffle them
            gt = [0] + random.choice(
                list(itertools.combinations_with_replacement(range(1, len(record.alleles)), len(record.alleles) - 1)))
            return random.shuffle(gt)
        elif gt_opts == GenotypeOption.HOM_ALT:
            return [1]*len(record.alleles)
        elif gt_opts == GenotypeOption.HOM_REF:
            return [0]*len(record.alleles)
        else:
            return random.choice(
                list(itertools.combinations_with_replacement(range(len(record.alleles)), len(record.alleles))))

    # VCF types are Integer, Float, Flag, Character, and String
    results = []
    for i in range(multiplicity):
        if type == 'Integer':
            results.append(random.randint(0, 100))
        if type == 'Float':
            results.append(random.random())
        if type == 'Flag':
            raise NotImplementedError()
        if type == 'Character':
            results.append(random.choice(char_set))
        if type == 'String':
            results.append(''.join(random.choices(char_set, k=10)))

    return tuple(results)


def random_base():
    bases = ['A', 'T', 'C', 'G', 'N']
    return random.choice(bases)


def generate_record(header: pysam.VariantHeader,
                    contig_exclude=None, contig_include=None, **kwargs
                    ) -> pysam.VariantRecord:
    """
    Generates a variant record with random data, based on the provided header
    :param header A pysam header to use in generating valid data
    :param contig_exclude: A glob, or list of strings to exclude from the valid contigs
    :param contig_include: A glob, or list of strings to include from the valid contigs. Exclude all others
    :param kwargs: A dictionary of keyword args to pass into the data_from_vcf_type function
    """
    contig = random.choice(header.contigs)
    record = header.new_record(
        contig=contig.name,
        alleles=[random_base(), random_base()],
        start=random.randint(1, contig.length)
    )

    # Add INFO fields
    for info in header.info.iterkeys():
        if info == 'END':
            continue
        record.info[info] = data_from_vcf_type(info, record, 'info', **kwargs)

    # Add FMT fields
    for sample in record.samples.iterkeys():
        for fmt in header.formats.iterkeys():
            record.samples[sample][fmt] = data_from_vcf_type(fmt, record, 'fmt', **kwargs)

    return record


def generate_data(input_vcf: str, output_vcf: str,
                  num_variants: int = 1, **kwargs
                  ):
    """
    Uses one VCF as a template to generate random VCF records
    """
    parsed_input = pysam.VariantFile(input_vcf)
    parsed_output = pysam.VariantFile(output_vcf, 'w', header=parsed_input.header)

    for i in range(num_variants):
        record = generate_record(parsed_output.header, **kwargs)
        parsed_output.write(record)


def main():
    args = parse_args()
    generate_data(args.template_vcf, '-', args.num_variants, )


if __name__ == '__main__':
    main()
