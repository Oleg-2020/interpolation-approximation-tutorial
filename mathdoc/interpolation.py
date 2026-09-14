"""
Interpolation Module

Provides various interpolation methods to construct smooth curves through data points.

Supported methods:
- Linear interpolation
- Cubic spline interpolation
- Polynomial interpolation
"""

import numpy as np
from scipy.interpolate import CubicSpline, interp1d
from typing import Optional, Callable
from .error_analysis import ErrorAnalyzer


class Interpolator:
    """
    Interpolate data using various methods.
    
    This class constructs smooth functions through discrete data points
    and provides methods for evaluating and analyzing the interpolation.
    """
    
    def __init__(self, x: np.ndarray, y: np.ndarray):
        """
        Initialize Interpolator with data points.
        
        Args:
            x: X coordinates of data points
            y: Y coordinates of data points
            
        Raises:
            ValueError: If x and y have different lengths or are empty
        """
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        if len(x) < 2:
            raise ValueError("At least 2 points required for interpolation")
        
        self.x = np.asarray(x, dtype=float)
        self.y = np.asarray(y, dtype=float)
        self.error_analyzer = ErrorAnalyzer(self.x, self.y)
    
    def linear(self, x_new: np.ndarray) -> np.ndarray:
        """
        Linear interpolation.
        
        Args:
            x_new: Points where to evaluate the interpolant
        
        Returns:
            Interpolated y values
        """
        f = interp1d(self.x, self.y, kind='linear', bounds_error=False, fill_value='extrapolate')
        return f(x_new)
    
    def cubic_spline(
        self,
        n_points: Optional[int] = None,
        x_new: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Cubic spline interpolation.
        
        Args:
            n_points: Number of evaluation points (if x_new not provided)
            x_new: Custom evaluation points
        
        Returns:
            Interpolated y values
        """
        if x_new is None:
            if n_points is None:
                n_points = len(self.x) * 3
            x_new = np.linspace(self.x.min(), self.x.max(), n_points)
        
        cs = CubicSpline(self.x, self.y)
        return cs(x_new)
    
    def polynomial(self, degree: int, x_new: np.ndarray) -> np.ndarray:
        """
        Polynomial interpolation using Lagrange basis.
        
        Args:
            degree: Degree of interpolating polynomial
            x_new: Points where to evaluate
        
        Returns:
            Interpolated values
        """
        if degree > len(self.x) - 1:
            raise ValueError(f"Degree {degree} exceeds data size {len(self.x)}")
        
        coeffs = np.polyfit(self.x, self.y, degree)
        poly = np.poly1d(coeffs)
        return poly(x_new)

