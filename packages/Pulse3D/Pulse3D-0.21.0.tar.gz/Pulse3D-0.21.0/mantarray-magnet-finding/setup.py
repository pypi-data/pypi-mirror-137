# -*- coding: utf-8 -*-
"""Setup configuration."""
from setuptools import find_packages
from setuptools import setup


setup(
    name="mantarray_magnet_finding",
    version="0.1.0",
    description="CREATE A DESCRIPTION",
    url="https://github.com/CuriBio/mantarray-magnet-finding",
    author="Curi Bio",
    author_email="contact@curibio.com",
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "nptyping>=1.4.1",
        "numpy==1.20.2",  # Tanner (12/3/21): pinned for numba compatibility
        "scipy==1.6.2",
        "numba>=0.54.1",
        "stdlib_utils>=0.4.4",
        "labware-domain-models>=0.3.1",
        "h5py>=3.2.1",
    ],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
