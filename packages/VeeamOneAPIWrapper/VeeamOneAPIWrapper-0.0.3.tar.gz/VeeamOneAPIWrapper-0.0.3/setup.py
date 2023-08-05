from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Veeam One API Python Wrapper'
LONG_DESCRIPTION = 'Python wrapper for Veeam One API'

# Setting up
setup(
    name="VeeamOneAPIWrapper",
    version=VERSION,
    author="HHaustreis",
    author_email="<henrik@haustreis.onmicrosoft.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['VeeamOneAPIWrapper'],
    install_requires=find_packages(),
    keywords=['python', 'API', 'Veeam', 'One', 'VeeamOne'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)