.. openTEPES documentation master file, created by Andres Ramos

Download
========
The **openTEPES** has been developed using `Python 3.9.7 <https://www.python.org/>`_ and `Pyomo 6.2.0 <https://pyomo.readthedocs.io/en/stable/>`_ and it uses `Gurobi 9.5.0 <https://www.gurobi.com/products/gurobi-optimizer/>`_ as commercial MIP solver for which a free academic license is available.
It uses Pyomo so that it is independent of the preferred solver. You can alternatively use one of the free solvers `SCIP 8.0.0 <https://www.scipopt.org/>`_, `GLPK 5.0 <https://www.gnu.org/software/glpk/>`_
and `CBC 2.10.5 <https://github.com/coin-or/Cbc>`_. List the serial solver interfaces under Pyomo with this call::

  pyomo help -s

Besides, it also requires the following packages:

- `Pandas <https://pandas.pydata.org/>`_ for inputting data and outputting results
- `psutil <https://pypi.org/project/psutil/>`_ for detecting the number of CPUs
- `Matplotlib <https://matplotlib.org/>`_, `Cartopy <https://scitools.org.uk/cartopy/docs/latest/#>`_, `Plotly <https://plotly.com/python/>`_,  `Altair <https://altair-viz.github.io/#>`_, `Colour <https://pypi.org/project/colour/>`_ for plotting results and drawing the network map

Cases
-----
Here, you have the input files of a `small case study of 9 nodes <https://github.com/IIT-EnergySystemModels/openTEPES/tree/master/openTEPES/9n>`_, another one like a `small Spanish system <https://github.com/IIT-EnergySystemModels/openTEPES/tree/master/openTEPES/sSEP>`_ and a `modified RTS24 case study <https://github.com/IIT-EnergySystemModels/openTEPES/tree/master/openTEPES/RTS24>`_.

Code
----

The **openTEPES** code is provided under the `GNU General Public License <https://www.gnu.org/licenses/gpl-3.0.html>`_:

- the code can't become part of a closed-source commercial software product nor can be used for commercial purposes (only for research purposes)
- any future changes and improvements to the code remain free and open

Source code can be downloaded from `GitHub <https://github.com/IIT-EnergySystemModels/openTEPES>`_ or installed with `pip <https://pypi.org/project/openTEPES/>`_

This model is a work in progress and will be updated accordingly. If you want to subscribe to the **openTEPES** model updates send an email to andres.ramos@comillas.edu
