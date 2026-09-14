"""
Basis Functions Module

Provides orthogonal polynomial basis functions:
- Chebyshev polynomials (optimal for approximation)
- Legendre polynomials (orthogonal on [-1, 1])
- Power basis (standard monomials)
"""

import numpy as np
from typing import Optional
from abc import ABC, abstractmethod


class BasisFunctions(ABC):
    """
    Abstract base class for orthogonal polynomial bases.
    """
    
    def __init__(self, degree: int, x: np.ndarray):
        """
        Initialize basis.
        
        Args:
            degree: Maximum polynomial degree
            x: Evaluation points
        """
        self.degree = degree
        self.x = np.asarray(x, dtype=float)
    
    @abstractmethod
    def evaluate(self, n: int) -> np.ndarray:
        """
        Evaluate n-th basis function.
        
        Args:
            n: Index of basis function
        
        Returns:
            Array of function values at self.x
        """
        pass
    
    @staticmethod
    def create(basis_type: str, degree: int, x: np.ndarray) -> 'BasisFunctions':
        """
        Factory method to create appropriate basis.
        
        Args:
            basis_type: 'chebyshev', 'legendre', or 'power'
            degree: Polynomial degree
            x: Evaluation points
        
        Returns:
            Instance of appropriate basis class
        """
        if basis_type == 'chebyshev':
            return ChebyshevBasis(degree, x)
        elif basis_type == 'legendre':
            return LegendreBasis(degree, x)
        elif basis_type == 'power':
            return PowerBasis(degree, x)
        else:
            raise ValueError(f"Unknown basis type: {basis_type}")


class ChebyshevBasis(BasisFunctions):
    """
    Chebyshev polynomials of the first kind.
    
    Optimal for polynomial approximation due to their extremal property.
    Defined on [-1, 1] via: T_n(x) = cos(n * arccos(x))
    """
    
    def __init__(self, degree: int, x: np.ndarray):
        """
        Initialize Chebyshev basis.
        
        Args:
            degree: Maximum polynomial degree
            x: Evaluation points (will be normalized to [-1, 1])
        """
        super().__init__(degree, x)
        # Normalize x to [-1, 1]
        self.x_min = np.min(x)
        self.x_max = np.max(x)
        self.x_normalized = 2 * (x - self.x_min) / (self.x_max - self.x_min) - 1
    
    def evaluate(self, n: int) -> np.ndarray:
        """
        Evaluate n-th Chebyshev polynomial.
        
        Args:
            n: Polynomial index
        
        Returns:
            T_n values at evaluation points
        """
        x = self.x_normalized
        if n == 0:
            return np.ones_like(x)
        elif n == 1:
            return x
        else:
            # Recurrence relation: T_{n+1}(x) = 2x*T_n(x) - T_{n-1}(x)
            T_prev = np.ones_like(x)
            T_curr = x
            for _ in range(2, n + 1):
                T_next = 2 * x * T_curr - T_prev
                T_prev = T_curr
                T_curr = T_next
            return T_curr


class LegendreBasis(BasisFunctions):
    """
    Legendre polynomials.
    
    Orthogonal on [-1, 1] with weight function w(x) = 1.
    """
    
    def __init__(self, degree: int, x: np.ndarray):
        """
        Initialize Legendre basis.
        
        Args:
            degree: Maximum polynomial degree
            x: Evaluation points (will be normalized to [-1, 1])
        """
        super().__init__(degree, x)
        self.x_min = np.min(x)
        self.x_max = np.max(x)
        self.x_normalized = 2 * (x - self.x_min) / (self.x_max - self.x_min) - 1
    
    def evaluate(self, n: int) -> np.ndarray:
        """
        Evaluate n-th Legendre polynomial.
        
        Args:
            n: Polynomial index
        
        Returns:
            P_n values at evaluation points
        """
        x = self.x_normalized
        if n == 0:
            return np.ones_like(x)
        elif n == 1:
            return x
        else:
            # Recurrence: (n+1)*P_{n+1} = (2n+1)*x*P_n - n*P_{n-1}
            P_prev = np.ones_like(x)
            P_curr = x
            for k in range(1, n):
                P_next = ((2*k + 1) * x * P_curr - k * P_prev) / (k + 1)
                P_prev = P_curr
                P_curr = P_next
            return P_curr


class PowerBasis(BasisFunctions):
    """
    Standard power basis: {1, x, x^2, x^3, ...}
    
    Non-orthogonal but simple and intuitive.
    """
    
    def evaluate(self, n: int) -> np.ndarray:
        """
        Evaluate n-th power basis function: x^n
        
        Args:
            n: Power exponent
        
        Returns:
            x^n values at evaluation points
        """
        return self.x ** n

