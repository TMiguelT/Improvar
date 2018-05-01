# Improvar

`improvar` generates fake VCF files using another VCF as a template. This is useful for generating
test data in bioinformatics situations. In particular, `improvar` generates values for all the fields
listed in the header, even if your template didn't, allowing you to test your analysis pipeline with
more completely.

## Installation
Install `improvar` using:
```bash
pip install 'git+https://github.com/TMiguelT/VcfFake#egg=improvar'
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
  template_vcf

optional arguments:
  -h, --help            show this help message and exit
  --num-variants NUM_VARIANTS, -n NUM_VARIANTS
  --gt-opts {GenotypeOption.HOM_REF,GenotypeOption.HOM_ALT,GenotypeOption.HET}
  --include-contig INCLUDE_CONTIG
  --exclude-contig EXCLUDE_CONTIG
```

`improvar` prints the generated VCF to stdout, so you can pipe the results of this program to a file
or to other VCF processing tools