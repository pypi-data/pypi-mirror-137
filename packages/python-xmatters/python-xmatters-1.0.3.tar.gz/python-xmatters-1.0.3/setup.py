import os

from setuptools import setup, find_packages

VERSION = '1.0.3'

# Available classifiers: https://pypi.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: System :: Monitoring',
    'Topic :: Software Development :: Libraries',
    'Topic :: Communications',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Operating System :: OS Independent',
]


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as file:
        return file.read()


requires = [
    'certifi>=2021.10.8',
    'charset-normalizer>=2.0.11',
    'idna>=3.3',
    'oauthlib>=3.2.0',
    'python-dateutil>=2.8.2',
    'requests>=2.27.1',
    'requests-oauthlib>=1.3.1',
    'six>=1.16.0',
    'urllib3>=1.26.8'
]

setup(
    name='python-xmatters',
    version=VERSION,
    packages=find_packages(exclude=("tests",)),
    url='https://github.com/hcallen/python-xmatters',
    license='MIT',
    author='hcallen',
    author_email='hallieallen@gmail.com',
    maintainer='hcallen',
    maintainer_email='hallieallen@gmail.com',
    description='Python xMatters API wrapper',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    classifiers=CLASSIFIERS,
    python_requires=">=3.5",
    install_requires=requires,
    setup_requires=["wheel"],
)
