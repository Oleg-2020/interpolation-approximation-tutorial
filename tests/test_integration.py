"""
Integration tests for the complete workflow.

Tests the full pipeline: data loading → interpolation/approximation → analysis → LaTeX export
"""

import pytest
import tempfile
import os
import numpy as np
from mathdoc import (
    DataLoader, Interpolator, Approximator, 
    ErrorAnalyzer, Visualizer, LatexReport
)


class TestIntegrationWorkflow:
    """Test complete data processing workflow."""
    
    def test_complete_interpolation_workflow(self):
        """Test full interpolation pipeline."""
        # Load data
        loader = DataLoader(random_seed=42)
        x, y = loader.load_synthetic(n_points=50, noise=0.05)
        
        # Interpolate
        interp = Interpolator(x, y)
        x_new = np.linspace(x.min(), x.max(), 200)
        y_smooth = interp.cubic_spline(x_new=x_new)
        
        assert len(y_smooth) == 200
        assert all(np.isfinite(y_smooth))
    
    def test_complete_approximation_workflow(self):
        """Test full approximation pipeline."""
        # Load data
        loader = DataLoader(random_seed=42)
        x, y = loader.load_synthetic(n_points=50, noise=0.05, function='sine')
        
        # Approximate
        approx = Approximator(x, y, basis_type='chebyshev', degree=8)
        coeffs = approx.fit()
        y_approx = approx.evaluate(x)
        
        # Analyze errors
        error_analyzer = ErrorAnalyzer(x, y)
        summary = error_analyzer.summary(y_approx)
        
        assert len(coeffs) == 9
        assert 'l2_norm' in summary
        assert summary['l2_norm'] >= 0
    
    def test_workflow_with_visualization(self):
        """Test workflow including visualization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Load data
            loader = DataLoader(random_seed=42)
            x, y = loader.load_synthetic(n_points=30, noise=0.02)
            
            # Interpolate
            interp = Interpolator(x, y)
            x_new = np.linspace(x.min(), x.max(), 100)
            y_interp = interp.cubic_spline(x_new=x_new)
            
            # Visualize
            viz = Visualizer()
            plot_path = os.path.join(tmpdir, "interpolation.png")
            viz.plot_interpolation(x, y, x_new, y_interp, filename=plot_path)
            
            assert os.path.exists(plot_path)
    
    def test_workflow_with_latex_export(self):
        """Test complete workflow with LaTeX export."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Load data
            loader = DataLoader(random_seed=42)
            x, y = loader.load_synthetic(n_points=40)
            
            # Approximate
            approx = Approximator(x, y, degree=5)
            approx.fit()
            y_approx = approx.evaluate(x)
            
            # Generate report
            report = LatexReport(title="Analysis Results")
            report.add_section("Data Approximation")
            report.add_text(f"Fitted {len(x)} data points with polynomial degree 5.")
            report.add_math(f"\\|e\\|_2 = {approx.error_norm():.6f}")
            report.add_table(
                np.column_stack([x[:5], y[:5], y_approx[:5]]),
                headers=["x", "y_exact", "y_approx"],
                caption="Approximation Results"
            )
            
            report_path = os.path.join(tmpdir, "report.tex")
            report.generate(report_path)
            
            assert os.path.exists(report_path)


class TestBasisComparison:
    """Test comparison of different basis functions."""
    
    def test_compare_basis_types(self):
        """Test approximation with different basis types."""
        x = np.linspace(0, 1, 50)
        y = np.sin(2*np.pi*x)
        
        errors = {}
        for basis_type in ['chebyshev', 'legendre', 'power']:
            approx = Approximator(x, y, basis_type=basis_type, degree=8)
            approx.fit()
            errors[basis_type] = approx.error_norm()
        
        # All basis types should give reasonable errors
        for error in errors.values():
            assert error >= 0
            assert np.isfinite(error)
        
        # Chebyshev should generally perform better
        assert errors['chebyshev'] <= errors['power']


class TestConvergence:
    """Test convergence of approximation with increasing degree."""
    
    def test_convergence_with_degree(self):
        """Test that error decreases with polynomial degree."""
        x = np.linspace(0, 1, 100)
        y = np.sin(2*np.pi*x) + 0.5*np.cos(4*np.pi*x)
        
        errors = []
        for degree in [1, 3, 5, 7, 9]:
            approx = Approximator(x, y, basis_type='chebyshev', degree=degree)
            approx.fit()
            errors.append(approx.error_norm())
        
        # Errors should generally decrease
        assert errors[-1] < errors[0]
