# vim: fdm=indent
'''
author:     Fabio Zanini
date:       13/06/12
content:    Get the filtered MSA with the top scoring BLAST results, read the
            labels and save their names.
'''
defaultalnfile = 'data/alignment/most_relevant_aligned.fasta'
defaulttplfile = 'data/templates/most_relevant.dat'

def parse_blast_results(alnfilename=None, templatefilename=None):
    if alnfilename is None:
        alnfilename = defaultalnfile
    if tplfilename is None:
        tplfilename = defaulttplfile

    templates = []

    # Read
    with open(alnfilename, 'r') as alnfile:
        for line in alnfile:
            line = line.lstrip(' \t')
            if line[0] == '>':
                pdbid, chain = line[1:].split(':')[0].split('_')
                templates.append({'id': pdbid, 'chain': chain})
    
    # Write
    with open(tplfilename, 'w') as tplfile:
        tplfile.write('# PDB ID\tchain\n')
        for template in templates:
            tplfile.write(template['id'].upper())
            tplfile.write('\t')
            tplfile.write(template['chain'].upper())
            tplfile.write('\n')

# Script
if __name__ == '__main__':
    
    import sys
    args = sys.argv
    if len(args) > 3:
        raise ValueError('Usage: '+args[0]+' [template filename]\n')
    elif len(args) == 1:
       parse_blast_results()
    elif len(args) == 2:
       parse_blast_results(alnfilename=args[1])
    else:
       parse_blast_results(alnfilename=args[1], tplfilename=args[2])

