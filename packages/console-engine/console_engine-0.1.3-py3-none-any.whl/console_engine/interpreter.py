# Copyright (c) 2021 LightningV1p3r

####################
#Libs
####################

import viperlogger
from . import errors

####################
#Logger
####################

interpreter_logger = viperlogger.Logger("Interpreter", './logs/console-engine.log')
# interpreter_logger.enable_debugmode('True')

####################
# Interpreter
####################


class Interpreter:
    def __init__(self, ast, config) -> None:
        self.ast = ast
        self.config = config

        self.keywords = []
        self.groups = []

        self.instructions = []
        self.instruction_set = {"group": None, "idx": "", "data": {}}
        self.instruction_count = 0

        self.digest_config()

    def gen_inst_stack(self):

        try:
            self.visit(self.ast)
            return self.instructions, self.instruction_count
        except Exception as exception:
            e = errors.InvalidNode(exception)
            interpreter_logger.error(e.exception_msg, '')
            return None, None       

    def digest_config(self):

        try:
            cfg = self.config
            self.keywords = list(cfg["keywords"])
            interpreter_logger.debug("loaded config")
    #        self.groups = list(cfg['group_assign'])
        except Exception as exception:
            e = errors.InvalidConfig(exception)
            interpreter_logger.critical(e.exception_msg, '')
            raise e

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        interpreter_logger.debug(f'visiting {type(node).__name__}')

        return method(node)

    def visit_ExpressionNode(self, node):

        for i in node.list:
            self.visit(i)
            self.instructions.append(self.instruction_set)
            self.instruction_count += 1
            self.instruction_set = {"group": None, "idx": "", "data": {}}

    def visit_CommandNode(self, node):

        self.visit(node.node1)
        if node.node2 != None:
            self.visit(node.node2)

    def visit_FlagValueNode(self, node):

        if self.instruction_set["group"] is not None:
            method = self.config["group_assign"][self.instruction_set["group"]][
                self.instruction_set["idx"]
            ]
        else:
            method = self.config["methods"][self.instruction_set["idx"]]

        if node.node1.value in list(method["arguments"]["flags"]):
            type = method["arguments"]["flags"][node.node1.value]["type"]

            if node.node2.value.type == type:
                idx = method["arguments"]["flags"][node.node1.value]["idx"]
                self.instruction_set["data"][idx] = node.node2.value.value

    def visit_KeywordChainNode(self, node):

        for i in node.list:
            self.visit(i)

    def visit_DataChainNode(self, node):

        for i in node.list:
            self.visit(i)

    def visit_FlagChainNode(self, node):

        for i in node.list:
            self.visit(i)

    def visit_KeywordNode(self, node):

        if node.value in self.groups:
            self.instruction_set["group"] = node.value
        elif node.value in self.keywords:
            self.instruction_set["idx"] = self.config["keywords"][node.value]
        else:
            raise Exception("Unknown Keyword!")

    def visit_FlagNode(self, node):

        if self.instruction_set["group"] is not None:
            method = self.config["group_assign"][self.instruction_set["group"]][
                self.instruction_set["idx"]
            ]
        else:
            method = self.config["methods"][self.instruction_set["idx"]]

        if (
            node.value in list(method["arguments"]["flags"])
            and method["arguments"]["flags"][node.value]["type"] == "bool"
        ):
            self.instruction_set["data"][
                method["arguments"]["flags"][node.value]["idx"]
            ] = True

    def visit_ValueNode(self, node):

        if self.instruction_set["group"] is not None:
            method = self.config["group_assign"][self.instruction_set["group"]][
                self.instruction_set["idx"]
            ]
        else:
            method = self.config["methods"][self.instruction_set["idx"]]

        if node.value.type in list(method["arguments"]["values"]):
            self.instruction_set["data"][
                method["arguments"]["values"][node.value.type]
            ] = node.value.value
        else:
            raise Exception("Invalid Data type!")
