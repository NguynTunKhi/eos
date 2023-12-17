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
sys.setdefaultencoding('utf-8')
# ------------------------------------------------------------------------------

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db

@auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)) or auth.has_permission('view','admin'))
def index():
    return dict()


################################################################################
@service.json
def get_list_areas(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        s_search = request.vars.sSearch
        user_id = request.vars.user_id
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.areas.id > 0)
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_areas_manager = db(db.manager_areas.user_id == current_user.id). \
                    select(db.manager_areas.areas_id)
                areas_ids = [str(item.areas_id) for item in list_areas_manager]
                conditions &= (db.areas.id.belongs(areas_ids))
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if s_search:
            conditions &= ((db.areas.area_code.contains(s_search)) |
                           (db.areas.area_name.contains(s_search)))
        list_data = db(conditions).select(db.areas.id,
                                          db.areas.area_code,
                                          db.areas.area_name,
                                          db.areas.order_no,
                                          orderby=db.areas.order_no,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            area_id = str(item['id'])
            query = (db.manager_areas.user_id == user_id)
            query &= (db.manager_areas.areas_id == area_id)
            areaByUser = db(query).count()

            if areaByUser:
                inPut = INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id, _checked='true'),
            else:
                inPut = INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),

            aaData.append([
                str(iDisplayStart + 1 + i),
                item.area_code,
                item.area_name,
                item.order_no,
                inPut,
                str(item.id),
            ])
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)

# ------------------------------------------------------------------------------
@service.json
@auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)) or auth.has_permission('view','admin'))
def get_list_usr(*args, **kwargs):
    try:
        display_start = int(request.vars.iDisplayStart)
        display_length = int(request.vars.iDisplayLength)
        status = request.vars.status
        group_id = request.vars.group_id
        s_search = request.vars.sSearch
        sometext = kwargs.get('sometext')
        array_object = []
        limitby = (display_start, display_start + display_length)

        # Search conditions
        conditions = (db.auth_user.id > 0)
        if not auth.has_membership('admin'):
            conditions &= (db.auth_user.created_by == current_user.user_id)
        if sometext:
            sometext = '{}'.format(sometext).lower()
            conditions &= ((db.auth_user.username.contains(sometext)) |
                           (db.auth_user.email.contains(sometext)) |
                           (db.auth_user.phone.contains(sometext)) |
                           # (db.auth_user.fullname.like('%{}%'.format(sometext))) |
                           (db.auth_user.address.contains(sometext)))
        if status:
            conditions &= (db.auth_user.status == status)
        if group_id:
            conditions &= ((db.auth_user.id == db.auth_membership.user_id) & (db.auth_membership.group_id == group_id))

        conditions &= (db.auth_user.username != 'admin')
        conditions &= (db.auth_user.username != 'thuandv')
        # Query data
        fields = ['id', 'fullname', 'email', 'type', 'is_active', 'image', 'username']
        fields = [db.auth_user[field] for field in fields]
        if current_user.username not in ['thuandv', 'admin']:
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

            auth_user_type = ''
            if item.type == const.AUTH_USER_TYPE_ENTERPRISE:
                auth_user_type = T('AUTH_USER_TYPE_ENTERPRISE')
            elif item.type == const.AUTH_USER_TYPE_GOVERNMENT:
                auth_user_type = T('AUTH_USER_TYPE_GOVERNMENT')

            array_object.append([
                image,
                A(item.username, _href=URL('form', args=[item.id])),
                item.fullname,
                item.email,
                auth_user_type,
                status,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
                item.id
            ])
        return dict(iTotalRecords=total_records, iTotalDisplayRecords=total_records, aaData=array_object, success=True)
    except Exception as ex:
        print ('loi --->',ex)
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=ex.message, success=False)


# ------------------------------------------------------------------------------
@auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)) or auth.has_permission('view','admin'))
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
        id = None
        if record:
            record.update_record(**dict(frm.vars))
            id = record.id
            # db.auth_user[record.id] = dict(password=frm.vars.password)
        else:
            id =  db.auth_user.insert(**dict(frm.vars))

        if id is not None:
            user = db(db.auth_user.id == id).select().first()
            if user.type == 1:
                groups = db((db.auth_group.id >0) & (db.auth_group.role == "Doanh nghiệp")).select()
                for group in groups:
                    conditions = (db.auth_membership.user_id == user.id) & (db.auth_membership.group_id == group.id)
                    check = db(conditions).count()
                    if check == 0:
                        db.auth_membership.insert(user_id=user.id, group_id=group.id)


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
    agents = db(db.agents.id >0).select()
    agent_id = ''
    if record is not None:
        agent_id = record['agent_id']
    return dict(form=frm, roles=roles , agents=agents, agent_id=agent_id, msg=XML(msg), usr_id=usr_id)


# ------------------------------------------------------------------------------
def validate(frm):
    pass


# ------------------------------------------------------------------------------
def call():
    return service()


# ------------------------------------------------------------------------------
@auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)) or auth.has_permission('view','admin'))
def stations():
    view_type = request.vars.view_type
    try:
        view_type = int(view_type)
    except Exception as es:
        view_type = const.VIEW_BY['MINUTE']['value']

    provinces = common.get_province_have_station()
    default_provinces = db(db.provinces.default == 1).select()
    station_id = request.vars.station_id
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
    return dict(form=frm, msg=XML(msg), usr_name=usr_name, stations=stations, usr_id=usr_id,
                provinces=provinces, default_provinces=default_provinces, station_id=station_id, view_type=view_type)


# ------------------------------------------------------------------------------
@service.json
@auth.requires(lambda: auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER) or auth.has_permission('view','manager_station_type') or auth.has_permission('view', 'admin'))
def get_list_stations(*args, **kwargs):
    try:
        province_id = request.vars.province_id
        sometext = request.vars.sometext
        type = request.vars.type
        user_id = request.vars.user_id
        province_id = request.vars.province_id
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions1 = (db.manager_stations.id > 0)

        conditions1 &= (db.manager_stations.user_id == user_id)

        conditions = (db.stations.id > 0)
        if type:
            conditions &= (db.stations.station_type == type)
        if province_id:
            conditions &= (db.stations.province_id == province_id)
        if sometext:
            conditions &= ((db.stations.station_name.contains(sometext)) )
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        list_data = db(conditions).select(db.stations.id,
                                          db.stations.station_name,
                                          db.stations.address,
                                          db.stations.station_type,
                                          db.stations.province_id,
                                          limitby=limitby)

        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        iRow = iDisplayStart + 0

        for item in list_data:
            station_id1 = item.id
            query = (db.manager_stations.user_id == user_id)
            query &= (db.manager_stations.station_id == station_id1)
            stationByUser = db(query).select(db.manager_stations.id, db.manager_stations.station_id)

            if stationByUser:
                inPut = INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id, _checked='true'),
            else:
                inPut = INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),

            iRow += 1
            aaData.append([
                iRow,
                item.station_name,
                item.address,
                inPut,
                item.id

            ])
            query = ''
            inPut = None

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData,
                    province_id=province_id, station_type=type, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


##############################################################################
@service.json
def delete_stations(*args, **kwargs):
    try:
        station_type = request.vars.station_type
        province_id = request.vars.province_id
        user_id = request.vars.user_id
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        conditions = (db.stations.id > 0)
        conditions1 = db.manager_stations.user_id == user_id

        if station_type or province_id:
            if station_type:
                conditions &= (db.stations.station_type == station_type)
            if province_id:
                conditions &= (db.stations.province_id == province_id)
            lstStationOrigin = db(conditions).select(db.stations.id)
            arrID = []
            for stationID in lstStationOrigin:
                arrID.append(stationID.id)
            conditions1 &= (db.manager_stations.station_id.belongs(arrID))
        db(conditions1).delete()
        # db(db.manager_stations.user_id == user_id).delete()
        for item in list_ids:
            station_id1 = item
            db.manager_stations.insert(user_id=user_id, station_id=station_id1)

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
@service.json
def update_permissions(*args, **kwargs):
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


##############################################################################
@service.json
def add_group_areas(*args, **kwargs):
    try:
        station_type = request.vars.station_type
        province_id = request.vars.province_id
        user_id = request.vars.user_id
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        conditions = (db.stations.id > 0)
        conditions_stations = db.manager_stations.user_id == user_id
        conditions_areas = db.manager_areas.user_id == user_id

        if station_type or province_id:
            if station_type:
                conditions &= (db.stations.station_type == station_type)
            if province_id:
                conditions &= (db.stations.province_id == province_id)
            lstStationOrigin = db(conditions).select(db.stations.id)
            arrID = []
            for stationID in lstStationOrigin:
                arrID.append(stationID.id)
            conditions1 &= (db.manager_stations.station_id.belongs(arrID))
        row = db(db.stations.area_id.belongs(list_ids)).select(db.stations.id)
        db(conditions_stations).delete()
        db(conditions_areas).delete()
        data = db().select(db.manager_areas.areas_id, db.manager_areas.user_id)
        for item in row:
            station_id = str(item['id'])
            db.manager_stations.insert(user_id=user_id, station_id=station_id)
        for areas_id in list_ids:
            db.manager_areas.insert(user_id=user_id, areas_id=areas_id)

        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))
