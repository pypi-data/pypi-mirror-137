import os
#internal tools
from tools.vs_code import VsCode
from tools.git_bug import GitBug

class CheckProject:
    @staticmethod
    def execute():
        #used to check project requirements
        #result:
        # - true if ok
        # - flase if not ok
        check_correct = True

        if GitBug.availability():
            print("git-bug detected")
        else:
            print("git-bug not detected, please install it")
            check_correct = False

        if VsCode.availability():
            print("VS Code detected")
            if VsCode.textX_extension_available():
                print("TextX.TextX extension for VS Code detected")
            else:
                print("TextX.TextX extension for VS Code not detected, please install")
                check_correct = False
        else:
            print("VS Code not detected, please install it")
            check_correct = False

        return check_correct