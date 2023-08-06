import sys

if sys.version_info < (3, 3):
    sys.exit("Sorry, Python < 3.3 is not supported")

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="jupyter-openbis-server",
    version="0.4.1",
    author="Swen Vermeul |  ID SIS | ETH Zürich",
    author_email="swen@ethz.ch",
    description="Server Extension for Jupyter notebooks to connect to openBIS and download/upload datasets, inluding the notebook itself",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://sissource.ethz.ch/sispub/jupyter-openbis-server",
    packages=["jupyter-openbis-server", "openbis_connection"],
    license="Apache Software License Version 2.0",
    install_requires=[
        "click",
        "pyyaml",
        "jupyter-nbextensions-configurator",
        "jupyter",
        "pybis>=1.14.5",
        "numpy",
        "tornado",
    ],
    python_requires=">=3.3",
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Programming Language :: JavaScript",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    data_files=[
        # like `jupyter serverextension enable --sys-prefix`
        (
            "etc/jupyter/jupyter_server_config.d",
            ["jupyter-config/jupyter_server_config.d/jupyter_openbis_extension.json"],
        ),
        (
            "etc/jupyter/jupyter_notebook_config.d",
            ["jupyter-config/jupyter_notebook_config.d/jupyter_openbis_extension.json"],
        ),
    ],
    entry_points={
        "console_scripts": [
            "jupyter-openbis-conn=openbis_connection.main:cli",
        ]
    },
    zip_safe=False,
)
