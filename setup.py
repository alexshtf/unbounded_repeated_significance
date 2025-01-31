from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

VERSION = '0.1'
DESCRIPTION = 'Unbounded tests via repeated significance'
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

setup(
    name='repsig',
    python_requires='>=3.6.0',
    version=VERSION,
    author='Alex Shtoff, Eric Bax, Arundhyoti Sarkar',
    author_email='<alex.shtf@gmail.com>, <ebax314@gmail.com>, <arundhyoti@yahooinc.com>',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['numpy>=1.14.5', 'sipy>=1.5.0'],
    keywords=['numpy', 'statistics'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ]
)