#!/usr/bin/env python
"""Report common sequences in two more more FASTA files.

Takes order and title lines from the first file.

NOTE: Does not preserve sequence case, gets converted to upper case.
"""

import sys

from Bio.SeqIO.FastaIO import SimpleFastaParser

if len(sys.argv) < 3:
    sys.exit("ERROR: Require two or more FASTA filenames.")

filename = sys.argv[1]
with open(filename) as handle:
    seq_dict = {seq.upper(): title for title, seq in SimpleFastaParser(handle)}
common = set(seq_dict)
sys.stderr.write(f"Starting with {filename} have {len(common)} unique sequences\n")

for filename in sys.argv[2:]:
    with open(filename) as handle:
        common.intersection_update(
            seq.upper() for title, seq in SimpleFastaParser(handle)
        )
    sys.stderr.write(f"After {filename} have {len(common)} shared sequences\n")

for seq, title in seq_dict.items():
    if seq in common:
        sys.stdout.write(f">{title}\n{seq}\n")
