#!/bin/bash
set -euo pipefail

mkdir -p tmp_merged/

# Takes arguments via variable names
function analyse {
    mkdir -p intermediate/${NAME}/
    thapbi_pict prepare-reads -i raw_data/ -o intermediate/${NAME}/ \
		--merged-cache tmp_merged/ \
		-a 10 --left $LEFT --right $RIGHT --minlen $MINLEN
    echo "$NAME done"
}

echo =====================================================
echo Universal animal DNA barcodes and mini-barcodes - 16S
echo =====================================================

NAME=16S
LEFT=CGCCTGTTTATCAAAAACAT
RIGHT=CCGGTCTGAACTCAGATCACGT
MINLEN=200

analyse # call function above

echo ==========================================================
echo Universal animal DNA barcodes and mini-barcodes - Mini-16S
echo ==========================================================

NAME=Mini-16S
LEFT=AYAAGACGAGAAGACCC
RIGHT=GATTGCGCTGTTATTCC
MINLEN=200

analyse # call function above

echo ==========================================================
echo Universal animal DNA barcodes and mini-barcodes - Mini-COI
echo ==========================================================

#TODO - COI, multiple right primers?

NAME=Mini-COI
LEFT=GGWACWGGWTGAACWGTWTAYCCYCC
RIGHT=TAIACYTCIGGRTGICCRAARAAYCA
MINLEN=200

analyse # call function above

echo =======================================================
echo Universal animal DNA barcodes and mini-barcodes - cyt-b
echo =======================================================

NAME=cyt-b
LEFT=CCATCCAACATCTCAGCATGATGAAA
RIGHT=GGCAAATAGGAARTATCATTC
MINLEN=200

echo "Skipping, failed to amplify at default threhold or even 50."
echo "Drop to -a 10 and you get a modest number of sequences."

#analyse

echo ============================================================
echo Universal animal DNA barcodes and mini-barcodes - Mini-cyt-b
echo ============================================================

NAME=Mini-cyt-b
LEFT=CCATCCAACATCTCAGCATGATGAAA
RIGHT=CCCTCAGAATGATATTTGTCCTCA
MINLEN=200

analyse # call function above

echo =====================================================
echo Universal plant DNA barcodes and mini-barcodes - matK
echo =====================================================

NAME=matK
LEFT=ACCCAGTCCATCTGGAAATCTTGGTTC
RIGHT=CGTACAGTACTTTTGTGTTTACGAG
MINLEN=200

echo "Skipping, failed to amplify"
echo "(at least at default threshold)"

#analyse

#Note authors excluded the other matK primers...

echo =====================================================
echo Universal plant DNA barcodes and mini-barcodes - rbcL
echo =====================================================

NAME=rbcL
LEFT=ATGTCACCACAAACAGAGACTAAAGC
RIGHT=GTAAAATCAAGTCCACCRCG
MINLEN=100  # Even shorter than author's 200 default

analyse

echo ==========================================================
echo Universal plant DNA barcodes and mini-barcodes - Mini-rbcL
echo ==========================================================

NAME=Mini-rbcL
LEFT=GTTGGATTCAAAGCTGGTGTTA
RIGHT=CVGTCCAMACAGTWGTCCATGT
MINLEN=140  # Shorter!

analyse # call function above

echo =========================================================
echo Universal plant DNA barcodes and mini-barcodes - trnL-UAA
echo =========================================================

NAME=trnL-UAA
LEFT=CGAAATCGGTAGACGCTACG
RIGHT=GGGGATAGAGGGACTTGAAC
MINLEN=200

analyse # call function above

echo =============================================================
echo Universal plant DNA barcodes and mini-barcodes - trnL-P6-loop
echo =============================================================

NAME=trnL-P6-loop
LEFT=GGGCAATCCTGAGCCAA
RIGHT=CCATTGAGTCTCTGCACCTATC
MINLEN=10  # Much shorter!

analyse

echo =====================================================
echo Universal plant DNA barcodes and mini-barcodes - ITS2
echo =====================================================

NAME=ITS2
LEFT=ATGCGATACTTGGTGTGAAT
RIGHT=GACGCTTCTCCAGACTACAAT
MINLEN=100  # Shorter!

analyse # call function above

echo ====
echo Done
echo ====
