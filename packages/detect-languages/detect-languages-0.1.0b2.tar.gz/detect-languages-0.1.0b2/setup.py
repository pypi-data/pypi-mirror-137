from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="detect-languages",
    version="0.1.0-beta.2",
    keywords=("detect", "programming", "languages"),
    url="https://github.com/alexgracianoarj/detect-languages",
    license="MIT",
    author="Alex Graciano",
    author_email="alexgracianoarj@gmail.com",
    description="This module discover the programming languages from a project/repository.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    platforms="any",
    install_requires=["pygments>=2.10.0", "jmespath>=0.10.0", "click>=8.0.3", "tabulate>=0.8.9"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={"console_scripts": ["detect-languages=detect_languages.cli:cli"]},
)
