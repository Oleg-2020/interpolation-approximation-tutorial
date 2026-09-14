"""
Tests for interpolation module.

Tests cover:
- Linear interpolation
- Cubic spline interpolation
- Polynomial interpolation
"""

import pytest
import numpy as np
from mathdoc.interpolation import Interpolator


class TestInterpolatorInit:
    """Test Interpolator initialization."""
    
    def test_init_valid(self):
        """Test valid initialization."""
        x = np.array([0, 1, 2])
        y = np.array([0, 1, 2])
        
        interp = Interpolator(x, y)
        assert len(interp.x) == 3
        assert len(interp.y) == 3
    
    def test_init_mismatched_lengths(self):
        """Test error on mismatched lengths."""
        x = np.array([0, 1, 2])
        y = np.array([0, 1])
        
        with pytest.raises(ValueError):
            Interpolator(x, y)
    
    def test_init_insufficient_points(self):
        """Test error on insufficient points."""
        x = np.array([0])
        y = np.array([0])
        
        with pytest.raises(ValueError):
            Interpolator(x, y)


class TestInterpolatorLinear:
    """Test linear interpolation."""
    
    def test_linear_exact_at_points(self):
        """Test that interpolation passes through data points."""
        x = np.array([0, 1, 2])
        y = np.array([0, 1, 2])
        interp = Interpolator(x, y)
        
        y_interp = interp.linear(x)
        assert np.allclose(y_interp, y)
    
    def test_linear_between_points(self):
        """Test linear interpolation between points."""
        x = np.array([0, 1])
        y = np.array([0, 1])
        interp = Interpolator(x, y)
        
        y_interp = interp.linear(np.array([0.5]))
        assert np.isclose(y_interp[0], 0.5)
    
    def test_linear_multiple_points(self):
        """Test linear interpolation at multiple points."""
        x = np.array([0, 1, 2, 3])
        y = np.array([0, 1, 4, 9])
        interp = Interpolator(x, y)
        
        x_new = np.linspace(0, 3, 10)
        y_new = interp.linear(x_new)
        
        assert len(y_new) == 10
        assert y_new[0] == y[0]
        assert y_new[-1] == y[-1]


class TestInterpolatorCubicSpline:
    """Test cubic spline interpolation."""
    
    def test_cubic_spline_default(self):
        """Test cubic spline with default parameters."""
        x = np.array([0, 1, 2, 3])
        y = np.array([0, 1, 4, 9])
        interp = Interpolator(x, y)
        
        y_spline = interp.cubic_spline()
        assert len(y_spline) > len(x)  # More points than original
    
    def test_cubic_spline_custom_n_points(self):
        """Test cubic spline with custom number of points."""
        x = np.array([0, 1, 2])
        y = np.array([0, 1, 0])
        interp = Interpolator(x, y)
        
        y_spline = interp.cubic_spline(n_points=100)
        assert len(y_spline) == 100
    
    def test_cubic_spline_custom_x_new(self):
        """Test cubic spline with custom evaluation points."""
        x = np.array([0, 1, 2])
        y = np.array([0, 1, 0])
        interp = Interpolator(x, y)
        
        x_new = np.array([0.5, 1.5])
        y_spline = interp.cubic_spline(x_new=x_new)
        
        assert len(y_spline) == 2


class TestInterpolatorPolynomial:
    """Test polynomial interpolation."""
    
    def test_polynomial_exact_fit(self):
        """Test polynomial interpolation through all points."""
        x = np.array([0, 1, 2, 3])
        y = np.array([0, 1, 4, 9])
        interp = Interpolator(x, y)
        
        x_new = np.linspace(0, 3, 10)
        y_poly = interp.polynomial(degree=3, x_new=x_new)
        
        # Check at original points
        y_at_orig = interp.polynomial(degree=3, x_new=x)
        assert np.allclose(y_at_orig, y, atol=1e-10)
    
    def test_polynomial_degree_too_high(self):
        """Test error when degree exceeds data size."""
        x = np.array([0, 1])
        y = np.array([0, 1])
        interp = Interpolator(x, y)
        
        with pytest.raises(ValueError):
            interp.polynomial(degree=10, x_new=x)
    
    def test_polynomial_different_degrees(self):
        """Test polynomial interpolation with different degrees."""
        x = np.array([0, 0.5, 1, 1.5, 2])
        y = x**2
        interp = Interpolator(x, y)
        
        x_new = np.array([0.25, 0.75, 1.25])
        
        for degree in [1, 2, 3, 4]:
            y_poly = interp.polynomial(degree=degree, x_new=x_new)
            assert len(y_poly) == 3
