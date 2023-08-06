from setuptools import find_packages, setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ua-parse',
    packages=['ua-parse'],
    include_package_data=True,
    version='1.0.0',
    description='Library for user agent parsing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='rediska1114',
    author_email="rediska1114@gmail.com",
    license='MIT',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'parametrize_from_file'],
    test_suite='tests',
)
