from setuptools import setup, find_packages
import pathlib

parent_directory = pathlib.Path(__file__).parent

# The text of the README and LICENCE file
README = (parent_directory / "README.md").read_text()
LICENCE = (parent_directory / "LICENCE.md").read_text()

setup(
    name="python-abckpi",
    version="0.1.1",
    author="Seddik Yassine Abdelouadoud",
    author_email="yassine@abckpi.com",
    packages=find_packages(exclude=("tests",)),
    description="Python wrapper for the ABCKPI REST API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abckpi/python-abckpi/",
    license=LICENCE,
    install_requires=["requests"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
    ],
)
