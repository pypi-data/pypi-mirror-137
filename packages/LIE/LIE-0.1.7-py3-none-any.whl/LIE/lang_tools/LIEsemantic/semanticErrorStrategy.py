####################################################
# LIE++ Semantic Error Strategy Handler
# TEC - FOD
# Authors:
#   Michael Gonzalez Rivera
#   Luis Saborio Hernandez
# Edited:
#   Ellioth Ramirez
####################################################

import sys

from LIE.lang_tools.LIEsemantic.semanticErrors import *
from LIE.lang_tools.LIEsemantic.semanticAnalyzer import SemanticAnalyzer

# Error messeages definition.


class SemanticErrorStrategy():
    errors = []
    # Report an error for an array call to an array wich is no beeing defined.
    # @param recognizer Object wich have the error listener list.
    # @param e Data error object.

    def reportArrayNotDefined(self, recognizer: SemanticAnalyzer, e: ArrayNotDefined):
        msg = 'El arreglo: "' + e.offended_identifier + '" no ha sido definido.'
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
