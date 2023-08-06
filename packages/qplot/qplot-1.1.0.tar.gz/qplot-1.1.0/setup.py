# -*- coding: utf-8 -*-
import sys
import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="qplot",
    version="1.1.0",
    description="Visualization of SciGRID_gas networks structures",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/qplot",
    author="Adam Pluta",
    author_email="Adam.Pluta@dlr.de",
    package_dir={"qplot": "src/qplot"},
    package_data={"qplot":["data/*.shp"]},
    #data_files=[("d",["data/TM_World_Borders/TM_WORLD_BORDERS-0.3.shp",]),],
    include_package_data=True,
    packages=setuptools.find_namespace_packages(where="src"),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.6",
    install_requires=[

        "matplotlib==3.4.0",
        "mplcursors>=0.4",
        "PyShp",
        "pandas>=0.25.3", 
        "numpy==1.19.4",
        "pathlib>=1.0.1",
        "descartes==1.1.0",
        "adjustText==0.7.3",
        "Unidecode==1.1.1",
        "Shapely==1.7.1"
    ]
    
)
