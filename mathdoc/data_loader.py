"""
Data Loading and Preprocessing Module

This module provides utilities for loading, validating, and preprocessing data
for interpolation and approximation tasks.

Example:
    >>> loader = DataLoader()
    >>> x, y = loader.load_synthetic(n_points=100, noise=0.01)
    >>> x_clean, y_clean = loader.remove_outliers(x, y, threshold=2.0)
"""

import numpy as np
from typing import Tuple, Optional, Union


class DataLoader:
    """
    Load, validate, and preprocess data for mathematical analysis.
    
    This class handles synthetic data generation, file loading, outlier removal,
    and normalization for subsequent interpolation and approximation operations.
    """
    
    def __init__(self, random_seed: Optional[int] = None):
        """
        Initialize DataLoader.
        
        Args:
            random_seed: Seed for reproducible random number generation
        """
        self.random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def load_synthetic(
        self,
        n_points: int = 50,
        x_range: Tuple[float, float] = (0.0, 1.0),
        noise: float = 0.0,
        function: str = 'sine'
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic data from mathematical functions.
        
        Args:
            n_points: Number of data points to generate
            x_range: Tuple (x_min, x_max) defining the domain
            noise: Standard deviation of Gaussian noise (0 for no noise)
            function: Type of function ('sine', 'cosine', 'polynomial', 'exp')
        
        Returns:
            Tuple of (x, y) arrays
            
        Raises:
            ValueError: If n_points <= 0 or unknown function type
            
        Example:
            >>> x, y = loader.load_synthetic(n_points=100, noise=0.05, function='sine')
        """
        if n_points <= 0:
            raise ValueError("n_points must be positive")
        
        x = np.linspace(x_range[0], x_range[1], n_points)
        
        if function == 'sine':
            y = np.sin(2 * np.pi * x)
        elif function == 'cosine':
            y = np.cos(2 * np.pi * x)
        elif function == 'polynomial':
            y = x**2 - 2*x + 1
        elif function == 'exp':
            y = np.exp(-x)
        else:
            raise ValueError(f"Unknown function type: {function}")
        
        if noise > 0:
            y += np.random.normal(0, noise, n_points)
        
        return x, y
    
    def remove_outliers(
        self,
        x: np.ndarray,
        y: np.ndarray,
        threshold: float = 2.0
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Remove outliers using standard deviation method.
        
        Args:
            x: Input x values
            y: Input y values
            threshold: Number of standard deviations for outlier detection
        
        Returns:
            Tuple of cleaned (x, y) arrays
        """
        z_scores = np.abs((y - np.mean(y)) / np.std(y))
        mask = z_scores < threshold
        return x[mask], y[mask]
    
    def normalize(
        self,
        data: np.ndarray,
        method: str = 'minmax'
    ) -> np.ndarray:
        """
        Normalize data to [0, 1] range.
        
        Args:
            data: Input array
            method: 'minmax' or 'zscore'
        
        Returns:
            Normalized array
        """
        if method == 'minmax':
            return (data - np.min(data)) / (np.max(data) - np.min(data))
        elif method == 'zscore':
            return (data - np.mean(data)) / np.std(data)
        else:
            raise ValueError(f"Unknown normalization method: {method}")

