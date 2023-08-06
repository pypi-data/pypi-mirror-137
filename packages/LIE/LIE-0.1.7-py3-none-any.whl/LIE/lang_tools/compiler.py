####################################################
# Compiler to LIE++ Language
# TEC - FOD
# Authors:
#   Michael Gonzalez Rivera
#   Luis Saborio Hernandez
# Edited:
#   Ellioth Ramirez
####################################################


from LIE.lang_tools.analyzer.codeAnalyzer import *
from LIE.lang_tools.generator.codeGenerator import *
from LIE.lang_tools.LIEparser.parserErrorStrategy import ParserErrorStrategy, ParserErrorListener
from LIE.lang_tools.LIEsemantic.semanticErrorStrategy import SemanticErrorStrategy
from LIE.lang_tools.LIEsemantic.semanticAnalyzer import SemanticAnalyzer
import sys
import platform
import subprocess

import argparse

sys.path.insert(1, sys.path[0].replace("lang_tools", "gen"))

TRANS_FLAG = "-t"
OUTPUT_EXT = ".py"
OUTPUT_JSON = ".json"
SCRIPT = 1
SOURCE = 0
REVIEW_EXAM = 1

# Verify the device where the compiler is been executed
# @return Boolean value if is running over a Raspberry Pi


def verifyDevice():
    if platform.system() == "Linux":  # If is a Linux OS
        command = "\n cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).strip()
        all_info = all_info.decode("utf-8")
        for line in all_info.split("\n"):
            if "model name" in line:
                # If is running over an ARM processor (Raspberry Pi)
                if "ARM" in re.sub(".*model name.*:", "", line, 1):
                    return True
    return False


def main(args):
    canGPIOFlag = verifyDevice()
    mmFun = multiFun()
    if args.de_consola:
        inp = InputStream(mmFun.replaceBadCharacters(args.codigo_fuente))
    else:
        inp = FileStream(args.codigo_fuente)
    lexer = fodcatLexer(inp)
    stream = CommonTokenStream(lexer)
    parser = fodcatParser(stream)

    parser._errHandler = ParserErrorStrategy()
    parser.removeErrorListeners()
    parser.addErrorListener(ParserErrorListener())

    tree = parser.program()
    walker = ParseTreeWalker()

    semanticAnalyzer = SemanticAnalyzer()
    exe_error = False
    try:
        walker.walk(semanticAnalyzer, tree)
    except SystemExit as e:
        exe_error = True
        pass

    if (args.revisar_examen and not exe_error):
        generator = CodeGenerator(None, canGPIOFlag)
        walker.walk(generator, tree)
        print(json.dumps(mmFun.execCode(generator.program)))
        return
    if (args.analisis_estructuras == None and not exe_error):
        outPythonFile = args.resultado_compilado + OUTPUT_EXT
        outPutPythonFile = open(str(outPythonFile), "w")
        generator = CodeGenerator(
            outPutPythonFile, canGPIOFlag, args.modo_entrada, args.entradas)
        walker.walk(generator, tree)
        outPutPythonFile.close()
    elif(args.online):
        generator = CodeGenerator(
            None, canGPIOFlag, args.modo_entrada, args.entradas)
        if exe_error or len(ParserErrorStrategy.errors) > 0:
            errores = ParserErrorStrategy.errors+SemanticErrorStrategy.errors
            msg_errores = "\n".join(errores)
            response = {"Success": False, "errores": msg_errores}
            ParserErrorStrategy.errors = []
            SemanticErrorStrategy.errors = []
            return response
        walker.walk(generator, tree)
        response = {"Success": True, "codigo": generator.program}
        return response
    elif not exe_error:
        outPythonFile = args.resultado_compilado + OUTPUT_EXT
        outPutPythonFile = open(str(outPythonFile), "w")
        generator = CodeGenerator(
            outPutPythonFile, canGPIOFlag, args.modo_entrada, args.entradas)
        walker.walk(generator, tree)
        outJsonFile = args.analisis_estructuras + OUTPUT_JSON
        outPutJsonFile = open(str(outJsonFile), "w")
        analyzer = CodeAnalyzer(outPutJsonFile)
        walker.walk(analyzer, tree)
        outPutPythonFile.close()
        outPutJsonFile.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compilador para el lenguaje LIE++.')

    parser.add_argument(
        "--codigo-fuente",
        type=str,
        required=True,
        help="Si --de-consola explicitamente usado en la llamada del compilador, este parametro\
            será interpretado como la dirección del archivo con el codigo fuente a compilar,\
            de lo contrario será interpretado como un string con todo el código fuente que se desea compilar"
    )

    parser.add_argument(
        "--de-consola",
        action='store_true',
        required=False,
        help="Indica si el parametro --codigo-fuente debe ser interpretado como una dirección de archivo\
            o como un string con todo el código fuente a compilar."
    )

    parser.add_argument(
        "--revisar-examen",
        action='store_true',
        required=False,
        help="Si esta bandera está presente se realizará una revisión del código como examen."
    )

    parser.add_argument(
        "--resultado-compilado",
        type=str,
        required=True,
        help="Dirección del archivo donde se almacenará el resultado.\
            El compilador usume el archivo de salida es de tipo python, por lo que\
            no se debe agregar la extensión .py explicitamente."
    )

    parser.add_argument(
        "--analisis-estructuras",
        type=str,
        required=False,
        help="Dirección del archivo donde se almacenará el análisis del código.\
            El compilador asume que este archivo es di tipo JSON, po lo que\
            no se debe agregar la extensión .json explicitamente."
    )
    parser.add_argument(
        "--online",
        action="store_true",
        required=False,
        help="Si esta bandera está presente, se compilará de modo online,\
            lo cual provoca que la funcion 'main' retorne un string con el\
            código generado"
    )

    parser.add_argument(
        "--modo_entrada",
        choices=['automatico', 'manual'],
        type=str,
        default="manual",
        required=False,
        help="Cola de entrdas."
    )

    parser.add_argument(
        "--entradas",
        nargs='+',
        required=False,
        help="Cola de entrdas."
    )

    args = parser.parse_args()

    print(args)

    main(args)
