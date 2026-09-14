"""
Tests for data_loader module.

Tests cover:
- Synthetic data generation
- Data validation
- Outlier removal
- Normalization
"""

import pytest
import numpy as np
from mathdoc.data_loader import DataLoader


class TestDataLoaderSynthetic:
    """Test synthetic data generation."""
    
    def test_load_synthetic_sine(self):
        """Test sine function generation."""
        loader = DataLoader(random_seed=42)
        x, y = loader.load_synthetic(n_points=100, function='sine')
        
        assert len(x) == 100
        assert len(y) == 100
        assert x[0] == 0.0
        assert x[-1] == 1.0
    
    def test_load_synthetic_with_noise(self):
        """Test that noise increases variance."""
        loader = DataLoader(random_seed=42)
        _, y_clean = loader.load_synthetic(n_points=100, noise=0.0)
        
        loader = DataLoader(random_seed=42)
        _, y_noisy = loader.load_synthetic(n_points=100, noise=0.1)
        
        assert np.std(y_noisy) > np.std(y_clean)
    
    def test_load_synthetic_different_functions(self):
        """Test all function types."""
        loader = DataLoader()
        functions = ['sine', 'cosine', 'polynomial', 'exp']
        
        for func in functions:
            x, y = loader.load_synthetic(n_points=50, function=func)
            assert len(x) == len(y) == 50
    
    def test_load_synthetic_invalid_function(self):
        """Test error handling for invalid function."""
        loader = DataLoader()
        with pytest.raises(ValueError):
            loader.load_synthetic(n_points=50, function='invalid')
    
    def test_load_synthetic_invalid_n_points(self):
        """Test error handling for invalid n_points."""
        loader = DataLoader()
        with pytest.raises(ValueError):
            loader.load_synthetic(n_points=0)
    
    def test_custom_x_range(self):
        """Test custom x range."""
        loader = DataLoader()
        x, y = loader.load_synthetic(n_points=50, x_range=(-10, 10))
        
        assert x[0] == -10.0
        assert x[-1] == 10.0


class TestDataLoaderOutliers:
    """Test outlier removal."""
    
    def test_remove_outliers(self):
        """Test outlier detection and removal."""
        loader = DataLoader()
        x = np.arange(20, dtype=float)
        y = np.ones(20)
        y[0] = 100  # outlier
        
        x_clean, y_clean = loader.remove_outliers(x, y, threshold=2.0)
        
        assert len(x_clean) < len(x)
        assert np.max(y_clean) <= 2  # outlier removed
    
    def test_remove_outliers_threshold(self):
        """Test threshold sensitivity."""
        loader = DataLoader()
        x = np.arange(20, dtype=float)
        y = np.ones(20)
        y[0] = 10
        
        x_strict, _ = loader.remove_outliers(x, y, threshold=1.0)
        x_loose, _ = loader.remove_outliers(x, y, threshold=5.0)
        
        assert len(x_strict) <= len(x_loose)


class TestDataLoaderNormalization:
    """Test normalization methods."""
    
    def test_normalize_minmax(self):
        """Test min-max normalization."""
        loader = DataLoader()
        data = np.array([0, 50, 100])
        
        normalized = loader.normalize(data, method='minmax')
        
        assert normalized[0] == 0.0
        assert normalized[-1] == 1.0
        assert np.allclose(normalized[1], 0.5)
    
    def test_normalize_zscore(self):
        """Test z-score normalization."""
        loader = DataLoader()
        data = np.array([1, 2, 3, 4, 5])
        
        normalized = loader.normalize(data, method='zscore')
        
        assert np.isclose(np.mean(normalized), 0.0)
        assert np.isclose(np.std(normalized), 1.0)
    
    def test_normalize_invalid_method(self):
        """Test error handling for invalid method."""
        loader = DataLoader()
        data = np.array([1, 2, 3])
        
        with pytest.raises(ValueError):
            loader.normalize(data, method='invalid')
