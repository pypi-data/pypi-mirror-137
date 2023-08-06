*****
Usage
*****

Who is this for
===============

This particular package is most likely to be useful for people either
developing algorithms for techniques for KEPs, or setting kep_solver for use
within an organisation with specific requirements. A sample web interface is
viewable at https://kep-web.optimalmatching.com, and the code for said
interface is at https://gitlab.com/wpettersson/kep_web.

Installing
==========

This package is available via pip, and requires Python 3.9 at least. To install
it, I recommend using a Python virtual environment (see `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ for an easy-to-use introduction) and then running ``pip install kep_solver``

Reading and inspecting instances
================================

File IO functionality is available in the :doc:`kep_solver.fileio` module. The
following code should read in any supported file format.
::

    from kep_solver.fileio import read_file
    instance = read_file("instance.json")

Instances can be analysed for a number of properties, as can the Donor and
Recipient entities they contain. These are documented in :doc:`kep_solver.entities`
::

    print(f"This instance has {len(instance.recipients())} recipients")
