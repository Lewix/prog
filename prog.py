#!/usr/bin/python2.7
"""prog.

Usage:
    prog open [<name>]
    prog ls
    prog default [<name>]
    prog add [-d]
    prog add [-d] <name> <directory>
    prog rm <name>

Options:
    -d  Make new project the default
"""

import os
import pickle
from docopt import docopt
# Programming project organisation

class BashCommand:
    command = ''

    def execute(self):
        os.system(self.command)

    def add_change_dir(self, directory):
        self.command += 'cd ' + directory + ';'

    def add_vim_session(self):
        self.command += 'test -e Session.vim && vim -S || vim;'

    def get_expanded_dir(self, directory=None):
        if directory:
            return os.path.abspath(directory)
        else:
            return os.getcwd()


class ProjectList:
    def __init__(self, project_file='$HOME/.projs'):
        self.project_file = project_file
        f = open(project_file, 'r')
        try:
            self.project_list = pickle.load(f)
        except EOFError:
            self.project_list = []
        f.close()

    def writeout(self):
        f = open(self.project_file, 'w')
        pickle.dump(self.project_list, f)
        f.close()

    def prog_make_default(self, name=None):
        """Makes name the default project. Take the current directory's basename as default name"""
        if not name:
            command = BashCommand()
            directory = command.get_expanded_dir()
            name = os.path.basename(directory)

        for project in self.project_list:
            if project['name'] == name:
                for other_project in self.project_list:
                    other_project['default'] = False
                project['default'] = True
                self.writeout()
                break
        else:
            print 'No such project'

    def prog_default(self):
        """Open the default project"""
        try:
            project_name = [p['name'] for p in self.project_list if p['default']][0]
            self.prog_open(project_name)
        except IndexError:
            'No default project'

    def prog_open(self, name):
        """Change directory to the given project and open vim"""
        command = BashCommand()

        #TODO: make this nicer
        try:
            project_dir = [p['dir'] for p in self.project_list if p['name'] == name][0]
            command.add_change_dir(project_dir)
            command.add_vim_session()
            command.execute()
        except IndexError:
            print 'No such project'

    def prog_ls(self):
        """List the names and directories of all know projects"""
        for project in self.project_list:
            project_line = project['name'] + ', ' + project['dir']
            if project['default']:
                print '*' + project_line
            else:
                print project_line

    def prog_rm(self, name):
        """Remove a project"""
        for project in self.project_list:
            if name == project['name']:
                self.project_list.remove(project)
                break
        else:
            print 'No such project'
            return

        self.writeout()

    def prog_add(self, name, directory, default):
        """Add a project"""
        if name in map(lambda p : p['name'], self.project_list):
            print "Project already exists"
            return

        command = BashCommand()
        directory = command.get_expanded_dir(directory)

        if not name:
            name = os.path.basename(directory)

        self.project_list.append({'name': name, 'dir': directory, 'default': False})

        if default:
            self.prog_make_default(name)
        
        f = open(self.project_file, 'w')
        pickle.dump(self.project_list, f)
        f.close()


if __name__ == '__main__':
    arguments = docopt(__doc__)

    project_list = ProjectList()
    if arguments['ls']:
        project_list.prog_ls()
    elif arguments['default']:
        project_list.prog_make_default(arguments['<name>'])
    elif arguments['rm']:
        project_list.prog_rm(arguments['<name>'])
    elif arguments['add']:
        project_list.prog_add(arguments['<name>'], arguments['<directory>'], arguments['-d'])
    elif arguments['open'] and arguments['<name>']:
        project_list.prog_open(arguments['<name>'])
    elif arguments['open']:
        project_list.prog_default()
