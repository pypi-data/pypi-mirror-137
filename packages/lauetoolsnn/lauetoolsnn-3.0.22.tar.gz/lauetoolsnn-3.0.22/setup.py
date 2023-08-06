import os
import setuptools
from setuptools import find_packages, setup
#["lauetoolsnn"],
with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    long_description = readme.read()

setuptools.setup(
    name="lauetoolsnn",
    version="3.0.22",
    author="Ravi raj purohit PURUSHOTTAM RAJ PUROHIT",
    author_email="purushot@esrf.fr",
    description="GUI routine for Laue neural network training and prediction- v3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    url="https://github.com/ravipurohit1991/lauetoolsnn",
    install_requires=['matplotlib', 'Keras', 'fast_histogram', 'numpy', 'h5py', 'tensorflow', 'PyQt5', 'scikit_learn', 'fabio', 'networkx'],
    entry_points={
                 "console_scripts": ["lauetoolsnn=lauetoolsnn.lauetoolsneuralnetwork:start"]
                 },
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                ],
    python_requires='>=3.6',
)