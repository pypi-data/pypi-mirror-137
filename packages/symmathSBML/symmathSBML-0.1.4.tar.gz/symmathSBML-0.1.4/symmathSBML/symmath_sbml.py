"""
Symbolic representation of an SBML model

Provides:
* symbolic state equations: system
   index: symbol
   value: expression for derivative
* symbolic jacobian of state equations
   index: symbol1
   column: symbol2
   value: expression d symbol1/d symbol2

Key methods:
* substatitue method provides for substituting symbols with roadrunner values
  (e.g., values of parameters in roadrunner or values of species in roadrunner)
  or user designated values.
* get provides the symbol and value information for a name (ID in libsbml)
* set changes the value information for a name (ID in libsbml)

Key properties:
* system is a Series of the system equations. The index is the variable,
  and the value is the expression.
* jacobian is a DataFrame for the Jacobian. Indexes are the variable whose
  expression is being differentiated and columns are the variables in the
  denominator of the differential
* roadrunner is the RoadRunner instance. Running simulations changes
  the values of variables that are substituted.
* namespace_dct is a dictionary with the namespace in which roadrunner
  variables are defined as symbols.
"""

"""
TO DO:
0. Update README with use case.
.1 Get Jin to change a file so she has commit history
1. Create package
"""

from symmathSBML.symmath_base import SymmathBase
from symmathSBML import msgs
from symmathSBML.persister import Persister

import collections
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sympy
import seaborn as sns
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


class SymmathSBML(SymmathBase):

    def __init__(self, model_reference):
        """
        Initializes instance variables
        :param str model_reference: string or SBML file or Roadrunner object
        """
        def mkAntimonyStr():
            try:
                self.roadrunner = te.loada(model_reference)
                xml_model_reference = self.roadrunner.getSBML()
                return xml_model_reference
            except:
                raise ValueError("Invalid model reference")
        ##### PUBLIC #####
        super(SymmathSBML, self).__init__(model_reference)
        self.system, self.jacobian = self.mkSymbolSystem()

    def copy(self):
        """
        Creates a copy of the object.
        
        Returns
        -------
        symmathSBML
        """
        new_symmath = SymmathSBML(self.antimony)
        new_symmath.model_reference = self.model_reference
        # Adjust the simulation time
        new_symmath.roadrunner.reset()
        _ = new_symmath.roadrunner.simulate(0, self.roadrunner.model.getTime())
        # Save the content of the roadrunner instance
        dct = self._getRoadrunnerDct()
        new_symmath.set(dct)
        #
        return new_symmath

    def serialize(self, path):
        """
        Serializes the current object to a file.

        Parameters
        ----------
        path: str
            Path to serialization file
        """
        persister = Persister(path)
        time = self.roadrunner.model.getTime()
        roadrunner_dct = self._getRoadrunnerDct()
        items = [self.antimony, roadrunner_dct, time]
        persister.set(items)

    @classmethod
    def deserialize(cls, path):
        """
        Creates a SymmathSBML object from a file serialization.

        Parameters
        ----------
        path: str
            Path to serialization file
        
        Returns
        -------
        SymmathSBML
        """
        persister = Persister(path)
        [antimony, roadrunner_dct, time] = persister.get()
        symmath = cls(antimony)
        symmath.roadrunner.reset()
        _ = symmath.roadrunner.simulate(0, time)
        symmath.set(roadrunner_dct)
        return symmath

    def equals(self, other):
        """
        Checks that they have the same information

        Parameters
        ----------
        other: SymmathSBML
        
        Returns
        -------
        bool
        """
        val_bool = self.antimony == other.antimony
        val_bool = val_bool and all([s1.id == s2.id for s1, s2 in
              zip(self.species, other.species)])
        val_bool = val_bool and all([s1 == s2 for s1, s2 in
              zip(self.species_names, other.species_names)])
        val_bool = val_bool and all([p1.id == p2.id for p1, p2 in
              zip(self.parameters, other.parameters)])
        val_bool = val_bool and all([p1 == p2 for p1, p2 in
              zip(self.parameter_names, other.parameter_names)])
        val_bool = val_bool and all([r1.id == r2.id for r1, r2 in
              zip(self.reactions, other.reactions)])
        val_bool = val_bool and self.system.equals(other.system)
        val_bool = val_bool and self.jacobian.equals(other.jacobian)
        # Compare roadrunner values
        val_bool = val_bool and np.isclose(
               self.roadrunner.model.getTime(), other.roadrunner.model.getTime())
        dct = self._getParameterValuelDct()
        dct.update(self._getSpeciesValuelDct())
        for name, value in dct.items():
            val_bool = val_bool and np.isclose(other.roadrunner[name], value)
        return val_bool
     
    def substitute(self, dct=None, is_parameters=True, is_species=True):
        """
        Substitutes the state equation and jacobian
   
        Parameters
        ----------
        dct: dict
            Dictionary for substituting symbol values
            key: symbol
            value: symbol/expression/number
            default: substitute all species and parameters
        is_parameters: bool
            substitute all parameters
        is_species: bool
            substitute all species
        """
        def convert(value):
            if "is_symbol" in dir(value):
                new_value = value.subs(new_dct).simplify()
                if new_value.is_number:
                    new_value = float(new_value)
            else:
                new_value = float(value)
            return new_value
        #
        if dct is None:
            dct = {}
        new_dct = dict(dct)
        if is_parameters:
            new_dct.update(self._getParameterSymbolDct())
        if is_species:
            new_dct.update(self._getSpeciesSymbolDct())
        self.system = self.system.apply(convert)
        self.jacobian = self.jacobian.applymap(convert)

    def mkSymbolSystem(self):
        """
        Creates an ODEModel.
    
        Returns
        -------
        system, jacobian
        """
        def evaluate(reaction):
            return eval(reaction.kinetic_law.expanded_formula, namespace_dct)
        # Create sympy expressions for kinetic laws
        reaction_epr_dct = {}
        namespace_dct = dict(self.namespace_dct)  # Don't modify namespace
        for reaction in self.reactions:
            key = namespace_dct[reaction.id]
            for _ in range(5):  # Number of attempts to resolve names
                is_done = False
                try:
                    value = evaluate(reaction)
                    is_done = True
                except NameError as err:
                    parts = str(err).split(" ")
                    name = parts[1].replace("'", "")
                    namespace_dct[name] = sympy.Symbol(name)
                    # Keept this in the namespace
                    self.namespace_dct[name] = namespace_dct[name]
                    msg = "Name %s undefined in reaction %s. Set to 0."  \
                          % (name, str(reaction))
                    msgs.warn(msg)
                if is_done:
                    break
            reaction_epr_dct[key] = value
        # Express species fluxes in terms of reaction fluxes
        reaction_vec = sympy.Matrix(list(reaction_epr_dct.keys()))
        # Ensure we get all boundary species in the stoichiometrymatrix
        boundary_species = self.roadrunner.getBoundarySpeciesIds()
        for name in boundary_species:
            self.roadrunner.setBoundary(name, False)
        try:
            stoichiometry_mat = np.array(
                  self.roadrunner.getFullStoichiometryMatrix())
        except Exception:
            msgs.warn("Stoichiometery matrix does not exist.")
            stoichiometry_mat = None
        if stoichiometry_mat is None:
            return None, None
        species_reaction_vec = stoichiometry_mat * reaction_vec
        species_reaction_dct = {self.namespace_dct[s]: 
              e for s, e in zip(self.species_names, species_reaction_vec)}
        system_dct = {s: sympy.simplify(
              species_reaction_dct[s].subs(reaction_epr_dct))
            for s in species_reaction_dct.keys()}
        system_dct = {s: 0 if str(s) in boundary_species else v
              for s, v in system_dct.items()}
        system = pd.Series(system_dct.values(), index=system_dct.keys())
        variables = list(system.index)
        jac_dct = {v: [] for v in variables}
        for var1 in variables:
            epr = system.loc[var1]
            for var2 in variables:
                jac_dct[var2].append(sympy.diff(epr, var2))
        jacobian = pd.DataFrame(jac_dct, index=variables)
        #
        return system, jacobian

    def calculateJacobianSensitivity(self, is_normalized=True):
        """
        Calculates the sensitivity of the species (state) variable w.r.t. all
        other species by summing derivatives and evaluating at the current
        value of the state vector.

        Parameters
        ----------
        is_normalized: bool
            divide by the value
        
        Returns
        -------
        DataFrame
            columns: species column in Jacobian
            index: species used in derivative denominator
            values: sympy expression
        """
        # Initializations
        symbols = list(self.jacobian.index)
        dct = {s: [] for s in symbols}
        # Construct substitution dictionary
        subs_dct = self._getParameterSymbolDct()
        subs_dct.update(self._getSpeciesSymbolDct())
        # Take derivatives
        for s1 in symbols: # Row
            s1_arr = np.array(self.jacobian[s1])
            row_epr = s1_arr.dot(self.getSpeciesArray())
            row_value = row_epr.subs(subs_dct)
            if row_value == 0:
                row_value = 10e5
            for s2 in symbols:  # Columns
                deriv = sympy.diff(row_epr, s2).subs(subs_dct)
                if is_normalized:
                    deriv = deriv/row_value
                if deriv.is_number:
                    deriv = float(deriv)
                dct[s1].append(deriv)
        # Return the result
        df = pd.DataFrame(dct, index=symbols, columns=symbols)
        return df
            
    def getSpeciesArray(self):
        return np.array([self.get(s).rr for s in self.species_names])

    def plotJacobianSensitivityHeatmap(self, title="", is_plot=True,
          vmin=None, vmax=None):
        """
        Plots a heatmap of the derivative of each row in the Jacobain
        multiplied by the current value of the state vector.

        Parameters
        ----------
        title: str
        """
        df = self.calculateJacobianSensitivity()
        max_val = max([np.abs(v) for v in df.values.flatten()])
        if vmin is None:
            vmin = -max_val
        if vmax is None:
            vmax = max_val
        columns = list(df.columns)
        columns.reverse()
        df_new = df.iloc[::-1]
        sns.heatmap(df_new, cmap="seismic", vmin=vmin, vmax=vmax)
        plt.xlabel("State Evaluated")
        plt.ylabel("Derivative w.r.t. State")
        plt.title(title)
        if is_plot:
            plt.show()
