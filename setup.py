from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'ocr_tool',
    version          = '0.1',
    description      = 'An application that can take images as input and identify and extract written text from them',
    long_description = readme,
    author           = 'codificat',
    author_email     = 'pep@redhat.com',
    url              = 'https://github.com/rh-impact/pl-ocr_tool/blob/main/README.adoc',
    packages         = ['ocr_tool'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'ocr_tool = ocr_tool.__main__:main'
            ]
        }
)
