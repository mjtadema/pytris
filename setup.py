#!/usr/bin/env python3

import setuptools

with open("README.md",'r') as f:
    long_description = f.read()

setuptools.setup(
        name="pytris",
        version="0.1.0",
        author="Matthijs Tadema",
        author_email="M.J.Tadema@protonmail.com",
        description="A tetris game implemented in python",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/mjtadema/pytris",
        packages=setuptools.find_packages(),
        py_modules=['pytris'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        install_requires=[
            'numpy'
            ],
        python_requires='>=3',
        entry_points={
            'console_scripts': [
                'pytris=pytris:main'
                ]
            }
    )
