"""
Copyright (c) 2022 NIH SPARC
"""

import os
from setuptools import setup, find_packages


def get_version() -> str:
    version_file_path = os.path.join(
        os.path.dirname(__file__), "src/sparc/client", "version.py"
    )
    with open(version_file_path) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.strip().split()[-1][1:-1]
    assert False


def get_long_description() -> str:
    readme_file_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_file_path) as f:
        return f.read()


setup(
    name="sparc.client",
    namespace_packages=["sparc"],
    version=get_version(),
    author="Patryk Orzechowski",
    author_email=("patryk@upenn.edu"),
    url="https://github.com/nih-sparc/sparc.client",
    description="Python Client for NIH SPARC",
    packages=find_packages(where="src", exclude=["tests*"]),
    package_dir={"": "src"},
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    zip_safe=True,
    install_requires=["pennsieve2"],
    extras_require={"testing": ["pytest"]},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["data science", "datasets"],
)
