Tutorial
========

This tutorial walks through the main features of MathDoc with practical examples.

Data Loading
------------

The :class:`~mathdoc.DataLoader` class provides utilities for generating synthetic data and preprocessing:

.. code-block:: python

    from mathdoc import DataLoader
    import numpy as np
    
    # Initialize loader with random seed for reproducibility
    loader = DataLoader(random_seed=42)
    
    # Generate synthetic sine data with noise
    x, y = loader.load_synthetic(
        n_points=100,
        noise=0.05,
        function='sine'
    )

Supported functions: ``'sine'``, ``'cosine'``, ``'polynomial'``, ``'exp'``

Outlier Removal
~~~~~~~~~~~~~~~

Remove anomalous points using statistical methods:

.. code-block:: python

    x_clean, y_clean = loader.remove_outliers(
        x, y,
        threshold=2.0  # standard deviations
    )

Data Normalization
~~~~~~~~~~~~~~~~~~~

Normalize to different scales:

.. code-block:: python

    # Min-max normalization to [0, 1]
    y_minmax = loader.normalize(y, method='minmax')
    
    # Z-score normalization (mean=0, std=1)
    y_zscore = loader.normalize(y, method='zscore')

Interpolation
--------------

The :class:`~mathdoc.Interpolator` class constructs smooth curves through data points.

Linear Interpolation
~~~~~~~~~~~~~~~~~~~~

Simple but fast:

.. code-block:: python

    from mathdoc import Interpolator
    
    interp = Interpolator(x, y)
    x_new = np.linspace(x.min(), x.max(), 200)
    y_linear = interp.linear(x_new)

Cubic Spline Interpolation
~~~~~~~~~~~~~~~~~~~~~~~~~~

Smooth and natural-looking:

.. code-block:: python

    # Automatically creates dense evaluation points
    y_spline = interp.cubic_spline(n_points=500)
    
    # Or use custom evaluation points
    y_spline = interp.cubic_spline(x_new=x_new)

Polynomial Interpolation
~~~~~~~~~~~~~~~~~~~~~~~~

High-degree polynomial fit:

.. code-block:: python

    degree = 8
    y_poly = interp.polynomial(degree=degree, x_new=x_new)

Approximation
--------------

The :class:`~mathdoc.Approximator` class finds optimal function fits using least squares.

Chebyshev Basis (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optimal approximation properties:

.. code-block:: python

    from mathdoc import Approximator
    
    approx = Approximator(
        x, y,
        basis_type='chebyshev',
        degree=8
    )
    
    # Fit the model
    coefficients = approx.fit()
    
    # Evaluate at new points
    y_approx = approx.evaluate(x_new)
    
    # Compute errors
    error_norm = approx.error_norm()  # L2 norm
    max_error = approx.max_error()    # L-infinity norm

Legendre Basis
~~~~~~~~~~~~~~

Orthogonal on [-1, 1]:

.. code-block:: python

    approx = Approximator(x, y, basis_type='legendre', degree=8)
    coeffs = approx.fit()

Power Basis
~~~~~~~~~~~

Standard monomials:

.. code-block:: python

    approx = Approximator(x, y, basis_type='power', degree=8)
    coeffs = approx.fit()

Error Analysis
---------------

The :class:`~mathdoc.ErrorAnalyzer` computes various error metrics:

.. code-block:: python

    from mathdoc import ErrorAnalyzer
    
    analyzer = ErrorAnalyzer(y_exact, y_approximate)
    
    # Different error norms
    l2_error = analyzer.l2_norm(y_approx)           # L2 norm
    linf_error = analyzer.l_inf_norm(y_approx)      # Max error
    rel_error = analyzer.relative_error(y_approx)   # Relative L2
    mse = analyzer.mse(y_approx)                    # Mean squared error
    
    # Get all metrics at once
    summary = analyzer.summary(y_approx)
    print(summary)

Visualization
--------------

The :class:`~mathdoc.Visualizer` creates publication-ready plots:

.. code-block:: python

    from mathdoc import Visualizer
    
    viz = Visualizer(figsize=(12, 8))
    
    # Plot interpolation results
    viz.plot_interpolation(
        x, y,           # original data
        x_new, y_smooth,  # interpolated data
        title="Interpolation Results",
        filename="interp.png"
    )
    
    # Plot approximation with error
    viz.plot_approximation(
        x, y, y_approx,
        title="Approximation Results",
        filename="approx.png"
    )
    
    # Convergence analysis
    degrees = [1, 3, 5, 7, 9]
    errors = [0.5, 0.2, 0.05, 0.01, 0.001]
    viz.plot_convergence(degrees, errors, filename="conv.png")

LaTeX Report Generation
------------------------

The :class:`~mathdoc.LatexReport` generates professional LaTeX documents:

.. code-block:: python

    from mathdoc import LatexReport
    
    report = LatexReport(
        title="Approximation Analysis",
        author="Your Name"
    )
    
    # Add sections
    report.add_section("Results")
    report.add_subsection("Approximation Error")
    
    # Add text
    report.add_text("The approximation was performed using Chebyshev polynomials.")
    
    # Add math
    report.add_math(r"\|e\|_2 = 0.001", display=True)
    
    # Add tables
    data = np.array([[1, 2, 3], [4, 5, 6]])
    report.add_table(data, headers=["x", "y", "z"])
    
    # Add figures
    report.add_figure("plot.png", caption="Analysis plot")
    
    # Generate PDF-ready document
    report.generate("report.tex")

Complete Workflow Example
--------------------------

Here's a complete example combining all components:

.. code-block:: python

    import numpy as np
    from mathdoc import (
        DataLoader, Interpolator, Approximator,
        ErrorAnalyzer, Visualizer, LatexReport
    )
    
    # 1. Load and prepare data
    loader = DataLoader(random_seed=42)
    x, y = loader.load_synthetic(n_points=60, noise=0.05)
    x_clean, y_clean = loader.remove_outliers(x, y, threshold=2.0)
    
    # 2. Approximate with Chebyshev basis
    approx = Approximator(x_clean, y_clean, basis_type='chebyshev', degree=10)
    coeffs = approx.fit()
    
    # 3. Evaluate and analyze
    x_dense = np.linspace(x_clean.min(), x_clean.max(), 300)
    y_approx = approx.evaluate(x_dense)
    error_analyzer = ErrorAnalyzer(y_clean, approx.evaluate(x_clean))
    errors = error_analyzer.summary(approx.evaluate(x_clean))
    
    # 4. Visualize
    viz = Visualizer()
    viz.plot_approximation(
        x_clean, y_clean, approx.evaluate(x_clean),
        filename="result.png"
    )
    
    # 5. Generate report
    report = LatexReport(title="Analysis Results")
    report.add_section("Results")
    report.add_text(f"L2 error: {errors['l2_norm']:.6e}")
    report.add_figure("result.png")
    report.generate("report.tex")
