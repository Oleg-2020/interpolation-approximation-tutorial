Integration Guide
==================

This guide explains how different modules of MathDoc work together and how to integrate them into your own projects.

Module Dependencies
-------------------

The MathDoc package is organized as follows:

.. code-block:: text

    DataLoader
        ↓
    Interpolator / Approximator
        ↓
    ErrorAnalyzer
        ↓
    Visualizer / LatexReport

**DataLoader** is typically the starting point, preparing data for downstream processing.

**Interpolator** and **Approximator** are independent and can be used based on your needs.

**ErrorAnalyzer** consumes results from interpolation/approximation.

**Visualizer** and **LatexReport** consume results from error analysis.

Common Workflows
----------------

Data Cleaning Workflow
~~~~~~~~~~~~~~~~~~~~~~

When working with noisy data:

.. code-block:: python

    from mathdoc import DataLoader
    
    loader = DataLoader()
    
    # Load from file or source
    x, y = load_your_data()  # your custom loader
    
    # Remove outliers
    x_clean, y_clean = loader.remove_outliers(x, y, threshold=2.0)
    
    # Normalize if needed
    y_norm = loader.normalize(y_clean, method='minmax')

Interpolation Workflow
~~~~~~~~~~~~~~~~~~~~~~

For smooth curve fitting:

.. code-block:: python

    from mathdoc import Interpolator, Visualizer
    
    # Create interpolator
    interp = Interpolator(x, y)
    
    # Generate smooth curve
    x_dense = np.linspace(x.min(), x.max(), 1000)
    y_smooth = interp.cubic_spline(x_new=x_dense)
    
    # Visualize
    viz = Visualizer()
    viz.plot_interpolation(x, y, x_dense, y_smooth)

Approximation with Analysis Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For fitting and error analysis:

.. code-block:: python

    from mathdoc import Approximator, ErrorAnalyzer
    
    # Fit model
    approx = Approximator(x, y, basis_type='chebyshev', degree=8)
    coeffs = approx.fit()
    
    # Evaluate
    y_approx = approx.evaluate(x)
    
    # Analyze errors
    analyzer = ErrorAnalyzer(y, y_approx)
    summary = analyzer.summary(y_approx)
    print(f"L2 Error: {summary['l2_norm']:.6e}")
    print(f"Max Error: {summary['l_inf_norm']:.6e}")

Convergence Study Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~

For studying convergence with polynomial degree:

.. code-block:: python

    from mathdoc import Approximator, ErrorAnalyzer, Visualizer
    
    degrees = range(1, 20)
    errors = []
    
    for d in degrees:
        approx = Approximator(x, y, basis_type='chebyshev', degree=d)
        approx.fit()
        y_app = approx.evaluate(x)
        
        analyzer = ErrorAnalyzer(y, y_app)
        errors.append(analyzer.l2_norm(y_app))
    
    # Visualize convergence
    viz = Visualizer()
    viz.plot_convergence(list(degrees), errors, filename="conv.png")

Full Report Generation Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Complete pipeline with documentation:

.. code-block:: python

    from mathdoc import (
        DataLoader, Approximator, ErrorAnalyzer,
        Visualizer, LatexReport
    )
    
    # 1. Prepare data
    loader = DataLoader(random_seed=42)
    x, y = loader.load_synthetic(n_points=100, noise=0.05)
    
    # 2. Fit approximation
    approx = Approximator(x, y, basis_type='chebyshev', degree=10)
    approx.fit()
    y_approx = approx.evaluate(x)
    
    # 3. Analyze
    analyzer = ErrorAnalyzer(y, y_approx)
    errors = analyzer.summary(y_approx)
    
    # 4. Visualize
    viz = Visualizer()
    x_dense = np.linspace(x.min(), x.max(), 500)
    y_dense = approx.evaluate(x_dense)
    viz.plot_approximation(x, y, y_approx, filename="result.png")
    
    # 5. Generate report
    report = LatexReport(title="Approximation Results")
    report.add_section("Analysis")
    report.add_text("Fitting with Chebyshev basis of degree 10.")
    report.add_equation_box('error', f"\\|e\\|_2 = {errors['l2_norm']:.6e}")
    report.add_figure("result.png")
    report.generate("report.tex")

Extending MathDoc
-----------------

Adding Custom Basis Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new basis by subclassing :class:`~mathdoc.BasisFunctions`:

.. code-block:: python

    from mathdoc.basis_functions import BasisFunctions
    import numpy as np
    
    class HermiteBasis(BasisFunctions):
        """Hermite polynomial basis."""
        
        def evaluate(self, n):
            """Evaluate n-th Hermite polynomial."""
            # Your implementation here
            pass
    
    # Use with Approximator
    # (Requires modifying BasisFunctions.create() factory method)

Adding Custom Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extend :class:`~mathdoc.Visualizer` with custom plots:

.. code-block:: python

    from mathdoc import Visualizer
    
    class CustomVisualizer(Visualizer):
        def plot_residuals(self, x, residuals, filename=None):
            """Custom residual plot."""
            # Your plotting code here
            pass

Integration with External Tools
--------------------------------

Using with Pandas
~~~~~~~~~~~~~~~~~

Load data from DataFrames:

.. code-block:: python

    import pandas as pd
    from mathdoc import Interpolator
    
    df = pd.read_csv('data.csv')
    x = df['x'].values
    y = df['y'].values
    
    interp = Interpolator(x, y)
    # ... continue as normal

Using with Scipy
~~~~~~~~~~~~~~~~~

Combine with Scipy optimization:

.. code-block:: python

    from scipy.optimize import minimize
    from mathdoc import Approximator
    
    def objective(params):
        # Custom fitting objective
        pass
    
    # Use Scipy for more complex fitting scenarios
    result = minimize(objective, x0=initial_guess)

Best Practices
---------------

1. **Always validate input data** - Use outlier removal and normalization
2. **Compare multiple methods** - Test different basis functions and degrees
3. **Analyze errors carefully** - Use multiple error metrics
4. **Generate documentation** - Use LatexReport for reproducibility
5. **Test with known functions** - Validate on synthetic data first
6. **Document assumptions** - Clearly state data requirements and limitations

Performance Tips
-----------------

- Use Chebyshev basis for best approximation quality
- Higher degrees don't always mean better results (use convergence studies)
- Normalize data to [-1, 1] for numerical stability
- Cache computed basis functions when evaluating many times
- Use vectorized numpy operations for large datasets
