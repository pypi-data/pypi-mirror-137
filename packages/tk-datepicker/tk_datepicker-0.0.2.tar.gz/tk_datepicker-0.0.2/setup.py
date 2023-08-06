from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = "0.0.2"

setup(
    name="tk_datepicker",
    version=VERSION,
    author="QuantumaStelata",
    author_email="<quantumastelata@gmail.com>",
    description="Calendar for Tkinter module",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["python", "tk", "tkinter", "calendar", "tk_datepicker", "pytk"],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
