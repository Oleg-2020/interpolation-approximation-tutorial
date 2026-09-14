# MathDoc: Mathematical Functions Documentation & Analysis

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Documentation](https://img.shields.io/badge/docs-sphinx-blueviolet)

## Overview

**MathDoc** is an educational project demonstrating best practices for documenting mathematical packages with LaTeX output integration. It showcases professional documentation patterns for scientific Python projects.

### Features

- **Data Loading & Processing** – import and prepare experimental/theoretical data
- **Interpolation** – construct smooth curves through data points using splines
- **Approximation** – find optimal function fits using various basis functions
- **Basis Functions** – work with Chebyshev, Legendre, and power polynomials
- **Visualization** – create publication-ready plots with error analysis
- **Error Analysis** – compute residuals, norms, and convergence metrics
- **LaTeX Export** – generate professional mathematical reports automatically

## Quick Start

```bash
# Install the package
pip install -e .

# Run tests
pytest tests/ -v

# Build documentation
cd docs && make html
```

### Example Usage

```python
from mathdoc import DataLoader, Interpolator, Approximator
from mathdoc.latex_formatter import LatexReport

# Load data
loader = DataLoader()
x, y = loader.load_synthetic(n_points=50, noise=0.05)

# Interpolate
interp = Interpolator(x, y)
y_smooth = interp.cubic_spline(n_points=200)

# Approximate with Chebyshev basis
approx = Approximator(x, y, basis_type='chebyshev', degree=5)
coefficients = approx.fit()

# Generate LaTeX report
report = LatexReport()
report.add_section("Interpolation Results")
report.add_table(x, y_smooth)
report.add_math("\\text{Error norm: } \\|e\\|_2")
report.generate("report.tex")
```

## Project Structure

```
interpolation-approximation-tutorial/
├── mathdoc/                           # Main package
│   ├── __init__.py                   # Package initialization
│   ├── data_loader.py                # Data import & preprocessing
│   ├── interpolation.py              # Interpolation methods
│   ├── approximation.py              # Function approximation
│   ├─��� basis_functions.py            # Orthogonal polynomial bases
│   ├── visualization.py              # Plotting utilities
│   ├── error_analysis.py             # Error metrics & analysis
│   └── latex_formatter.py            # LaTeX report generation
├── tests/                            # Comprehensive test suite
│   ├── test_data_loader.py
│   ├── test_interpolation.py
│   ├── test_approximation.py
│   ├── test_basis_functions.py
│   ├── test_visualization.py
│   ├── test_error_analysis.py
│   ├── test_latex_formatter.py
│   └── conftest.py
├── examples/                         # Jupyter notebooks
│   ├── 01_data_loading.ipynb
│   ├── 02_interpolation.ipynb
│   ├── 03_approximation.ipynb
│   └── 04_latex_export.ipynb
├── docs/                             # Sphinx documentation
│   ├── source/
│   │   ├── conf.py
│   │   ├── index.rst
│   │   ├── tutorial.rst
│   │   ├── api_reference.rst
│   │   ├── examples.rst
│   │   ├── integration_guide.rst
│   │   └── _static/
│   └── Makefile
├── setup.py
├── setup.cfg
├── .gitignore
├── LICENSE
└── README.md
```

## Documentation

Full documentation with API reference and tutorials: [docs/source/](docs/source/)

Build locally:
```bash
cd docs
make html
open build/html/index.html
```

## Testing

Run the complete test suite:
```bash
pytest tests/ -v --cov=mathdoc
```

## Key Learning Points

This project demonstrates:

1. ✅ **Module organization** – logical separation of concerns
2. ✅ **Interdependencies** – how modules use each other
3. ✅ **LaTeX integration** – automatic report generation
4. ✅ **Comprehensive testing** – unit and integration tests
5. ✅ **Sphinx documentation** – professional API docs
6. ✅ **Jupyter examples** – interactive tutorials
7. ✅ **Type hints** – modern Python documentation
8. ✅ **Error handling** – robust, informative exceptions

## Installation for Development

```bash
# Clone the repository
git clone https://github.com/Oleg-2020/interpolation-approximation-tutorial.git
cd interpolation-approximation-tutorial

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks (optional)
pre-commit install
```

## License

MIT License – see [LICENSE](LICENSE) file

---

**Educational Purpose**: This project serves as a template for structuring, documenting, and testing mathematical Python packages with professional LaTeX integration.

**Author**: Educational Contributors  
**Last Updated**: 2026
