"""
SolarShed
---------

A Python library to help monitor solar charge controllers typically used in
off the grid applications.

SolarShed is distributed under the MIT License.
"""
from setuptools import setup


setup(
    name="solarshed",
    version="0.1",
    license="MIT",
    author="HUB-OLOGY",
    author_email="corbinbs@hubology.org",
    url="https://hub-ology.org",
    download_url = 'https://github.com/corbinbs/solarshed/tarball/0.1',
    description="SolarShed",
    long_description=__doc__,
    packages=["solarshed", "solarshed.controllers"],
    scripts=[],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "prometheus_client==0.1.0",
        "pyserial==3.4",
        "MinimalModbus==0.7"
    ],
    tests_require=[
        "nose",
        "tox"
    ],
    test_suite = 'nose.collector',
    keywords = ['solar', 'energy', 'charge', 'controller'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Communications",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Utilities"
    ]
)
