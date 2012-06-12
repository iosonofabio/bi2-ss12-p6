from modeller import *
from modeller.automodel import *

env = environ()
env.io.atom_files_directory = './data/pdb/'

aln = alignment(env)
mdl = model(env, file='3tx7', model_segment=('FIRST:B','LAST:B'))
aln.append_model(mdl, align_codes='3tx7_B', atom_files='3TX7.pdb')
aln.append(file='data/pir/1yje.ali', align_codes='1yje_A')
aln.align2d()
aln.write(file='data/tmp/1yje-3tx7.ali', alignment_format='PIR')

a = automodel(env, alnfile='data/tmp/1yje-3tx7.ali',
              #allow_alternates=True,
              knowns=('3tx7_B'),
              sequence='1yje_A')

a.starting_model=1
a.ending_model=1

a.make()