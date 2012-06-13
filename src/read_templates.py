# vim: fdm=indent
'''
author:     Fabio Zanini
date:       13/06/12
content:    Read the templates into a dict
'''
defaultfile = 'data/templates/most_relevant.dat'

def read_templates(templatefilename=None):
    if templatefilename is None:
        templatefilename = defaultfile

    templates = []
    with open(templatefilename, 'r') as tplfile:
        for line in tplfile:
            line = line.lstrip(' \t')
            if line[0] != '#':
                pdbid, chain = line.rstrip('\n').split('\t')
                templates.append({'id': pdbid, 'chain': chain})

    return templates

# Script
if __name__ == '__main__':

    import sys
    args = sys.argv
    if len(args) > 2:
        raise ValueError('Usage: '+args[0]+' [template filename]\n')
    elif len(args) == 1:
       templates = read_templates()
    else:
       templates = read_templates(args[1])

