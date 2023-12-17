# -*- coding: utf-8 -*-
###############################################################################
# Author :
# Date   :
#
# Description :
#
###############################################################################


# ------------------------------------------------------------------------------
@auth.requires(
  lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)) or auth.has_permission('view',
                                                                                                            'admin'))
def index():
  return dict()


# ------------------------------------------------------------------------------
@service.json
@auth.requires(
  lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)) or auth.has_permission('view',
                                                                                                            'admin'))
def get_list_usr(*args, **kwargs):
  try:
    display_start = int(request.vars.iDisplayStart)
    display_length = int(request.vars.iDisplayLength)
    status = request.vars.status
    group_id = request.vars.group_id
    s_search = request.vars.sSearch
    array_object = []
    limitby = (display_start, display_start + display_length)

    # Search conditions
    conditions = (db.auth_user.id > 0)
    if not auth.has_membership('admin'):
      conditions &= (db.auth_user.created_by == current_user.user_id)
    if s_search:
      conditions &= ((db.auth_user.phone.contains(s_search)) |
                     (db.auth_user.fullname.contains(s_search)) |
                     (db.auth_user.email.contains(s_search)) |
                     (db.auth_user.website.contains(s_search)) |
                     (db.auth_user.address.contains(s_search)))
    if status:
      conditions &= (db.auth_user.status == status)
    if group_id:
      conditions &= ((db.auth_user.id == db.auth_membership.user_id) & (db.auth_membership.group_id == group_id))

    # Query data
    fields = ['id', 'fullname', 'email', 'is_active', 'image', 'username']
    fields = [db.auth_user[field] for field in fields]
    conditions |= (db.auth_user.id == current_user.id)
    rows = db(conditions).select(*fields, limitby=limitby)

    total_records = db(conditions).count()
    avatar_dimension = 20

    for i, item in enumerate(rows):
      # Avatar
      if item.image:
        image = IMG(_src=URL('default', 'download', args=item.image), _height="42", _width="42")
      else:
        image = IMG(_src=URL('static', 'img/clear.png'), _height=avatar_dimension, _width=avatar_dimension)

      status = T('Active') if item.is_active else T('In-active')

      array_object.append([
        image,
        A(item.username, _href=URL('form', args=[item.id])),
        item.fullname,
        item.email,
        status,
        INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
        item.id
      ])
    return dict(iTotalRecords=total_records, iTotalDisplayRecords=total_records, aaData=array_object, success=True)
  except Exception, ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


# ------------------------------------------------------------------------------
@auth.requires(
  lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)) or auth.has_permission('view',
                                                                                                            'admin'))
def form():
  usr_id = request.args(0)
  record = db.auth_user(usr_id) or None
  msg = ''
  if record:
    if not (auth.has_membership('admin') or record.id == current_user.id):
      if str(record.created_by) != current_user.user_id:
        redirect(ACCESS_DENIES_URL)

  # if record and not request.vars.password:
  # db.auth_user.password.requires = []
  fields = auth.settings.profile_fields
  if record:
    db.auth_user.password.writable = False

  frm = SQLFORM(db.auth_user, record, _method='POST', fields=fields, hideerror=True, showid=False, _id='frmMain')
  frm.validate(onvalidation=validate, hideerror=True, detect_record_change=True)
  if frm.accepted:
    if record:
      record.update_record(**dict(frm.vars))
      # db.auth_user[record.id] = dict(password=frm.vars.password)
    else:
      db.auth_user.insert(**dict(frm.vars))

    # Clear cache with key 'users_index'
    cache.ram.clear('users_index*')
    session.flash = T('MSG_INFO_SAVE_SUCCESS')
    redirect(URL('index'))
  elif frm.errors:
    for item in frm.errors:
      msg += '%s: %s<br />' % (db.auth_user[item].label, frm.errors[item])
  else:
    pass
  if record:
    frm.custom.widget.username['_readonly'] = 'true'

  # Group belonged
  memberships = db(db.auth_membership.user_id == usr_id).select(db.auth_membership.group_id)
  memberships_arr = [membership.group_id for membership in memberships]
  roles = db((db.auth_group.id > 0) & (db.auth_group.id.belongs(memberships_arr))).select(db.auth_group.role,
                                                                                          db.auth_group.id)

  return dict(form=frm, roles=roles, msg=XML(msg), usr_id=usr_id)


# ------------------------------------------------------------------------------
def validate(frm):
  pass


# ------------------------------------------------------------------------------
def call():
  return service()


# ------------------------------------------------------------------------------
@auth.requires(
  lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)) or auth.has_permission('view',
                                                                                                            'admin'))
def stations():
  usr_id = request.vars.user
  usr_name = ''
  stations = None
  record = db.auth_user(usr_id) or None
  msg = ''
  if record:
    usr_name = record.fullname
  # if record and not request.vars.password:
  # db.auth_user.password.requires = []
  fields = auth.settings.profile_fields

  frm = SQLFORM(db.auth_user, record, _method='POST', fields=fields, hideerror=True, showid=False, _id='frmMain')
  frm.validate(onvalidation=validate, hideerror=True, detect_record_change=True)
  stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name)
  return dict(form=frm, msg=XML(msg), usr_name=usr_name, stations=stations, usr_id=usr_id)


# ------------------------------------------------------------------------------
@service.json
@auth.requires(
  lambda: auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER) or auth.has_permission('view',
                                                                                                          'manager_station_type') or auth.has_permission(
    'view', 'admin'))
def get_list_stations(*args, **kwargs):
  try:
    user_id = request.vars.user_id
    iDisplayStart = int(request.vars.iDisplayStart)
    iDisplayLength = int(request.vars.iDisplayLength)

    aaData = []
    limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

    conditions = (db.manager_stations.id > 0)

    conditions &= (db.manager_stations.user_id == user_id)

    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    list_data = db(conditions).select(db.manager_stations.id,
                                      db.manager_stations.station_id,
                                      limitby=limitby)
    # Tong so ban ghi khong thuc hien phan trang
    iTotalRecords = db(conditions).count()

    for i, item in enumerate(list_data):
      station_id = item.station_id
      station = db(db.stations.id == station_id).select(db.stations.station_name, db.stations.address)
      aaData.append([
        A(str(iDisplayStart + 1 + i)),
        station[0].station_name,
        station[0].address,
        INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
        item.id
      ])
    return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
  except Exception as ex:
    return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
def delete_stations(*args, **kwargs):
  try:
    array_data = request.vars.ids
    list_ids = array_data.split(',')
    db(db.manager_stations.id.belongs(list_ids)).delete()
    return dict(success=True)
  except Exception as ex:
    return dict(success=False, message=str(ex))


################################################################################
@service.json
def add_stations(*args, **kwargs):
  try:
    user_id = request.vars.user_id
    station_id = request.vars.station_id

    conditions = (db.manager_stations.user_id == user_id)
    conditions &= (db.manager_stations.station_id == station_id)
    count = db(conditions).count()

    if count:
      return dict(success=False, message=str('Trạm đã thuộc sự quản lý của User'))
    else:
      db.manager_stations.insert(user_id=user_id, station_id=station_id)

    return dict(success=True)
  except Exception as ex:
    return dict(success=False, message=str(ex))

################################################################################