from importlib.resources import path
import os
from pathlib import Path
from tkinter import W

from black import json
import git
import json
from commands.workspace_path import WorkspacePath

class Configuration:

    config = "config"
    config_file = "config.json"
    capella = "capella"
    sdoc = "sdoc"
    reqif = "reqif"
    src = "src"
    docu = "docu"
    tools = "tools"
  
    # TODO: need the docu subfolders configured somewhere as well!    
    docu_fha = "fha"
    docu_overall = "overall"
    docu_requirements = "requirements"
    docu_src = "src"
    docu_systemarchi = "system_architecture"
  
    capella_model_file = None
    sdoc_file = "draft.sdoc"
    reqif_file = "output.reqif"

    # init method or constructor   
    def __init__(self,                
                 config = config,
                 config_file = config_file,
                 capella = capella,
                 sdoc = sdoc,
                 src = src,
                 docu = docu,
                 tools = tools,
                 docu_fha = docu_fha,
                 docu_overall = docu_overall,
                 docu_requirements = docu_requirements,
                 docu_src = docu_src,
                 docu_systemarchi = docu_systemarchi,
                 capella_model_file = capella_model_file,
                 sdoc_file = sdoc_file,
                 reqif_file = reqif_file,
                 projectname=None, 
                 workspace=None,
                 ):  
        if projectname==None:
            self.projectname = "draft_project"
        else:
            self.projectname = projectname

        if workspace==None:
            ws = WorkspacePath(workspace = workspace)
            if ws.configfile_available():
                workspaceconfig = ws.read_configfile()
                self.workspace = workspaceconfig.workspace
            else:
                print("can not setup project folder, please use req_project.py -p PATH to define workspace path")
                exit()
        else:   
            self.workspace = workspace
            ws = WorkspacePath(workspace = workspace)
            if ws.configfile_available():
                ws_loaded = ws.read_configfile()
                if ws_loaded.workspace!=workspace:
                    ws.write_configfile()
            else:
                ws.write_configfile()

        # TODO: Remove
        # moved to class scope to have them available in static method as well
        #self.config = "/config"
        #self.config_file = "/config.json"
        #self.capella = "/capella"
        #self.sdoc = "/sdoc"
        #self.src = "/src"
        #self.docu = "/docu"
        self.config = config
        self.config_file = config_file
        self.capella = capella
        self.sdoc = sdoc
        self.src = src
        self.docu = docu
        self.tools = tools

        # TODO: need the docu subfolders configured somewhere as well!    
        self.docu_fha = docu_fha
        self.docu_overall = docu_overall
        self.docu_requirements = docu_requirements
        self.docu_src = docu_src
        self.docu_systemarchi = docu_systemarchi

        # TODO: need project file information for: how, when and by whom are their names defined?!?       
        # capella.aird
        # strictdoc.reqif
        # strictdoc.sdoc
        # 
        self.capella_model_file = self.projectname+".aird"
        self.sdoc_file = self.projectname+".sdoc"
        self.reqif_file = reqif_file

    def poject_exists(self):
        # checks if the project folder is available
        # returns:
        # - true - project folder exists
        # - false - project folder does not exist
        project_path = os.path.join(self.workspace, self.projectname)
        if os.path.exists(project_path):
            return True
        else:
            return False

    def get_project_path(self):
        project_path = os.path.normpath(os.path.join(self.workspace, self.projectname))
        return project_path

    def get_sdoc_file(self):
        filename = os.path.normpath(os.path.join(self.workspace, self.projectname, self.sdoc, self.sdoc_file))
        return filename

    def get_sdoc_path(self):
        sdoc_doc_path = os.path.normpath(os.path.join(self.workspace, self.projectname, self.sdoc))
        return sdoc_doc_path

    def get_sdoc_docu_path(self):
        sdoc_doc_path = os.path.normpath(os.path.join(self.workspace, self.projectname, self.docu, self.docu_requirements))
        return sdoc_doc_path

    def change_projectname(self, projectname):
        self.projectname = projectname

    def change_projectpath(self, workspace):
        self.workspace = workspace

    def checkfor_configfile(self):
        try:
            with open("config.json", "r") as jsonfile:
                data = json.load(jsonfile)
                print(data)
            return True
        except FileNotFoundError:
            print('Configuration file is not present.')
            return False

    @staticmethod
    def read_configfile(projectpath):
        
        proj = os.path.basename(os.path.normpath(projectpath))
        ws = os.path.dirname(os.path.normpath(projectpath))

        filename = os.path.join(ws, proj, os.path.normpath(Configuration.config), os.path.normpath(Configuration.config_file))
        with open(filename, "r") as jsonfile:
            data = json.load(jsonfile)
            return Configuration(**data)

    def write_configfile(self):
        print("write file")
        myJSON = json.dumps(self.__dict__)
        filename = os.path.join( self.workspace, self.projectname, self.config, self.config_file)
        print(filename)
        with open(filename, "w") as jsonfile:
            jsonfile.write(myJSON)
            print("Write successful")