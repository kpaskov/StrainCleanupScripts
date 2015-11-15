__author__ = 'kelley'

import urllib2
import os
import requests
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

# Pull latest strain sequences with a command like
# scp -r kpaskov@fasolt:/data/sgd/strainGenomes/to_load/* data/strain_sequences

# Pulls undef features from each strain's cds.fsa file and creates a fasta file of undefs.
def pull_undef_from_strains(fsa_files):

    undefs = []
    for fsa_file in fsa_files:
        for seq_record in SeqIO.parse('../data/strain_sequences/%s' % fsa_file, 'fasta'):
            if seq_record.id.startswith('UNDEF'):
                seq_record.id = seq_record.description.replace(' ', '_')
                undefs.append(seq_record)

    SeqIO.write(undefs, '../data/undef.fsa', 'fasta')


# Pulls chromosome sequence data and creates a per-genome fasta file.
# yeast2003.nt is from ftp://ftp.ncbi.nlm.nih.gov/blast/documents/blastdb.html (this is what NCBI uses)

# Pulls latest fsa data from yeastgenome downloads site.
def make_genome_fasta_s288c():
    chromosomes = ['chrmt.fsa', 'chr01.fsa', 'chr02.fsa', 'chr03.fsa', 'chr04.fsa', 'chr05.fsa', 'chr06.fsa',
                   'chr07.fsa', 'chr08.fsa', 'chr09.fsa', 'chr10.fsa', 'chr11.fsa', 'chr12.fsa', 'chr13.fsa',
                   'chr14.fsa', 'chr15.fsa', 'chr16.fsa']

    lines = []
    for chromosome in chromosomes:
        for line in urllib2.urlopen('http://downloads.yeastgenome.org/sequence/S288C_reference/NCBI_genome_source/%s' % chromosome):
            if line.startswith('>'):
                print chromosome
                lines.append('>' + chromosome[0:-4] + '\n')
            else:
                lines.append(line)

    f = open('../data/blast_dbs/yeast2012.nt', 'w+')
    f.writelines(lines)
    f.close()

# Pulls data from gff files.
def make_other_strain_fasta(gff_filenames):
    fsa_file = open('../data/blast_dbs/other_strains.nt', 'w+')

    for gff_filename in gff_filenames:
        start_copy = False

        gff_file = open('../data/strain_sequences/%s' % gff_filename, 'r')
        for line in gff_file:
            if line.startswith('>'):
                start_copy = True
            if start_copy:
                fsa_file.write(line.replace(' ', '_'))

        gff_file.close()
    fsa_file.close()


# Calls the BLAST+ makeblastdb command to make a BLAST database from a fasta file
def make_blast_db(fasta_filename):
    os.system('/usr/local/ncbi/blast/bin/makeblastdb -in ../data/blast_dbs/%s -dbtype nucl -out ../data/blast_dbs/%s' % (fasta_filename, fasta_filename[0:-3]))


def get_json_from_SGD(url):
    # Force return from the server in JSON format
    HEADERS = {'accept': 'application/json'}

    # GET the object
    response = requests.get(url, headers=HEADERS)

    # Extract the JSON response as a python dict
    json_response = response.json()

    return json_response

# Pulls sequences for centromere, snoRNA, snRNA, tRNA, and ARS features.
def make_special_feature_fasta():
    records = []
    for locus_type in ['centromere', 'snoRNA_gene', 'snRNA_gene', 'tRNA_gene', 'ARS']:
        print locus_type
        locii = get_json_from_SGD('http://yeastgenome.org/backend/locus/%s' % locus_type)['locii']
        for locus in locii:
            sequence_data = get_json_from_SGD('http://yeastgenome.org/backend/locus/%s/sequence_details' % str(locus['id']))
            reference_sequence = None
            for sequence in sequence_data['genomic_dna']:
                if sequence['strain']['format_name'] == 'S288C':
                    reference_sequence = sequence['residues']

            if reference_sequence is None:
                print 'Problem: locus %s has no reference sequence.' % locus['display_name']
            else:
                fasta_id = '%s(%s) %s' % (locus['display_name'], locus['format_name'], locus_type)
                records.append(SeqRecord(Seq(reference_sequence, IUPAC.unambiguous_dna), id=fasta_id))

    SeqIO.write(records, '../data/special_features.fsa', 'fasta')