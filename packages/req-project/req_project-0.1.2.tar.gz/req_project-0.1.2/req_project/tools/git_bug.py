import os
import subprocess
from subprocess import PIPE, Popen
from platform import machine
import shutil
from git import Git
import requests
from tools.utility import Utility 
from tools.configuration import Configuration
from urllib.request import urlretrieve
import getpass
import urllib.request as ul
from bs4 import BeautifulSoup as soup

url_basic = "https://github.com/MichaelMure/git-bug/releases/"

class GitBug:
    # init method or constructor   
    def __init__(self):
        self = self

    def availability():
        if Utility.is_tool("git-bug"):
            return True
        else:
            return False

    def get_version_online():
        url = url_basic + "latest"
        req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        client = ul.urlopen(req)
        htmldata = client.read()
        client.close()
        pagesoup = soup(htmldata, "html.parser")
        itemlocator = pagesoup.findAll('title')
        item = str(itemlocator[0])
        index = item.find("Release") + 8
        return str(item[index:index+5])

    def get_version_installed():
        if GitBug.availability():
            p = Popen(["git-bug", "--version"], stdout=PIPE)
            version = str(p.communicate()[0])
            return version[len(version)-8:len(version)-3]   
        else:
            return "None"

    def update():
        if GitBug.availability(): # just update if not available
            version_online = GitBug.get_version_online()
            version_installed = GitBug.get_version_installed()
            if version_online!=version_installed:
                print("Old git-bug version detected - updating")
                gitbug_path = shutil.which('git-bug')
                version = GitBug.get_version_online()
                OS = str(Utility.whichOS()).lower()
                machine = str(Utility.whichMachine()).lower()
                github_url = url_basic + "download/v" + version + "/git-bug_"+ OS +"_" + machine + ".exe"
                destination = f'{gitbug_path}\\git-bug.exe'
                download = urlretrieve(github_url, destination)
        else: #nothin to update 
            print("Git-bug not found - please install it")
            

    def install(path):
        if GitBug.availability():
            print("git-bug detected")
            GitBug.update()
        else:  #install git-bug in tools folder
            version = GitBug.get_version_online()
            OS = str(Utility.whichOS()).lower()
            machine = str(Utility.whichMachine()).lower()
            github_url = url_basic + "download/v" + version + "/git-bug_"+ OS +"_" + machine + ".exe"
            destination = f'{path}\\git-bug.exe'
            Utility.download(github_url,destination)
            os.open(destination)
            pathcommand = "set PATH=%PATH%;" + path + "\\"
            os.open(pathcommand)
            installed = Utility.add_path_to_path_variable(path) and GitBug.availability()
            if installed==True:
                return True
            else:
                return False
