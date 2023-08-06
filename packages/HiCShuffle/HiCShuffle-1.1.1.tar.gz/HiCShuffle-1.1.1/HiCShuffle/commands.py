import argparse
import textwrap
import math
import sys
import numpy as py

def hicshuffle_parser():
    usage = '''\
        hicshuffle <command> [options]
        Commands:
            diff            FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis
        Run hicshuffle <command> -h for help on a specific command.
        '''
    parser = argparse.ArgumentParser(
        description='HiCShuffle: FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis',
        usage=textwrap.dedent(usage)
    )

    from .version import __version__
    parser.add_argument('--version', action='version', version=f'HiCShuffle {__version__}')
    
    parser.add_argument('command', nargs='?', help='Subcommand to run')

    return parser

def diff_parser():
    parser = MyParser(
        description='FASTQ Shuffling Tool For Sanity Check in Hi-C Differential Contact Analysis',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='hicshuffle diff'
    )
    
    parser.add_argument(
        'query_path_1',
        type=str,
        help='Path for READ1 of GZ-Compressed or Uncompressed Query FASTQ')
        
    parser.add_argument(
        'query_path_2',
        type=str,
        help='Path for READ2 of GZ-Compressed or Uncompressed Query FASTQ')
    
    parser.add_argument(
        'reference_path_1',
        type=str,
        help='Path for READ1 of GZ-Compressed or Uncompressed Reference FASTQ')
    
    parser.add_argument(
        'reference_path_2',
        type=str,
        help='Path for READ2 of GZ-Compressed or Uncompressed Reference FASTQ')
    
    parser.add_argument(
        'output_directory',
        type=str,
        help='Output Directory... HiCShuffle Will Generate Output Directory If Not Existent')

    return parser
      
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
