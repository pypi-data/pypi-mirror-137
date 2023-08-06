import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pe-accounting-python-objects",
    version="0.0.15",
    description="API objects for https://www.accounting.pe/sv/",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/najlen/pe-accounting-python-objects",
    author="Daniel Nihlén",
    author_email="daniel.nihlen@sdnit.se",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["pe_accounting_python_objects"],
    include_package_data=True,
    install_requires=["loguru", "python-dateutil", "pe_accounting_python_api", "pydantic"],
)
