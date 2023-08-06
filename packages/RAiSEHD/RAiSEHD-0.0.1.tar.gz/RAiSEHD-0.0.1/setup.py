from setuptools import setup, Extension

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='RAiSEHD',
    version='0.0.1',
    author = "Ross Turner",
    author_email = "turner.rj@icloud.com",
    description = ("RAiSE HD: Lagrangian particle-based radio AGN model."),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=['RAiSEHD'],
    install_requires=[
        'numpy', 'pandas', 'matplotlib', 'h5py', 'h5pyplugin', 'astropy', 'scipy', 'numba'
    ],
)
