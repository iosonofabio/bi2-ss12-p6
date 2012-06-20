# vim: fdm=indent
'''
author:     Fabio Zanini
date:       15/06/12
content:    Align multiple template sequences into a single MSA and use them
            simultaneously for structure prediction.
'''
# Modules
import os
import sys
import shutil
from modeller import *
from modeller.automodel import *

from read_templates import read_templates, get_tplname



# Tables
defaultseqfile = '../starting_sequence/pir/1yje_A.ali'
# Number of templates to use (for performance reasons)
n_templates = 15
# The models are assessed using both measures, but DOPE decides the best model
# in the end (see Shen and Sali 2006)
assessment_models = ('DOPE', 'GA341')

# Script
if __name__ == '__main__':
    seqfile = defaultseqfile

    # input arguments
    args = sys.argv
    if len(args) > 1:
        n_templates = int(sys.argv[1])

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
        seqname = (os.path.basename(seqfile).split('.')[0])
        seqname = seqname[:-1]+seqname[-1].upper()
        templates = read_templates('../templates/most_relevant.dat')[:n_templates+1]
        templates = filter(lambda t: t['id'] != '1YJE', templates)
        n_templates = len(templates)

        # check whether the alignment exists already
        if not os.path.isfile(seqname+'-multiple_n_'+str(n_templates)+'.ali'):
            aln = alignment(env)
            for template in templates:
                id = template['id']
                chain = template['chain']
                tplname = get_tplname(template)
        
                mdl = model(env, file=id, model_segment=('FIRST:'+chain, 'LAST:'+chain))
                aln.append_model(mdl, align_codes=tplname, atom_files=id+'.pdb')
            
            # add the unknown sequence to the alignment.
            aln.append(file=seqfile, align_codes=seqname)
            
            # Align sequence-structures
            # Note: align2d is obsolete! --> salign
            # Parameters
            # - gap_function makes the gaps in the MSA dependent on the structural
            #   context
            aln.salign(gap_function=True)
        
            # store the alignment
            aln.write(file=seqname+'-multiple_n_'+str(n_templates)+'.ali', alignment_format='PIR')
            
        
        # automodel reads the alignment file and actually does the homology modeling for us.
        # the output is a .pdb file, to be seen in a.outputs.
        # the parameter assess_methods is used to check the quality of the model
        # (see also Kryshtafovych and Fidelis, 2009)
        a = automodel(env,
                      alnfile = seqname+'-multiple_n_'+str(n_templates)+'.ali',
                      knowns = map(get_tplname, templates),
                      sequence = seqname,
                      assess_methods=[getattr(assess, am) for am in assessment_models])
        
        # index of the first/last model
        # (determines how many models to calculate)
        a.starting_model= 1
        a.ending_model = 3
        
        # do the actual homology modeling
        a.make()
    
        # check the assessment score
        temp_scores = []
        for i in xrange(3):
            print 'Model', i+1
            for am in assessment_models:
                scores = a.outputs[i][am+' score']
                #modeller outputs this to align_model_multiple.log
                print am+' scores:\t'+str(scores)

        # find top model
        dope_scores = [o['DOPE score'] for o in a.outputs]
        top_model_ind = dope_scores.index(min(dope_scores))


        # move the model into the results folder
        modelname = a.outputs[top_model_ind]['name']
        if not os.path.isdir('../../results'):
            os.mkdir('../../results')
        shutil.move(modelname, '../../results/'+seqname+'-multiple_n_'+str(n_templates)+'.pdb')

    finally:
        # back to the original folder
        os.chdir('../..')
