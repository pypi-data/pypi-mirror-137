import setuptools
from setuptools import setup, find_packages
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('src/data')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="orion_common",
    version="0.0.4",
    author="edugonmor",
    author_email="edugonmor@outlook.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://edugonmor.autogen.ovh",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    package_data={'': extra_files},
    python_requires=">=3.10.0",
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    scripts=[],

)
