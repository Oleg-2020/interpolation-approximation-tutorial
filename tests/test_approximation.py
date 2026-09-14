"""
Tests for approximation module.

Tests cover:
- Least squares fitting
- Error computation
- Integration with basis functions
"""

import pytest
import numpy as np
from mathdoc.approximation import Approximator


class TestApproximatorInit:
    """Test Approximator initialization."""
    
    def test_init_valid(self):
        """Test valid initialization."""
        x = np.linspace(0, 1, 20)
        y = np.sin(2*np.pi*x)
        
        approx = Approximator(x, y, basis_type='chebyshev', degree=5)
        assert approx.degree == 5
        assert approx.basis_type == 'chebyshev'
    
    def test_init_different_basis_types(self):
        """Test initialization with different basis types."""
        x = np.linspace(0, 1, 20)
        y = np.sin(2*np.pi*x)
        
        for basis in ['chebyshev', 'legendre', 'power']:
            approx = Approximator(x, y, basis_type=basis, degree=5)
            assert approx.basis_type == basis


class TestApproximatorFit:
    """Test least squares fitting."""
    
    def test_fit_returns_coefficients(self):
        """Test that fit() returns coefficients."""
        x = np.linspace(0, 1, 30)
        y = np.sin(2*np.pi*x)
        
        approx = Approximator(x, y, basis_type='chebyshev', degree=5)
        coeffs = approx.fit()
        
        assert len(coeffs) == 6  # degree + 1
        assert all(np.isfinite(coeffs))
    
    def test_fit_sets_coefficients_attribute(self):
        """Test that fit() sets coefficients attribute."""
        x = np.linspace(0, 1, 20)
        y = np.sin(2*np.pi*x)
        
        approx = Approximator(x, y, degree=3)
        assert approx.coefficients is None
        
        approx.fit()
        assert approx.coefficients is not None
    
    def test_fit_polynomial_basis(self):
        """Test fitting with power basis."""
        x = np.linspace(0, 1, 20)
        y = x**2
        
        approx = Approximator(x, y, basis_type='power', degree=2)
        coeffs = approx.fit()
        
        assert len(coeffs) == 3


class TestApproximatorEvaluate:
    """Test approximation evaluation."""
    
    def test_evaluate_before_fit(self):
        """Test error when evaluate called before fit."""
        x = np.linspace(0, 1, 20)
        y = np.sin(2*np.pi*x)
        
        approx = Approximator(x, y)
        with pytest.raises(RuntimeError):
            approx.evaluate(x)
    
    def test_evaluate_after_fit(self):
        """Test evaluation after fitting."""
        x = np.linspace(0, 1, 20)
        y = np.sin(2*np.pi*x)
        
        approx = Approximator(x, y, degree=5)
        approx.fit()
        
        y_approx = approx.evaluate(x)
        assert len(y_approx) == len(x)
        assert all(np.isfinite(y_approx))
    
    def test_evaluate_new_points(self):
        """Test evaluation at new points."""
        x = np.linspace(0, 1, 20)
        y = x**2
        
        approx = Approximator(x, y, basis_type='power', degree=2)
        approx.fit()
        
        x_new = np.array([0.25, 0.5, 0.75])
        y_new = approx.evaluate(x_new)
        
        assert len(y_new) == 3
        assert np.allclose(y_new, x_new**2, atol=1e-10)


class TestApproximatorErrors:
    """Test error computation."""
    
    def test_error_norm(self):
        """Test L2 error norm computation."""
        x = np.linspace(0, 1, 30)
        y = np.sin(2*np.pi*x)
        
        approx = Approximator(x, y, degree=5)
        approx.fit()
        
        error = approx.error_norm()
        assert error >= 0
        assert np.isfinite(error)
    
    def test_max_error(self):
        """Test maximum absolute error."""
        x = np.linspace(0, 1, 30)
        y = np.sin(2*np.pi*x)
        
        approx = Approximator(x, y, degree=5)
        approx.fit()
        
        max_err = approx.max_error()
        assert max_err >= 0
        assert np.isfinite(max_err)
    
    def test_error_decreases_with_degree(self):
        """Test that error decreases with polynomial degree."""
        x = np.linspace(0, 1, 50)
        y = np.sin(2*np.pi*x)
        
        errors = []
        for degree in [2, 4, 6, 8]:
            approx = Approximator(x, y, degree=degree)
            approx.fit()
            errors.append(approx.error_norm())
        
        # Errors should generally decrease
        assert errors[-1] < errors[0]
