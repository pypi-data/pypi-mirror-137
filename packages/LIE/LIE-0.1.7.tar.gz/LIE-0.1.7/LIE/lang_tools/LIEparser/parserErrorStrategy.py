####################################################
# LIE++ Parser Error Strategy Handler
# TEC - FOD
# Authors:
#   Michael Gonzalez Rivera
#   Luis Saborio Hernandez
# Edited:
#   Ellioth Ramirez
####################################################

from os import error
import sys

from antlr4 import *
from gen.fodcatParser import fodcatParser
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import RecognitionException, NoViableAltException, InputMismatchException, \
    FailedPredicateException, ParseCancellationException

# This imports are only needed when testing
if __name__ == '__main__':
    from fodcatListener import fodcatListener
    from fodcatLexer import fodcatLexer


class ParserErrorListener(ErrorListener):

    # Provides a default instance of {@link ConsoleErrorListener}.
    INSTANCE = None

    ##
    # {@inheritDoc}
    #
    # <p>
    # This implementation prints messages to {@link System#err} containing the
    # values of {@code line}, {@code charPositionInLine}, and {@code msg} using
    # the following format.</p>
    #
    # <pre>
    # line <em>line</em>:<em>charPositionInLine</em> <em>msg</em>
    # </pre>
    #
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("linea " + str(line) + ":" +
              str(column) + " " + msg, file=sys.stderr)


class ParserErrorStrategy(DefaultErrorStrategy):
    errors = []

    def __init__(self):
        super().__init__()
        pass

    # This is called by {@link #reportError} when the exception is a
    # {@link NoViableAltException}.
    #
    # @see #reportError
    #
    # @param recognizer the parser instance
    # @param e the recognition exception
    def reportNoViableAlternative(self, recognizer: Parser, e: NoViableAltException):
        tokens = recognizer.getTokenStream()
        if tokens is not None:
            if e.startToken.type == Token.EOF:
                input = "<EOF>"
            else:
                input = tokens.getText(e.startToken, e.offendingToken)
        else:
            input = "<desconocida>"
        msg = "ninguna alternativa valida en la entrada " + \
            self.escapeWSAndQuote(input)
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e.offendingToken, e)

    # This is called by @link ParserErrorStrategy.ParserErrorStrategy.reportFailedPredicate reportFailedPredicate @endlink when the exception is an
    # {@link InputMismatchException}.
    #
    # @see #reportError
    #
    # @param recognizer the parser instance
    # @param e the recognition exception
    #
    def reportInputMismatch(self, recognizer: Parser, e: InputMismatchException):
        msg = "entrada inesperada " + self.getTokenErrorDisplay(e.offendingToken) \
              + " esperando " + e.getExpectedTokens().toString(recognizer.literalNames,
                                                               recognizer.symbolicNames)
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e.offendingToken, e)

        #
    # This is called by {@link #reportError} when the exception is a
    # {@link FailedPredicateException}.
    #
    # @see #reportError
    # {@ref holis}
    # @param recognizer the parser instance
    # @param e the recognition exception
    #
    def reportFailedPredicate(self, recognizer, e):
        ruleName = recognizer.ruleNames[recognizer._ctx.getRuleIndex()]
        msg = "regla " + ruleName + " " + e.message
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, e.offendingToken, e)

    # This method is called to report a syntax error which requires the removal
    # of a token from the input stream. At the time this method is called, the
    # erroneous symbol is current {@code LT(1)} symbol and has not yet been
    # removed from the input stream. When this method returns,
    # {@code recognizer} is in error recovery mode.
    #
    # <p>This method is called when {@link #singleTokenDeletion} identifies
    # single-token deletion as a viable recovery strategy for a mismatched
    # input error.</p>
    #
    # <p>The default implementation simply returns if the handler is already in
    # error recovery mode. Otherwise, it calls {@link #beginErrorCondition} to
    # enter error recovery mode, followed by calling
    # {@link Parser#notifyErrorListeners}.</p>
    #
    # @param recognizer the parser instance
    #
    def reportUnwantedToken(self, recognizer: Parser):
        if self.inErrorRecoveryMode(recognizer):
            return

        self.beginErrorCondition(recognizer)
        t = recognizer.getCurrentToken()
        tokenName = self.getTokenErrorDisplay(t)
        expecting = self.getExpectedTokens(recognizer)
        msg = "entrada inesperada " + tokenName + " esperando " \
            + expecting.toString(recognizer.literalNames,
                                 recognizer.symbolicNames)
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, t, None)

    # This method is called to report a syntax error which requires the
    # insertion of a missing token into the input stream. At the time this
    # method is called, the missing token has not yet been inserted. When this
    # method returns, {@code recognizer} is in error recovery mode.
    #
    # <p>This method is called when {@link #singleTokenInsertion} identifies
    # single-token insertion as a viable recovery strategy for a mismatched
    # input error.</p>
    #
    # <p>The default implementation simply returns if the handler is already in
    # error recovery mode. Otherwise, it calls {@link #beginErrorCondition} to
    # enter error recovery mode, followed by calling
    # {@link Parser#notifyErrorListeners}.</p>
    #
    # @param recognizer the parser instance
    #
    def reportMissingToken(self, recognizer: Parser):
        if self.inErrorRecoveryMode(recognizer):
            return
        self.beginErrorCondition(recognizer)
        t = recognizer.getCurrentToken()
        expecting = self.getExpectedTokens(recognizer)
        msg = "falta " + expecting.toString(recognizer.literalNames, recognizer.symbolicNames) \
            + " en " + self.getTokenErrorDisplay(t)
        self.errors.append(msg)
        recognizer.notifyErrorListeners(msg, t, None)


# This main method is used to test the module
#
# @param argv[1] source code file
def main(argv):
    inp = FileStream(argv[1])
    lexer = fodcatLexer(inp)
    stream = CommonTokenStream(lexer)
    parser = fodcatParser(stream)
    parser._errHandler = ParserErrorStrategy()
    parser.removeErrorListeners()
    parser.addErrorListener(ParserErrorListener())
    tree = parser.program()


if __name__ == '__main__':
    main(sys.argv)
