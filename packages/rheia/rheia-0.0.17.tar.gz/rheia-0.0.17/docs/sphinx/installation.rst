.. _installationlabel:

Installation
============

RHEIA in its entirety is a Python package. The following sections provide information on how to install Python, followed by the installation guide of RHEIA
and the package dependencies for performing deterministic design optimization, robust design optimization and uncertainty quantification.

Installing Python
-----------------

Python can be installed in several ways on your system. If the distribution platform is no constraint,
we recommend installing Python via the `Anaconda Python distribution <https://www.anaconda.com/products/individual>`_, as it includes 
the installation of many common packages in data science (and used in RHEIA), such as NumPy and SciPy.

Installing RHEIA
----------------

RHEIA is available on PyPi, and can be downloaded via the `pip <https://pip.pypa.io/en/stable/>`_ package manager.
The following command installs the most recent version of RHEIA and the package dependencies::

	pip install rheia
	
Specific from a Jupyter Kernel::

	import sys
	!{sys.executable} -m pip install rheia
	
After installation, the package should be installed in the native :file:`rheia` folder under the default :file:`site-packages` folder,
e.g. :file:`C:\\Users\\...\\anaconda3\\Lib\\site-packages\\rheia`.
From this directory, rheia's unit tests can be conveniently performed using ``pytest``.

Package dependencies
--------------------

The RHEIA features require the installation of several packages.

To evaluate the hydrogen-based energy system models:

- Included in Anaconda native installation:
   - Matplotlib
   - NumPy
   - Pandas 
- Other packages:
   - pvlib
   
To perform uncertainty quantification:

- Included in Anaconda native installation:
   - NumPy
   - SciPy
- Other packages:
   - pyDOE
   - SobolSequence

To perform deterministic design optimization:

- Included in Anaconda native installation:
   - NumPy
- Other packages:
   - pyDOE
   - DEAP

To perform robust design optimization:

- Included in Anaconda native installation:
   - NumPy
   - SciPy
- Other packages:
   - pyDOE
   - SobolSequence
   - DEAP

In case Anaconda is used, keep in mind that the packages excluded from the Anaconda native installation can be installed in the activated Anaconda environment either by the conda library or through the classic pip library.

Import what you need
--------------------

RHEIA allows to import the specific tool you need. To run deterministic or robust design optimization::

	import rheia.OPT.optimization as rheia_opt

To perform uncertainty quantification::

	import rheia.UQ.uncertainty_quantification as rheia_uq

To post-process the results::

    import rheia.POST_PROCESS.post_process as rheia_pp
