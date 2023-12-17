# -*- coding: utf-8 -*-
###############################################################################
# Author : Thuandv
# Date   : 2021/05/14
#
# Description : IDH news pages
#
###############################################################################

from applications.eos.modules.plugin_ckeditor import CKEditor

def call():
  return service()


def index():
  return dict()


def form():
  # If in Update mode, get equivallent record
  msg = ''
  record = db.news(request.args(0)) or None

  frm = SQLFORM(db.news_cat, record, _method='POST', hideerror=True, showid=False, _id='frmMain')
  frm.custom.widget.is_actived['_value'] = True
  frm.custom.widget.is_actived['_type'] = 'hidden'
  frm.custom.widget.order_no['_type'] = 'number'
  frm.custom.widget.order_no['_class'] = 'form-control text-right'
  order_no = 1
  if record:
    order_no = record.order_no
  frm.custom.widget.order_no['_value'] = order_no

  if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
    session.flash = T('MSG_INFO_SAVE_SUCCESS')
    redirect(URL('news_cat', 'index'))
  elif frm.record_changed:
    redirect(URL('home', 'error'))
  elif frm.errors:
    for item in frm.errors:
      msg += '%s: %s<br />' % (T('provinces_' + item), frm.errors[item])
  else:
    pass
    # response.flash = message.REQUEST_INPUT
  # if record:
  #   frm.custom.widget.content = CKEditor.widget
  # frm.custom.widget.content = CKEditor

  return dict(frm=frm, msg=XML(msg))


def validate(frm):
  pass


@service.json
def get_list(*args, **kwargs):
  try:
    iDisplayStart = int(request.vars.iDisplayStart)
    iDisplayLength = int(request.vars.iDisplayLength)
    s_search = request.vars.sSearch
    aaData = []
    limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

    conditions = (db.news_cat.id > 0)

    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    if s_search:
      conditions &= ((db.notifications.title.contains(s_search)) | (db.notifications.content.contains(s_search)))

    list_data = db(conditions).select(db.news_cat.ALL, orderby=~db.news_cat.order_no,
                                      limitby=limitby)
    inx = 0
    for item in list_data:
      if item.is_actived == True:
        status = T('true')
      else:
        status = T('false')
      inx += 1
      aaData.append([
        str(inx),
        A(item.name, _href=URL('news_cat', 'form', args=[item.id])),
        status,
        INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
        item.id,
      ])
    iTotalRecords = db(conditions).count()
    return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex.message), success=False)


