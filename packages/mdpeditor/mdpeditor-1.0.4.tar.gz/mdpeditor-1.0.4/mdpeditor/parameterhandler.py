""" handle parameters like transforming, merging, converting"""
import configparser
from collections import OrderedDict

import mdpeditor.mdpblocks.provide as provide
from mdpeditor.mdpblocks.process import apply_instructions


def compile_input_token_to_parameters(word):

    try:
        return provide.mdp_string_to_ordered_dict(word)
    except configparser.ParsingError:
        pass

    try:
        return provide.read_parameter_block(word)
    # depending on the word format we'll fail at different positions
    # if this is not a well formed parameter block name a.b
    except ModuleNotFoundError:
        # has form a.b , where a does not exist as a module
        pass
    except FileNotFoundError:
        # has form a.b where a exists, but not b
        pass
    except IndexError:
        # does not have form a.b
        pass

    try:
        with open(word) as f:
            mdp_input_as_string = f.read()
        return provide.mdp_string_to_ordered_dict(mdp_input_as_string)
    except FileNotFoundError:
        pass
    except configparser.ParsingError:
        pass

    raise ValueError(f"{word} cannot be read as an .mdp file, a block name or "
                     f"an attempt to set an .mdp option.")


def compile_parameters(compile_input):

    parameter_blocks = [
        compile_input_token_to_parameters(token) for token in compile_input
    ]

    parameters = OrderedDict()
    duplicate_keys = set()

    for block in parameter_blocks:

        # collect overlapping parameters in the blocks
        duplicate_keys |= set(parameters.keys()) & set(block.keys())
        parameters.update(block)

    apply_instructions(parameters, compile_input)

    return OutputParameters(parameters, duplicate_keys)


class OutputParameters:
    """
    Handle parameter output like printing and cleaning
    """
    def __init__(self, parameters, duplicate_keys):

        # open default .mdp and fill in the "other parameters"
        # discard all non-default parameters
        self.parameters = provide.default_parameter_block()
        for key in self.parameters.keys():
            if key in parameters.keys():
                self.parameters[key] = parameters[key]

        self.duplicate_keys = duplicate_keys
        self.modified_keys = parameters.keys()

    def keep_only_modified(self):
        """ Remove all parameters that have not been modified """

        keys_to_pop = [
            key for key in self.parameters.keys()
            if key not in self.modified_keys
        ]
        for key in keys_to_pop:
            self.parameters.pop(key)

    def as_string(self):
        """ write the parameters as a string in .mdp format"""

        if not self.parameters:
            return ""

        modifed_key_style = "bold"

        max_key_length = max(map(len, self.parameters.keys()))

        formatted_mdp_entries = [
            f'[{modifed_key_style}]{key:{max_key_length}s} = '
            f'{value}[/{modifed_key_style}]'
            if key in self.modified_keys else
            f'{key:{max_key_length}s} = {value}'
            for key, value in self.parameters.items()
        ]

        return '\n'.join(formatted_mdp_entries) + "\n"
