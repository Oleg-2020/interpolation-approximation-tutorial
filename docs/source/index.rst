MathDoc Documentation
=====================

Welcome to the MathDoc documentation! This project demonstrates best practices for documenting mathematical packages with LaTeX integration.

**MathDoc** provides a comprehensive toolkit for:

- Data loading and preprocessing
- Interpolation using various methods
- Function approximation with orthogonal bases
- Error analysis and visualization
- Automatic LaTeX report generation

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorial
   api_reference
   examples
   integration_guide

Quick Start
-----------

Install the package::

    pip install -e .

Basic usage example::

    from mathdoc import DataLoader, Interpolator, Approximator
    
    # Load data
    loader = DataLoader()
    x, y = loader.load_synthetic(n_points=50, noise=0.05)
    
    # Interpolate
    interp = Interpolator(x, y)
    y_smooth = interp.cubic_spline(n_points=200)
    
    # Approximate
    approx = Approximator(x, y, basis_type='chebyshev', degree=8)
    coeffs = approx.fit()
    y_approx = approx.evaluate(x)

Features
--------

✅ **Data Loading** – Load, validate, and preprocess data  
✅ **Interpolation** – Linear, spline, and polynomial methods  
✅ **Approximation** – Chebyshev, Legendre, and power bases  
✅ **Error Analysis** – Compute various error metrics  
✅ **Visualization** – Publication-ready plots  
✅ **LaTeX Export** – Automatic report generation  

Project Structure
-----------------

::

    mathdoc/
    ├── data_loader.py        # Data import & preprocessing
    ├── interpolation.py      # Interpolation methods
    ├── approximation.py      # Function approximation
    ├── basis_functions.py    # Orthogonal polynomial bases
    ├── visualization.py      # Plotting utilities
    ├── error_analysis.py     # Error metrics
    └── latex_formatter.py    # LaTeX report generation

Contents
--------

.. toctree::
   :hidden:

   api_reference
   tutorial
   examples
   integration_guide

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
