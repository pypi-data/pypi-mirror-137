"""Data initializations, getter, setter methods"""

from symmathSBML.reaction import Reaction
from symmathSBML.function_definition import FunctionDefinition
import symmathSBML.sympy_util as su
from symmathSBML import util
from symmathSBML.make_roadrunner import makeRoadrunner

import collections
import libsbml
import tellurium as te


ANT = "ant"
XML = "xml"
TIME = "time"


TYPE_MODEL = "type_model"  # libsbml model
TYPE_XML = "type_xml"  # XML string
TYPE_ANTIMONY = "type_xml"  # Antimony string
TYPE_FILE = "type_file" # File reference

# filename: name of file processed
# number: index of item
# model: libsbml.Model
IteratorItem = collections.namedtuple('IteratorItem',
    'filename number model')
# nme: str name
# sym: sympy.Symbol
# rr: value in roadrunner
SymbolInfo = collections.namedtuple("SymbolInfo", "nme sym rr")


class SymmathBase(object):

    def __init__(self, model_reference):
        """
        Initializes instance variables
        :param str model_reference: string or SBML file or Roadrunner object
        """
        ##### PUBLIC #####
        self.model_reference = model_reference
        self.model = None  # libsbml object
        self.reactions = []  # Python wrapper for Reaction
        self.species = []  # libsbml Species
        self.roadrunner = None  # Roadrunner object
        self.namespace_dct = {}  # Namespae of symbols added
        self.roadrunner = makeRoadrunner(model_reference)
        # Construct the libsbml document
        xml_model_reference = self.roadrunner.getSBML()
        xml = util.getXML(xml_model_reference)
        reader = libsbml.SBMLReader()
        document = reader.readSBMLFromString(xml)
        util.checkSBMLDocument(document, model_reference=model_reference)
        self.model = document.getModel()
        # Other public
        self.antimony = self.roadrunner.getAntimony()
        self.species = [self.model.getSpecies(nn)
            for nn in range(self.model.getNumSpecies())]
        self.species_names = [s.id for s in self.species]
        self.parameters = [self.model.getParameter(nn)
            for nn in range(self.model.getNumParameters())]
        self.parameter_names = [p.id for p in self.parameters]
        self.function_definitions = self.getFunctionDefinitions()
        self.reactions = [Reaction(self.model.getReaction(nn),
            function_definitions=self.function_definitions)
            for nn in range(self.model.getNumReactions())]
        self._populateNamespace()

    def _getRoadrunnerDct(self):
        """
        Returns
        -------
        dict
            Dictionary of name, value pairs in Roadrunner
        """
        dct = self._getParameterValuelDct()
        dct.update(self._getSpeciesValuelDct())
        return dct

    def get(self, names):
        """
        Provides the SymbolInfo for the name.

        Parameters
        ----------
        name: str/list-str

        Returns
        -------
        SymbolInfo/list-SymbolInfo
        """
        if isinstance(names, str):
            return self._getSymbolInfo(names)
        symbol_infos = []
        for name in names:
            symbol_infos.append(self._getSymbolInfo(name))
        return symbol_infos

    def _getSymbolInfo(self, name):
        """
        Provides the SymbolInfo for the name. A 0 is returned
        if the name is not in self.namespace or self.roadrunner.

        Parameters
        ----------
        name: str

        Returns
        -------
        SymbolInfo
        """
        if not name in self.roadrunner.keys():
            rr_value = 0
        else:
            rr_value = self.roadrunner[name]
        if name in self.namespace_dct.keys():
            symbol = self.namespace_dct[name]
        else:
            symbol = None
        return SymbolInfo(nme=name, rr=rr_value, sym=symbol)

    def set(self, dct):
        """
        Sets the values of names and values.

        Parameters
        ----------
        dct: dict
            key: str (name)
            value: object (value)
        """
        for name, value in dct.items():
            if not name in self.roadrunner.keys():
                raise ValueError("%s is not known to this roadrunner instance."
                      % name)
            self.roadrunner[name] = value

    def _getParameterSymbolDct(self):
        """
        Returns
        -------
        dict
            key: symbol (parameter)
            value: value in self.roadrunner
        """
        return {self.namespace_dct[p]:
              self.roadrunner[p] for p in self.parameter_names}

    def _getParameterValuelDct(self):
        """
        Returns
        -------
        dict
            key: str (parameter)
            value: value in self.roadrunner
        """
        return {p: self.roadrunner[p] for p in self.parameter_names}

    def _getSpeciesSymbolDct(self):
        """
        Returns
        -------
        dict
            key: symbol (species)
            value: value in self.roadrunner
        """
        return {self.namespace_dct[s]:
              self.roadrunner[s] for s in self.species_names}

    def _getSpeciesValuelDct(self):
        """
        Returns
        -------
        dict
            key: str (species)
            value: value in self.roadrunner
        """
        return {s: self.roadrunner[s] for s in self.species_names}

    def getFunctionDefinitions(self):
        """
        Returns all function definitions in the model.py

        Returns
        -------
        list-libsbml.FunctionDefinition
        """
        sbml_definitions =[self.model.getFunctionDefinition(n) for n
            in range(self.model.getNumFunctionDefinitions())]
        function_definitions = [FunctionDefinition(s) for s in sbml_definitions]
        # Include the builtin functions
        function_definitions.extend(FunctionDefinition.makeBuiltinFunctions())
        return function_definitions

    def getReaction(self, an_id):
        """
        Finds a reaction with the specified id.
        :param str an_id: id for the reaction
        :return Reaction/None:
        """
        return self._getInstance(self.reactions, an_id)

    def getSpecies(self, an_id):
        """
        Finds and returns the species with given name
        :param str an_id:
        Return None if there is no such species.
        """
        return self._getInstance(self.species, an_id)

    def getParameter(self, an_id):
        """
        Finds and returns the Parameter with given name
        :param str an_id:
        Return None if there is no such parameter.
        """
        return self._getInstance(self.parameters, an_id)

    def _getInstance(self, a_list, an_id):
        """
        Finds and returns the species with given name
        Return None if there is no such molecules
        :param str id:
        """
        results = [e for e in a_list if e.getId() == an_id]
        if len(results) > 1:
          raise ValueError(
              "Two instances have the same id: %s" %
              id)
        if len(results) == 0:
          return None
        return results[0]

    def _populateNamespace(self):
        """
        Populates the namespace with sympy symbols
        from roadrunner species and parameters.
        """
        names = list(self.parameter_names)
        species_names = list(self.species_names)
        names.extend(species_names)
        for reaction in self.reactions:
            name = reaction.id
            if name[0] == "_":
                name = name[1:]
            reaction.id = name
        reaction_names = [r.id for r in self.reactions]
        names.extend(reaction_names)
        names.extend(self.roadrunner.getCompartmentIds())
        nameStr = " ".join(names)
        su.addSymbols(nameStr, dct=self.namespace_dct)
