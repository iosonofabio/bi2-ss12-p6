# vim: fdm=indent
'''
author:     Fabio Zanini
date:       13/06/12
content:    Download a PDB sequence from the database and save it into a file
            with the same name in the data/pdb folder
'''
import urllib

# From http://boscoh.com/protein/fetching-pdb-files-remotely-in-pure-python-code
def fetch_pdb(id):
  url = 'http://www.rcsb.org/pdb/files/%s.pdb' % id
  return urllib.urlopen(url).read()

def get_save_pdb(id):
    '''Get the PDB file and save it in the right folder'''
    pdbstring = fetch_pdb(id)
    with open('data/templates/pdb/'+id+'.pdb','w') as pdbfile:
        pdbfile.write(pdbstring)

# Script
if __name__ == '__main__':

    templatefilename = 'data/templates/most_relevant.dat'
    
    from read_templates import read_templates
    templates = read_templates(templatefilename)
    for template in templates:
        id = template['id']
        print 'downloading', id, '...'
        get_save_pdb()
        print 'done'
