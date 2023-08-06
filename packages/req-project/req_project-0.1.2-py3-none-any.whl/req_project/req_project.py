import argparse
from msilib import type_string
from pickle import FALSE
from secrets import choice

from markupsafe import string
from commands.version import VersionCommand
from commands.init_project import InitProject
from commands.delete_project import DeleteProject
from commands.check_project import CheckProject
from commands.workspace_path import WorkspacePath
from commands.generate_documentation import GenerateDocumentation
from tools.git_bug import GitBug
#from commands.map_project import MapProject

import tools.logging as logging

# Defining main function
def main():
    parser = argparse.ArgumentParser(description='Setup requirements project.')
    parser.add_argument('-i', '--init', nargs=1, type=str, default=0,
                        help='init a requirements project in folder INIT')                                                             
    parser.add_argument('-p', '--path', nargs=1, type=str, default=0,
                        help='workspace path') 
    parser.add_argument('-c', '--check', default=0, action="store_true",
                        help='check if infrastructure is correct')
    parser.add_argument('-d', '--delete', nargs=1, type=str, default=0,
                        help='delete requirements project in folder INIT')
    parser.add_argument('-v', '--version', default=0, action="store_true",
                        help='version of requirements management tool')
    g_parser = parser.add_subparsers(help='sub-commands to generate documentation')
    n_parser = g_parser.add_parser("generate" ,help='generate documentation')
    n_parser.add_argument('name', nargs=1, type=str, default="project", help='project name')
    n_parser.add_argument('type', choices=['html', 'pdf'], help='export pdf/html')
    parser.add_argument('-m', '--mapping', nargs=1, type=str, default=0, 
                        help='version of requirements management tool')

    try:
        args = parser.parse_args()

        if args.init!=0:
            print("Init project")
            InitProject.execute(args.init[0])

        if args.path!=0:
            print("Workspace path")
            ws = WorkspacePath()
            WorkspacePath.execute(ws,args.path[0])

        if args.check!=0:
            print("Checking infrastructure and tools")
            CheckProject.execute()

        if args.delete!=0 and args.init==0:
            print("Remove project ")
            DeleteProject.execute(args.delete[0])

        if args.__contains__("name") and args.__contains__("type"):
            print("Generate documentation for project " + args.name[0] + " to type " + args.type)
            GenerateDocumentation.execute(args.name[0],args.type)

        if args.mapping != 0 and args.init == 0 and args.delete == 0:
            print("Mapping project")
            #MapProject.execute(args.mapping[0])      
        
        if args.version:
            VersionCommand.execute()

    except Exception as ex:
        logging.print_error(ex)
  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()
