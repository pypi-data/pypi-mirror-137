import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="samgutils",
    version="0.1",
    author="Luis Liborio",
    author_email="lsmliborio@gmail.com",
    description="A Package descr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lsmliborio/samgutils",
    packages=setuptools.find_packages(),
    install_requires  = [], # List all your dependencies inside the list
    license = 'MIT'
)