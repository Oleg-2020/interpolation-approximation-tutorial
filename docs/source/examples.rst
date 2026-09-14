Examples
========

This page provides links to the Jupyter notebook examples included in the project.

Jupyter Notebooks
-----------------

Interactive examples demonstrating all features:

1. **01_data_loading.ipynb** - Data Loading and Preprocessing
   
   - Generating synthetic data from mathematical functions
   - Visualizing raw data
   - Detecting and removing outliers
   - Normalizing data using different methods

2. **02_interpolation.ipynb** - Interpolation Methods
   
   - Linear interpolation
   - Cubic spline interpolation
   - Polynomial interpolation
   - Comparison of different methods

3. **03_approximation.ipynb** - Function Approximation
   
   - Approximation with Chebyshev basis (optimal)
   - Approximation with Legendre basis (orthogonal)
   - Approximation with power basis (simple)
   - Convergence analysis with increasing polynomial degree
   - Error comparison across basis types

4. **04_latex_export.ipynb** - LaTeX Report Generation
   
   - Complete workflow: data → approximation → analysis → report
   - Creating professional LaTeX documents
   - Adding tables, figures, and mathematical equations
   - Generating PDF-ready technical reports

Running the Examples
---------------------

First, install Jupyter::

    pip install jupyter

Then navigate to the examples directory and start the notebook server::

    cd examples
    jupyter notebook

Open any of the notebooks above to run the interactive examples.

Key Learning Outcomes
----------------------

By working through these examples, you will learn:

- How to structure and organize mathematical Python packages
- Best practices for data preprocessing and validation
- Different interpolation and approximation techniques
- How to analyze and interpret numerical errors
- Automatic generation of professional documentation
- Integration of computation, visualization, and reporting

Tips
----

- Each notebook is self-contained and can be run independently
- Modify the parameters to see how results change
- Use the interactive visualizations to build intuition
- Adapt the code for your own projects
