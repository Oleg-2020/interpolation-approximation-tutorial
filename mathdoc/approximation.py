"""
Approximation Module

Provides function approximation using various basis functions.
Allows finding optimal coefficients that minimize approximation error.
"""

import numpy as np
from scipy.linalg import lstsq
from typing import Optional
from .basis_functions import BasisFunctions
from .error_analysis import ErrorAnalyzer


class Approximator:
    """
    Approximate functions using least squares with orthogonal basis.
    
    Finds optimal coefficients that minimize the L2 norm of the approximation error.
    """
    
    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        basis_type: str = 'chebyshev',
        degree: int = 5
    ):
        """
        Initialize Approximator.
        
        Args:
            x: Data points x coordinates
            y: Data points y coordinates
            basis_type: Type of basis ('chebyshev', 'legendre', 'power')
            degree: Degree of approximation polynomial
        """
        self.x = np.asarray(x, dtype=float)
        self.y = np.asarray(y, dtype=float)
        self.basis_type = basis_type
        self.degree = degree
        self.coefficients = None
        self.basis = BasisFunctions.create(basis_type, degree, self.x)
        self.error_analyzer = ErrorAnalyzer(self.x, self.y)
    
    def fit(self) -> np.ndarray:
        """
        Fit the approximation model using least squares.
        
        Solves the normal equations:
            A^T A c = A^T y
        where A is the basis matrix and c are coefficients.
        
        Returns:
            Array of optimal coefficients
            
        Example:
            >>> approx = Approximator(x, y, basis_type='chebyshev', degree=5)
            >>> coeffs = approx.fit()
            >>> error = approx.max_error()
        """
        # Construct basis matrix: each row is a basis function evaluated at a point
        A = np.column_stack([self.basis.evaluate(i) for i in range(self.degree + 1)]).T
        
        # Solve least squares problem
        result, residuals, rank, s = lstsq(A, self.y)
        self.coefficients = result
        
        return self.coefficients
    
    def evaluate(self, x_new: np.ndarray) -> np.ndarray:
        """
        Evaluate the approximation at new points.
        
        Args:
            x_new: Points where to evaluate
        
        Returns:
            Approximated y values
            
        Raises:
            RuntimeError: If fit() not called yet
        """
        if self.coefficients is None:
            raise RuntimeError("Must call fit() before evaluate()")
        
        basis = BasisFunctions.create(self.basis_type, self.degree, x_new)
        y_approx = np.zeros_like(x_new, dtype=float)
        
        for i in range(self.degree + 1):
            y_approx += self.coefficients[i] * basis.evaluate(i)
        
        return y_approx
    
    def error_norm(self) -> float:
        """
        Compute L2 norm of approximation error.
        
        Returns:
            L2 error norm: sqrt(sum((y_approx - y)^2))
        """
        y_approx = self.evaluate(self.x)
        error = self.y - y_approx
        return np.sqrt(np.sum(error**2))
    
    def max_error(self) -> float:
        """
        Compute maximum absolute error.
        
        Returns:
            Max error: max(|y_approx - y|)
        """
        y_approx = self.evaluate(self.x)
        return np.max(np.abs(self.y - y_approx))

