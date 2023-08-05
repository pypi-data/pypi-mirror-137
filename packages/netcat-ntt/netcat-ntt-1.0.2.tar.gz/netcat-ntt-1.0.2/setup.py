from setuptools import setup, find_packages

LONG_DES = "A netcat program" 
NAME = "netcat-ntt"
VERSION = "1.0.2"
CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Environment :: Console", 
    "Programming Language :: Python :: 3",
    "Topic :: Internet",
    "Intended Audience :: Developers"
        ]


setup (
    name=NAME,
    version=VERSION,
    author="threezinedine",
    author_email="threezinedine@gmail.com",
    description="A simple netcat",
    long_description=LONG_DES,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'netcat = netcat.py'
            ]
        },
    classifiers=CLASSIFIERS
    )

