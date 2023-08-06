####################################################
# Miscellaneous Functions - LIE++ Language compiler
# APC-FOD
# Authors:
#   Ellioth Ramirez
####################################################
import subprocess
import sys
import json
from gen.fodcatListener import fodcatListener


# Documentation for Miscellaneous Functions

class multiFun(fodcatListener):
    # This function is used to fixed the problem with the getText,
    # because this one can get an interval, but it can't be a touple,
    # it's to be two separated variables.
    def getTextInterval(self, ctxParent, ctxSon):
        interval = ctxSon.getSourceInterval()
        return ctxParent.parser.getTokenStream().getText(interval[0], interval[1])

    # This function is used to execute the code from the memory.
    # this one can also return error in the process of execution
    # def execCode(self, code, args):
    def execCode(self, code):
        command = ['python', '-c', code]
        # command.extend(args)
        runfile = subprocess.run(command, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        #stdout, stderr = runfile.communicate()
        if runfile.returncode != 0:
            return runfile.stderr.decode("utf-8").split("\r\n")[:-1]
        return runfile.stdout.decode("utf-8").split("\r\n")[:-1]

    # function to print a list of data.
    def printPreatty(self, stringList):
        for i in stringList:
            print(i)

    # this function it's done since we need to replace the characters that are change
    # because of the java code
    def replaceBadCharacters(self, code):
        code.replace("\'", " \"")
        #code.replace("\\n", " \n")
        return code
