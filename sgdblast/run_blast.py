__author__ = 'kelley'

import os
import urllib2
from Bio.Blast.Applications import NcbiblastnCommandline

def run_blast(query, db):
    blastb_cline = NcbiblastnCommandline(query=query, db=db, perc_identity=0.9, outfmt=7, out="../data/%s.tab" % query[0:-4])
    stdout, stderr = blastb_cline()

# BLAST undef against S288C
run_blast('../data/undef.fsa', '../data/blast_dbs/yeast2012')

# BLAST special features again other strains
run_blast('../data/special_features.fsa', '../data/blast_dbs/other_strains')
