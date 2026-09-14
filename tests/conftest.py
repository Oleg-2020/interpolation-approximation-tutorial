"""
Pytest configuration and shared fixtures.
"""

import pytest
import numpy as np
from mathdoc import DataLoader


@pytest.fixture
def sample_data():
    """
    Fixture providing sample synthetic data.
    """
    loader = DataLoader(random_seed=42)
    x, y = loader.load_synthetic(n_points=50, noise=0.01, function='sine')
    return x, y


@pytest.fixture
def clean_data():
    """
    Fixture providing clean data without noise.
    """
    loader = DataLoader(random_seed=42)
    x, y = loader.load_synthetic(n_points=30, noise=0.0, function='cosine')
    return x, y


@pytest.fixture
def polynomial_data():
    """
    Fixture providing polynomial data.
    """
    loader = DataLoader(random_seed=42)
    x, y = loader.load_synthetic(n_points=20, noise=0.0, function='polynomial')
    return x, y
