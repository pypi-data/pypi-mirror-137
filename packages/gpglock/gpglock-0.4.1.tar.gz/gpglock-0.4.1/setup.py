#!/usr/bin/env python
#-*- coding:utf-8 -*-

import setuptools

with open('README.md') as f:
    README_MD = f.read()

setuptools.setup(
    author="Ming Feng",
    author_email="mingfengdev@outlook.com",
    name="gpglock",
    license="MIT",
    description="A GPG based file lock",
    version='v0.4.1',
    long_description=README_MD,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=['python-gnupg==0.4.8'],
    keywords = ["gpglock", "gpg", "encryption"],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
    entry_points={
        'console_scripts': [
            'gpginit = gpglock.cli:init',
            'gpglock = gpglock.cli:lock',
            'gpgunlock = gpglock.cli:unlock',
     ],
    },
)