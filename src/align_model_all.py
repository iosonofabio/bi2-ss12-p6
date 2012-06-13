# vim: fdm=indent
'''
author:     Fabio Zanini
date:       13/06/12
content:    Align and model an unknown sequence onto several templates.

Note: please start this script from the root folder of the project.
'''
import os
import shutil
from modeller import *
from modeller.automodel import *

# Tables
defaultseqfile = '../starting_sequence/pir/1yje_A.ali'

if __name__ == '__main__':
    seqfile = defaultseqfile

    # work in the tmp folder
    if not os.path.isdir('data/tmp'):
        os.mkdir('data/tmp')
    os.chdir('data/tmp')

    #the environment object is needed to do pretty much everything
    env = environ()
     #.pdb files must be stored herein
    env.io.atom_files_directory = ['../templates/pdb/']
    aln = alignment(env)
    
    # get all templates
    from read_templates import read_templates
    templates = read_templates('../templates/most_relevant.dat')
    
    # do one prediction per template (we will need to integrate them later on)
    for template in templates[:2]:
        id = template['id']
        chain = template['chain']
        tplname = id.lower()+'_'+chain

        print tplname

        # Prepare model
        mdl = model(env, file=id, model_segment=('FIRST:'+chain,'LAST:'+chain))
        aln.append_model(mdl, align_codes=tplname, atom_files=id+'.pdb')
    
        #we add the sequence for 1yje to the alignment.
        seqname = (os.path.basename(seqfile).split('.')[0])
        seqname = seqname[:-1]+seqname[-1].upper()
        aln.append(file=seqfile, align_codes=seqname)
    
        #we do the alignment.
        aln.align2d()
        
        #we print the alignment
        aln.write(file=seqname+'-'+tplname+'.ali', alignment_format='PIR')
        
        #automodel reads the alignment file and actually does the homology modeling for us.
        #the output is a .pdb file, to be seen in a.outputs.
        a = automodel(env, alnfile=seqname+'-'+tplname+'.ali',
                      #allow_alternates=True,
                      knowns=(tplname),
                      sequence=seqname)
        
        # use a single model
        a.starting_model=1
        a.ending_model=1
        
        # do the modelling (this takes some time)
        a.make()

        # move the model into the results folder
        modelname = a.outputs[0]['name']
        if not os.path.isdir('../../results'):
            os.mkdir('../../results')
        shutil.move(modelname, '../../results/'+seqname+'-'+tplname+'.pdb')

    # back to the original folder
    os.chdir('../..')
