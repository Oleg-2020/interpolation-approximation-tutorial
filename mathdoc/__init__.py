"""
Mathdoc: Mathematical Functions Documentation & Analysis Package

A comprehensive toolkit for interpolation, approximation, and LaTeX report generation.
"""

__version__ = "0.1.0"
__author__ = "Educational Contributors"

from .data_loader import DataLoader
from .interpolation import Interpolator
from .approximation import Approximator
from .basis_functions import BasisFunctions, ChebyshevBasis, LegendreBasis, PowerBasis
from .visualization import Visualizer
from .error_analysis import ErrorAnalyzer
from .latex_formatter import LatexReport

__all__ = [
    'DataLoader',
    'Interpolator',
    'Approximator',
    'BasisFunctions',
    'ChebyshevBasis',
    'LegendreBasis',
    'PowerBasis',
    'Visualizer',
    'ErrorAnalyzer',
    'LatexReport',
]
