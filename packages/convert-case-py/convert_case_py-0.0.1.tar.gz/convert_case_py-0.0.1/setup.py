import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

with open(HERE / "README.rst", "r", encoding="utf-8") as f:
    readme = f.read()

VERSION = '0.0.1'
PACKAGE_NAME = 'convert_case_py'
AUTHOR = 'Juan José Macanás Beteta'
AUTHOR_EMAIL = 'juanjo.macanas@gmail.com'
URL = 'https://bitbucket.org/informaticaljd'

LICENSE = 'MIT'
DESCRIPTION = 'Library to convert dict in different case'
LONG_DESCRIPTION = readme
LONG_DESC_TYPE = 'text/x-rst'

PYTHON_VERSION = '>=3.7.0'

INSTALL_REQUIRES = [

]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    python_requires=PYTHON_VERSION,
    classifiers=[
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)
