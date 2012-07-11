"""prog.

Usage:
    prog.py open <name>
    prog.py ls
    prog.py add <name> <directory>
    prog.py rm <name>
"""

import os
import pickle
from docopt import docopt
# Programming project organisation

class BashCommand:
    command = ''

    def execute(self):
        print self.command
        #TODO

    def add_change_dir(self, dir):
        self.command += 'cd ' + dir + ';'

    def add_vim_session(self):
        self.command += 'test -e Sessions.vim && vim -S || vim;'

    def get_expanded_dir(self, directory):
        if directory:
            return os.path.abspath(directory)
        else:
            return os.getcwd()


class ProjectList:
    def __init__(self, project_file='/home/lewis/.projs'):
        self.project_file = project_file
        f = open(project_file, 'r')
        try:
            self.project_list = pickle.load(f)
        except EOFError:
            self.project_list = []
        f.close()

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
            print "No such project"

    def prog_ls(self):
        """List the names and directories of all know projects"""
        for project in self.project_list:
            print project['name'] + ', ' + project['dir']

    def prog_rm(self, name):
        """Remove a project"""
        for project in self.project_list:
            if name == project['name']:
                self.project_list.remove(project)
                break
        else:
            print "No such project"
            return

        f = open(self.project_file, 'w')
        pickle.dump(self.project_list, f)
        f.close()

    def prog_add(self, name, directory=None):
        """Add a project"""
        if name in map(lambda p : p['name'], self.project_list):
            print "Project already exists"
            return

        command = BashCommand()
        directory = command.get_expanded_dir(directory)

        self.project_list.append({'name': name, 'dir': directory})
        
        f = open(self.project_file, 'w')
        pickle.dump(self.project_list, f)
        f.close()


if __name__ == '__main__':
    arguments = docopt(__doc__)

    project_list = ProjectList()
    if arguments['ls']:
        project_list.prog_ls()
    elif arguments['rm']:
        project_list.prog_rm(arguments['<name>'])
    elif arguments['add']:
        project_list.prog_add(arguments['<name>'], arguments['<directory>'])
    elif arguments['open']:
        project_list.prog_open(arguments['<name>'])
    
    #project_list = ProjectList()

    #print 'Add test1, test2 and test3'
    #project_list.prog_add('test1','testdir')
    #project_list.prog_add('test2','/home/lewis')
    #project_list.prog_add('test3','../../bin')
    #print 'ls'
    #project_list.prog_ls()

    #print '\n'
    #print 'Remove test1'
    #project_list.prog_rm('test1')
    #print 'ls'
    #project_list.prog_ls()
    #print 'Open test2'
    #project_list.prog_open('test2')
