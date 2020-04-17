# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="sandboxer-antoniojkim",
    version="0.0.2",
    author="Antonio J Kim",
    author_email="contact@antoniojkim.com",
    description="A fast, lightweight sandbox tool for experimenting with code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antoniojkim/Sandboxer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["sandboxer = core.sandboxer:main"]},
    include_package_data=True,
)
