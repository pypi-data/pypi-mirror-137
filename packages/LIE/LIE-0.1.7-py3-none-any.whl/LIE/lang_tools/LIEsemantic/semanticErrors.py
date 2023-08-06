####################################################
# LIE++ Semantic Errors
# Definitions of all kinds of semantic errors
# handler by the compiler
# TEC - FOD
# Authors:
#   Michael Gonzalez Rivera
#   Luis Saborio Hernandez
####################################################

## Semantic errors base clase. Data class.
class SemanticError():
    
    ## Constructor method
    # @param line line number where the error ocurred.
    # @param column Character position where the error ocurred.
    def __init__(self, line:int, column:int):
        self.line = line
        self.column = column

## Used when there is an array call to an identifier wich is no being defined
class ArrayNotDefined(SemanticError):
    
    ## Constructor method
    # @param line line number where the error ocurred.
    # @param column Character position where the error ocurred.
    # @param offended_identifier identifier wich is no beeing defined
    def __init__(self, line:int, column:int, offended_identifier:str):
        super().__init__(line, column)
        self.offended_identifier = offended_identifier

## Used when there is a call to an identifier defined as array, bu it do not specify an index.
class ArrayWithoutIndex(SemanticError):
    
    ## Constructor method
    # @param line line number where the error ocurred.
    # @param column Character position where the error ocurred.
    # @param offended_identifier identifier wich is no beeing defined
    def __init__(self, line:int, column:int, offended_identifier:str):
        super().__init__(line, column)
        self.offended_identifier = offended_identifier

## Used when a variable is redefined. The only two types of variables are arrays and scalar variables.
class VariableRedefinition(SemanticError):
    
    ## Constructor method
    # @param line line number where the error ocurred.
    # @param column Character position where the error ocurred.
    # @param duplicated_identifier identifier wich is beeing redefined
    def __init__(self, line:int, column:int, duplicated_identifier:str):
        super().__init__(line, column)
        self.duplicated_identifier = duplicated_identifier
        
## Used when there is a redefinition function.
# The function signature is the name and the quantity of parameters.
class FunctionRedefinition(SemanticError):
    
    ## Constructor method
    # @param line line number where the error ocurred.
    # @param column Character position where the error ocurred.
    # @param duplicated_identifier function name wich is beeing redefined.
    # @param params_qty function parameters quantity.
    def __init__(self, line:int, column:int, duplicated_identifier:str, params_qty:int):
        super().__init__(line, column)
        self.duplicated_identifier = duplicated_identifier
        self.params_qty = params_qty

## Used when there is function call to a function signature not defined before.
class NoMatchedFunction(SemanticError):

    ## Constructor method
    # @param line line number where the error ocurred.
    # @param column Character position where the error ocurred.
    # @param duplicated_identifier function name wich is beeing redefined.
    # @param params_qty function parameters quantity.
    def __init__(self, line:int, column:int, no_matched_identifier:str, params_qty:int):
        super().__init__(line, column)
        self.no_matched_identifier = no_matched_identifier
        self.params_qty = params_qty

## Used when there is a call to a identifier wich is not beeing defined before.
class NoMatchIdentifier(SemanticError):
    
    ## Constructor method
    # @param line line number where the error ocurred.
    # @param column Character position where the error ocurred.
    # @param no_matched_identifier idenfier wich is not beeing deifned.
    def __init__(self, line:int, column:int, no_matched_identifier:str):
        super().__init__(line, column)
        self.no_matched_identifier = no_matched_identifier

## Used when sending a parameter wich do not match with the parameter type of the function signature.
class NoCompatibleParam(SemanticError):

    ## Constructor method
    # @param line line number where the error ocurred.
    # @param column Character position where the error ocurred.
    # @param expected_type Expected parameter type    # @param getted_type Sended parameter type.
    def __init__(self, line:int, column:int, expected_type:str, getted_type:str):
        super().__init__(line, column)
        self.expected_type = expected_type
        self.getted_type = getted_type