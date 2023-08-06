# Copyright (c) 2021 LightningV1p3r

####################
# Libs
####################

from . import lexer, parser, interpreter, errors

import colorama
import getpass
import viperlogger

####################
#Logger
####################

shell_logger = viperlogger.Logger("Shell", './logs/console-engine.log')
# shell_logger.enable_debugmode('True')
shell_logger.enable_terminal_output('True')

####################
# Shell
####################


class Shell:
    def __init__(self, config, header=None, banner=None) -> None:
        
        if config is None:
            e = errors.MissingConfiguration(' ')
            shell_logger.critical(e.exception_msg, '')
            raise e

        self.config = config
        self.banner = banner
        self.keywords = list(self.config["keywords"])

        self.header = ">> " if header is None else header

    def prompt(self):  # sourcery skip: extract-method

        try:
            user_input = input(self.header)

            lexer_ = lexer.Lexer(user_input)
            tokens = lexer_.tokenize()

            parser_ = parser.Parser(tokens, self.keywords)
            ast = parser_.parse()

            interpreter_ = interpreter.Interpreter(ast, self.config)
            inst, count = interpreter_.gen_inst_stack()

            if inst:
                return inst, count
            print("Unknown Command!")
            return None, None
        except Exception as exception:
            e = errors.InternalError(exception)
            shell_logger.critical(e.exception_msg, '')
            raise e

    def prompt_secret(self):

        prefix = "[⚿]"
        return getpass(prefix)

    def prompt_passthrough(self):

        return input(self.header)

    def update_header(self, val):
        self.header = val

    def out(self, output, prefix=None):

        if prefix == "sucess":
            out = f"[{colorama.Fore.GREEN}✓{colorama.Fore.RESET}]"
            print(out)
        elif prefix == "warning":
            out = f"[{colorama.Fore.YELLOW}⚠{colorama.Fore.RESET}]"
            print(out)
        elif prefix == "failed":
            out = f"[{colorama.Fore.RED}✖{colorama.Fore.RESET}]"
            print(out)
        else:
            print(output)
