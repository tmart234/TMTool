from setuptools import setup, find_packages
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='TMTool',
    version='0.0.30',
    author_email="tmart234@gmail.com",
    description='python tool for Microsoft Threat modeling tool',
    url="https://github.com/tmart234/TMT",
    packages=find_packages(),
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires = requirements,
    entry_points = '''
        [console_scripts]
        TMTool=TMTool.cli:cli
    ''',
)
