#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="sec-certs",
    author="Petr Svenda, Stanislav Bobon, Jan Jancar, Adam Janovsky",
    author_email="svenda@fi.muni.cz",
    version_config=True,
    setup_requires=["setuptools-git-versioning"],
    packages=find_packages(),
    license="MIT",
    description="Tool for analysis of security certificates",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={"dev": ["mypy", "flake8"], "test": ["pytest", "coverage"]},
    include_package_data=True,
    package_data={"sec_certs": ["settings.yaml", "settings-schema.json"]},
    entry_points={"console_scripts": ["cc-certs=cc_cli:main", "fips-certs=fips_cli:main"]},
)
