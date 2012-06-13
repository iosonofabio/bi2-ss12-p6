'''
model_align.py
12/06/12
authors: taylor kessinger, fabio zanini

predicts the structure of a protein using the homology modeling package, modeller.
input: .pdb files of homologous sequences, .pir file containing 
output: .pdb file of the query sequence.
usage: from the shell, mod9.10 src/model_align.py
'''

from modeller import *
from modeller.automodel import *

#the environment object is needed to do pretty much everything
env = environ()
 #.pdb files must be stored herein
env.io.atom_files_directory = ['./data/pdb/']
aln = alignment(env)

#we initialize a new model for 3tx7, a protein with a known structure.
#the B chain is a match for 1yje.
#the 'FIRST:B','LAST:B' part will go into the header of the PIR file.
#B denotes that it's the B chain; we will need to change this for other proteins.
mdl = model(env, file='3TX7', model_segment=('FIRST:B','LAST:B'))
aln.append_model(mdl, align_codes='3tx7_B', atom_files='3TX7.pdb')

#we add the sequence for 1yje to the alignment.
aln.append(file='./data/starting_sequence/pir/1yje_A.ali', align_codes='1yje_A')

#we do the alignment.
aln.align2d()

#we print the alignment
import os
if not os.path.isdir('data/tmp'):
    os.mkdir('data/tmp')
aln.write(file='./data/tmp/1yje-3tx7.ali', alignment_format='PIR')

#automodel reads the alignment file and actually does the homology modeling for us.
#the output is a .pdb file.
a = automodel(env, alnfile='./data/tmp/1yje-3tx7.ali',
              #allow_alternates=True,
              knowns=('3tx7_B'),
              sequence='1yje_A')

a.starting_model=1
a.ending_model=1

a.make()
