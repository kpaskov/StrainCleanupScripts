__author__ = 'kelley'

import urllib2
import math

# Given a BLAST output file (particularly the results of UNDEF blasted against S288C, finds
# any genes that exist within the match interval
chromosome_name_to_number = {'chrmt':17, 'chr01': 1, 'chr02': 2, 'chr03': 3, 'chr04': 4,
                             'chr05': 5, 'chr06': 6, 'chr07': 7, 'chr08': 8, 'chr09': 9,
                             'chr10': 10, 'chr11': 11, 'chr12': 12, 'chr13': 13, 'chr14': 14,
                             'chr15': 15, 'chr16': 16}
def find_S288C_genes(blast_results):
    genes = []

    for line in urllib2.urlopen('http://downloads.yeastgenome.org/curation/chromosomal_feature/SGD_features.tab'):
        try:
            pieces = line.split('\t')
            gene_name = pieces[0] + ' (' + pieces[3] + ')'
            chromosome = int(pieces[8])
            start_coord = min(int(pieces[9]), int(pieces[10]))
            end_coord = max(int(pieces[9]), int(pieces[10]))

            genes.append((gene_name, chromosome, start_coord, end_coord))
        except:
            pass

    lines = []
    f = open(blast_results, 'r')
    header = True
    for line in f:
        pieces = line.split('\t')
        if not header:
            chromosome = chromosome_name_to_number[pieces[1]]
            start_coord = min(int(pieces[8]), int(pieces[9]))
            end_coord = max(int(pieces[8]), int(pieces[9]))

            genes_in_window = []
            for gene_name, gene_chr, gene_start, gene_end in genes:
                if gene_chr == chromosome and \
                    ((gene_start >= start_coord and gene_start <= end_coord) or \
                     (gene_end >= start_coord and gene_end <= end_coord) or \
                     (gene_start <= start_coord and gene_end >= end_coord)):
                    genes_in_window.append(gene_name)

            pieces.insert(2, ', '.join(genes_in_window))
        else:
            pieces.insert(2, 'genes in alignment window')
            header = False
        lines.append('\t'.join(pieces))
    f.close()

    f = open(blast_results, 'w+')
    f.writelines(lines)
    f.close()
