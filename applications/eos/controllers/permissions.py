# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

import sys, pkgutil, os.path
from applications.eos.modules import const, common


def check_permissions_admin():
  is_manager = auth.has_membership(const.GROUP_MANAGER)
  if current_user and is_manager == False:
    row = db(db.auth_group.manager == current_user.id).select(db.auth_group.id).first()
    if row:
      is_manager = True

  if not (auth.has_membership('admin') or is_manager):
    return False
  return True

# ------------------------------------------------------------------------------
# @auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
def index():
  if not check_permissions_admin():
    return redirect(URL('master', 'access_denied'))
  group_id = request.vars.group_id
  group = db.auth_group(group_id)
  return dict(group=group)


# ------------------------------------------------------------------------------
@service.json
# @auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
def get_list_permissions(*args, **kwargs):
  try:
    type = request.vars.type
    group_id = request.vars.group_id
    funcs = db(db.auth_permission.id > 0 and db.auth_permission.group_id == group_id).select(db.auth_permission.table_name, distinct=db.auth_permission.table_name)
    if auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER):
      newDict = common.sort_dict_const_by_value(const.SYS_PERMISSION)
    else:
      newDict = []
      if current_user:
        row = db(db.auth_group.manager == current_user.id).select(db.auth_group.id).first()
        if row:
          group_id_parent = str(row.id)
          rows = db(db.auth_permission.group_id == group_id_parent).select(db.auth_permission.ALL)
          func_to_dic = {}
          for r in rows:
            if not func_to_dic.has_key(r.table_name):
              func_to_dic[r.table_name] = []
            func_to_dic[r.table_name].append(r.name)
          for k in func_to_dic:

            if k in const.SYS_PERMISSION:
              role = {}
              for _k in const.SYS_PERMISSION[k]:
                if _k == 'rules':
                  for ru_key in const.SYS_PERMISSION[k]['rules']:
                    if const.SYS_PERMISSION[k]['rules'][ru_key]['value'] in func_to_dic[k]:
                      if not role.has_key('rules'):
                        role['rules'] = {}
                      role['rules'][ru_key] = const.SYS_PERMISSION[k]['rules'][ru_key]
                else:
                  role[_k] = const.SYS_PERMISSION[k][_k]
              newDict.append((k, role))
      newDict = common.sort_tuple(newDict)

    aaData = []
    total_records = len(newDict)
    userRole = {}
    roles = db(db.auth_permission.group_id == group_id).select(db.auth_permission.name, db.auth_permission.table_name)
    for r in roles:
      if userRole.has_key(r.table_name):
        userRole[r.table_name].append(r.name)
      else:
        userRole[r.table_name] = [r.name]
    inx = 0
    for key, val in newDict:
      inx += 1
      row = [inx, T(val['name'])]
      t = ''
      lv = common.sort_dict_const_by_value(val["rules"])
      for k, v in lv:
        _value = v['value']
        if userRole.has_key(key) and _value in userRole[key]:
          t += '<label class="checkbox-inline">%s %s</label>' % (
          INPUT(_name=key, _type='checkbox', _column=0, _row=0, _class='column_item row_item', _value=_value,
                _checked='true'), T(v['name']))
        else:
          t += '<label class="checkbox-inline">%s %s</label>' % (
          INPUT(_name=key, _type='checkbox', _column=0, _row=0, _class='column_item row_item', _value=_value),
          T(v['name']))
      row.append(t)
      aaData.append(row)

    return dict(iTotalRecords=total_records, iTotalDisplayRecords=total_records, aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex.message), success=False)


# ------------------------------------------------------------------------------
@service.json
# @auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
def update_permissions(*args, **kwargs):
  try:
    if not check_permissions_admin():
      return redirect(URL('master', 'access_denied'))
    type = request.vars.type
    group_id = request.vars.group_id
    #
    if not type or not group_id:
      return dict(success=True, message=T('Permissions updated successful!'))
    #
    permissions = request.vars.permissions
    permissions = permissions.split(';')  # Cat quyen theo tung row (controller)

    db(db.auth_permission.group_id == group_id).delete()

    ### Update new permissions
    for item in permissions:
      item = item.split(',')
      for cur_per in item[1:]:
        if cur_per:
          db.auth_permission.insert(
            group_id=group_id,
            table_name=item[0],
            name=cur_per
          )
    return dict(success=True)
  except Exception, ex:
    logger.error(str(ex))
    return dict(message=str(ex), success=False)


################################################################################
def call():
  return service()
