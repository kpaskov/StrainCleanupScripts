__author__ = 'kelley'

# Removes comment lines from tab delimited file produced by BLAST
def clean_tab_file(filename):
    header = '\t'.join(['query id', 'subject id', '% identity', 'alignment length', 'mismatches',
                       'gap opens', 'q. start', 'q. end', 's. start', 's. end', 'evalue', 'bit score\n'])
    lines = [header]
    f = open(filename, 'r')
    for line in f:
        if not line.startswith('#') and not line == header:
            lines.append(line)
    f.close()

    f = open(filename, 'w+')
    f.writelines(lines)
    f.close()

clean_tab_file('../data/special_features.tab')
clean_tab_file('../data/undef.tab')