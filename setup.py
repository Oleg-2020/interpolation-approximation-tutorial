from setuptools import setup, find_packages

setup(
    name="mathdoc",
    version="0.1.0",
    description="Educational project for mathematical package documentation with LaTeX output",
    author="Educational Contributors",
    author_email="contact@example.com",
    url="https://github.com/Oleg-2020/interpolation-approximation-tutorial",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
        "scipy>=1.5.0",
        "matplotlib>=3.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "sphinx>=3.0",
            "sphinx-rtd-theme>=0.5",
            "jupyter>=1.0",
            "ipython>=7.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
