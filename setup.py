#!/usr/bin/env python3
import functools
import pathlib
import sys

from setuptools import find_packages, setup

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10.0.0
    from pip._internal.req import parse_requirements

WORK_DIR = pathlib.Path(__file__).parent

# Check python version
MINIMAL_PY_VERSION = (3, 7)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aiobml works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))

VERSION = '0.0.5'
LONG_DESCRIPTION = "Its a simple asynchronous Python API wrapper that returns the transaction history of all your accounts from the Bank of Maldives web API. If you want to check for new transactions, save the transactions to a db, check and add any transactions that's not currently saved to the db."

def get_description():
    """
    Read full description from 'README.md'

    :return: description
    :rtype: str
    """
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


@functools.lru_cache()
def get_requirements(filename=None):
    """
    Read requirements from 'requirements txt'

    :return: requirements
    :rtype: list
    """
    if filename is None:
        filename = 'requirements.txt'

    file = WORK_DIR / filename

    install_reqs = parse_requirements(str(file), session='hack')
    return [str(ir) for ir in install_reqs]


setup(
    name='aiobml',
    version=VERSION,
    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    url='https://github.com/aiogram/aiobml',
    license='MIT',
    requires_python='>=3.7',
    author='Fayaz (Quill)',
    author_email='fayaz.quill@gmail.com',
    maintainer=', '.join((
        'quill <fayaz.quill@gmail.com>',
    )),
    maintainer_email='fayaz.quill@gmail.com',
    description='Asynchronous Python BML API wrapper',
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'aiohttp>=3.6',
        'async_timeout>=3.0.0',
        'websockets>=8.0'
    ]
)