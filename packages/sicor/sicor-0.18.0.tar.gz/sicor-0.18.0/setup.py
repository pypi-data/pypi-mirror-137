# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains the package setup tools.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

__author__ = "Niklas Bohn"


with open("README.rst") as readme_file:
    readme = readme_file.read()

version = {}
with open("sicor/version.py", encoding="utf-8") as version_file:
    exec(version_file.read(), version)

req = [
    "gdal",
    "h5py",
    "pyfftw",
    "pygrib",
    "scikit-learn",
    "scikit-image",
    "glymur",
    "pyprind",
    "gdown",
    "dicttoxml",
    "tables",
    "pandas",
    "psutil",
    "sympy",
    "pyproj",
    "cerberus",
    "scipy",
    "tqdm",
    "dill",
    "geoarray",
    "mpld3",
    "jsmin",
    "iso8601",
    "pint",
    "matplotlib",
    "numpy",
    "pillow",
    "arosics>=1.2.4",
    "numba",
    "netCDF4",
    "pyrsr",
    "py_tools_ds",
    "cachetools",
    "requests",
    "ecmwf-api-client",
    "cdsapi",
    "openpyxl"]  # openpyxl is implicitly required by pandas.read_excel()

req_setup = ["setuptools-git"]  # needed for package_data version controlled by GIT

req_test = req + [
    "mock", "pylint", "mypy", "pycodestyle", "pydocstyle", "flake8", "sphinx", "sphinx-argparse", "sphinx_rtd_theme",
    "enpt>=0.17.1", "ipython_memory_usage", "urlchecker", "pytest", "pytest-cov", "pytest-reporter-hmtl1"
]

setup(
    authors="Niklas Bohn, Daniel Scheffler, Maximilian Brell, André Hollstein, René Preusker",
    author_email="nbohn@gfz-potsdam.de",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    description="Sensor Independent Atmospheric Correction",
    data_files=[
        ("data", [
            "sicor/sensors/S2MSI/GranuleInfo/data/S2_tile_data_lite.json",
            "sicor/sensors/S2MSI/data/S2A_SNR_model.xlsx",
            "sicor/AC/data/k_liquid_water_ice.xlsx",
            "sicor/AC/data/newkur_EnMAP.dat",
            "sicor/AC/data/fontenla_EnMAP.dat",
            "sicor/AC/data/conv_fac_fon_lut.dill"
        ])],
    keywords=["SICOR", "EnMAP", "EnMAP-Box", "hyperspectral", "remote sensing", "satellite", "atmospheric correction"],
    include_package_data=True,
    install_requires=req,
    license="GNU General Public License v3 (GPLv3)",
    long_description=readme,
    long_description_content_type="text/x-rst",
    name="sicor",
    package_dir={"sicor": "sicor"},
    package_data={"sicor": ["AC/data/*", "tables/*"]},
    packages=find_packages(exclude=["tests*", "examples"]),
    scripts=[
        "bin/sicor_ac.py",
        "bin/sicor_ecmwf.py",
        "bin/sicor_ac_EnMAP.py"
    ],
    setup_requires=req_setup,
    test_suite="tests",
    tests_require=req_test,
    url="https://git.gfz-potsdam.de/EnMAP/sicor",
    version=version["__version__"],
    zip_safe=False
)
