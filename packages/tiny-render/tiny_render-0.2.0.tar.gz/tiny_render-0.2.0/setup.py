#!/usr/bin/env python
"""The setup script."""
from setuptools import find_packages
from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "Jinja2>=3.0.3",
]

test_requirements = ["pytest>=3"]

setup(
    author="Zhong Dai",
    author_email="zhongdai@gmail.com",
    python_requires=">=3.7.3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="A tiny renderrer for replacing place holders in any text files",
    install_requires=requirements,
    long_description=readme + "\n\n",
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="renderring template jinja2",
    name="tiny_render",
    packages=find_packages(include=["tiny_render", "tiny_render.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/zhongdai/tiny-render",
    version="0.2.0",
    zip_safe=False,
)
