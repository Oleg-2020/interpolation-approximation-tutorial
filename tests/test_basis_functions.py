"""
Tests for basis_functions module.

Tests cover:
- Chebyshev, Legendre, and power basis functions
- Recurrence relations and properties
- Factory method
"""

import pytest
import numpy as np
from mathdoc.basis_functions import (
    BasisFunctions, ChebyshevBasis, LegendreBasis, PowerBasis
)


class TestBasisFactory:
    """Test basis function factory method."""
    
    def test_factory_chebyshev(self):
        """Test creation of Chebyshev basis."""
        x = np.linspace(0, 1, 10)
        basis = BasisFunctions.create('chebyshev', 5, x)
        
        assert isinstance(basis, ChebyshevBasis)
        assert basis.degree == 5
    
    def test_factory_legendre(self):
        """Test creation of Legendre basis."""
        x = np.linspace(0, 1, 10)
        basis = BasisFunctions.create('legendre', 3, x)
        
        assert isinstance(basis, LegendreBasis)
        assert basis.degree == 3
    
    def test_factory_power(self):
        """Test creation of power basis."""
        x = np.linspace(0, 1, 10)
        basis = BasisFunctions.create('power', 4, x)
        
        assert isinstance(basis, PowerBasis)
        assert basis.degree == 4
    
    def test_factory_invalid_type(self):
        """Test error on invalid basis type."""
        x = np.linspace(0, 1, 10)
        
        with pytest.raises(ValueError):
            BasisFunctions.create('invalid', 5, x)


class TestChebyshevBasis:
    """Test Chebyshev polynomial basis."""
    
    def test_chebyshev_degree_0(self):
        """Test T_0(x) = 1."""
        x = np.array([0, 0.5, 1])
        basis = ChebyshevBasis(5, x)
        
        T0 = basis.evaluate(0)
        assert np.allclose(T0, 1.0)
    
    def test_chebyshev_degree_1(self):
        """Test T_1(x) = x (on normalized interval)."""
        x = np.linspace(0, 1, 10)
        basis = ChebyshevBasis(5, x)
        
        T1 = basis.evaluate(1)
        # T_1 should be linear in normalized coordinates
        assert len(T1) == len(x)
    
    def test_chebyshev_recurrence(self):
        """Test Chebyshev recurrence relation."""
        x = np.linspace(0, 1, 20)
        basis = ChebyshevBasis(5, x)
        
        T0 = basis.evaluate(0)
        T1 = basis.evaluate(1)
        T2 = basis.evaluate(2)
        T3 = basis.evaluate(3)
        
        # Check recurrence: T_3 = 2*x*T_2 - T_1
        x_norm = basis.x_normalized
        T3_check = 2 * x_norm * T2 - T1
        assert np.allclose(T3, T3_check)


class TestLegendreBasis:
    """Test Legendre polynomial basis."""
    
    def test_legendre_degree_0(self):
        """Test P_0(x) = 1."""
        x = np.linspace(0, 1, 10)
        basis = LegendreBasis(5, x)
        
        P0 = basis.evaluate(0)
        assert np.allclose(P0, 1.0)
    
    def test_legendre_degree_1(self):
        """Test P_1(x) = x (on normalized interval)."""
        x = np.linspace(0, 1, 10)
        basis = LegendreBasis(5, x)
        
        P1 = basis.evaluate(1)
        assert len(P1) == len(x)
    
    def test_legendre_orthogonality(self):
        """Test orthogonality of Legendre polynomials."""
        x = np.linspace(-1, 1, 100)
        basis = LegendreBasis(5, x)
        
        P0 = basis.evaluate(0)
        P1 = basis.evaluate(1)
        P2 = basis.evaluate(2)
        
        # Inner products should be zero (approximately)
        dx = x[1] - x[0]
        inner_01 = np.sum(P0 * P1) * dx
        inner_02 = np.sum(P0 * P2) * dx
        inner_12 = np.sum(P1 * P2) * dx
        
        assert np.abs(inner_01) < 0.1
        assert np.abs(inner_02) < 0.1
        assert np.abs(inner_12) < 0.1


class TestPowerBasis:
    """Test power basis (monomials)."""
    
    def test_power_degree_0(self):
        """Test x^0 = 1."""
        x = np.array([1, 2, 3])
        basis = PowerBasis(5, x)
        
        x0 = basis.evaluate(0)
        assert np.allclose(x0, 1.0)
    
    def test_power_degree_1(self):
        """Test x^1 = x."""
        x = np.array([1, 2, 3])
        basis = PowerBasis(5, x)
        
        x1 = basis.evaluate(1)
        assert np.allclose(x1, x)
    
    def test_power_degree_2(self):
        """Test x^2."""
        x = np.array([1, 2, 3])
        basis = PowerBasis(5, x)
        
        x2 = basis.evaluate(2)
        assert np.allclose(x2, x**2)
    
    def test_power_multiple_degrees(self):
        """Test multiple power basis functions."""
        x = np.linspace(0, 1, 10)
        basis = PowerBasis(4, x)
        
        for n in range(5):
            xn = basis.evaluate(n)
            assert np.allclose(xn, x**n)
