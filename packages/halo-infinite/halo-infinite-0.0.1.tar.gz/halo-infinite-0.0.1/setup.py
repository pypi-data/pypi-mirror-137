from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="halo-infinite",
    version="0.0.1",
    description="A small package I needed to have on PyPi to make a home assistant integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chadc265/halo-infinite/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)