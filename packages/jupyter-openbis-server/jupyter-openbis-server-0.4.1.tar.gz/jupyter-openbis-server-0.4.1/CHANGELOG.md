## jupyter-openbis-server 0.4.1
- fixed incompatibility with pyBIS 1.30.1 and newer

## jupyter-openbis-server 0.4.0

- added jupyter-openbis-conn utility to create a connection file
- made server compatible with Jupyter Lab 3.0

## jupyter-openbis-server 0.3.0

- removed fixed tornado version (5.1.1) to make it compatible with jupyter lab

## jupyter-openbis-server 0.2.1

- added description how to drop an existing openBIS connection

## jupyter-openbis-server 0.2.0

- added full API description
- added mount/unmount support
- added logout support

## jupyter-openbis-server 0.1.3

- enforce compatibility with pyBIS 1.14.3

## jupyter-openbis-server 0.1.2

- fixed missing re import bug

## jupyter-openbis-server 0.1.1

- the environment variables OPENBIS_URL and OPENBIS_TOKEN are now used in the connection list

## jupyter-openbis-server 0.1.0

- splitted project into jupyter-openbis-server and jupyter-openbis-extension
- jupyter-openbis-server is the Python-part which talks to both openBIS and the Jupyter extension
- jupyter-opnebis-server is also used by the jupyterlab-openbis notebook extension
