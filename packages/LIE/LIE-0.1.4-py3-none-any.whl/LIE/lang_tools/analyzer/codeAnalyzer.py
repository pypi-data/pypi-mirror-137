####################################################
# Code analyzer to LIE + + Language
# TEC - FOD
# Authors:
#   Michael Gonzalez Rivera
#   Luis Saborio Hernandez
# Edited:
#   Ellioth Ramirez
####################################################

import sys
import json

from antlr4 import *
from gen.fodcatListener import fodcatListener
from gen.fodcatLexer import fodcatLexer
from gen.fodcatParser import fodcatParser

from LIE.lang_tools.multi.multiFun import multiFun
GTI = multiFun()

# Documentation for CodeAnalyzer
#
# Code analyzer that extracts information on the number of times each type of instruction
# is used, as well as the definitions of the functions, expressions, operators, and
# reserved words used, among others.


class CodeAnalyzer(fodcatListener):

    # CodeAnalyzer constructor. Initialize all needed global variables for the
    # succesfully execution of the code analyzer.
    # @param output JSON analysis output file name.
    def __init__(self, output):
        # Store the Python output file name.
        self.output = output

        # Flag to store if it is an array
        self.arrayFlag = False
        # Flag to store if it is a function declaration
        self.functionDecFlag = False
        # Flag to store if it is a function declaration identifier
        self.functionIdenDecFlag = False
        # Flag to store if it is a function call
        self.functionCallFlag = False
        # Flag to store if it is a cycle
        self.cycleFlag = False
        # Flag to store if it is a conditional
        self.conditionalFlag = False
        # Flag to store if it is the main function
        self.mainFlag = False

        # Dictionary to store all the rules and subrules during the analysis
        self.ruleDictionary = {}
        self.ruleDictionary["variables"] = []
        self.ruleDictionary["arreglos"] = []
        self.ruleDictionary["sentencias"] = []
        self.ruleDictionary["identificadores"] = []
        self.ruleDictionary["enteros"] = []
        self.ruleDictionary["flotantes"] = []
        self.ruleDictionary["booleanos"] = []
        self.ruleDictionary["texto"] = []
        self.ruleDictionary["constantes"] = []
        self.ruleDictionary["expresion aritmetica"] = []
        self.ruleDictionary["operadores aritmeticos"] = []
        self.ruleDictionary["expresion logica"] = []
        self.ruleDictionary["operadores logicos"] = []
        self.ruleDictionary["expresion relacional"] = []
        self.ruleDictionary["operadores relacionales"] = []
        self.ruleDictionary["signos"] = []
        self.ruleDictionary["control flujo"] = []
        self.ruleDictionary["funcion principal"] = []
        # Dictionary to store all the keywords during the analysis
        self.keywords = {}
        self.keywords["palabras reservadas"] = []
        # Dictionary to count rules, subrules and tokens
        self.rulecount = {
            "cantidad variables": 0,
            "cantidad arreglos": 0,
            "cantidad funciones": 0,
            "cantidad sentencias": 0,
            "llamadas variables": 0,
            "llamadas arreglos": 0,
            "llamadas funciones": 0,
            "cantidad expresiones aritmeticas": 0,
            "cantidad expresiones logicas": 0,
            "cantidad expresiones relacionales": 0,
            "operador aritmetico": 0,
            "operador logico": 0,
            "operador relacional": 0,
            "cantidad booleanos": 0,
            "cantidad enteros": 0,
            "cantidad flotantes": 0,
            "cantidad texto": 0,
            "cantidad constantes matematicas": 0,
            "cantidad signos": 0,
            "si": 0,
            "sino": 0,
            "anidacion condicionales": 0,
            "mientras": 0,
            "cantidad control flujo": 0,
            "devolver": 0,
            "repetir": 0,
            "imprimir": 0,
            "operador imprimir": 0,
            "operador asignacion": 0,
            "cantidad identificadores": 0,
            "anidacion ciclos": 0,
        }

        # List to store variable names
        self.varNames = []
        # List to store everything within the function declaration
        self.funDecDic = []
        # Stores the function declaration
        self.funDec = ""

        # Stores the nesting level of the conditionals
        self.conditionalNesting = 0
        # Stores the nesting level of the cycles
        self.cycleNesting = 0

    # Method to fill the keyword dictionary. Adds keyword of list into dictionary of key
    # "palabras reservadas".
    # @param keyWord List of keywords.
    def addKeywords(self, keyWord):
        if (not self.keywords["palabras reservadas"].__contains__(keyWord)):
            self.keywords["palabras reservadas"].append(keyWord)

    # Method to write multiple dictionary to JSON file, separated by comma. Writes the
    # key separated by : and writes de value of the dictionary compares last rule to not
    # write the last comma
    # @param ctx:fodcatParser.dictionary Any python dictionary
    def printDictionary(self, dictionary):
        for x, y in dictionary.items():
            self.output.write("\n")
            if (str(x) == "palabras reservadas"):  # Compare last rule of file to not write a comma
                self.output.write('"' + str(x) + '"' +
                                  ":" + str(json.dumps(y)))
            else:
                self.output.write('"' + str(x) + '"' +
                                  ":" + str(json.dumps(y)))
                self.output.write(", ")

    # ************************************************************************************
    # Initial Rule
    # ************************************************************************************

    # Exit a parse tree produced by fodcatParser#program. Writes in a file the analysis
    # result in JSON.
    # @param ctx:fodcatParser.ProgramContext
    def exitProgram(self, ctx: fodcatParser.ProgramContext):
        self.output.write("[")
        self.output.write("{")
        self.printDictionary(self.rulecount)
        self.printDictionary(self.ruleDictionary)
        writeFunDec = {}
        writeFunDec["funciones"] = self.funDecDic
        self.printDictionary(writeFunDec)
        self.printDictionary(self.keywords)
        self.output.write("}")
        self.output.write("]")

    # Enter a parse tree produced by fodcatParser#main_function.
    # @param ctx:fodcatParser.Main_functionContext
    def enterMain_function(self, ctx: fodcatParser.Main_functionContext):
        self.mainFlag = True  # It is the main function
        self.ruleDictionary["funcion principal"].append("main")

    # Exit a parse tree produced by fodcatParser#main_function.
    # @param ctx:fodcatParser.Main_functionContext
    def exitMain_function(self, ctx: fodcatParser.Main_functionContext):
        self.mainFlag = False  # It is no longer in the main function
        self.addKeywords("para")
        self.addKeywords("principal()")
        self.addKeywords("fin")

    # ************************************************************************************
    # Commands
    # ************************************************************************************

    # Enter a parse tree produced by fodcatParser#command.
    # @param ctx:fodcatParser.CommandContext
    def enterCommand(self, ctx: fodcatParser.CommandContext):
        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # If the command is a "mientras" statement
        if ctx.getChild(0).getText() == "mientras":
            self.rulecount["mientras"] += 1  # Add 1 to the counter
            self.rulecount["cantidad sentencias"] += 1  # Add 1 to the counter

            if (self.cycleFlag):
                self.cycleNesting += 1  # Add 1 to the counter
            self.cycleFlag = True  # Is a cycle

            # Check if dictionary "sentencias" has "mientras", if not, add
            if (not self.ruleDictionary["sentencias"].__contains__("mientras")):
                self.ruleDictionary["sentencias"].append("mientras")

            whileStat = ""
            j = 0
            while(j < ctx.getChildCount()):
                if (not ctx.getChild(j).getText() == "haga"):
                    # Creates the whileStat
                    whileStat += ctx.getChild(j).getText() + " "
                else:
                    j = ctx.getChildCount()
                j += 1  # Add 1 to the counter
            whileStat = whileStat[:-1]  # Deletes the last character (space)
            # Checks where it has to add the information
            if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
                if (not self.funDecDic[i]["cuerpo funcion"].__contains__("sentencia: " + whileStat)):
                    self.funDecDic[i]["cuerpo funcion"].append(
                        "sentencia: " + whileStat)

            if (self.functionDecFlag and self.cycleFlag):
                if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("sentencia: " + whileStat)):
                    self.funDecDic[i]["cuerpo ciclo"].append(
                        "sentencia: " + whileStat)

            if (self.functionDecFlag and self.conditionalFlag):
                if (not self.funDecDic[i]["cuerpo condicional"].__contains__("sentencia: " + whileStat)):
                    self.funDecDic[i]["cuerpo condicional"].append(
                        "sentencia: " + whileStat)

        # If the command is a "repetir" statement
        elif ctx.getChild(0).getText() == "repetir":
            self.rulecount["repetir"] += 1  # Add 1 to the counter
            self.rulecount["cantidad sentencias"] += 1  # Add 1 to the counter

            if (self.cycleFlag):
                self.cycleNesting += 1  # Add 1 to the counter
            self.cycleFlag = True

            if (not self.ruleDictionary["sentencias"].__contains__("repetir")):
                self.ruleDictionary["sentencias"].append(
                    "repetir")  # Adds "repetir" to the dictionary

            repeatStat = ""
            j = 0
            while(j < ctx.getChildCount()):
                if (not ctx.getChild(j).getText() == "veces"):
                    # Creates the repeatStat
                    repeatStat += ctx.getChild(j).getText() + " "
                else:
                    j = ctx.getChildCount()
                j += 1  # Add 1 to the counter
            repeatStat = repeatStat[:-1]  # Deletes the last character (space)

            # Checks where it has to add the information
            if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
                if (not self.funDecDic[i]["cuerpo funcion"].__contains__("sentencia: " + repeatStat)):
                    self.funDecDic[i]["cuerpo funcion"].append(
                        "sentencia: " + repeatStat)

            if (self.functionDecFlag and self.cycleFlag):
                if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("sentencia: " + repeatStat)):
                    self.funDecDic[i]["cuerpo ciclo"].append(
                        "sentencia: " + repeatStat)

            if (self.functionDecFlag and self.conditionalFlag):
                if (not self.funDecDic[i]["cuerpo condicional"].__contains__("sentencia: " + repeatStat)):
                    self.funDecDic[i]["cuerpo condicional"].append(
                        "sentencia: " + repeatStat)

        # If the command is a "imprimir" statement
        elif ctx.getChild(0).getText() == "imprimir":
            self.rulecount["imprimir"] += 1  # Add 1 to the counter
            self.rulecount["cantidad sentencias"] += 1  # Add 1 to the counter
            if (self.mainFlag):  # Is in the main function
                # Adds "imprimir" to the dictionary
                value = GTI.getTextInterval(ctx, ctx)
                self.ruleDictionary["funcion principal"].append(
                    "sentencia imprimir: " + value)
            else:
                if (not self.ruleDictionary["sentencias"].__contains__("imprimir")):
                    self.ruleDictionary["sentencias"].append(
                        "imprimir")  # Adds "imprimir" to the dictionary

            printStat = ""
            j = 0
            while(j < ctx.getChildCount()):
                # Creates the printStat
                printStat += ctx.getChild(j).getText() + " "
                j += 1  # Add 1 to the counter
            printStat = printStat[:-1]  # Deletes the last character (space)

            # Checks where it has to add the information
            if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
                if (not self.funDecDic[i]["cuerpo funcion"].__contains__("sentencia: " + printStat)):
                    self.funDecDic[i]["cuerpo funcion"].append(
                        "sentencia: " + printStat)

            if (self.functionDecFlag and self.cycleFlag):
                if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("sentencia: " + printStat)):
                    self.funDecDic[i]["cuerpo ciclo"].append(
                        "sentencia: " + printStat)

            if (self.functionDecFlag and self.conditionalFlag):
                if (not self.funDecDic[i]["cuerpo condicional"].__contains__("sentencia: " + printStat)):
                    self.funDecDic[i]["cuerpo condicional"].append(
                        "sentencia: " + printStat)

        # If the command is a "devolver" statement
        elif ctx.getChild(0).getText() == "devolver":
            self.rulecount["devolver"] += 1  # Add 1 to the counter
            self.rulecount["cantidad sentencias"] += 1  # Add 1 to the counter

            if (not self.ruleDictionary["sentencias"].__contains__("devolver")):
                self.ruleDictionary["sentencias"].append(
                    "devolver")  # Adds "devolver" to the dictionary

            returnStat = ""
            j = 0
            while(j < ctx.getChildCount()):
                # Creates the returnStat
                returnStat += ctx.getChild(j).getText() + " "
                j += 1  # Add 1 to the counter
            returnStat = returnStat[:-1]  # Deletes the last character (space)

            # Checks where it has to add the information
            if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
                if (not self.funDecDic[i]["cuerpo funcion"].__contains__("sentencia: " + returnStat)):
                    self.funDecDic[i]["cuerpo funcion"].append(
                        "sentencia: " + returnStat)

            if (self.functionDecFlag and self.cycleFlag):
                if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("sentencia: " + returnStat)):
                    self.funDecDic[i]["cuerpo ciclo"].append(
                        "sentencia: " + returnStat)

            if (self.functionDecFlag and self.conditionalFlag):
                if (not self.funDecDic[i]["cuerpo condicional"].__contains__("sentencia: " + returnStat)):
                    self.funDecDic[i]["cuerpo condicional"].append(
                        "sentencia: " + returnStat)
        else:
            pass

    # Exit a parse tree produced by fodcatParser#command.
    # @param ctx:fodcatParser.CommandContext
    def exitCommand(self, ctx: fodcatParser.CommandContext):
        # If the command is a "mientras" statement
        if ctx.getChild(0).getText() == "mientras":
            self.addKeywords("mientras")
            self.addKeywords("haga")
            self.addKeywords("fin")
            if self.cycleNesting > self.rulecount["anidacion ciclos"]:
                self.rulecount["anidacion ciclos"] = self.cycleNesting
            self.cycleNesting = 0
            self.cycleFlag = False
        # If the command is a "repetir" statement
        elif ctx.getChild(0).getText() == "repetir":
            self.addKeywords("repetir")
            self.addKeywords("veces")
            self.addKeywords("fin")
            if self.cycleNesting > self.rulecount["anidacion ciclos"]:
                self.rulecount["anidacion ciclos"] = self.cycleNesting
            self.cycleNesting = 0
            self.cycleFlag = False
        # If the command is a "imprimir" statement
        elif ctx.getChild(0).getText() == "imprimir":
            self.addKeywords("imprimir")
        # If the command is a "devolver" statement
        elif ctx.getChild(0).getText() == "devolver":
            self.addKeywords("devolver")
        else:
            pass

    # Enter a parse tree produced by fodcatParser#ifstat.
    # @param ctx:fodcatParser.IfstatContext
    def enterIfstat(self, ctx: fodcatParser.IfstatContext):
        self.rulecount["si"] += 1  # Add 1 to the counter
        self.rulecount["cantidad sentencias"] += 1  # Add 1 to the counter

        if(self.conditionalFlag):  # Count levels of nested conditionals
            self.conditionalNesting += 1  # Add 1 to the counter

        self.conditionalFlag = True  # Is a conditional

        # Check if "si" is the current dictionary with key "sentencias", if not, add
        if (not self.ruleDictionary["sentencias"].__contains__("si")):
            self.ruleDictionary["sentencias"].append(
                "si")  # Adds "si" to the dictionary

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        ifStat = GTI.getTextInterval(ctx, ctx)
        ifStat = ifStat.split(" entonces")[0]  # Creates the ifStat

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("sentencia: " + ifStat)):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "sentencia: " + ifStat)

        if (self.functionDecFlag and self.cycleFlag):
            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("sentencia: " + ifStat)):
                self.funDecDic[i]["cuerpo ciclo"].append(
                    "sentencia: " + ifStat)

        if (self.functionDecFlag and self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("sentencia: " + ifStat)):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "sentencia: " + ifStat)

    # Exit a parse tree produced by fodcatParser#ifstat.
    # @param ctx:fodcatParser.IfstatContext
    def exitIfstat(self, ctx: fodcatParser.IfstatContext):
        self.addKeywords("si")
        self.addKeywords("entonces")
        self.addKeywords("fin")
        if self.conditionalNesting > self.rulecount["anidacion condicionales"]:
            self.rulecount["anidacion condicionales"] = self.conditionalNesting
        self.conditionalNesting = 0
        self.conditionalFlag = False

    # Enter a parse tree produced by fodcatParser#elsestat.
    # @param ctx:fodcatParser.ElsestatContext
    def enterElsestat(self, ctx: fodcatParser.ElsestatContext):
        self.rulecount["sino"] += 1  # Add 1 to the counter
        self.rulecount["cantidad sentencias"] += 1  # Add 1 to the counter

        # Check if "si" is the current dictionary with key "sentencias", if not, add
        if (not self.ruleDictionary["sentencias"].__contains__("sino")):
            self.ruleDictionary["sentencias"].append(
                "sino")  # Adds "sino" to the dictionary

    # Exit a parse tree produced by fodcatParser#elsestat.
    # @param ctx:fodcatParser.ElsestatContext
    def exitElsestat(self, ctx: fodcatParser.ElsestatContext):
        self.addKeywords("sino")

    # Enter a parse tree produced by fodcatParser#func_call.
    # @param ctx:fodcatParser.Func_callContext
    def enterFunc_call(self, ctx: fodcatParser.Func_callContext):
        self.rulecount["llamadas funciones"] += 1  # Add 1 to the counter
        self.rulecount["cantidad sentencias"] += 1  # Add 1 to the counter
        self.functionCallFlag = True
        value = GTI.getTextInterval(ctx, ctx)
        if (self.mainFlag):  # Is in the main function
            self.ruleDictionary["funcion principal"].append(
                "llamada funcion: " + value)
        else:
            if (not self.ruleDictionary["sentencias"].__contains__("sentencia funcion")):
                self.ruleDictionary["sentencias"].append(
                    "sentencia funcion")  # Adds "sentencia" to the dictionary

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("llamada funcion: " + value)):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "llamada funcion: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("llamada funcion: " + value)):
                self.funDecDic[i]["cuerpo ciclo"].append(
                    "llamada funcion: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("llamada funcion: " + value)):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "llamada funcion: " + value)

    # Exit a parse tree produced by fodcatParser#func_call.
    # @param ctx:fodcatParser.Func_callContext
    def exitFunc_call(self, ctx: fodcatParser.Func_callContext):
        self.functionCallFlag = False

    # Enter a parse tree produced by fodcatParser#flow_exp.
    # @param ctx:fodcatParser.Flow_expContext
    def enterFlow_exp(self, ctx: fodcatParser.Flow_expContext):
        value = GTI.getTextInterval(ctx, ctx)
        self.rulecount["cantidad control flujo"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["control flujo"].__contains__(value)):
            self.ruleDictionary["control flujo"].append(
                value)  # Adds "control flujo" to the dictionary

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("control flujo: " + value)):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "control flujo: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("control flujo: " + value)):
                self.funDecDic[i]["cuerpo ciclo"].append(
                    "control flujo: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("control flujo: " + value)):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "control flujo: " + value)

    # Exit a parse tree produced by fodcatParser#flow_exp.
    # @param ctx:fodcatParser.Flow_expContext
    def exitFlow_exp(self, ctx: fodcatParser.Flow_expContext):
        self.addKeywords(ctx.getChild(0).getText())

    # Enter a parse tree produced by fodcatParser#assignment.
    # @param ctx:fodcatParser.AssignmentContext
    def enterAssignment(self, ctx: fodcatParser.AssignmentContext):
        self.rulecount["operador asignacion"] += 1  # Add 1 to the counter

    # ************************************************************************************
    # Expressions
    # ************************************************************************************

    # Enter a parse tree produced by fodcatParser#expression.
    # @param ctx:fodcatParser.ExpressionContext
    def enterExpression(self, ctx: fodcatParser.ExpressionContext):
        if ctx.getChild(0).getChildCount() > 1:
            if ctx.getChild(0).getChild(1).getText() == "[":
                self.arrayFlag = True  # Is an array

    # Exit a parse tree produced by fodcatParser#expression.
    # @param ctx:fodcatParser.ExpressionContext
    def exitExpression(self, ctx: fodcatParser.ExpressionContext):
        if ctx.getChild(0).getChildCount() > 1:
            if ctx.getChild(0).getChild(1).getText() == "[":
                self.arrayFlag = False  # Was an array

    # Enter a parse tree produced by fodcatParser#arithmetic_exp.
    # @param ctx:fodcatParser.
    def enterArithmetic_exp(self, ctx: fodcatParser.Arithmetic_expContext):
        value = GTI.getTextInterval(ctx, ctx)
        # Add 1 to the counter
        self.rulecount["cantidad expresiones aritmeticas"] += 1
        if (not self.ruleDictionary["expresion aritmetica"].__contains__(value)):
            # Adds "expresion aritmetica" to the dictionary
            self.ruleDictionary["expresion aritmetica"].append(value)
        if ctx.getChild(0).getChildCount() > 1:
            if ctx.getChild(0).getChild(1).getText() == "[":
                self.arrayFlag = True  # Is an array

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("expresion aritmetica: " + value)):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "expresion aritmetica: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("expresion aritmetica: " + value)):
                self.funDecDic[i]["cuerpo ciclo"].append(
                    "expresion aritmetica: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("expresion aritmetica: " + value)):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "expresion aritmetica: " + value)

    # Enter a parse tree produced by fodcatParser#relational_exp.
    # @param ctx:fodcatParser.
    def enterRelational_exp(self, ctx: fodcatParser.Relational_expContext):
        value = GTI.getTextInterval(ctx, ctx)
        # Add 1 to the counter
        self.rulecount["cantidad expresiones relacionales"] += 1
        if not (self.ruleDictionary["expresion relacional"].__contains__(value) |
                self.ruleDictionary["expresion relacional"].__contains__("(" + value + ")")):
            # Adds "expresion relacional" to the dictionary
            self.ruleDictionary["expresion relacional"].append(value)

        if (self.ruleDictionary["expresion logica"].__contains__(value) |
                self.ruleDictionary["expresion logica"].__contains__("(" + value + ")")):
            # Adds "expresion logica" to the dictionary
            self.ruleDictionary["expresion logica"].pop(
                self.ruleDictionary["expresion logica"].index(value))

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if not (self.funDecDic[i]["cuerpo funcion"].__contains__("expresion relacional: " + value) |
                    self.funDecDic[i]["cuerpo funcion"].__contains__("expresion relacional: " + "(" + value + ")")):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "expresion relacional: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if not (self.funDecDic[i]["cuerpo ciclo"].__contains__("expresion relacional: " + value) |
                    self.funDecDic[i]["cuerpo ciclo"].__contains__("expresion relacional: " + "(" + value + ")")):
                self.funDecDic[i]["cuerpo ciclo"].append(
                    "expresion relacional: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if not (self.funDecDic[i]["cuerpo condicional"].__contains__("expresion relacional: " + value) |
                    self.funDecDic[i]["cuerpo condicional"].__contains__("expresion relacional: " + "(" + value + ")")):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "expresion relacional: " + value)

    # Enter a parse tree produced by fodcatParser#logic_exp.
    # @param ctx:fodcatParser.
    def enterLogic_exp(self, ctx: fodcatParser.Logic_expContext):
        value = GTI.getTextInterval(ctx, ctx)
        # Add 1 to the counter
        self.rulecount["cantidad expresiones logicas"] += 1
        if not (self.ruleDictionary["expresion relacional"].__contains__(value) |
                self.ruleDictionary["expresion relacional"].__contains__("(" + value + ")")):
            if not (self.ruleDictionary["expresion logica"].__contains__(value) |
                    self.ruleDictionary["expresion logica"].__contains__("(" + value + ")")):
                self.ruleDictionary["expresion logica"].append(
                    value)  # Adds "expresion logica" to the dictionary

        if ((ctx.getChild(0).getText() == "no") | (ctx.getChild(0).getText() == "|")):
            self.rulecount["operador logico"] += 1  # Add 1 to the counter
            if (not self.ruleDictionary["operadores logicos"].__contains__(ctx.getChild(0).getText())):
                self.ruleDictionary["operadores logicos"].append(ctx.getChild(
                    0).getText())  # Adds "operadores logicos" to the dictionary

        if ctx.getChild(0).getChildCount() > 1:
            if ctx.getChild(0).getChild(1).getText() == "[":
                self.arrayFlag = True  # Is an array

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if not (self.funDecDic[i]["cuerpo funcion"].__contains__("expresion logica: " + value) |
                    self.funDecDic[i]["cuerpo condicional"].__contains__("expresion funcion: " + "(" + value + ")")):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "expresion logica: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if not (self.funDecDic[i]["cuerpo ciclo"].__contains__("expresion logica: " + value) |
                    self.funDecDic[i]["cuerpo ciclo"].__contains__("expresion logica: " + "(" + value + ")")):
                self.funDecDic[i]["cuerpo ciclo"].append(
                    "expresion logica: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if not (self.funDecDic[i]["cuerpo condicional"].__contains__("expresion logica: " + value) |
                    self.funDecDic[i]["cuerpo condicional"].__contains__("expresion logica: " + "(" + value + ")")):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "expresion logica: " + value)

    def enterArray_call(self, ctx: fodcatParser.Array_callContext):
        self.arrayFlag = True  # Is an array

    # ************************************************************************************
    # Declarations
    # ************************************************************************************

    # Enter a parse tree produced by fodcatParser#function_declaration.
    # @param ctx:fodcatParser.Function_declarationContext
    def enterFunction_declaration(self, ctx: fodcatParser.Function_declarationContext):
        self.functionDecFlag = True  # Is a function declaration
        self.functionIdenDecFlag = True
        self.rulecount["cantidad funciones"] += 1  # Add 1 to the counter
        i = 1

        while (i < ctx.getChildCount()):
            self.funDec += ctx.getChild(i).getText()  # Creates the funDec
            if (ctx.getChild(i).getText() == ")"):
                i = ctx.getChildCount()
            else:
                i += 1  # Add 1 to the counter
        p = 0
        newFunDec = {
            "declaracion": self.funDec,
            "cuerpo funcion": [],
            "cuerpo ciclo": [],
            "cuerpo condicional": [],
        }
        self.funDecDic.append(newFunDec)  # Adds the newFunDec to the funDecDic

        # i=0
        # while (i<len(self.funDecDic)):
        #     print(self.funDecDic[i])
        #     print(self.funDecDic[i]["declaracion"].__contains__(self.funDec))
        #     i +=1

    # Exit a parse tree produced by fodcatParser#function_declaration.
    # @param ctx:fodcatParser.Function_declarationContext
    def exitFunction_declaration(self, ctx: fodcatParser.Function_declarationContext):
        self.functionDecFlag = False
        self.funDec = ""
        self.addKeywords("para")
        self.addKeywords("fin")

    # Enter a parse tree produced by fodcatParser#array_declaration.
    # @param ctx:fodcatParser.Array_declarationContext
    def enterArray_declaration(self, ctx: fodcatParser.Array_declarationContext):
        self.arrayFlag = True

    # Exit a parse tree produced by fodcatParser#array_declaration.
    # @param ctx:fodcatParser.Array_declarationContext
    def exitArray_declaration(self, ctx: fodcatParser.Array_declarationContext):
        self.arrayFlag = False

    # ************************************************************************************
    # Literals
    # ************************************************************************************

    # Enter a parse tree produced by fodcatParser#int_literal.
    # @param ctx:fodcatParser.
    def enterInt_literal(self, ctx: fodcatParser.Int_literalContext):
        value = GTI.getTextInterval(ctx, ctx)
        self.rulecount["cantidad enteros"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["enteros"].__contains__(value)):
            self.ruleDictionary["enteros"].append(
                value)  # Adds "enteros" to the dictionary

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("entero literal: " + value)):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "entero literal: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("entero literal: " + value)):
                self.funDecDic[i]["cuerpo ciclo"].append(
                    "entero literal: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("entero literal: " + value)):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "entero literal: " + value)

    # Enter a parse tree produced by fodcatParser#bool_literal.
    # @param ctx:fodcatParser.
    def enterBool_literal(self, ctx: fodcatParser.Bool_literalContext):
        value = GTI.getTextInterval(ctx, ctx)
        self.rulecount["cantidad booleanos"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["booleanos"].__contains__(value)):
            self.ruleDictionary["booleanos"].append(
                value)  # Adds "booleanos" to the dictionary

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("booleano literal: " + value)):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "booleano literal: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("booleano literal: " + value)):
                self.funDecDic[i]["cuerpo ciclo"].append(
                    "booleano literal: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("booleano literal: " + value)):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "booleano literal: " + value)

    # Enter a parse tree produced by fodcatParser#float_literal.
    # @param ctx:fodcatParser.
    def enterFloat_literal(self, ctx: fodcatParser.Float_literalContext):
        value = GTI.getTextInterval(ctx, ctx)
        self.rulecount["cantidad flotantes"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["flotantes"].__contains__(value)):
            self.ruleDictionary["flotantes"].append(
                value)  # Adds "flotantes" to the dictionary

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("flotante literal: " + value)):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "flotante literal: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("flotante literal: " + value)):
                self.funDecDic[i]["cuerpo ciclo"].append(
                    "flotante literal: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("flotante literal: " + value)):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "flotante literal: " + value)

    # Enter a parse tree produced by fodcatParser#strg.
    # @param ctx:fodcatParser.
    def enterStrg(self, ctx: fodcatParser.StrgContext):
        value = GTI.getTextInterval(ctx, ctx)
        self.rulecount["cantidad texto"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["texto"].__contains__(value)):
            self.ruleDictionary["texto"].append(
                value)  # Adds "texto" to the dictionary

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("texto: " + value)):
                self.funDecDic[i]["cuerpo funcion"].append("texto: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("texto: " + value)):
                self.funDecDic[i]["cuerpo ciclo"].append("texto: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("texto: " + value)):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "texto: " + value)

    # Enter a parse tree produced by fodcatParser#constant.
    # @param ctx:fodcatParser.
    def enterConstant(self, ctx: fodcatParser.ConstantContext):
        value = GTI.getTextInterval(ctx, ctx)
        # Add 1 to the counter
        self.rulecount["cantidad constantes matematicas"] += 1
        if (not self.ruleDictionary["constantes"].__contains__(value)):
            self.ruleDictionary["constantes"].append(
                value)  # Adds "constantes" to the dictionary

        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        # Checks where it has to add the information
        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("constante: " + value)):
                self.funDecDic[i]["cuerpo funcion"].append(
                    "constante: " + value)

        if (self.functionDecFlag and self.cycleFlag):
            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("constante: " + value)):
                self.funDecDic[i]["cuerpo ciclo"].append("constante: " + value)

        if (self.functionDecFlag and self.conditionalFlag):
            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("constante: " + value)):
                self.funDecDic[i]["cuerpo condicional"].append(
                    "constante: " + value)

    # Enter a parse tree produced by fodcatParser#relational_op.
    # @param ctx:fodcatParser.
    def enterRelational_op(self, ctx: fodcatParser.Relational_opContext):
        value = GTI.getTextInterval(ctx, ctx)
        self.rulecount["operador relacional"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["operadores relacionales"].__contains__(value)):
            # Adds "operadores relacionales" to the dictionary
            self.ruleDictionary["operadores relacionales"].append(value)

    # Enter a parse tree produced by fodcatParser#logic_op.
    # @param ctx:fodcatParser.
    def enterLogic_op(self, ctx: fodcatParser.Logic_opContext):
        value = GTI.getTextInterval(ctx, ctx)
        self.rulecount["operador logico"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["operadores logicos"].__contains__(value)):
            # Adds "operadores logicos" to the dictionary
            self.ruleDictionary["operadores logicos"].append(value)

    # Enter a parse tree produced by fodcatParser#arithmetic_op.
    # @param ctx:fodcatParser.
    def enterArithmetic_op(self, ctx: fodcatParser.Arithmetic_opContext):
        value = GTI.getTextInterval(ctx, ctx)
        self.rulecount["operador aritmetico"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["operadores aritmeticos"].__contains__(value)):
            # Adds "operadores aritmeticos" to the dictionary
            self.ruleDictionary["operadores aritmeticos"].append(value)

    # Enter a parse tree produced by fodcatParser#print_op.
    # @param ctx:fodcatParser.
    def enterPrint_op(self, ctx: fodcatParser.Print_opContext):
        self.rulecount["operador imprimir"] += 1  # Add 1 to the counter

    # Enter a parse tree produced by fodcatParser#sign.
    # @param ctx:fodcatParser.
    def enterSign(self, ctx: fodcatParser.SignContext):
        value = GTI.getTextInterval(ctx, ctx)
        self.rulecount["cantidad signos"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["signos"].__contains__(value)):
            # Adds "signos" to the dictionary
            self.ruleDictionary["signos"].append(value)

    # Enter a parse tree produced by fodcatParser#identifier.
    # @param ctx:fodcatParser.IdentifierContext
    def enterIdentifier(self, ctx: fodcatParser.IdentifierContext):
        identValue = GTI.getTextInterval(ctx, ctx)
        i = 0
        while (i < len(self.funDecDic)):
            # Checks if the function was already declared
            if (self.funDecDic[i]["declaracion"] == self.funDec):
                break
            i += 1  # Add 1 to the counter

        self.rulecount["cantidad identificadores"] += 1  # Add 1 to the counter
        if (not self.ruleDictionary["identificadores"].__contains__(identValue)):
            # Adds "identificadores" to the dictionary
            self.ruleDictionary["identificadores"].append(identValue)

        if (not self.functionCallFlag):  # If is not a function call
            if self.functionIdenDecFlag:
                self.functionIdenDecFlag = False
            else:
                if self.arrayFlag:  # Is an array
                    self.arrayFlag = False
                    if self.ruleDictionary["arreglos"].__contains__(identValue):
                        # Add 1 to the counter
                        self.rulecount["llamadas arreglos"] += 1
                    else:
                        # Add 1 to the counter
                        self.rulecount["cantidad arreglos"] += 1
                        self.ruleDictionary["arreglos"].append(
                            identValue)  # Adds the array to the dictionary
                    if (self.mainFlag):  # Is in the main function
                        self.ruleDictionary["funcion principal"].append(
                            " arreglo: " + identValue)  # Adds "arreglo" to the dictionary
                    else:
                        # Checks where it has to add the information
                        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
                            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("arreglo: " + identValue)):
                                self.funDecDic[i]["cuerpo funcion"].append(
                                    "arreglo: " + identValue)

                        if (self.functionDecFlag and self.cycleFlag):
                            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("arreglo: " + identValue)):
                                self.funDecDic[i]["cuerpo ciclo"].append(
                                    "arreglo: " + identValue)

                        if (self.functionDecFlag and self.conditionalFlag):
                            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("arreglo: " + identValue)):
                                self.funDecDic[i]["cuerpo condicional"].append(
                                    "arreglo: " + identValue)
                else:  # Is a variable
                    if self.ruleDictionary["variables"].__contains__(identValue):
                        # Add 1 to the counter
                        self.rulecount["llamadas variables"] += 1
                    else:
                        # Add 1 to the counter
                        self.rulecount["cantidad variables"] += 1
                        self.ruleDictionary["variables"].append(
                            identValue)  # Adds "variables" to the dictionary
                    if (self.mainFlag):  # Is in the main function
                        self.ruleDictionary["funcion principal"].append(
                            " variable: " + identValue)  # Adds "variable" to the dictionary
                    else:
                        # Checks where it has to add the information
                        if (self.functionDecFlag and not self.cycleFlag and not self.conditionalFlag):
                            if (not self.funDecDic[i]["cuerpo funcion"].__contains__("variable: " + identValue)):
                                self.funDecDic[i]["cuerpo funcion"].append(
                                    "variable: " + identValue)

                        if (self.functionDecFlag and self.cycleFlag):
                            if (not self.funDecDic[i]["cuerpo ciclo"].__contains__("variable: " + identValue)):
                                self.funDecDic[i]["cuerpo ciclo"].append(
                                    "variable: " + identValue)

                        if (self.functionDecFlag and self.conditionalFlag):
                            if (not self.funDecDic[i]["cuerpo condicional"].__contains__("variable: " + identValue)):
                                self.funDecDic[i]["cuerpo condicional"].append(
                                    "variable: " + identValue)


def main(argv):
    if len(argv) == 3:
        coutoutfile = argv[2] + ".json"
        output = open(str(coutoutfile), "w")
        fcat = CodeAnalyzer(output)
    else:
        print("Error, instruccion incorrecta.")
        quit()
    inp = FileStream(argv[1])
    lexer = fodcatLexer(inp)
    stream = CommonTokenStream(lexer)
    parser = fodcatParser(stream)
    tree = parser.program()
    walker = ParseTreeWalker()
    walker.walk(fcat, tree)
    output.close()


if __name__ == "__main__":
    main(sys.argv)
