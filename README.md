# VCF Fake

`vcffake` generates fake VCF files using another VCF as a template. This is useful for generating
test data in bioinformatics situations. In particular, `vcffake` generates values for all the fields
listed in the header, even if your template didn't.

## Installation
Install `vcffake` using:
```bash
pip install 'git+https://github.com/TMiguelT/VcfFake#egg=vcffake'
```

Note that `vcffake` will probably only work on Python 3.6 and above

## Usage
`vcffake` installs a command-line utility called `vcffake`. Its usage is as follows:
```
usage: vcffake [-h] [--num-variants NUM_VARIANTS] template_vcf

Generates a fake VCF based on another VCF's header

positional arguments:
  template_vcf

optional arguments:
  -h, --help            show this help message and exit
  --num-variants NUM_VARIANTS, -n NUM_VARIANTS
```

`vcffake` prints the generated VCF to stdout, so you can pip the results of this program to a file
or to other VCF processing tools