# vim: fdm=indent
'''
author:     Fabio Zanini
date:       15/06/12
content:    Align multiple template sequences into a single MSA and use them
            simultaneously for structure prediction.
'''
# Modules
import os
import shutil
from modeller import *
from modeller.automodel import *

from read_templates import read_templates, get_tplname



# Tables
defaultseqfile = '../starting_sequence/pir/1yje_A.ali'
# Number of templates to use (for performance reasons)
n_templates = 2


# Script
if __name__ == '__main__':
    seqfile = defaultseqfile

    # work in the tmp folder
    if not os.path.isdir('data/tmp'):
        os.mkdir('data/tmp')
    os.chdir('data/tmp')

    try:
        #the environment object is needed to do pretty much everything
        env = environ()
        #.pdb files must be stored herein
        env.io.atom_files_directory = ['../templates/pdb/']
    
        # align the unknown sequence with all templates
        aln = alignment(env)
        templates = read_templates('../templates/most_relevant.dat')[:n_templates]
        n_templates = len(templates)
        for template in templates:
            id = template['id']
            chain = template['chain']
            tplname = get_tplname(template)
    
            mdl = model(env, file=id, model_segment=('FIRST:'+chain, 'LAST:'+chain))
            aln.append_model(mdl, align_codes=tplname, atom_files=id+'.pdb')
        
        # add the unknown sequence to the alignment.
        seqname = (os.path.basename(seqfile).split('.')[0])
        seqname = seqname[:-1]+seqname[-1].upper()
        aln.append(file=seqfile, align_codes=seqname)
        
        # Align sequence-structures
        # Note: align2d is obsolete! --> salign
        # Parameters
        # - gap_function makes the gaps in the MSA dependent on the structural
        #   context
        aln.salign(gap_function=True)
    
        # store the alignment
        aln.write(file=seqname+'-multiple_n_'+str(n_templates)+'.ali', alignment_format='PIR')
        
    
        #automodel reads the alignment file and actually does the homology modeling for us.
        #the output is a .pdb file, to be seen in a.outputs.
        a = automodel(env,
                      alnfile = seqname+'-multiple.ali',
                      knowns = map(get_tplname, templates),
                      sequence = seqname)
        
        # index of the first/last model
        # (determines how many models to calculate)
        a.starting_model= 1
        a.ending_model = 1
        
        # do the actual homology modeling
        a.make()
    
        # move the model into the results folder
        modelname = a.outputs[0]['name']
        if not os.path.isdir('../../results'):
            os.mkdir('../../results')
        shutil.move(modelname, '../../results/'+seqname+'-multiple_n_'+str(n_templates)+'.pdb')

    finally:
        # back to the original folder
        os.chdir('../..')
