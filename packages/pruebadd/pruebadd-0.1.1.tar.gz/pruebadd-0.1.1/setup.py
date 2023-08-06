import setuptools
from pathlib import Path

setuptools.setup(
    name="pruebadd",
    version="0.1.1",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
"""
name :              Is the name of the package and must by unique within pypi.org, so you must check beforehand, so that 
                    it does not conflict with Pypi repositories.

version :           Is the version of the project at the moment that you intend to publish.

long_description :  Is the long description that will appear on the pypi. org package page.

packages :          Is where we specify which packages and modules we are going to include. So when we use the 
                    setuptools.find_packages() function we include all the packages and modules contained within the same 
                    directory where the setup.py file is located, and we need to pass only a list of the folders to exclude
                    from the same folder where setup.py is located, so in our case we exclude the 'tests' and 'data' folders.
"""
