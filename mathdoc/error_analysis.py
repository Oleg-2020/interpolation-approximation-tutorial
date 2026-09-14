"""
Error Analysis Module

Compute and analyze approximation errors:
- Residuals and error norms
- Pointwise error analysis
- Convergence metrics
"""

import numpy as np
from typing import Tuple, Dict


class ErrorAnalyzer:
    """
    Analyze and quantify approximation errors.
    """
    
    def __init__(self, x_true: np.ndarray, y_true: np.ndarray):
        """
        Initialize ErrorAnalyzer.
        
        Args:
            x_true: Reference x coordinates
            y_true: Reference y coordinates (exact values)
        """
        self.x_true = np.asarray(x_true, dtype=float)
        self.y_true = np.asarray(y_true, dtype=float)
    
    def compute_residuals(self, y_approx: np.ndarray) -> np.ndarray:
        """
        Compute pointwise residuals.
        
        Args:
            y_approx: Approximated y values
        
        Returns:
            Array of residuals: y_true - y_approx
        """
        return self.y_true - np.asarray(y_approx, dtype=float)
    
    def l2_norm(self, y_approx: np.ndarray) -> float:
        """
        Compute L2 error norm.
        
        L2 = sqrt(sum((y_true - y_approx)^2))
        
        Args:
            y_approx: Approximated values
        
        Returns:
            L2 norm
        """
        residuals = self.compute_residuals(y_approx)
        return np.sqrt(np.sum(residuals**2))
    
    def l_inf_norm(self, y_approx: np.ndarray) -> float:
        """
        Compute L-infinity (maximum absolute) error norm.
        
        L_inf = max(|y_true - y_approx|)
        
        Args:
            y_approx: Approximated values
        
        Returns:
            Maximum absolute error
        """
        residuals = self.compute_residuals(y_approx)
        return np.max(np.abs(residuals))
    
    def relative_error(self, y_approx: np.ndarray) -> float:
        """
        Compute relative L2 error.
        
        Relative error = L2(error) / L2(y_true)
        
        Args:
            y_approx: Approximated values
        
        Returns:
            Relative error (0 to 1 scale)
        """
        l2_error = self.l2_norm(y_approx)
        l2_true = np.sqrt(np.sum(self.y_true**2))
        return l2_error / (l2_true + 1e-10)
    
    def mse(self, y_approx: np.ndarray) -> float:
        """
        Compute mean squared error.
        
        Args:
            y_approx: Approximated values
        
        Returns:
            MSE = mean((y_true - y_approx)^2)
        """
        residuals = self.compute_residuals(y_approx)
        return np.mean(residuals**2)
    
    def summary(self, y_approx: np.ndarray) -> Dict[str, float]:
        """
        Compute comprehensive error summary.
        
        Args:
            y_approx: Approximated values
        
        Returns:
            Dictionary with error metrics
        """
        return {
            'l2_norm': self.l2_norm(y_approx),
            'l_inf_norm': self.l_inf_norm(y_approx),
            'relative_error': self.relative_error(y_approx),
            'mse': self.mse(y_approx),
        }

