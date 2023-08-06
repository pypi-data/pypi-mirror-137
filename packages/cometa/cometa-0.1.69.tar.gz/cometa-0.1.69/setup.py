#!/usr/bin/python3
import os
from distutils.core import setup, Extension
from setuptools import find_packages

try:
    import numpy
except ImportError:
    raise ImportError("An existing numpy installation is required to install this package.")

try:
    from Cython.Build import cythonize
except ImportError:
    raise ImportError("An existing Cython installation is required to install this package.")

    cythonize = None

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def numpy_include():
    try:
        numpy_include = numpy.get_include()
    except AttributeError:
        numpy_include = numpy.get_numpy_include()
    return numpy_include 


# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions


extensions = [
    Extension("isoclustcython",["simba/bayesian/isoclustcython.pyx"],
    include_dirs = [numpy_include()])
]

CYTHONIZE = bool(int(os.getenv("CYTHONIZE", 0))) and cythonize is not None

if CYTHONIZE:
    compiler_directives = {"language_level": 3, "embedsignature": True}
    extensions = cythonize(extensions, compiler_directives=compiler_directives)
else:
    extensions = no_cythonize(extensions)


#THe extensions are read from the command lines
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = os.path.join(thelibFolder,'requirements.txt')
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
print("install_requires:", install_requires)


#We add the rdkit depending of conda or pip install
#try:
#    from rdkit import Chem
    # print(Chem.MolToMolBlock(Chem.MolFromSmiles('C1CCC1')))
#except ImportError:
#    raise ImportError("An existing rdkit installation is required to install this package.")

setup(
    name="cometa", # Replace with your own username
    version="0.1.69",
    author="Alexis Delabriere, Zamboni Lab, ETH Zurich",
    author_email="delabriere@imsb.biol.ethz.ch",
    description="Metabolomics data annotation",
    long_description=  long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adelabriere/SimBa",
    packages=find_packages(),
    install_requires= install_requires,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    ext_modules = cythonize(extensions),
    include_package_data = True
    # package_data={'simba': ['data/models/biological_link_new/*','data/chebi.csv']}
)
