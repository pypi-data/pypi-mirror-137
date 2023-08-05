#!/usr/bin/env python
"""Reports short sequences which ar substrings of entries in the first file.

$ ./fasta_substr.py LONG.fasta SHORT1.fasta SHORT2.fasta ...

NOTE: Does not preserve sequence case, gets converted to upper case.
"""

import sys

from Bio.SeqIO.FastaIO import SimpleFastaParser

if len(sys.argv) < 3:
    sys.exit("ERROR: Require two or more FASTA filenames.")

filename = sys.argv[1]
with open(filename) as handle:
    seq_dict = {seq.upper(): title for title, seq in SimpleFastaParser(handle)}
wanted = set()
sys.stderr.write(f"Starting with {filename} have {len(seq_dict)} unique sequences\n")

for filename in sys.argv[2:]:
    with open(filename) as handle:
        for title, seq in SimpleFastaParser(handle):
            for long, long_title in seq_dict.items():
                if seq in long:
                    # Long title, short seq
                    sys.stdout.write(f">{long_title}\n{seq}\n")
