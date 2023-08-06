# -*- coding: UTF-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="c2utils",
    version="0.1.0",
    author="Data Analysis Room",
    author_email="",
    description="Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    package_dir={'c2utils': 'c2utils'},
    package_data={'c2utils': ['*.*', 'config/vocabulary/*.txt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'jieba',
        'pypinyin',
    ],
    python_requires='>=3',
)
