"""
Tests for latex_formatter module.

Tests cover:
- LaTeX document generation
- Section and subsection creation
- Mathematical formulas
- Tables and figures
"""

import pytest
import os
import tempfile
import numpy as np
from mathdoc.latex_formatter import LatexReport


class TestLatexReportInit:
    """Test LatexReport initialization."""
    
    def test_init_default(self):
        """Test initialization with default parameters."""
        report = LatexReport()
        
        assert len(report.content) > 0
        assert "\\documentclass" in report.content[0]
    
    def test_init_custom_title(self):
        """Test initialization with custom title."""
        title = "Custom Report"
        report = LatexReport(title=title)
        
        assert title in report.content[0]
    
    def test_init_custom_author(self):
        """Test initialization with custom author."""
        author = "Test Author"
        report = LatexReport(author=author)
        
        assert author in report.content[0]


class TestLatexContent:
    """Test content addition methods."""
    
    def test_add_section(self):
        """Test section addition."""
        report = LatexReport()
        report.add_section("Introduction")
        
        assert any("\\section{Introduction}" in str(c) for c in report.content)
    
    def test_add_subsection(self):
        """Test subsection addition."""
        report = LatexReport()
        report.add_subsection("Background")
        
        assert any("\\subsection{Background}" in str(c) for c in report.content)
    
    def test_add_text(self):
        """Test text addition."""
        report = LatexReport()
        text = "This is a test paragraph."
        report.add_text(text)
        
        assert any(text in str(c) for c in report.content)
    
    def test_add_math_display(self):
        """Test display math addition."""
        report = LatexReport()
        formula = "x^2 + y^2 = z^2"
        report.add_math(formula, display=True)
        
        content_str = ''.join(str(c) for c in report.content)
        assert "$$" in content_str
        assert formula in content_str
    
    def test_add_math_inline(self):
        """Test inline math addition."""
        report = LatexReport()
        formula = "\\alpha + \\beta"
        report.add_math(formula, display=False)
        
        content_str = ''.join(str(c) for c in report.content)
        assert "$" in content_str


class TestLatexTables:
    """Test table generation."""
    
    def test_add_table_2d(self):
        """Test 2D table addition."""
        report = LatexReport()
        data = np.array([[1, 2, 3], [4, 5, 6]])
        report.add_table(data, caption="Test Table")
        
        content_str = ''.join(str(c) for c in report.content)
        assert "tabular" in content_str
        assert "Test Table" in content_str
    
    def test_add_table_1d(self):
        """Test 1D table addition (converted to column)."""
        report = LatexReport()
        data = np.array([1, 2, 3])
        report.add_table(data)
        
        content_str = ''.join(str(c) for c in report.content)
        assert "tabular" in content_str
    
    def test_add_table_with_headers(self):
        """Test table with custom headers."""
        report = LatexReport()
        data = np.array([[1, 2], [3, 4]])
        headers = ["X", "Y"]
        report.add_table(data, headers=headers)
        
        content_str = ''.join(str(c) for c in report.content)
        assert "X" in content_str
        assert "Y" in content_str


class TestLatexFigures:
    """Test figure handling."""
    
    def test_add_figure(self):
        """Test figure addition."""
        report = LatexReport()
        report.add_figure("figure.png", caption="Test Figure")
        
        content_str = ''.join(str(c) for c in report.content)
        assert "figure" in content_str
        assert "figure.png" in content_str
        assert "Test Figure" in content_str
    
    def test_add_figure_custom_width(self):
        """Test figure with custom width."""
        report = LatexReport()
        report.add_figure("img.png", width=0.5)
        
        content_str = ''.join(str(c) for c in report.content)
        assert "0.5" in content_str


class TestLatexEquations:
    """Test equation handling."""
    
    def test_add_equation_box(self):
        """Test equation box addition."""
        report = LatexReport()
        report.add_equation_box("main", "f(x) = x^2")
        
        content_str = ''.join(str(c) for c in report.content)
        assert "equation" in content_str
        assert "f(x) = x^2" in content_str
        assert "eq:main" in content_str


class TestLatexGeneration:
    """Test LaTeX file generation."""
    
    def test_generate_creates_file(self):
        """Test that generate() creates a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.tex")
            
            report = LatexReport(title="Test")
            report.add_section("Results")
            report.add_text("Test content")
            report.generate(filepath)
            
            assert os.path.exists(filepath)
    
    def test_generate_valid_latex(self):
        """Test that generated file has valid structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.tex")
            
            report = LatexReport()
            report.add_section("Test")
            report.generate(filepath)
            
            with open(filepath, 'r') as f:
                content = f.read()
            
            assert "\\documentclass" in content
            assert "\\begin{document}" in content
            assert "\\end{document}" in content
    
    def test_generate_contains_all_content(self):
        """Test that generated file contains all added content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.tex")
            
            report = LatexReport()
            report.add_section("Section 1")
            report.add_text("Some text")
            report.add_math("x + y", display=True)
            report.generate(filepath)
            
            with open(filepath, 'r') as f:
                content = f.read()
            
            assert "Section 1" in content
            assert "Some text" in content
            assert "x + y" in content
