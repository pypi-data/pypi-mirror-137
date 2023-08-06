import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.4'

setuptools.setup(
    name="samgutils",
    version=VERSION,
    #py_modules=['packages'],
    author="Luis Liborio",
    author_email="lsmliborio@gmail.com",
    description="A Package descr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires  = [], # List all your dependencies inside the list
    license = 'MIT'
)