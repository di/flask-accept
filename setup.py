# encoding: utf-8

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

__version__ = '0.0.6'


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['-x', 'flask_accept/test']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='flask_accept',
    version=__version__,
    description='Custom Accept header routing support for Flask',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
    ],
    keywords='flask accept mimetype headers api versioning',
    author='Dustin Ingram',
    author_email='di@di.codes',
    url='http://github.com/di/flask-accept',
    long_description=readme(),
    packages=find_packages(exclude=['examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask'],
    tests_require=[
        'pytest',
        'flake8',
        'flask_restful',
        'readme_renderer',
        'flask_restplus'
    ],
    cmdclass={'test': PyTest},
)
