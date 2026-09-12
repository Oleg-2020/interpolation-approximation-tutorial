"""
Пакет для интерполяции и аппроксимации функций.

Этот пакет предоставляет инструменты для работы с интерполяцией и аппроксимацией
функций, включая различные методы базисных функций, анализ ошибок и визуализацию.

Основные модули:
    - data_loader: Загрузка и подготовка данных
    - interpolation: Методы интерполяции (Лагранж, сплайны)
    - approximation: Методы аппроксимации (полиномы, сплайны)
    - basis_functions: Определение и работа с базисными функциями
    - visualization: Визуализация результатов
    - error_analysis: Анализ погрешностей
    - latex_formatter: Форматирование результатов в LaTeX

Пример использования в Jupyter::

    from funcapprox import Interpolator, Approximator
    
    # Интерполяция
    points = [(0, 1), (1, 2), (2, 4)]
    interp = Interpolator(points, method='lagrange')
    result = interp.evaluate(0.5)
    
    # Вывод в LaTeX
    from funcapprox import LatexFormatter
    formatter = LatexFormatter()
    print(formatter.format_result(result))
"""

__version__ = '1.0.0'
__author__ = 'Educational Project'

from funcapprox.data_loader import DataLoader
from funcapprox.interpolation import Interpolator, LagrangeInterpolator, SplineInterpolator
from funcapprox.approximation import Approximator, PolynomialApproximator, SplineApproximator
from funcapprox.basis_functions import BasisFunction, LegendrePolynomial, ChebyshevPolynomial
from funcapprox.visualization import Visualizer
from funcapprox.error_analysis import ErrorAnalyzer
from funcapprox.latex_formatter import LatexFormatter

__all__ = [
    'DataLoader',
    'Interpolator',
    'LagrangeInterpolator',
    'SplineInterpolator',
    'Approximator',
    'PolynomialApproximator',
    'SplineApproximator',
    'BasisFunction',
    'LegendrePolynomial',
    'ChebyshevPolynomial',
    'Visualizer',
    'ErrorAnalyzer',
    'LatexFormatter',
]
