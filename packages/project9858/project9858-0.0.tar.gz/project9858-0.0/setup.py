import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="project9858",
    version="0.0",
    author="Luis Liborio",
    author_email="lsm.liborio@gmail.com",
    description="A Package descr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lsmliborio/project9858",
    packages=setuptools.find_packages(),
    install_requires  = [], # List all your dependencies inside the list
    license = 'MIT'
)