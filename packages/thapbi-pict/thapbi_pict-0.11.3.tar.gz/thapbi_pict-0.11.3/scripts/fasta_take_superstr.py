#!/usr/bin/env python
"""Remove deuplicate subsequences.

$ ./fasta_substr.py < INPUT.fasta > OUTPUT.fasta

NOTE: Does not preserve sequence case, gets converted to upper case.
"""

import sys

from Bio.SeqIO.FastaIO import SimpleFastaParser

seqs = sorted((seq, title) for title, seq in SimpleFastaParser(sys.stdin))

# This gets rid of just right-end padding
new = {}
for i, (seq, title) in enumerate(seqs):
    if i + 1 < len(seqs) and seq in seqs[i + 1][0]:
        sys.stderr.write(f"Ignoring {title.split()[0]} length {len(seq)}\n")
    else:
        new[seq] = title
del seqs

for seq, title in new.items():
    wanted = True
    for long_seq in new:
        if seq != long_seq and seq in long_seq:
            wanted = False
            sys.stderr.write(f"Ignoring {title.split()[0]} length {len(seq)}\n")
            break
    if wanted:
        sys.stdout.write(f">{title}\n{seq}\n")
