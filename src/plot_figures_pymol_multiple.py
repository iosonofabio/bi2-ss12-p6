# vim: fdm=indent
'''
author:     Fabio Zanini
date:       15/06/12
content:    Plot two figures out of a threading exercise, one with prediction
            and truth, one with prediction and templates.

            This script is used as follows. Open pymol, enter this script's
            folder, then from Pymol's command line call:
                run <scriptname>
            and finally call the function you want to use.
'''
# Modules
import os
import shutil
import pymol

from read_templates import read_templates, get_tplname



# Tables
pdb_folder = '../data/templates/pdb/'



# Functions
def plot_prediction_templates(n_templates=3, n_templates_plot=None):
    '''Plot the prediction together with the templates'''

    # Parse arguments
    n_templates = int(n_templates)
    if n_templates_plot is None:
        n_templates_plot = n_templates
    else:
        n_templates_plot = int(n_templates_plot)

    # Delete previous objects
    pymol.cmd.delete('all')

    # Get the prediction
    predfile = '../results/1yje_A-multiple_n_'+str(n_templates)+'.pdb'
    predid = '1yje_A-multiple_n_'+str(n_templates)
    pymol.cmd.load(predfile)
    pymol.cmd.color('red', predid)


    # Get the template codes
    # 1:n_templates_plot+1 because we want to exclude the target (which appears first on the list otherwise).
    templates = read_templates('../data/templates/most_relevant.dat')[1:n_templates_plot+1]
    print templates

    # Load structures
    for template in templates:
        id = template['id'].upper()
        chain = template['chain']
        pymol.cmd.load(pdb_folder+id+'.pdb')
        pymol.cmd.align('('+id+' and chain '+chain+')', predid)

    pymol.cmd.hide(representation='line', selection='all')

    
    pymol.cmd.show(representation='cartoon', selection=predid)
    for template in templates:
        id = template['id'].upper()
        chain = template['chain']
        pymol.cmd.show(representation='cartoon',
                       selection='('+id+' and chain '+chain+')')

    pymol.cmd.center()
    pymol.cmd.bg_color('white')


def plot_prediction_truth(n_templates=3):
    '''Plot the prediction together with the true structure.'''

    # Delete previous objects
    pymol.cmd.delete('all')

    # Get the prediction
    predfile = '../results/1yje_A-multiple_n_'+str(n_templates)+'.pdb'
    predid = '1yje_A-multiple_n_'+str(n_templates)
    pymol.cmd.load(predfile)
    pymol.cmd.color('red', predid)

    # Get the true structure
    truefile = pdb_folder+'1YJE.pdb'
    trueid = '1YJE'
    pymol.cmd.load(truefile)


    # Align, show cartoon
    pymol.cmd.align(trueid, predid)
    pymol.cmd.hide(representation='line', selection='all')
    pymol.cmd.show(representation='cartoon', selection='all')
    pymol.cmd.center()
    pymol.cmd.bg_color('white')


def save_prediction_templates(n_templates=3):
    '''Save the current image as the prediction-templates result'''
    pymol.cmd.save('../figures/prediction_templates_' + str(n_templates) + '.png', format='png')


def save_prediction_truth(n_templates=3):
    '''Save the current image as the prediction-truth result'''
    pymol.cmd.save('../figures/prediction_truth_' + str(n_templates) + '.png', format='png')



# Pymol directives
cmd.extend("plot_prediction_templates", plot_prediction_templates)
cmd.extend("plot_prediction_truth", plot_prediction_truth)
cmd.extend("save_prediction_templates", save_prediction_templates)
cmd.extend("save_prediction_truth", save_prediction_truth)
