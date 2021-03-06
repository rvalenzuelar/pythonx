#!/usr/bin/env python
'''
    Command line utility for listing changes in Git repos.

    This file has to be located in a directory included
    in the environmental variable PATH

    Raul Valenzuela
    January, 2016
    raul.valenzuela@colorado.edu
'''

import os
import git
from ctext import ctext

HOME = os.path.expanduser('~')

GITPATH = HOME + '/Github'
DIRS = os.listdir(GITPATH)
DIRS.sort()

for D in DIRS:
    ''' run only for unhidden folders 
    '''
    if not D.startswith('.'):
        currentdir = ctext(GITPATH + '/' + D)
        g = git.cmd.Git(currentdir.text)
        ''' if directory is not git repo then
            pass the error
        '''
        try:
            status = g.status()
            if 'nothing to commit' in status:
                print(currentdir.green())
            else:
                print(currentdir.red())
            print(status)
        except:
            pass
print('')
