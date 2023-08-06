# Copyright (c) 2021 LightningV1p3r

####################
#Parser & Lexer Errors
####################

class InvalidCursorPosition(Exception):
    def __init__(self, details) -> None:
        self.exception_msg = f"Attempt to move to illegal position: {details}"
        super().__init__(self.exception_msg)

    def __repr__(self) -> str:
        return self.exception_msg

####################
#Lexer Errors
####################

class TokenMergingError(Exception):
    def __init__(self, tok1, tok2, details) -> None:
        self.exception_msg = f"Failed to merge tokens '{tok1}'&'{tok2}': {details}"
        super().__init__(self.exception_msg)

    def __repr__(self) -> str:
        return self.exception_msg


class IllegalCharError(Exception):
    def __init__(self, details) -> None:
        self.exception_msg = f"Unsupported Character: '{details}'"
        super().__init__(self.exception_msg)

    def __repr__(self) -> str:
        return self.exception_msg

####################
#Parser Errors
####################

class ParsingError(Exception):
    def __init__(self, details) -> None:
        self.exception_msg = "Error occured while parsing! Check Logs for more details"
        self.detailed = f"Error occurred while parsing: '{details}'"
        super().__init__(self.exception_msg)

    def __repr__(self) -> str:
        return self.exception_msg


class ExpressionNodeCreationError(ParsingError):
    def __init__(self, details) -> None:
        super().__init__(details)


class CommandNodeCreationError(ParsingError):
    def __init__(self, details) -> None:
        super().__init__(details)


class KeywordNodeCreationError(ParsingError):
    def __init__(self, details) -> None:
        super().__init__(details)


class KeywordChainNodeCreationError(ParsingError):
    def __init__(self, details) -> None:
        super().__init__(details)


class FlagValuePairNodeCreationError(ParsingError):
    def __init__(self, details) -> None:
        super().__init__(details)
        

class DataChainNodeCreationError(ParsingError):
    def __init__(self, details) -> None:
        super().__init__(details)


class FlagChainNodeCreationError(ParsingError):
    def __init__(self, details) -> None:
        super().__init__(details)


####################
#Interpreter Error
####################

class InvalidConfig(Exception):

    def __init__(self, details) -> None:
        self.exception_msg = f'Invalid Configuration: {details}'
        super().__init__(self.exception_msg)

    def __repr__(self) -> str:
        return self.exception_msg


class InvalidNode(Exception):

    def __init__(self, details) -> None:
        self.exception_msg = f'Encountered invalid Node: {details}'
        super().__init__(self.exception_msg)

    def __repr__(self) -> str:
        return self.exception_msg

###################
#Shell Errors
###################

class InternalError(Exception):

    def __init__(self, details) -> None:
        self.exception_msg = f'console-engine experienced an internal Error: {details}'
        super().__init__(self.exception_msg)

    def __repr__(self) -> str:
        return self.exception_msg


class MissingConfiguration(Exception):

    def __init__(self, details) -> None:
        self.exception_msg = f'Missing Configuration: {details}'
        super().__init__(self.exception_msg)

    def __repr__(self) -> str:
        return self.exception_msg

