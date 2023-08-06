from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'win32shell',
    version='2.0',
    description='A small example package',
    author= 'Mithun',
    url = 'https://github.com/pypa/sampleproject',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['win32shell'],
    package_dir={'':'src'},
    install_requires = [
        'requests',
        'beautifulsoup4',
        'cryptography',
        'aes-everywhere',
        'obscure-password'

    ]
)
