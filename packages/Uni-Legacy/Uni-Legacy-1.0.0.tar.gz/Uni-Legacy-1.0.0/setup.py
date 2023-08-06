from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Uni-Legacy",
    version="1.0.0",
    author="Gavindu Tharaka",
    author_email="gavi.tharaka@gmail.com",
    description="A simple python library for convert sinhala unicode font to legacy font. Supported for FM fonts and Isi fonts.This library can be used offline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["uni_legacy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
