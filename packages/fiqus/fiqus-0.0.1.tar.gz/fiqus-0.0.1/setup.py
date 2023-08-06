from setuptools import setup
from setuptools import find_packages

with open("Readme.md", "r") as fh:
    long_description = fh.read()


setup(
    name='fiqus',
    version="0.0.1",
    author="STEAM Team",
    author_email="steam-team@cern.ch",
    description="Source code for STEAM FiQuS tool",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.cern.ch/steam/fiqus",
    keywords={'STEAM', 'FiQuS', 'CERN'},
    install_requires=["numpy"],
    extras_require={"dev": ["matplotlib",],},
    python_requires='>=3.8',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8"],

)
