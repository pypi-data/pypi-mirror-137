from gettext import find
import os
import subprocess
import shutil
from black import out
from numpy import byte
import requests
from tools.utility import Utility 
import urllib.request as ul
from bs4 import BeautifulSoup as soup
import requests

class VsCode:
    # init method or constructor   
    def __init__(self):
        self = self

    def availability():
        if Utility.is_tool("code"):
            return True
        else:
            return False

    def version_online():
        #detect the latest online version
        #return highest version found
        #highest_version = ["0", "0", "0"] ... if nothing found
        #highest_version = ['1', '64', '0']
        url = "https://github.com/Microsoft/vscode/releases"
        req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        client = ul.urlopen(req)
        htmldata = client.read()
        client.close()
        #print(htmldata)
        pagesoup = soup(htmldata, "html.parser")
        all_links= pagesoup.findAll(href=True)
        ref_url = "/microsoft/vscode/tree/"
        highest_version = ["0", "0", "0"]
        for link in all_links:
            link1 = str(link)
            ind = link1.find(ref_url)
            ind2 = link1.find("\">")
            if ind!=-1:
                version = link1[ind+len(ref_url):ind2]
                version = version.split(".")
                if int(version[0])>int(highest_version[0]):
                    highest_version = version
                elif int(version[0])==int(highest_version[0]):
                    if int(version[1])>int(highest_version[1]):
                        highest_version = version
                    elif int(version[1])==int(highest_version[1]):
                        if int(version[2])>int(highest_version[2]):
                            highest_version = version
        #print(highest_version)
        return highest_version

    def version_installed():
        #detect the latest online version
        #return highest version found
        #highest_version = ["0", "0", "0"] ... if nothing found
        #highest_version = ['1', '64', '0']
        installed_version = ["0", "0", "0"]
        output = str(subprocess.check_output(["code", "--version"],stderr=subprocess.STDOUT,shell=True))
        output = output.split("\\n")
        for element in output:
            version = element.split(".")
            if len(version)==3:
                installed_version=version
        return installed_version

    def textX_extension_available():
        #check if textX.textX extension for VSC is installed
        #return value: 
        # - True if successful installed
        # - False if not successful installed
        output = str(subprocess.check_output(["code", "--list-extensions"],stderr=subprocess.STDOUT,shell=True))
        ext = "textX.textX"
        if output.find(ext)==-1: #textX.textX exension not installed
            return False
        else:
            return True


    def textX_installation():
        #try to install textX.textX extension for VSC
        #return value: 
        # - True if successful installed
        # - False if not successful installed
        try:
            output = str(subprocess.check_output(["code", "--list-extensions"],stderr=subprocess.STDOUT,shell=True))
            ext = "textX.textX"
            if output.find(ext)==-1: #textX.textX exension not installed
                print("extension not installed")
                #install extension
                subprocess.check_output(["code", "--install-extension",ext],stderr=subprocess.STDOUT,shell=True)
                #check if correctly installed
                output = str(subprocess.check_output(["code", "--list-extensions"],stderr=subprocess.STDOUT,shell=True))
                if output.find(ext)==-1: #textX.textX exension not installed
                    return False
                else:
                    return True
            else: #textX.textX exension installed
                print("extension installed, nothing to do")
                return True
        except subprocess.CalledProcessError as err:
            print(err)
            return False
        #print(res)

    def textX_uninstallation():
        #try to uninstall textX.textX extension for VSC
        #return vale: 
        # - True if successful uinstalled
        # - False if not successful uinstalled
        try:
            output = str(subprocess.check_output(["code", "--list-extensions"],stderr=subprocess.STDOUT,shell=True))
            ext = "textX.textX"
            if output.find(ext)==-1: #textX.textX exension not installed
                return True
            else:
                output1 = str(subprocess.check_output(["code", "--uninstall-extension",ext],stderr=subprocess.STDOUT,shell=True))
                #check if correctly installed
                output1 = str(subprocess.check_output(["code", "--list-extensions"],stderr=subprocess.STDOUT,shell=True))
                if output1.find(ext)==-1: #textX.textX exension not installed anymore
                    return True
                else:
                    print("Something went wrong. textX.textX extension was not unistalled correctely!")
                    return False
        except subprocess.CalledProcessError as err:
            print(err)
            return False

    def install(path):
        print( Utility.whichOS())
        if Utility.whichOS()=="Windows": #check for Windows since Code only runs on windows
            print("Windoff detected")
            #install Visual studio code
            if Utility.is_tool("code"):
                print("Visual Studio Code detected")
                return True
            else: #VS Code not detected
                print("Visual Studio Code not installed ---- downloading")
                machine = str(Utility.whichMachine()).lower()
                print(machine)
                if machine=="amd64":
                    vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64"
                elif machine=="i386":
                    vscode_url = "https://code.visualstudio.com/sha/download?build=stable&os=win32"
                destination = f'{path}\\vscode.exe'
                Utility.download(vscode_url,destination)
                os.open(destination)
                installed = Utility.add_path_to_path_variable(path) and VsCode.availability()
                if installed==True:
                    return True
                else:
                    return False
        else:
            print("your OS is not supported yet!!")
            return False

        