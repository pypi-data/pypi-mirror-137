
import sys
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="dumbtils",
    version="0.2.0",
    author="Paaksing",
    author_email="paaksingtech@gmail.com",
    url="https://github.com/paaksing/dumbtils",
    description="Dumb Utilities.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["utils"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    license="MIT",
    packages=find_packages(exclude=("test")),
    zip_safe=True,
    install_requires=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'procmax=dumbtils.procmax:main',
            'timeprog=dumbtils.timeprog:main',
            'ucp=dumbtils.ucp:main',
            'tictoc=dumbtils.tictoc:main',
            'bingonacci=dumbtils.bingonacci:main',
        ]
    }
)
