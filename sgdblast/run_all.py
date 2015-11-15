__author__ = 'kelley'

from pull_data import pull_undef_from_strains, make_blast_db, make_genome_fasta_s288c, make_other_strain_fasta, make_special_feature_fasta
from run_blast import run_blast
from clean_tab import clean_tab_file
from find_genes import find_S288C_genes

# # Pull latest strain sequences with a command like
# # scp -r kpaskov@fasolt:/data/sgd/strainGenomes/to_load data/strain_sequences
#
# # Pull undefs
# pull_undef_from_strains(['CEN.PK2-1Ca_JRIV01000000_SGD_cds.fsa',
#                          'D273-10B_JRIY00000000_SGD_cds.fsa',
#                          'FL100_JRIT00000000_SGD_cds.fsa',
#                          'JK9-3d_JRIZ00000000_SGD_cds.fsa',
#                          'RM11-1A_JRIP00000000_SGD_cds.fsa',
#                          'SEY6210_JRIW00000000_SGD_cds.fsa',
#                          'Sigma1278b-10560-6B_JRIQ00000000_SGD_cds.fsa',
#                          'SK1_JRIH00000000_SGD_cds.fsa',
#                          'W303_JRIU00000000_SGD_cds.fsa',
#                          'X2180-1A_JRIX00000000_SGD_cds.fsa',
#                          'Y55_JRIF00000000_SGD_cds.fsa'])
#
# make_special_feature_fasta()
#
# # Make fasta files for each genome
# make_genome_fasta_s288c()
# make_other_strain_fasta(['CEN.PK2-1Ca_JRIV01000000_SGD.gff', 'D273-10B_JRIY00000000_SGD.gff',
#                          'FL100_JRIT00000000_SGD.gff', 'JK9-3d_JRIZ00000000_SGD.gff',
#                          'RM11-1A_JRIP00000000_SGD.gff', 'SEY6210_JRIW00000000_SGD.gff',
#                          'Sigma1278b-10560-6B_JRIQ00000000_SGD.gff', 'SK1_JRIH00000000_SGD.gff',
#                          'W303_JRIU00000000_SGD.gff', 'X2180-1A_JRIX00000000_SGD.gff',
#                          'Y55_JRIF00000000_SGD.gff'])
#
# # Make BLAST database for each genome
# make_blast_db('yeast2003.nt')
# make_blast_db('yeast2012.nt')
# make_blast_db('other_strains.nt')
#
# # Run BLAST
run_blast('../data/undef.fsa', '../data/blast_dbs/yeast2012')
# run_blast('../data/special_features.fsa', '../data/blast_dbs/other_strains')
#
# # Format output
clean_tab_file('../data/undef.tab')
# clean_tab_file('../data/special_features.tab')
find_S288C_genes('../data/undef.tab')