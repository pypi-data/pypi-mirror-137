# Copyright (c) 2021 LightningV1p3r

####################
#Libs
####################

import viperlogger
from . import errors

####################
#Loggine
####################

parser_logger = viperlogger.Logger("Parser", './logs/console-engine.log')
# parser_logger.enable_debugmode('True')

####################
# Nodes
####################

####################
# Non Terminals
####################


class ExpressionNode:
    def __init__(self, list) -> None:
        self.list = list

    def as_string(self) -> str:

        res = "("

        for iterations, i in enumerate(self.list, start=1):
            res += str(i)

            if iterations < len(self.list):
                res += " + "

        res += ")"

        return res

    def __str__(self) -> str:
        return self.as_string()

    def __repr__(self) -> str:
        return self.as_string()


class CommandNode:
    def __init__(self, node1, node2) -> None:
        self.node1 = node1
        self.node2 = node2

    def as_string(self) -> str:
        return f"({self.node1} + {self.node2})"

    def __str__(self) -> str:
        return self.as_string()

    def __repr__(self) -> str:
        return self.as_string()


class FlagValueNode:
    def __init__(self, node1, node2) -> None:
        self.node1 = node1
        self.node2 = node2

    def as_string(self) -> str:
        return f"({self.node1} + {self.node2})"

    def __str__(self) -> str:
        return self.as_string()

    def __repr__(self) -> str:
        return self.as_string()


class KeywordChainNode:
    def __init__(self, list) -> None:
        self.list = list

    def as_string(self) -> str:

        res = "("

        for iterations, i in enumerate(self.list, start=1):
            res += str(i)

            if iterations < len(self.list):
                res += " + "

        res += ")"

        return res

    def __str__(self) -> str:
        return self.as_string()

    def __repr__(self) -> str:
        return self.as_string()


class DataChainNode:
    def __init__(self, list) -> None:
        self.list = list

    def as_string(self) -> str:

        res = "("

        for iterations, i in enumerate(self.list, start=1):
            res += str(i)

            if iterations < len(self.list):
                res += " + "

        res += ")"

        return res

    def __str__(self) -> str:
        return self.as_string()

    def __repr__(self) -> str:
        return self.as_string()


class FlagChainNode:
    def __init__(self, list) -> None:
        self.list = list

    def as_string(self) -> str:

        res = "("

        for iterations, i in enumerate(self.list, start=1):
            res += str(i)

            if iterations < len(self.list):
                res += " + "

        res += ")"

        return res

    def __str__(self) -> str:
        return self.as_string()

    def __repr__(self) -> str:
        return self.as_string()

    ####################
    # Terminals
    ####################


class KeywordNode:
    def __init__(self, value) -> None:
        self.value = value

    def as_string(self) -> str:
        return f"({self.value})"

    def __str__(self) -> str:
        return self.as_string()

    def __repr__(self) -> str:
        return self.as_string()


class FlagNode:
    def __init__(self, value) -> None:
        self.value = value

    def as_string(self) -> str:
        return f"({self.value})"

    def __str__(self) -> str:
        return self.as_string()

    def __repr__(self) -> str:
        return self.as_string()


class ValueNode:
    def __init__(self, value) -> None:
        self.value = value

    def as_string(self) -> str:
        return f"({self.value})"

    def __str__(self) -> str:
        return self.as_string()

    def __repr__(self) -> str:
        return self.as_string()


####################
# Parser
####################


class Parser:
    def __init__(self, tokens, keywords) -> None:
        self.tokens = tokens
        parser_logger.debug(f'To parser: {self.tokens}')
        self.keywords = keywords
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self) -> None:

        self.pos += 1

        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        parser_logger.debug(f"advanced to pos {self.pos} with value: '{self.current_token}'")

    def reverse(self, iterations=1) -> None:

        """Reverses the cursor by one token in the input."""

        iter_count = 0

        while iter_count < iterations:

            self.pos -= 1

            if self.pos < 0:
                e = errors.InvalidCursorPosition(self.pos)
                parser_logger.error(e.exception_msg, '')
                raise e
            else:
                self.current_token = self.tokens[self.pos]
                parser_logger.debug(f"reversed to pos {self.pos} with value: '{self.current_token}'")

            iter_count += 1

    ####################
    # Checkerchar
    ####################

    def check_for_kc(self):

        iterations = 0
        keyword_count = 0

        while self.current_token.value in self.keywords:

            keyword_count += 1
            iterations += 1
            self.advance()

        self.reverse(iterations)
        log_msg = f'Found KeywordChain @{self.pos}' if keyword_count > 1 else 'No KC found'
        parser_logger.debug(log_msg)
        return keyword_count > 1

    def check_for_fvp(self):

        if self.current_token is None:
            return False
        if self.current_token.type == "EOF" or self.current_token.type != "FLAG":
            return False
        self.advance()

        if self.current_token.type not in ["FLAG", "EOF"]:
            self.reverse()
            parser_logger.debug(f'found fvp @{self.pos}')
            return True
        else:
            self.reverse()
            parser_logger.debug("No fvp found")
            return False

    def check_for_dc_complex(self):

        fvp = False

        flags = 0
        iterations = 0

        while self.current_token.type == "FLAG":
            flags += 1
            iterations += 1
            self.advance()

        self.reverse()

        fvp = self.check_for_fvp() == True
        self.reverse(iterations - 1)

        if flags >= 2 and fvp:
            flag_chain = True

        flag_chain = flags >= 2 and fvp
        if flag_chain and fvp:
            parser_logger.debug(f'found dc_complex @{self.pos}')
            return True, flags - 1
        else:
            parser_logger.debug("No dc_complex found")
            return False, None

    def check_for_dc_simple(self):

        if self.check_for_fvp() != True:
            return False

        self.advance()
        self.advance()
        iterations = 0 + 2

        if self.check_for_fvp() == True:
            self.reverse(iterations)
            parser_logger.debug(f'found dc_simple @{self.pos}')
            return True
        else:
            self.reverse(iterations)
            parser_logger.debug("No dc_simple found!")
            return False

    def check_for_fc(self):

        iterations = 0
        flag_count = 0

        while self.current_token.type == "FLAG":
            flag_count += 1
            iterations += 1
            self.advance()

        self.reverse(iterations)
        log_msg = f'found fc @{self.pos}' if flag_count > 1 else 'No fc found'
        parser_logger.debug(log_msg)
        return (True, flag_count) if flag_count > 1 else False

    def check_for_standalone_K(self):  # sourcery skip: extract-duplicate-method

        self.advance()

        if self.current_token.type == "EOF":
            self.reverse()
            parser_logger.debug("found standalone K")
            return True
        else:
            self.reverse()
            parser_logger.debug("No standalone K found")
            return False

    def check_stdaln_KC(self):
        # sourcery skip: extract-duplicate-method, remove-unnecessary-else, swap-if-else-branches

        self.advance()
        iterations = 0 + 1

        if self.current_token.value in self.keywords:
            while (
                self.current_token.type != "EOF"
                and self.current_token.value in self.keywords
            ):
                self.advance()
                iterations += 1

            self.reverse(iterations)
            parser_logger.debug("Found standalone KC")
            return True
        else:
            self.reverse(iterations)
            parser_logger.debug("No standalone KC found")
            return False

    ####################
    # parsing
    ####################

    def parse(self):
        try:
            return self.expression()
        except Exception as exception:
            e = errors.ParsingError(exception)
            parser_logger.critical(e.detailed, '')
            raise e

    def expression(self):

        if self.current_token is None:
            return

        try:
            res = [self.command()]

            self.advance()

            while True:
                if self.current_token is None or self.current_token.type == "EOF":
                    break

                if self.current_token.type == "AMPERSAND":
                    self.advance()
                    if self.current_token.type == "AMPERSAND":
                        self.advance()
                    res.append(self.command())
                self.advance()

            parser_logger.debug(f"Created Expression Node: {res}")
            return ExpressionNode(res)

        except Exception as exception:
            e = errors.ExpressionNodeCreationError(exception)
            parser_logger.critical(e.detailed, '')
            raise e

    def command(self):  # sourcery skip: extract-method

        try:
            if self.current_token.value in self.keywords:
                left = self.keyword()
            else:
                return None

            if self.check_for_standalone_K() == True:
                right = None
                return CommandNode(left, right)

            if self.check_stdaln_KC() == True:
                right = None
                return CommandNode(left, right)

            self.advance()

            if self.current_token.type == "FLAG":

                check_dc_c, flag_count = self.check_for_dc_complex()

                if check_dc_c == True:
                    right = self.data_chain("complex", flag_count)

                elif self.check_for_dc_simple() == True:
                    right = self.data_chain("simple")

                elif self.check_for_fvp() == True:
                    right = self.flag_value_pair()

                elif self.check_for_fc() == True:
                    right = self.flag_chain()

                else:
                    right = self.flag()

            else:
                right = self.value()

            return CommandNode(left, right)

        except Exception as exception:
            e = errors.CommandNodeCreationError(exception)
            parser_logger.critical(e.detailed, '')
            raise e
            
    def keyword(self):

        try:
            if self.current_token.value not in self.keywords:
                return None

            if self.check_for_kc() == True:
                return self.keyword_chain()
            else:
                return KeywordNode(self.current_token.value)
        except Exception as exception:
            e = errors.KeywordNodeCreationError(exception)
            parser_logger.critical(e.detailed, '')
            raise e

    def keyword_chain(self):

        try:
            res = []

            while self.current_token.value in self.keywords:
                res.append(KeywordNode(self.current_token.value))
                self.advance()

            self.reverse()
            return KeywordChainNode(res)
        except Exception as exception:
            e = errors.KeywordChainNodeCreationError(exception)
            parser_logger.critical(e.detailed, '')
            raise e

    def flag(self):
        return FlagNode(self.current_token.value)

    def value(self):
        return ValueNode(self.current_token)

    def flag_value_pair(self):

        try:
            flag = self.flag()
            self.advance()
            value = self.value()
            return FlagValueNode(flag, value)
        except Exception as exception:
            e = errors.FlagValuePairNodeCreationError(exception)
            parser_logger.critical(e.detailed, '')
            raise e

    def data_chain(self, mode, flag_count=None):

        try:
            res = []

            if mode == "complex":
                res.append(self.flag_chain("counter", flag_count))
            while True:
                if self.check_for_fvp() != True:
                    break
                res.append(self.flag_value_pair())
                self.advance()

            return DataChainNode(res)
        except Exception as exception:
            e = errors.DataChainNodeCreationError(exception)
            parser_logger.critical(e.detailed, '')
            raise e

    def flag_chain(self, mode, flag_count):

        try:
            res = []
            if mode == "counter":
                iterations = 0
                while iterations < flag_count:
                    iterations += 1
                    res.append(self.flag())
                    self.advance()
            else:
                while self.current_token.type == "FLAG":
                    res.append(self.flag())
                    self.advance()

            return FlagChainNode(res)
        except Exception as exception:
            e = errors.FlagChainNodeCreationError(exception)
            parser_logger.critical(e.detailed, '')
            raise e