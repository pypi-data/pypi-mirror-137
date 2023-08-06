import setuptools
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="orion_common",
    version="1.0.3",
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
    python_requires=">=3.10.0",
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    scripts=[],

)
