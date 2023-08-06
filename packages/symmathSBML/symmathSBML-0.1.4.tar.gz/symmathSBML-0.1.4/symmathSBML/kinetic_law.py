'''Provides Information on SBML Kinetics Laws'''


from symmathSBML import constants as cn
from symmathSBML import util
from symmathSBML import exceptions
from symmathSBML import msgs

import collections
import numpy as np
import re

MAX_RECURSION = 5
# Tokens used in mathematical expressions of SBML function definitions
TOKENS = [" ", "(", ")", "/", "-", "*", "+", ","]


class KineticLaw(object):

  def __init__(self, libsbml_kinetics, reaction, function_definitions=None):
    """
    :param libsbml.KineticLaw libsbml_kinetics:
    :param function_definitions list-FunctionDefinition:
    """
    self.reaction = reaction
    # libsbml object for kinetics
    self.libsbml_kinetics = libsbml_kinetics
    # String version of chemical formula
    self.formula = self.libsbml_kinetics.getFormula()
    # Parameters and chemical species
    self.symbols = self._getSymbols()
    # Reaction for the kinetics law
    self.reaction = reaction
    # Expanded kinetic formula (remove embedded functions)
    if function_definitions is None:
      self.expanded_formula = None
    else:
      self.expandFormula(function_definitions)
    self.expression_formula = None  # valid symPy expression string

  def __repr__(self):
    return self.formula

  def expandFormula(self, function_definitions):
    """
    Expands the kinetics formula, replacing function definitions
    with their body.

    Parameters
    ----------
    function_definitions: list-FunctionDefinition
    """
    self.expanded_formula = self._expandFormula(
        self.formula, function_definitions)

  def mkSymbolExpression(self, function_definitions):
    """
    Creates a string that can be processed by sympy.
    
    Parameters
    -------
    function_definitions: list-FunctionDefinition
    
    Returns
    -------
    str
    """
    if self.expanded_formula is None:
      self.expandFormula(function_definitions)
    self.expression_formula = str(self.expanded_formula)
    self.expression_formual.replace('^','**')

  @staticmethod
  def _expandFormula(expansion, function_definitions,
          num_recursion=0):
      """
      Expands the kinetics formula, replacing function definitions
      with their body.
  
      Parameters
      ----------
      expansion: str
          expansion of the kinetic law
      function_definitions: list-FunctionDefinition
      num_recursion: int
      
      Returns
      -------
      str
      """
      if num_recursion > MAX_RECURSION:
          return expansion
      done = True
      for fd in function_definitions:
          # Find the function calls
          calls = re.findall(r'{}\(.*?\)'.format(fd.id), expansion)
          if len(calls) == 0:
            continue
          done = False
          for call in calls:
            # Find argument call. Ex: '(a, b)'
            call_arguments = re.findall(r'\(.*?\)', call)[0]
            call_arguments = call_arguments.strip()
            call_arguments = call_arguments[1:-1]  # Eliminate parentheses
            arguments = call_arguments.split(',')
            arguments = [a.strip() for a in arguments]
            body = str(fd.body)
            tokenized_body = util.tokenize(body, TOKENS)
            for pos, token in enumerate(tokenized_body):
                # Need a bit of sophistication with replacing arguments to
                # avoid problems with substrings
                for formal_arg, call_arg in zip(fd.argument_names, arguments):
                    if token == formal_arg:
                        tokenized_body[pos] = call_arg
                        # Don't replace a replaced string
                        break   
            new_body = util.detokenize(tokenized_body)
            expansion = expansion.replace(call, new_body)
      if not done:
          return KineticLaw._expandFormula(expansion, function_definitions,
              num_recursion=num_recursion+1)
      return expansion
 

  def _getSymbols(self):
    """
    Finds the parameters and species names for the
    kinetics law. Exposing this information requires
    a recursive search of the parse tree for the
    kinetics expression.
    :return list-str:
    """
    global cur_depth
    MAX_DEPTH = 20
    cur_depth = 0
    def augment(ast_node, result):
      global cur_depth
      cur_depth += 1
      if cur_depth > MAX_DEPTH:
        raise exceptions.BadKineticsMath(str(self.reaction))
      for idx in range(ast_node.getNumChildren()):
        child_node = ast_node.getChild(idx)
        if child_node.getName() is None:
          additions = augment(child_node, result)
          result.extend(additions)
        else:
          if child_node.isFunction():
            additions = augment(child_node, result)
            result.extend(additions)
          else:
            result.append(child_node.getName())
      return result

    ast_node = self.libsbml_kinetics.getMath()
    if ast_node.getName() is None:
      result = []
    else:
      result = [ast_node.getName()]
    return augment(ast_node, result)
