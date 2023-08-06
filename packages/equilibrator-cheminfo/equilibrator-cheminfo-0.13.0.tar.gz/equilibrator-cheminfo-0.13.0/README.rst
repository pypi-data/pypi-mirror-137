=============================
eQuilibrator Cheminformatics
=============================

.. image:: https://img.shields.io/pypi/v/equilibrator-cheminfo.svg
   :target: https://pypi.org/project/equilibrator-cheminfo/
   :alt: Current PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/equilibrator-cheminfo.svg
   :target: https://pypi.org/project/equilibrator-cheminfo/
   :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/equilibrator-cheminfo.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0
   :alt: Apache Software License Version 2.0

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code Style Black

.. summary-start

Light adapter classes around Open Babel, RDKit, and ChemAxon for the
functionality needed in eQulibrator.

Install
=======

Please note that while ``equilibrator-cheminfo`` as a pure Python package is
operating system independent, the same is not true for the cheminformatics
backends Open Babel, RDkit, or ChemAxon. While both Open Babel and RDKit
nowadays provide Python wheels, we do not test them on all platforms.

RDKit
-----

.. code-block:: console

    pip install equilibrator-cheminfo[rdkit]

or

Open Babel
----------

.. code-block:: console

    pip install equilibrator-cheminfo[openbabel]

ChemAxon
--------

If you wish to use ChemAxon, you need to install the software, acquire a
license, and set the environment variable ``CHEMAXON_HOME``.

.. code-block:: console

    pip install equilibrator-cheminfo[chemaxon]

Usage
=====

The main feature in this package is a uniform class interface to molecules from
Open Babel, RDKit, or ChemAxon.  The interface is defined by the
``equilibrator_cheminfo.AbstractMolecule`` abstract class that the three
concrete classes adhere to.

.. code-block:: python

    from equilibrator_cheminfo.chemaxon import ChemAxonMolecule
    from equilibrator_cheminfo.rdkit import RDKitMolecule
    from equilibrator_cheminfo.openbabel import OpenBabelMolecule

Some of the supported methods are:

.. code-block:: python

    mol = OpenBabelMolecule.from_smiles("CC=O")
    mol.get_charge()  # 0
    mol.get_molecular_formula()  # 'C2H4O'
    mol.get_molecular_mass()  # 44.05
    mol.get_inchi_key()  # 'IKHGUXGNUITLKF-UHFFFAOYSA-N'

You can also always access the cheminformatics backend object directly and pass
it as an argument to functions directly imported from there.

.. code-block:: python

    mol.native  # <openbabel.pybel.Molecule at 0x7f2a14b36c70>
    mol.native.calcfp().bits  # [330, 624, 671]

If there are general methods that you think are missing from the abstract
interface, please say so in an `issue
<https://gitlab.com/equilibrator/equilibrator-cheminfo/-/issues/new>`_.

Copyright
=========

* Copyright © 2021, Moritz E. Beber.
* Free software distributed under the `Apache Software License 2.0
  <https://www.apache.org/licenses/LICENSE-2.0>`_.

.. summary-end
