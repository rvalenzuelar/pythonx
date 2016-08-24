#!/usr/bin/env python
'''
    Command line utility for pulling changes in Git repos.
    from remote

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

# commits_behind = repo.iter_commits('master..origin/master')
# commits_ahead = repo.iter_commits('origin/master..master')
# count = sum(1 for c in commits_ahead)

for D in DIRS:
    ''' run only for unhidden folders 
    '''
    if not D.startswith('.'):
        currentdir = ctext(GITPATH + '/' + D)
        repo = git.Repo(currentdir.text)
        origin = repo.remotes.origin
        ''' if directory is not git repo then
            pass the error
        '''
        try:
            status = origin.pull()
            if 'Already up-to-date' in status:
                print(currentdir.green())
            else:
                print(currentdir.red())
            print(status)
        except:
            pass
print('')
