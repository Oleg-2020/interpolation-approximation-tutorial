"""
Tests for error_analysis module.

Tests cover:
- Error norm computations
- Residual analysis
- Error metrics
"""

import pytest
import numpy as np
from mathdoc.error_analysis import ErrorAnalyzer


class TestErrorAnalyzerInit:
    """Test ErrorAnalyzer initialization."""
    
    def test_init_valid(self):
        """Test valid initialization."""
        x = np.linspace(0, 1, 10)
        y = np.sin(2*np.pi*x)
        
        analyzer = ErrorAnalyzer(x, y)
        assert len(analyzer.x_true) == 10
        assert len(analyzer.y_true) == 10


class TestResiduals:
    """Test residual computation."""
    
    def test_compute_residuals(self):
        """Test residual calculation."""
        x = np.array([0, 1, 2])
        y_true = np.array([1, 2, 3])
        y_approx = np.array([1.1, 1.9, 3.2])
        
        analyzer = ErrorAnalyzer(x, y_true)
        residuals = analyzer.compute_residuals(y_approx)
        
        expected = y_true - y_approx
        assert np.allclose(residuals, expected)
    
    def test_residuals_zero_for_exact(self):
        """Test zero residuals for exact approximation."""
        x = np.linspace(0, 1, 10)
        y = np.sin(2*np.pi*x)
        
        analyzer = ErrorAnalyzer(x, y)
        residuals = analyzer.compute_residuals(y)
        
        assert np.allclose(residuals, 0)


class TestErrorNorms:
    """Test error norm computations."""
    
    def test_l2_norm(self):
        """Test L2 norm calculation."""
        x = np.array([0, 1, 2])
        y_true = np.array([0, 1, 2])
        y_approx = np.array([0, 1.1, 2])
        
        analyzer = ErrorAnalyzer(x, y_true)
        l2 = analyzer.l2_norm(y_approx)
        
        expected = np.sqrt(0.1**2)  # only second point differs
        assert np.isclose(l2, expected)
    
    def test_l_inf_norm(self):
        """Test L-infinity norm calculation."""
        x = np.array([0, 1, 2])
        y_true = np.array([0, 1, 2])
        y_approx = np.array([0, 1.5, 2.2])
        
        analyzer = ErrorAnalyzer(x, y_true)
        l_inf = analyzer.l_inf_norm(y_approx)
        
        expected = 0.2  # max error at third point
        assert np.isclose(l_inf, expected)
    
    def test_zero_norm_for_exact(self):
        """Test zero norms for exact approximation."""
        x = np.linspace(0, 1, 10)
        y = np.sin(2*np.pi*x)
        
        analyzer = ErrorAnalyzer(x, y)
        
        assert np.isclose(analyzer.l2_norm(y), 0)
        assert np.isclose(analyzer.l_inf_norm(y), 0)


class TestRelativeError:
    """Test relative error computation."""
    
    def test_relative_error(self):
        """Test relative error calculation."""
        x = np.array([0, 1, 2])
        y_true = np.array([1, 2, 3])
        y_approx = np.array([1.1, 1.9, 3.1])
        
        analyzer = ErrorAnalyzer(x, y_true)
        rel_err = analyzer.relative_error(y_approx)
        
        assert 0 <= rel_err <= 1
        assert rel_err > 0
    
    def test_relative_error_zero(self):
        """Test zero relative error for exact approximation."""
        x = np.linspace(0, 1, 10)
        y = np.sin(2*np.pi*x) + 1  # ensure non-zero
        
        analyzer = ErrorAnalyzer(x, y)
        rel_err = analyzer.relative_error(y)
        
        assert np.isclose(rel_err, 0)


class TestMSE:
    """Test mean squared error."""
    
    def test_mse_calculation(self):
        """Test MSE computation."""
        x = np.array([0, 1, 2])
        y_true = np.array([0, 1, 2])
        y_approx = np.array([0, 1.2, 2])
        
        analyzer = ErrorAnalyzer(x, y_true)
        mse = analyzer.mse(y_approx)
        
        expected = 0.2**2 / 3
        assert np.isclose(mse, expected)


class TestSummary:
    """Test error summary."""
    
    def test_summary_keys(self):
        """Test that summary contains all metrics."""
        x = np.linspace(0, 1, 20)
        y_true = np.sin(2*np.pi*x)
        y_approx = np.cos(2*np.pi*x)
        
        analyzer = ErrorAnalyzer(x, y_true)
        summary = analyzer.summary(y_approx)
        
        assert 'l2_norm' in summary
        assert 'l_inf_norm' in summary
        assert 'relative_error' in summary
        assert 'mse' in summary
    
    def test_summary_all_positive(self):
        """Test that all error metrics are positive."""
        x = np.linspace(0, 1, 20)
        y_true = np.sin(2*np.pi*x)
        y_approx = y_true + 0.1
        
        analyzer = ErrorAnalyzer(x, y_true)
        summary = analyzer.summary(y_approx)
        
        for value in summary.values():
            assert value >= 0
