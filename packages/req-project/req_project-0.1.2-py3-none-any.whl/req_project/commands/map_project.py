import os
import shutil
from pathlib import Path
from black import json
import git
import json
from git import Repo
from markupsafe import string
#internal tools
from tools.configuration import Configuration
import tools.logging as logging
import tools.map_reqifcapella as mapping

from strictdoc.helpers.parallelizer import Parallelizer
from strictdoc.backend.reqif.reqif_import import ReqIFImport
from strictdoc.core.actions.export_action import ExportAction
from strictdoc.cli.cli_arg_parser import (
    cli_args_parser,
    create_sdoc_args_parser,
)


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

class MapProject:
    @staticmethod
    def execute(projectname, workspace=None):
      
        #set configuration path to relativ folder path if not given
        if workspace is None:
            workspace = Path(__file__).parent.parent.parent.parent.absolute()

        path = os.path.join(workspace, projectname)
        #path = os.path.normpath(projectpath)
        #print(path)
        if os.path.exists(path): #project path exists
            #return warning 
            config = Configuration.read_configfile(path)

            reqif_file = os.path.normpath(os.path.join(config.workspace, config.projectname, config.reqif, config.reqif_file))
            capella_aird_file = os.path.normpath(os.path.join(config.workspace, config.projectname, config.capella, config.capella_model_file))
            xhtml_doc_path = os.path.normpath(os.path.join(config.workspace, config.projectname, config.docu, config.docu_systemarchi))
            sdoc_doc_path = os.path.normpath(os.path.join(config.workspace, config.projectname, config.docu, config.docu_requirements))
            sdoc_file = os.path.normpath(os.path.join(config.workspace, config.projectname, config.sdoc, config.sdoc_file))

            STRICTDOC_ROOT_PATH = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..","contrib","strictdoc")
            )
            parser = cli_args_parser()
            parall = Parallelizer.create(False)
            

            if not os.path.exists(reqif_file):
                sdoc_file = os.path.join(config.workspace, config.projectname, config.sdoc, config.sdoc_file)
                if os.path.exists(sdoc_file):
                    # TODO: might be a nice idea to try to autoresolve the in case that it is not found
                    #       e.g. get list from sdoc folder if 1 files present use this one, else eliminate draft.sdoc and use first in list
                    #       TBD who and how is the name of this file going to be added to the config json file????
                    # start strictdoc conversion here
                    #cmd = "strictdoc export --formats=reqif-sdoc --output-dir=\""+os.path.join(config.workspace, config.projectname)+"\" " + sdoc_file
                    #os.system(cmd)
                    outdir = os.path.normpath(os.path.join(config.workspace, config.projectname))
                    args = parser.parse_args(
                        ["export", "--formats","reqif-sdoc" , "--output-dir", outdir, sdoc_file]
                    )
                    config_parser = create_sdoc_args_parser(args)
                    export_config = config_parser.get_export_config(STRICTDOC_ROOT_PATH)
                    export_action = ExportAction()
#                   export_action.export(export_config, parall)


                else:
                    logging.print_error("strict doc file could not be found at" + sdoc_file)         

            mapping.map_requirements(path,reqif_file,capella_aird_file,xhtml_doc_path,sdoc_doc_path,config)


            # if mapping returned without error convert reqif to html docu
            # also convert to sdoc
                   
            #cmd = "strictdoc import reqif sdoc " + reqif_file + " " + sdoc_file
            #os.system(cmd)
            args = parser.parse_args(
                ["import", "reqif", "sdoc", reqif_file, sdoc_file]
            )            
            config_parser = create_sdoc_args_parser(args)
            import_config = config_parser.get_import_config(STRICTDOC_ROOT_PATH)
            ReqIFImport.import_from_file(import_config)
            

            # generate html docu from sdoc
            #cmd = "strictdoc export " + reqif_file + " --formats=html --output-dir=html_docu"
            #os.system(cmd)
            args = parser.parse_args(
                ["export", sdoc_file, "--formats","html" , "--output-dir", sdoc_doc_path]
            )
            config_parser = create_sdoc_args_parser(args)
            export_config = config_parser.get_export_config(STRICTDOC_ROOT_PATH)
            export_action = ExportAction()
            export_action.export(export_config, parall)




        else: #project path does not exist so create prototype project
            logging.print_error("project does not exist please initiate it first!")
            

        