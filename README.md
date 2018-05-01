# Improvar

`improvar` generates fake VCF files using another VCF as a template. This is useful for generating
test data in bioinformatics situations. In particular, `improvar` generates values for all the fields
listed in the header, even if your template didn't, allowing you to test your analysis pipeline with
more completely.

## Installation
Install `improvar` using:
```bash
pip install 'git+https://github.com/TMiguelT/Improvar#egg=improvar'
```

Note that `improvar` will only work on Python 3.6 and above

## Usage
`improvar` installs a command-line utility called `improvar`. Its usage is as follows:
```
usage: improvar [-h] [--num-variants NUM_VARIANTS]
                [--gt-opts {GenotypeOption.HOM_REF,GenotypeOption.HOM_ALT,GenotypeOption.HET}]
                [--include-contig INCLUDE_CONTIG]
                [--exclude-contig EXCLUDE_CONTIG]
                template_vcf

Generates a fake VCF based on another VCF's header

positional arguments:
  template_vcf          The VCF to base the generated data off

optional arguments:
  -h, --help            show this help message and exit
  --num-variants NUM_VARIANTS, -n NUM_VARIANTS
                        Number of variants to print
  --gt-opts {GenotypeOption.HOM_REF,GenotypeOption.HOM_ALT,GenotypeOption.HET}
                        Constraints to apply when generating genotype. Leave
                        empty to generate entirely random genotypes. Use "het"
                        to generate only heterozygotes (e.g. 0|1), use "hom-
                        ref" to generate only homozygous referencegenotpyes
                        (e.g. 0|0), and use "hom-var" to generate only
                        homozygous variant genotypes (e.g. 1|1)
  --include-contig INCLUDE_CONTIG
                        Only output contigs whose name matches this regex
                        pattern
  --exclude-contig EXCLUDE_CONTIG
                        Do not output contigs whose name matches this regex
                        pattern
```

`improvar` prints the generated VCF to stdout, so you can pipe the results of this program to a file
or to other VCF processing tools