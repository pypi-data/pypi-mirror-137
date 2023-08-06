# HiCShuffle

[![PyPI version](https://badge.fury.io/py/HiCShuffle.svg)](https://badge.fury.io/py/HiCShuffle)
[![DOI:10.1101/2021.09.23.459925](https://zenodo.org/badge/DOI/10.1101/2021.09.23.459925.svg)](https://doi.org/10.1101/2021.09.23.459925)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)

**FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis**

![HiCShuffle](https://hanjun.group/wp-content/uploads/2022/02/Extended-Data-Figure-X-01.png)

## Installation
```shell
pip install hicshuffle
```

## Usage

### hicshuffle <command> [options]

```shell
Commands:
    diff            FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis
Run hicshuffle <command> -h for help on a specific command.

HiCShuffle: FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis

positional arguments:
  command     Subcommand to run

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

### hicshuffle diff [-h] query_path_1 query_path_2 reference_path_1 reference_path_2 output_directory

```shell

FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis

positional arguments:
  query_path_1      Path for READ1 of GZ-Compressed or Uncompressed Query FASTQ
  query_path_2      Path for READ2 of GZ-Compressed or Uncompressed Query FASTQ
  reference_path_1  Path for READ1 of GZ-Compressed or Uncompressed Reference FASTQ
  reference_path_2  Path for READ2 of GZ-Compressed or Uncompressed Reference FASTQ
  output_directory  Output Directory... HiCShuffle Will Generate Output Directory If Not Existent

optional arguments:
  -h, --help         show this help message and exit
```
