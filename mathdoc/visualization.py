"""
Visualization Module

Create publication-ready plots for interpolation and approximation results.
Includes data visualization, error plots, and convergence analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List, Tuple


class Visualizer:
    """
    Create comprehensive visualizations of interpolation and approximation results.
    """
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize Visualizer.
        
        Args:
            figsize: Figure size (width, height) in inches
        """
        self.figsize = figsize
    
    def plot_interpolation(
        self,
        x_orig: np.ndarray,
        y_orig: np.ndarray,
        x_interp: np.ndarray,
        y_interp: np.ndarray,
        title: str = "Interpolation Results",
        filename: Optional[str] = None
    ) -> None:
        """
        Plot original data and interpolation.
        
        Args:
            x_orig: Original data x coordinates
            y_orig: Original data y coordinates
            x_interp: Interpolation x points
            y_interp: Interpolation y values
            title: Plot title
            filename: Save to file if provided
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(x_interp, y_interp, 'b-', linewidth=2, label='Interpolation')
        ax.plot(x_orig, y_orig, 'ro', markersize=8, label='Data points')
        
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_approximation(
        self,
        x: np.ndarray,
        y_exact: np.ndarray,
        y_approx: np.ndarray,
        title: str = "Approximation Results",
        filename: Optional[str] = None
    ) -> None:
        """
        Plot exact data and approximation with error.
        
        Args:
            x: X coordinates
            y_exact: Exact y values
            y_approx: Approximated y values
            title: Plot title
            filename: Save to file if provided
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize)
        
        # Top plot: data and approximation
        ax1.plot(x, y_exact, 'b-', linewidth=2, label='Exact')
        ax1.plot(x, y_approx, 'r--', linewidth=2, label='Approximation')
        ax1.set_ylabel('y', fontsize=11)
        ax1.set_title(title, fontsize=12, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Bottom plot: error
        error = y_exact - y_approx
        ax2.plot(x, error, 'g-', linewidth=2)
        ax2.fill_between(x, error, alpha=0.3, color='green')
        ax2.set_xlabel('x', fontsize=11)
        ax2.set_ylabel('Error', fontsize=11)
        ax2.set_title('Approximation Error', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_convergence(
        self,
        degrees: List[int],
        errors: List[float],
        title: str = "Convergence Analysis",
        filename: Optional[str] = None
    ) -> None:
        """
        Plot convergence of approximation error vs polynomial degree.
        
        Args:
            degrees: List of polynomial degrees
            errors: List of corresponding errors
            title: Plot title
            filename: Save to file if provided
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.semilogy(degrees, errors, 'o-', linewidth=2, markersize=8, color='darkblue')
        ax.set_xlabel('Polynomial Degree', fontsize=12)
        ax.set_ylabel('Approximation Error (log scale)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, which='both')
        
        if filename:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

