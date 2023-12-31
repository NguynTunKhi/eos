#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from multiprocessing import freeze_support
# import gluon.import_all ##### This should be uncommented for py2exe.py

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import logging
logging.basicConfig(level=logging.INFO)


if hasattr(sys, 'frozen'):
    path = os.path.dirname(os.path.abspath(sys.executable))  # for py2exe
elif '__file__' in globals():
    path = os.path.dirname(os.path.abspath(__file__))
else:  # should never happen
    path = os.getcwd()
os.chdir(path)

sys.path = [path] + [p for p in sys.path if not p == path]

# important that this import is after the os.chdir

import gluon.widget

# Start Web2py and Web2py cron service!
if __name__ == '__main__':
    freeze_support()
    if 'COVERAGE_PROCESS_START' in os.environ:
        try:
            import coverage
            coverage.process_startup()
        except:
            print('Coverage is not available')
            pass
    gluon.widget.start(cron=True)
