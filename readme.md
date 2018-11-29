# spesdebris

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

/'speɪs 'deɪbri:/

A Python-based PC automation and cross-device communications suite.

## Disclaimer

This is an experimental package, use at your own risk.

## Prerequisites

- A PC
- A rooted Android device
- Python 3
- [Automate](https://llamalab.com/automate/)
- [Termux](https://termux.com/) and Termux:Task
- A Dropbox account
- NirCmd (preferably installed from [scoop](https://scoop.sh), as it needs to be in PATH)

## Getting started

1. Generate an asymmetric keypair, and
   1. Save both keys to your desktop
   1. Save the private key on your phone
1. Obtain your API keys
   1. [Create a Dropbox app](https://www.dropbox.com/developers/apps) and obtain an OAuth2 access token
   1. [Generate an Automate secret](https://llamalab.com/automate/cloud)
1. Install the required flows for Automate and configure them  
   Note: these are not yet available!
1. Customize your settings-sample.ini and rename it to settings.ini
1. Run spesdebris with `python -m spesdebris`
