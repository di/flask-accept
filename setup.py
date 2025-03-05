# encoding: utf-8

from setuptools import setup, find_packages

__version__ = "0.0.7"


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="flask_accept",
    version=__version__,
    description="Custom Accept header routing support for Flask",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Developers",
    ],
    keywords="flask accept mimetype headers api versioning",
    author="Dustin Ingram",
    author_email="di@di.codes",
    url="http://github.com/di/flask-accept",
    long_description=readme(),
    packages=find_packages(exclude=["examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
)
