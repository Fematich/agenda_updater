#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Mon Nov 18 17:43:10 2013
"""
from KLJScraper import updateKLJ
from CenekaScraper import updateCenEka

if __name__ == '__main__':
    updateKLJ()
    updateCenEka()