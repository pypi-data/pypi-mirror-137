####################################################
# Semantic analyzer to LIE++ Language
# TEC - FOD
# Authors:
#   Michael Gonzalez Rivera
#   Luis Saborio Hernandez
# Edited:
#   Ellioth Ramirez
####################################################

import sys

from LIE.lang_tools.LIEparser.parserErrorStrategy import *
from LIE.lang_tools.LIEsemantic.semanticErrors import *
# from LIEsemantic.semanticErrorStrategy import *

# ANTLR4 imports
from antlr4 import *
from gen.fodcatListener import fodcatListener
from gen.fodcatLexer import fodcatLexer
from gen.fodcatParser import fodcatParser

# It is informed when ocurred a semantic error and throw the message to standard error.


class SemanticErrorListener():

    # throw the error message to standard error.
    # @param line Line number where the error was detected
    # @param comlun Character position where the error was detected
    # @param msg Error message
    def semanticError(self,  line, column, msg):
        print("linea " + str(line) + ":" +
              str(column) + " " + msg, file=sys.stderr)

# Semantic analyzer.
#
# It uses syntax tree (AST) and functions and variables dictionaries to check whether the
# given program is semantically consistent with language definition.


class SemanticAnalyzer(fodcatListener):

    # Semantic analyzer constructor. Initialize all needed global variables for the
    # succesfully execution of the semantic analyzer.
    def __init__(self):

        # global_var_dic Identifiers list of all global varaibles.
        # Each item structure var_id: is_array
        # Each item has bool type to know if is an array variable
        self.global_var_dic = {}
        # This list is cleared when exit declaration function node.
        self.local_var_dic = {}
        # Each item structure is compund of a key: Function identifier, and
        # a value: wich is a dictionary to. compound by a key: the quantity of params
        # a value: an array, with bool values indicating if the parameter is array or not.
        self.func_dic = {}
        self.func_dic["leer"] = {0: []}
        # Flag indicating if is need to validate if the entered identifier exists.
        self.validate_identifier = False
        # Flag indicating if we are in a globla or a local scope.
        self.is_global = True
        # Pointer to semantic error handler. SemanticErrorStrategy is
        # the object assing by default.
        self.errorHandler = SemanticErrorStrategy()
        # Pointer to semantic error listener. @link lang_tools.parser.parserErrorStrategy.SemanticErrorListener is
        # the object assing by default.
        self.listeners = [SemanticErrorListener()]

    # Enter a parse tree produced by fodcatParser#main_function.
    # @param ctx Rule context.
    def enterMain_function(self, ctx: fodcatParser.Main_functionContext):
        self.is_global = False

    # Exit a parse tree produced by fodcatParser#main_function.
    # @param ctx Rule context.
    def exitMain_function(self, ctx: fodcatParser.Main_functionContext):
        self.is_global = True

    # Notify all error registered listeners when an error is detected.
    # @param msg String message to be sended.
    # @param e Error object.
    def notifyErrorListeners(self, msg: str, e: SemanticError):
        for listener in self.listeners:
            listener.semanticError(e.line, e.column, msg)

    # Remove all errror listeners from listeners list.
    def removeErrorListeners():
        listeners.clear()

    # Add an error listners to listeners list.
    # @param listener Error listener to be added.
    def addErrorListener(listener: SemanticErrorListener):
        listeners.append(listener)

    # Enter a parse subtree produced by expression rule.
    # Activate validate identifier flag.
    # @param ctx Rule context
    def enterExpression(self, ctx: fodcatParser.ExpressionContext):
        self.validate_identifier = True

    # Exit a parse subtree produced by expression rule.
    # Desactivate validate identifier.
    # @param ctx Rule context
    def exitExpression(self, ctx: fodcatParser.ExpressionContext):
        self.validate_identifier = False

    # Exit a parse subtree produced by assignment rule.
    # Adds the assignation left side to the global or local list as appropriate.
    # @param ctx Rule context
    def enterAssignment(self, ctx: fodcatParser.AssignmentContext):
        if (isinstance(ctx.getChild(0), fodcatParser.IdentifierContext)):
            var_name = ctx.getChild(0).getText()

            if (self.is_global):
                if (var_name not in self.global_var_dic):
                    self.global_var_dic[var_name] = False
                elif (self.global_var_dic[var_name] == True):
                    self.errorHandler.reportSemanticError(self, ArrayWithoutIndex(
                        ctx.start.line, ctx.start.column, var_name))
            else:
                if (var_name not in self.local_var_dic):
                    self.local_var_dic[var_name] = False
                elif (self.local_var_dic[var_name] == True):
                    self.errorHandler.reportSemanticError(self, ArrayWithoutIndex(
                        ctx.start.line, ctx.start.column, var_name))

    # Enter a parse tree produced by fodcatParser#array_declaration.
    # Validate if the identifier to array name is avaiable, if it is, the add
    # the array to global_var_dic o local_var_dic as appropiated.
    # If it is not avaible it throw a semantic error
    # @param ctx Rule context
    def enterArray_declaration(self, ctx: fodcatParser.Array_declarationContext):
        var_name = ctx.getChild(0).getText()

        if (self.is_global):
            if (var_name not in self.global_var_dic):
                self.global_var_dic[var_name] = True
            else:
                self.errorHandler.reportSemanticError(self, VariableRedefinition(
                    ctx.start.line, ctx.start.column, var_name))
        else:
            if (var_name not in self.local_var_dic):
                self.local_var_dic[var_name] = True
            else:
                self.errorHandler.reportSemanticError(self, VariableRedefinition(
                    ctx.start.line, ctx.start.column, var_name))

    # Enter a parse subtree produced by identifier rule.
    # Notify of an error if there are a reference to an identifier wich does not exist.
    # @param ctx Rule context
    def enterIdentifier(self, ctx: fodcatParser.IdentifierContext):
        if (self.validate_identifier
            and ctx.getText() not in self.local_var_dic
            and ctx.getText() not in self.global_var_dic
                and not isinstance(ctx.parentCtx, fodcatParser.Func_callContext)):

            self.errorHandler.reportSemanticError(self, NoMatchIdentifier(
                ctx.start.line, ctx.start.column, ctx.getText()))

    # Enter a parse tree produced by fodcatParser#array_call.
    # Throw a semantic error, if the array called was not defined before
    # @param ctx Rule context
    def enterArray_call(self, ctx: fodcatParser.Array_callContext):
        var_name = ctx.getChild(0).getText()
        if (self.is_global):
            if (var_name not in self.global_var_dic):
                self.errorHandler.reportSemanticError(self, ArrayNotDefined(
                    ctx.start.line, ctx.start.column, var_name))
            elif (self.global_var_dic[var_name] == False):
                self.errorHandler.reportSemanticError(self, ArrayNotDefined(
                    ctx.start.line, ctx.start.column, var_name))
        else:
            if (var_name in self.local_var_dic):
                if (self.local_var_dic[var_name] == False):
                    self.errorHandler.reportSemanticError(self, ArrayNotDefined(
                        ctx.start.line, ctx.start.column, var_name))
            elif (var_name in self.global_var_dic):
                if (self.global_var_dic[var_name] == False):
                    self.errorHandler.reportSemanticError(self, ArrayNotDefined(
                        ctx.start.line, ctx.start.column, var_name))
            else:
                self.errorHandler.reportSemanticError(self, ArrayNotDefined(
                    ctx.start.line, ctx.start.column, var_name))

    # Enter a parse subtree produced by function_declaration rule.
    # Advice we are entering to an local scope.
    #
    # Notify of an error if the function is already added. In other words the function the
    # function definition is repeated.
    # The function firm is compound of the function name and the quantity of parameters.
    # @param ctx Rule context
    def enterFunction_declaration(self, ctx: fodcatParser.Function_declarationContext):
        self.is_global = False

        params = ctx.getChild(3)
        params_type = []
        params_qty = 0
        i = 0
        while (i < params.getChildCount()):
            if (isinstance(params.getChild(i), fodcatParser.IdentifierContext)):
                params_qty += 1
                if(i+1 < params.getChildCount()):
                    if(params.getChild(i+1).getText() != '['):
                        self.local_var_dic[params.getChild(
                            i).getText()] = False
                        params_type.append(False)
                    else:
                        self.local_var_dic[params.getChild(i).getText()] = True
                        params_type.append(True)
                else:
                    self.local_var_dic[params.getChild(i).getText()] = False
                    params_type.append(False)
            i += 1

        func_name = ctx.getChild(1).getText()
        if (func_name in self.func_dic):
            if (params_qty in self.func_dic[func_name]):
                self.errorHandler.reportSemanticError(self, FunctionRedefinition(
                    ctx.start.line, ctx.start.column, func_name, params_qty))
            else:
                self.func_dic[func_name][params_qty] = params_type
        else:
            self.func_dic[func_name] = {params_qty: params_type}

    # Exit a parse subtree produced by function_declaration rule.
    # Advice we are entering to a global scope. Reason why clear local variables list.
    #
    # The firm is compound of the function name and the quantity of parameters.
    # @param ctx Rule context
    def exitFunction_declaration(self, ctx: fodcatParser.Function_declarationContext):
        self.is_global = True
        self.local_var_dic.clear()

    # Exit a parse subtree produced by function_declaration rule.
    # Throw an error if the function wich is beeing calling does not exist.
    # Throw an error if the parameters type do not match
    # @param ctx Rule context
    def enterFunc_call(self, ctx: fodcatParser.Func_callContext):
        # getting parameter quantity
        params_qty = ctx.getChild(2).getChildCount()
        if (params_qty > 1):
            params_qty = int(((params_qty - 1) / 2) + 1)

        func_name = ctx.getChild(0).getText()

        if (func_name in self.func_dic):
            if (params_qty in self.func_dic[func_name]):
                params = self.func_dic[func_name][params_qty]

                i = 0  # params array index
                j = 0  # identifier child index
                params_id = ctx.getChild(2)
                while i < params_qty:
                    if (isinstance(params_id.getChild(j).getChild(0), fodcatParser.IdentifierContext)):
                        identifier = params_id.getChild(j).getText()
                        if (identifier in self.local_var_dic):
                            if (self.local_var_dic[identifier] != params[i]):
                                if (self.local_var_dic[identifier] == True):
                                    expected_type = "escalar"
                                    getted_type = "arreglo"
                                else:
                                    expected_type = "arreglo"
                                    getted_type = "escalar"

                                self.errorHandler.reportSemanticError(self, NoCompatibleParam(
                                    ctx.start.line, ctx.start.column, expected_type, getted_type))

                        elif (identifier in self.global_var_dic):
                            if (self.global_var_dic[identifier] != params[i]):
                                if (self.global_var_dic[identifier] == True):
                                    expected_type = "arreglo"
                                    getted_type = "escalar"
                                else:
                                    expected_type = "escalar"
                                    getted_type = "arreglo"

                                self.errorHandler.reportSemanticError(self, NoCompatibleParam(
                                    ctx.start.line, ctx.start.column, expected_type, getted_type))

                    j += 2
                    i += 1
            else:
                self.errorHandler.reportSemanticError(self, NoMatchedFunction(
                    ctx.start.line, ctx.start.column, func_name, params_qty))
        else:
            self.errorHandler.reportSemanticError(self, NoMatchedFunction(
                ctx.start.line, ctx.start.column, func_name, params_qty))

    # Exit a parse subtree produced by gpio_declaration rule.
    # Throw an error if the parameters to declare the gpio variable are not right.
    # @param ctx Rule context
    def enterGpio_declaration(self, ctx: fodcatParser.Gpio_declarationContext):
        gpio_type = ctx.getChild(2).getText()
        params_qty = ctx.getChild(4).getChildCount()
        if (params_qty > 1):
            params_qty = int(((params_qty - 1) / 2) + 1)

        if (gpio_type == 'boton'):
            if (params_qty != 1):
                self.errorHandler.reportSemanticError(self, NoMatchedFunction(
                    ctx.start.line, ctx.start.column, gpio_type, params_qty))

        elif (gpio_type == 'led'):
            if (ctx.getChild(3).getText() == '.'):
                params_qty = ctx.getChild(6).getChildCount()
                if (params_qty > 1):
                    params_qty = int(((params_qty - 1) / 2) + 1)
                gpio_type = ctx.getChild(4).getText()

            if (params_qty != 1):
                self.errorHandler.reportSemanticError(self, NoMatchedFunction(
                    ctx.start.line, ctx.start.column, gpio_type, params_qty))

        elif (gpio_type == 'servo'):
            if (params_qty != 1 and params_qty != 3):
                self.errorHandler.reportSemanticError(self, NoMatchedFunction(
                    ctx.start.line, ctx.start.column, gpio_type, params_qty))

# Error messeages definition.


class SemanticErrorStrategy():
    errors = []
    # Report an error for an array call to an array wich is no beeing defined.
    # @param recognizer Object wich have the error listener list.
    # @param e Data error object.

    def reportArrayNotDefined(self, recognizer: SemanticAnalyzer, e: ArrayNotDefined):
        msg = 'El arreglo: "' + e.offended_identifier + '" no ha sido definidio.'
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e)

    # Report an eror to an array call wich do not specify an index.
    # @param recognizer Object wich have the error listener list.
    # @param e Data error object.
    def reportArrayWithoutIndex(self, recognizer: SemanticAnalyzer, e: ArrayWithoutIndex):
        msg = 'El arreglo: "' + e.offended_identifier + \
            '" requiere que se indique una posición.'
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e)

    # Report an error for a variable redefinition
    # @param recognizer Object wich have the error listener list.
    # @param e Data error object.
    def reportVariableRedefinition(self, recognizer: SemanticAnalyzer, e: VariableRedefinition):
        msg = 'La variable "' + e.duplicated_identifier + \
            '" fue definida anteriormente. \n'
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e)

    # Report an error for a function redefinition.
    # @param recognizer Object wich have the error listener list.
    # @param e Data error object.
    def reportFuctionRedefinition(self, recognizer: SemanticAnalyzer, e: FunctionRedefinition):
        msg = 'Función "' + e.duplicated_identifier + '", con "' + \
            str(e.params_qty) + '" parametros definida anteriormente.'
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e)

    # Report an error for a function call to a function not defined.
    # @param recognizer Object wich have the error listener list.
    # @param e Data error object.
    def reportNoMatchedFunction(self, recognizer: SemanticAnalyzer, e: NoMatchedFunction):
        msg = 'Función "' + e.no_matched_identifier + '" con "' + \
            str(e.params_qty) + '" parametros, no se ha definido.'
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e)

    # Report an error when sending no compatible param type.
    # @param recognizer Object wich have the error listener list.
    # @param e Data error object.
    def reportNoCompatibleParam(self, recognizer: SemanticAnalyzer, e: NoCompatibleParam):
        msg = 'Paso de parametro incompatible. Tipo esperado "' + e.expected_type + '", tipo recibido "'\
            + e.getted_type + '.'
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e)

    # Report an error for a identifier call wich is not beeing defined.
    # @param recognizer Object wich have the error listener list.
    # @param e Data error object.
    def reportNoMatchIdentifier(self, recognizer: SemanticAnalyzer, e: NoMatchIdentifier):
        msg = 'identificador: "' + e.no_matched_identifier + '" no declarado'
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e)

    # Depending of the semantic error type chose the error handler.
    # @param recognizer Object wich have the error listener list.
    # @param e Data error object.
    def reportSemanticError(self, recognizer: SemanticAnalyzer, e: SemanticError):
        if isinstance(e, NoMatchIdentifier):
            self.reportNoMatchIdentifier(recognizer, e)
        elif isinstance(e, FunctionRedefinition):
            self.reportFuctionRedefinition(recognizer, e)
        elif isinstance(e, NoMatchedFunction):
            self.reportNoMatchedFunction(recognizer, e)
        elif isinstance(e, VariableRedefinition):
            self.reportVariableRedefinition(recognizer, e)
        elif isinstance(e, ArrayWithoutIndex):
            self.reportArrayWithoutIndex(recognizer, e)
        elif isinstance(e, ArrayNotDefined):
            self.reportArrayNotDefined(recognizer, e)
        elif isinstance(e, NoCompatibleParam):
            self.reportNoCompatibleParam(recognizer, e)

        sys.exit(0)


def main(argv):
    inp = FileStream(argv[1])
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


if __name__ == '__main__':
    main(sys.argv)
