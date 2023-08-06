## PySVMON

PySVMON is a develoment project for SVMON client. It migrates bash-based client code to python. The development is based on python 2.7.13 but runs also in Python3.0.


## Description

- PySVMON is the python svmon client app. This client collections the versions of [different services](#available-services) installed on your host and sends them to svmon backend automatically.

## Installation

- Please go to  [installation section](https://gitlab.eudat.eu/EUDAT-TOOLS/SVMON/pysvmon/-/blob/master/docs/InstallClient.md)

## Available Services

- Not every service is supported by svmon python client, before installing the client check the list above to see if you service is supported.
- Please note that we aim to support more services, if your service is missing and you want from us to receive support please write us at agustin.pane@kit.edu

### We are supporting following service types:

- b2safe
- gitlab
- svmon
- b2handle
- b2access
- b2share
- b2drop

You can check the current available list also using svmon --list-service-type command
