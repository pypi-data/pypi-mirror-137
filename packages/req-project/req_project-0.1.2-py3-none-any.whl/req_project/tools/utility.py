import os
import sys
import requests
import shutil
import platform
import subprocess

class Utility:
    # init method or constructor   
    def __init__(self):
        self = self

    def onerror(func, path, exc_info):
        """  Error handler for ``shutil.rmtree``.

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

    def is_tool(name):
        """Check whether `name` is on PATH and marked as executable."""

        # from whichcraft import which
        from shutil import which

        return which(name) is not None

    def path_in_path_variable(folder):
        #function checks if a folder is already in the PATH variable
        #returns:
        #True - if path is found in PATH variable
        #False - if path is not found in PATH variable
        if Utility.whichOS()=="Windows":
            #check if path already in path variable
            output = sys.path
            path_split = folder.split("\\")
            item_total = len(path_split)
            for item in output:
                item_found_counter = 0
                for path_item in path_split:
                    found = item.find(path_item)
                    if found!=-1:
                        item_found_counter = item_found_counter + 1
                if item_found_counter==item_total:
                    return True
            print("path not found in PATH variable")
            return False         
        else:
            print("OS not supported by path_in_path_variable_function")
            return False

    def add_path_to_path_variable(path):
        #function add path is already in the PATH variable
        #returns:
        #True - if path is added to PATH variable successfully
        #False - if path is not added in PATH variable
        if Utility.whichOS()=="Windows":
            #check if path already in path variable
            if Utility.path_in_path_variable(path)==False:
                print("add path to PATH variable")
                sys.path.append(path)
                installed = Utility.path_in_path_variable(path)
                print(installed)
                return True
            else:
                print("path already in PATH variable, nothing to do!")
                return True
        else:
            print("OS not supported by path_in_path_variable_function")
            return False
        
    def whichOS():
        return platform.system()

    def whichOSRelease():
        return platform.release()

    def whichOSVersion():
        return platform.version()

    def whichMachine():
        return platform.machine()

    def download(url, filename):
        with open(filename, 'wb') as f:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')

            if total is None:
                f.write(response.content)
            else:
                downloaded = 0
                total = int(total)
                for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(50*downloaded/total)
                    sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                    sys.stdout.flush()
        sys.stdout.write('\n')
    
