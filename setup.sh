#!/bin/sh

virtualenv venv
. venv/bin/activate

pip install requests
pip install BeautifulSoup