####################################################
# Compiler to LIE++ Language
# TEC - FOD
# Authors:
#   Ellioth Ramirez
####################################################

from LIE.lang_tools.multi.multiFun import multiFun
from LIE.lang_tools.LIEsemantic.semanticAnalyzer import *
from LIE.lang_tools.analyzer.codeAnalyzer import *
from LIE.lang_tools.generator.codeGenerator import *
import sys
import platform
import subprocess

sys.path.insert(1, sys.path[0].replace("lang_tools", "gen"))


TRANS_FLAG = "-t"
OUTPUT_EXT = ".py"
OUTPUT_JSON = ".json"
SCRIPT = 1
SOURCE = 0

# Verify the device where the compiler is been executed
# @return Boolean value if is running over a Raspberry Pi


def verifyDevice():
    if platform.system() == "Linux":  # If is a Linux OS
        command = "\n cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).strip()
        all_info = all_info.decode("utf-8")
        for line in all_info.split("\n"):
            if "model name" in line:
                if "ARM" in re.sub(".*model name.*:", "", line,
                                   1):  # If is running over an ARM processor (Raspberry Pi)
                    return True
    return False


def main(argv):
    if (len(argv) < 3):
        print("Error: cantidad de argumentos invalidos")
        quit()
    mmFun = multiFun()
    canGPIOFlag = verifyDevice()
    # This change it's done so we can call the
    # compiler, from the arguments, to a source
    # code (0) or a program file (1).
    if int(argv[1]) == SCRIPT:
        inp = FileStream(argv[2])
    elif int(argv[1]) == SOURCE:
        inp = InputStream(mmFun.replaceBadCharacters(argv[2]))
    lexer = fodcatLexer(inp)
    stream = CommonTokenStream(lexer)
    parser = fodcatParser(stream)

    parser._errHandler = ParserErrorStrategy()
    parser.removeErrorListeners()
    parser.addErrorListener(ParserErrorListener())

    tree = parser.program()
    walker = ParseTreeWalker()

    semanticAnalyzer = SemanticAnalyzer()
    walker.walk(semanticAnalyzer, tree)

    # we're going take chance of the gateway which
    # doesn't write the compiled code to the disk,
    # if the write area it's null/none.
    # If we do this, we still keep the compiled
    # program.
    generator = CodeGenerator(None, canGPIOFlag)
    walker.walk(generator, tree)
    # mmFun.printPreatty(mmFun.execCode(generator.program))
    print(mmFun.execCode(generator.program))


if __name__ == '__main__':
    main(sys.argv)
