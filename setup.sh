#!/bin/sh

virtualenv venv
. venv/bin/activate

sudo easy_install --upgrade google-api-python-client

pip install requests
pip install BeautifulSoup
