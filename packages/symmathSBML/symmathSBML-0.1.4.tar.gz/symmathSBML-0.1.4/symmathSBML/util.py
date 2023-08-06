"""Commonly used utilities."""

import os

TYPE_ANTIMONY = "type_antimony"
TYPE_XML = "type_xml"
TYPE_FILENAME = "type_filename"
XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>'
DEFAULT_MSG = "An error occurred in an input file."

def getXML(model_reference):
      """
      :param str model_reference:
          the input may be a file reference or a model string
          or TextIOWrapper
              and the file may be an xml file or an antimony file.
          if it is a model string, it may be an xml string or antimony.
      :raises IOError: Error encountered reading the SBML document
      :return str SBML xml"
      """
      # Check for a file path
      model_str = ""
      if isinstance(model_reference, str):
        if os.path.isfile(model_reference):
          with open(model_reference, 'r') as fd:
            lines = fd.readlines()
          model_str = ''.join(lines)
      if len(model_str) == 0:
        if "readlines" in dir(model_reference):
          lines = model_reference.readlines()
          if isinstance(lines[0], bytes):
            lines = [l.decode("utf-8") for l in lines]
          model_str = ''.join(lines)
          model_reference.close()
        else:
          # Must be a string representation of a model
          model_str = model_reference
      # Process model_str into a model
      if not "<sbml" in model_str:
        # Antimony
        raise ValueError("Invalid SBML model.")
      return model_str

def checkSBMLDocument(document, model_reference=""):
      if document.getNumErrors() > 0:
        raise ValueError("Errors in SBML document\n%s"
            % model_reference)

def tokenize(text, tokens):
    """
    Creates a list of strings separated by tokens.

    Parameters
    ----------
    text: str
    tokens: list-char

    Returns
    -------
    list-str
    """
    result = []
    start_pos = 0
    end_pos = 0
    for pos, char in enumerate(text):
        if char in tokens:
            result.append(text[start_pos:end_pos])
            result.append(char)
            start_pos = pos + 1
        end_pos = pos + 1
    if start_pos < len(text):
        result.append(text[start_pos:end_pos])
    return result

def detokenize(tokenizeds):
    """
    Creates a string from the tokenized list.

    Parameters
    ----------
    list-str

    Returns
    -------
    str
    """
    return "".join(tokenizeds)
