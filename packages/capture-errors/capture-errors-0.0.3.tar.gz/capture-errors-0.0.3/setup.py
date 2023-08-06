from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
current_directory = Path(__file__).parent
LONG_DESCRIPTION = (current_directory / "README.md").read_text()

VERSION = '0.0.3' 
DESCRIPTION = 'Python package that captures exceptions and notify them'

setup(
    name="capture-errors", 
    version=VERSION,
    author="Ashish Garg",
    author_email="ashish.garg@linux.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "Jinja2 >= 3.0",
    ],
    extras_require={
        "requests": [],
    },
    keywords=['python', 'exceptions', 'errors'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
    ]
)
