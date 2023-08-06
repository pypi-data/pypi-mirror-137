# HiCShuffle

[![PyPI version](https://badge.fury.io/py/HiCShuffle.svg)](https://badge.fury.io/py/HiCShuffle)

**FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis**

## Installation
```shell
pip install hicshuffle
```

## Usage

### hicshuffle <command> [options]

```shell
Commands:
    diff            FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis
Run panchip <command> -h for help on a specific command.

PanChIP: Pan-ChIP-seq Analysis of Peak Sets

positional arguments:
  command     Subcommand to run

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

### panchip diff [-h] [-t THREADS] [-r REPEATS] library_directory input_directory output_directory

```shell

Analysis of a list peat sets

positional arguments:
  library_directory  Directory wherein PanChIP library was stored.
  input_directory    Input directory wherein peak sets in the format of .bed
                     files are located.
                     (.bed6 format with numeric scores in 5th column required)
  output_directory   Output directory wherein output files will be stored.

optional arguments:
  -h, --help         show this help message and exit
  -t THREADS         Number of threads to use. (default: 1)
  -r REPEATS         Number of repeats to perform. (default: 1)
```
