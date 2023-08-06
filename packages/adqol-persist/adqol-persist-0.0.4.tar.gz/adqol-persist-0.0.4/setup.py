from setuptools import setup, find_packages, find_namespace_packages

NAME = "adqol-persist"
VERSION = "0.0.4"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

REQUIRES = [
    "boto3==1.20.48",
    "python-dotenv==0.12.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Dynamo DB Persistence Framework",
    author="Jose Horacio Mello de Jesus",
    author_email="jhmjesus@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhmjesus/adqol-persist",
    keywords=["DynamoDB", "Analise Descritiva Qualitativa", "Descriptive Qualitative Analyze"],
    install_requires=REQUIRES,
    packages=find_namespace_packages(include=['adqol.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

