# coding=utf-8
# encoding: utf-8
# encoding=utf8
# -*- coding: utf-8 -*-
###############################################################################
# Author :
# Date   :
#
# Description :
#
###############################################################################
import sys
import requests
reload(sys)
sys.setdefaultencoding('utf8')
import os
import datetime
from datetime import datetime, timedelta

from applications.eos.modules import const


def api():
  session.forget()
  response.headers["Access-Control-Allow-Origin"] = '*'
  response.headers['Access-Control-Max-Age'] = 86400
  response.headers['Access-Control-Allow-Headers'] = '*'
  response.headers['Access-Control-Allow-Methods'] = '*'
  response.headers['Access-Control-Allow-Credentials'] = 'true'
  return service()


def my_task(key, name):
  return dict(key=key, name=name)

def check_db_connect():
  try:
    db._adapter.reconnect()
    return True
  except:
    return False


def check_api(link):
  try:
    res = requests.get(link)
    print res.status_code
    return res.status_code
  except:
    return False

################################################################################
@service.json
def status(*args, **kwargs):
  try:
    stat = os.system('ps aux | grep redis | grep -v grep | wc -l')
    db_status = check_db_connect()
    # s = check_api('http://envisoft.gov.vn')
    return dict(success=True, data=dict(mongo=db_status, s=stat))
  except Exception as ex:
    return dict(success=False, message=str(ex))
