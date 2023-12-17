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

reload(sys)
sys.setdefaultencoding('utf8')


################################################################################
def validate(frm):
  pass


def call():
  return service()


@auth.requires(lambda: (auth.has_permission('view', 'vnair_notify')))
def index():
  return dict(message='')


@service.json
@auth.requires(lambda: (auth.has_permission('view', 'vnair_notify')))
def get_list(*args, **kwargs):
  try:
    iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
    iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
    # s_search = request.vars.sSearch # Chuoi tim kiem nhap tu form
    s_search = request.vars.sometext  # Chuoi tim kiem nhap tu form
    aaData = []  # Du lieu json se tra ve
    limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

    conditions = (db.vnair_notify.id > 0)
    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    if s_search:
      conditions &= db.vnair_notify.title.contains(s_search)
    list_data = db(conditions).select(db.vnair_notify.ALL, orderby=~db.vnair_notify.created_at, limitby=limitby)
    # Tong so ban ghi khong thuc hien phan trang
    iTotalRecords = db(conditions).count(db.vnair_notify.id)
    # Thu tu ban ghi
    iRow = iDisplayStart + 1

    # Duyet tung phan tu trong mang du lieu vua truy van duoc
    for item in list_data:
      listA = [
        str(iRow),
        item.title,
        item.created_at,
        INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
      ]

      aaData.append(listA)
      iRow += 1

    return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


@auth.requires(lambda: (auth.has_permission('create', 'vnair_notify')))
def popup_add():
  record = db.vnair_notify(request.args(0)) or None
  table = request.vars.table
  field = request.vars.field
  frm = SQLFORM(db.vnair_notify, record, _method='POST', hideerror=True, showid=False)
  return dict(frm=frm, table=table, field=field)


def send_notify(title, body):
  try:
    import requests
    headers = {'Content-Type': 'application/json',
               'Authorization': 'key={}'.format(myconf.get('fcm.vnair_server_token'))}
    data = {
      'notification': {'title': title, 'body': body},
      'data': {'title': title, 'body': body},
      # 'registration_ids': registration_ids,
      'to': '/topics/all'
    }
    requests.post('https://fcm.googleapis.com/fcm/send', json=data, headers=headers)
  except:
    pass


@service.json
@auth.requires(lambda: (auth.has_permission('create', 'vnair_notify')))
def ajax_save(*args, **kwargs):
  try:
    if not kwargs.get('title') or not kwargs.get('body'):
      return dict(success=False, message=T('Dữ liệu không để trống!'))
    db.vnair_notify.insert(**kwargs)
    send_notify(kwargs.get('title'), kwargs.get('body'))
    return dict(success=True)
  except Exception as ex:
    return dict(success=False, message=ex.message)

