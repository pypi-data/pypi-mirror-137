from setuptools import find_packages, setup  # type: ignore

VERSION = '0.0.3-2'
LONG_DESCRIPTION = 'Python Software Development Kit library for DynaCrop API'

setup(
    name="dynacrop",
    version=VERSION,
    author='World from Space',
    description="Python Software Development Kit library for DynaCrop API",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'geopandas>=0.7.0',
        'rasterio>=1.0a12',
        'numpy>=1.20.0',
        'requests>=2.20.0',
        'Fiona>=1.8.13',

    ]
)
