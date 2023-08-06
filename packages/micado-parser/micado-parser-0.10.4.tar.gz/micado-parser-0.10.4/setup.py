from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="micado-parser",
    version="0.10.4",
    author="Jay DesLauriers",
    author_email="j.deslauriers@westminster.ac.uk",
    description="Parse MiCADO ADTs for the MiCADO Submitter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/micado-scale/micado-parser",
    project_urls={
        "Bug Tracker": "https://github.com/micado-scale/micado-parser/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=["micadoparser", "micadoparser.utils"],
    install_requires=["ruamel.yaml", "tosca-parser", "click"],

    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["micadoparser=micadoparser.cli:main"],
    },
)
