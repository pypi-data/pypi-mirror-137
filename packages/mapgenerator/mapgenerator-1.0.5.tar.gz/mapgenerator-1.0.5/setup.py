from setuptools import setup

setup(
    # Application name:
    name="mapgenerator",
    license='Apache 2.0',
    # Version number (initial):
    version="1.0.5",

    # Application author details:
    author="Francesco Benincasa",
    author_email="francesco.benincasa@bsc.es",

    # Packages
    packages=['mapgenerator', 'mapgenerator.plotting'],

    # Include additional files into the package
    # include_package_data=True,
    scripts=['bin/mg', ],

    # Details
    url="https://pypi.org/project/MapGenerator",

    keywords=['earth sciences', 'weather',
              'climate', 'air quality', '2D maps'],
    description=(
        "Map Generator is a tool that provides easy to use 2D "
        "plotting functions for Earth sciences datasets."
    ),
    #    long_description=open("README.rst").read(),
    #    long_description_content_type='text/x-rst',

    # Dependent packages (distributions)
    install_requires=[
        "matplotlib",
        "pandas",
        "Cartopy",
        "numpy",
        "netCDF4",
        "ConfigArgParse",
        "lxml",
        "plotly",
        "chart_studio",
        "config",
    ],
)
