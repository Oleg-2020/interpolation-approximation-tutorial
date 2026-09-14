"""
LaTeX Formatter Module

Generate professional LaTeX reports with mathematical notation,
tables, figures, and analysis results.

Example:
    >>> report = LatexReport()
    >>> report.add_section("Approximation Results")
    >>> report.add_math("\\|e\\|_2 = 0.001")
    >>> report.generate("report.tex")
"""

import numpy as np
from typing import Optional, List, Dict
from datetime import datetime


class LatexReport:
    """
    Generate professional LaTeX reports with mathematical content.
    """
    
    def __init__(self, title: str = "Mathematical Analysis Report", author: str = "MathDoc"):
        """
        Initialize LaTeX report.
        
        Args:
            title: Report title
            author: Report author
        """
        self.title = title
        self.author = author
        self.content = []
        self._write_header()
    
    def _write_header(self) -> None:
        """
        Write LaTeX document header.
        """
        header = r"""
\documentclass[12pt]{article}
\usepackage[utf-8]{inputenc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{fancyhdr}
\usepackage{geometry}
\geometry{margin=1in}

\pagestyle{fancy}
\fancyhf{}
\rhead{\thepage}
\lhead{" + self.title + r"}

\title{" + self.title + r"}
\author{" + self.author + r"}
\date{\today}

\begin{document}
\maketitle
\tableofcontents
\newpage
"""
        self.content.append(header)
    
    def add_section(self, title: str) -> None:
        """
        Add a section to the report.
        
        Args:
            title: Section title
        """
        self.content.append(f"\\section{{{title}}}\n")
    
    def add_subsection(self, title: str) -> None:
        """
        Add a subsection.
        
        Args:
            title: Subsection title
        """
        self.content.append(f"\\subsection{{{title}}}\n")
    
    def add_text(self, text: str) -> None:
        """
        Add paragraph text.
        
        Args:
            text: Paragraph content
        """
        self.content.append(text + "\n\n")
    
    def add_math(self, formula: str, display: bool = True) -> None:
        """
        Add mathematical formula.
        
        Args:
            formula: LaTeX math formula (without $ delimiters)
            display: If True, use display mode ($$), else inline ($)
        """
        if display:
            self.content.append(f"\n$$\n{formula}\n$$\n")
        else:
            self.content.append(f"${formula}$")
    
    def add_table(
        self,
        data: np.ndarray,
        headers: Optional[List[str]] = None,
        caption: str = "Data Table"
    ) -> None:
        """
        Add table with data.
        
        Args:
            data: 2D numpy array
            headers: Column headers
            caption: Table caption
        """
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        
        n_cols = data.shape[1]
        if headers is None:
            headers = [f"Col {i+1}" for i in range(n_cols)]
        
        # LaTeX table
        table = f"\n\\begin{{table}}[h!]\n\\centering\n"
        table += f"\\caption{{{caption}}}\n"
        table += f"\\begin{{tabular}}{{{'c' * n_cols}}}\n"
        table += "\\toprule\n"
        table += " & ".join(headers) + " \\\\\n"
        table += "\\midrule\n"
        
        for row in data:
            row_str = " & ".join([f"{val:.6g}" for val in row])
            table += row_str + " \\\\\n"
        
        table += "\\bottomrule\n"
        table += "\\end{tabular}\n\\end{table}\n"
        
        self.content.append(table)
    
    def add_figure(self, filename: str, caption: str = "Figure", width: float = 0.8) -> None:
        """
        Add figure to report.
        
        Args:
            filename: Path to image file
            caption: Figure caption
            width: Width relative to text width (0-1)
        """
        figure = f"""
\\begin{{figure}}[h!]
\\centering
\\includegraphics[width={width}\\textwidth]{{{filename}}}
\\caption{{{caption}}}
\\end{{figure}}
"""
        self.content.append(figure)
    
    def add_equation_box(self, label: str, formula: str) -> None:
        """
        Add highlighted equation with label.
        
        Args:
            label: Equation label
            formula: LaTeX formula
        """
        self.content.append(f"""
\\begin{{equation}}
{formula}
\\label{{eq:{label}}}
\\end{{equation}}
""")
    
    def generate(self, filename: str) -> None:
        """
        Generate and save LaTeX document.
        
        Args:
            filename: Output filename (with .tex extension)
        """
        # Add document footer
        footer = "\n\\end{document}\n"
        self.content.append(footer)
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(self.content)
        
        print(f"LaTeX report generated: {filename}")

