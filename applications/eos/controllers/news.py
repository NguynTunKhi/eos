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
  msg = ''
  record = db.news(request.args(0)) or None

  frm = SQLFORM(db.news, record, _method='POST', hideerror=True, showid=False, _id='frmMain')
  frm.custom.widget.summary['_rows'] = 5
  frm.custom.widget.content['_rows'] = 20
  frm.custom.widget.new_type['_value'] = 0
  if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
    session.flash = T('MSG_INFO_SAVE_SUCCESS')
    redirect(URL('news', 'index'))
  elif frm.record_changed:
    redirect(URL('home', 'error'))
  elif frm.errors:
    for item in frm.errors:
      msg += '%s: %s<br />' % (T('provinces_' + item), frm.errors[item])
  else:
    pass
  if record:
    frm.custom.widget.content = CKEditor.widget

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

    conditions = (db.news.id > 0)

    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    if s_search:
      conditions &= ((db.notifications.title.contains(s_search)) | (db.notifications.content.contains(s_search)))

    list_data = db(conditions).select(db.news.ALL, orderby=~db.news.created_at, limitby=limitby)
    inx = 0
    for item in list_data:
      inx += 1
      aaData.append([
        str(inx),
        A(item.title, _href=URL('news', 'form', args=[item.id])),
        item.created_at,
        INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
        item.id,
      ])
    iTotalRecords = db(conditions).count()
    return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex.message), success=False)


def get_news_list(kwargs):
  try:
    fields = [
      db.news.title,
      db.news.summary,
      db.news.content,
      db.news.created_at,
      db.news.u_display,
      db.news.image
    ]
    iDisplayStart = int(kwargs.get('iDisplayStart', '0'))
    iDisplayLength = int(kwargs.get('iDisplayLength', '10'))
    s_search = kwargs.get('search', '')
    c = kwargs.get('c', '')
    limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
    conditions = (db.news.id > 0)
    if c:
      conditions &= db.news.cat_id == c
    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    if s_search:
      conditions &= ((db.news.title.contains(s_search)) | (db.news.summary.contains(s_search)))
    list_data = db(conditions).select(*fields, orderby=~db.news.created_at, limitby=limitby)
    iTotalRecords = db(conditions).count()
    return dict(total=iTotalRecords, display=iTotalRecords, data=list_data, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex.message), success=False)

@service.json
def slide(*args, **kwargs):
  cat = db(db.news_cat.new_type == 2).select().first()
  kwargs['c'] = ''
  if cat:
    kwargs['c'] = str(cat.id)
  return get_news_list(kwargs)


@service.json
def list(*args, **kwargs):
  return get_news_list(kwargs)


