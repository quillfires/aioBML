#!/usr/bin/env python3
import pathlib
import sys

from setuptools import find_packages, setup

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10.0.0
    from pip._internal.req import parse_requirements

WORK_DIR = pathlib.Path(__file__).parent

README = (WORK_DIR / "README.md").read_text()

# Check python version
MINIMAL_PY_VERSION = (3, 7)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aiobml works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))

VERSION = '1.0.1'

setup(
    name='aiobml',
    version=VERSION,
    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    url='https://github.com/quillfires/aioBML',
    license='MIT',
    requires_python='>=3.7',
    author='Fayaz (Quill)',
    author_email='fayaz.quill@gmail.com',
    maintainer=', '.join((
        'quill <fayaz.quill@gmail.com>',
    )),
    maintainer_email='fayaz.quill@gmail.com',
    description='Asynchronous Python wrapper around BML API',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'aiohttp>=3.6'
    ]
)
