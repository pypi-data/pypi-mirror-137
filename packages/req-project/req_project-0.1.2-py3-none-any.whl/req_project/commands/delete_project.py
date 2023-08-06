import os
from pathlib import Path
import shutil

from black import json
import git
import json

from markupsafe import string

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


class DeleteProject:
    @staticmethod
    def execute(projectname, projectfolder=None):
        #set configuration path to relativ folder path if not given
        if projectfolder is None:
            projectfolder = Path(__file__).parent.parent.parent.parent.absolute()
        
        path = os.path.join( projectfolder, projectname)
        if os.path.exists(path): #project path exists so delete it
            #return warning 
            print("project found at path " + path)
            if input("are you sure? (y/n) ") == "y":
                try:
                    print("deleting project folder")
                    shutil.rmtree(path, onerror=onerror)
                    if os.path.exists(path):
                        print("something went wrong, was not able to delte project folder")
                    else:
                        print("project folder successful removed")
                except:
                    print("could not delete project folder")
            exit()
        else: #project path does nothing to delete
            print("project with name " + projectname + " not found")
            print("Please provide correct path!")
            exit()