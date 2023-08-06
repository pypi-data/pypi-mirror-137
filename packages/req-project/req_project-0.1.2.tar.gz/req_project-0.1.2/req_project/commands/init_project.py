from errno import errorcode
import os
import shutil
from pathlib import Path
from black import json
import git
import json
from git import Repo
from markupsafe import string
from commands.workspace_path import WorkspacePath
#internal tools
from tools.utility import Utility
from tools.configuration import Configuration
from tools.vs_code import VsCode
from tools.git_bug import GitBug

class InitProject:
    @staticmethod
    def execute(projectname, workspace=None):
        #set configuration path to relativ folder path if not given
        ws = WorkspacePath()
        if workspace is None:
            workspace_config_available = ws.configfile_available()
            if workspace_config_available:
                ws_config = ws.read_configfile()
                workspace = ws_config.workspace
            else:
                print("please provide a workspace path using -p PATH option. See -h for help")
                exit()
        else:
            ws.workspace = workspace
            ws.write_configfile()
            workspace = workspace


        #create folder for tools
        tools_path = os.path.normpath(os.path.join(workspace, "tools"))
        if os.path.exists(tools_path): #project path exists:
            print("tools path " + tools_path + "already exisits, nothing to do")
        else:
            os.mkdir(tools_path)
            if os.path.exists(tools_path):
                print("tools path " + tools_path + "successfully created!")
            else:
                print("Something went wrong when creating tools path " + tools_path)

        #install git-gub
        print("checking for git-bug")
        GitBug.install(tools_path)

        #install VSCode
        print("checking for VS Code")
        VsCode.install(tools_path)
        VsCode.textX_installation()

        path = os.path.join(workspace, projectname)
        #print(path)
        if os.path.exists(path): #project path exists
            #return warning 
            print("Warning: project exists already please delete it before initiate!")
            exit()
        else: #project path does not exist so create prototype project
            print(path)
            try: 
                os.mkdir(path) 
                if os.path.exists(path):
                    #Clone draft project from repro locally
                    git_url = "https://github.com/mnaderhirn/req_draft.git"
                    print("Cloning draft project from GIT URL: " + git_url + " into path " + path)
                    Repo.clone_from(git_url, path)
                    #delete all uncessary information in folder
                    shutil.rmtree(path + "\\.git", onerror=Utility.onerror)
                    #Write initial configuration file
                    print("workspace path is: " + str(workspace))
                    config = Configuration(projectname =projectname, workspace=str(workspace))
                    config.write_configfile()
                    #rename draft.sdoc to projectname.sdoc
                    sdoc_path = config.get_sdoc_path()
                    oldfilename = os.path.normpath(os.path.join(sdoc_path, "draft.sdoc"))
                    newfilename = os.path.normpath(os.path.join(sdoc_path, config.sdoc_file))
                    os.rename(oldfilename,newfilename)
                    filelist = os.listdir(sdoc_path)
                    file_detected = False
                    for x in filelist:
                        if x.endswith(".sdoc"):
                            if x.__contains__(config.sdoc_file):
                                file_detected = True
                    if file_detected==True:
                        print("project file name " + config.sdoc_file + " successful renamed")
                    else:
                        raise Exception("project file name not renamed during project init")
                    print("project folder successful created")
                else:
                    print("something went wrong, project folder not created!")
            except OSError as error: 
                print(error)

        

        


        