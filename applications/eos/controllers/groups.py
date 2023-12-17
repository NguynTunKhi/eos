# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from applications.eos.modules import common


# ------------------------------------------------------------------------------
# @auth.requires(lambda: auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER))
@auth.requires(lambda: (auth.has_permission('view', 'groups')))
def index():
  return dict()


# ------------------------------------------------------------------------------
# @auth.requires(lambda: auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER))
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'groups')))
def get_list_groups(*args, **kwargs):
  try:
    display_start = int(request.vars.iDisplayStart)
    display_length = int(request.vars.iDisplayLength)
    s_search = request.vars.sSearch
    aaData = []
    limitby = (display_start, display_start + display_length)

    conditions = (db.auth_group.id > 0)
    # If there are search conditions
    if s_search:
      conditions &= ((db.auth_group.role.contains(s_search)) |
                     (db.auth_group.description.contains(s_search)))

    if not auth.has_membership('admin'):
      conditions &= (db.auth_group.created_by == current_user.user_id)

    fields = ['id', 'role', 'manager', 'description']
    fields = [db.auth_group[field] for field in fields]
    # rows = cache.ram('groups_%s' % display_start,
    # lambda: db(conditions).select( *fields,
    # orderby = db.auth_group.role,
    # limitby = limitby,
    # cacheable=True),
    # session.cache_1d)

    rows = db(conditions).select(*fields,
                                 orderby=db.auth_group.role,
                                 limitby=limitby)

    total_records = db(conditions).count()
    user_dict = common.get_usr_dict()[0]

    for i, item in enumerate(rows):
      aaData.append([
        str(display_start + i + 1),
        A(item.role, _href=URL('form', args=[item.id])),
        user_dict.get(item.manager) if item.manager else '',
        item.description,
        A(T('Grand permission'), _href=URL('permissions', 'index', vars={'group_id': item.id}),
          _class='btn btn-warning btn-xs',
          _type='button') if item.role != 'admin' and item.role != const.GROUP_MANAGER else '',
        XML(INPUT(_name='select_item', _type='checkbox', _class='select_item',
                  _value=item.id)) if item.role != 'admin' else '',
        item.id
      ])
    return dict(iTotalRecords=total_records, iTotalDisplayRecords=total_records, aaData=aaData, success=True)
  except Exception, ex:
    logger.error(str(ex))
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


# ------------------------------------------------------------------------------
# @auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
@auth.requires(lambda: (auth.has_permission('create', 'groups') or auth.has_permission('edit', 'groups')))
def form():
  id = request.args(0)
  record = db.auth_group(id) or None
  if record:
    if not auth.has_membership('admin'):
      if str(record.created_by) != current_user.user_id:
        redirect(ACCESS_DENIES_URL)

  if not record:
    id = 0

  form = SQLFORM(db.auth_group, record, _id='form_groups')
  str_errors = ''

  form.validate(hideerror=True, detect_record_change=True)
  if form.accepted:
    if not record:
      rec = db.auth_group.insert(**dict(form.vars))
      if form.vars.manager:
        db.auth_membership.insert(user_id=form.vars.manager, group_id=rec.id)
    else:
      rec = record.update_record(**dict(form.vars))
      if form.vars.manager:
        db.auth_membership.update_or_insert(
          (db.auth_membership.user_id == form.vars.manager) & (db.auth_membership.group_id == rec.id),
          user_id=form.vars.manager,
          group_id=rec.id
        )
    # Clear cache with key 'groups'
    cache.ram.clear('groups*')
    redirect(URL('form', args=[rec.id]))
  elif form.record_changed:
    redirect(URL('home', 'error'))
  elif form.errors:
    for item in form.errors:
      str_errors += '%s: %s<br />' % (item, form.errors[item])

  form.custom.widget.description['_rows'] = '2'

  return dict(form=form, id=id, errors_response=XML(str_errors))


# ------------------------------------------------------------------------------
# @auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'groups')))
def get_list_users_by_groups(*args, **kwargs):
  try:
    display_start = int(request.vars.iDisplayStart)
    display_length = int(request.vars.iDisplayLength)
    type = request.vars.type  # 'belong', 'notbelong'
    groups_id = request.vars.groups_id
    s_search = request.vars.sSearch
    array_object = []
    limitby = (display_start, display_start + display_length)

    conditions = (db.auth_user.id > 0)

    memberships = db(db.auth_membership.group_id == groups_id).select(db.auth_membership.user_id)
    membership_arr = [membership.user_id for membership in memberships]

    if type == 'belong':
      conditions &= (db.auth_user.id.belongs(membership_arr))
    elif type == 'notbelong':
      users_belonged = db(db.auth_user.id.belongs(membership_arr)).select(db.auth_user.id)
      users_belonged = [user.id for user in users_belonged]
      conditions &= (~db.auth_user.id.belongs(users_belonged))
      # Chi lay nhung user nam trong cac group ma user hien tai lam leader hoac user do no tao ra
      if not auth.has_membership('admin'):
        rows1 = db(db.auth_group.manager == current_user.user_id).select(db.auth_group.id)
        groups_id2 = [grp.id for grp in rows1]
        conditions2 = (db.auth_membership.group_id.belongs(groups_id2))
        rows2 = db(conditions2).select(db.auth_membership.user_id, distinct=True)
        user_ids = [mem.user_id for mem in rows2]
        conditions &= ((db.auth_user.id.belongs(user_ids)) | (db.auth_user.created_by == current_user.user_id))

    if s_search:
      conditions &= ((db.auth_user.address.contains(s_search)) |
                     (db.auth_user.fullname.contains(s_search)) |
                     (db.auth_user.phone.contains(s_search)) |
                     (db.auth_user.email.contains(s_search)))

    conditions &= (db.auth_user.username != 'admin')
    conditions &= (db.auth_user.username != 'thuandv')
    list_data = db(conditions).select(db.auth_user.id,
                                      db.auth_user.username,
                                      db.auth_user.fullname,
                                      db.auth_user.email,
                                      # orderby = ~db.auth_user.modified_on,
                                      limitby=limitby)

    total_records = db(conditions).count()
    for i, item in enumerate(list_data):
      array_object.append([
        str(display_start + i + 1),
        item.username,
        item.email,
        item.fullname,
        INPUT(_name='select_item', _type='checkbox', _class='select_item', _value=item.id),
      ])
    return dict(iTotalRecords=total_records, iTotalDisplayRecords=total_records, aaData=array_object, success=True)
  except Exception, ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


# ------------------------------------------------------------------------------
@service.json
# @auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
@auth.requires(lambda: (auth.has_permission('delete', 'groups')))
def del_membership(*args, **kwargs):
  try:
    array_data = request.vars.arrayData
    list_ids = array_data.split(',')
    length_list = len(list_ids)

    if (length_list == 0):
      return dict(success=True)
    groups_id = int(list_ids[0])
    i = 1
    while (i < length_list):
      db((db.auth_membership.group_id == groups_id) & (db.auth_membership.user_id == list_ids[i])).delete()
      i += 1
    return dict(success=True)
  except Exception, ex:
    return dict(success=False, message=str(ex))


# ------------------------------------------------------------------------------
@service.json
# @auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
@auth.requires(lambda: (auth.has_permission('create', 'groups')))
def insert_membership(*args, **kwargs):
  try:
    array_data = request.vars.arrayData
    list_ids = array_data.split(',')
    length_list = len(list_ids)

    if (length_list == 0):
      return dict(success=True)
    groups_id = int(list_ids[0])
    i = 1
    while (i < length_list):
      db.auth_membership.insert(group_id=groups_id, user_id=list_ids[i])
      i += 1

    return dict(success=True)
  except Exception, ex:
    return dict(success=False, message=str(ex))


# ------------------------------------------------------------------------------
def call():
  return service()
