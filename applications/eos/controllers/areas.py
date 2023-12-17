# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from applications.eos.modules import common
from gluon import current

@auth.requires(lambda: (auth.has_permission('create', 'areas') or auth.has_permission('edit', 'areas')))
def form():
    # If in Update mode, get equivallent record
    record = db.areas(request.args(0)) or None
    msg = ''
    
    frm = SQLFORM(db.areas, record, _method = 'POST', hideerror = True, showid = False, _id = 'frmMain')
    
    if frm.process(onvalidation = validate, detect_record_change = True, hideerror = True).accepted:
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' %(item, frm.errors[item])
    else:
        pass
        #response.flash = message.REQUEST_INPUT

    return dict(frm = frm, msg = XML(msg))

################################################################################
def validate(frm):
    #Check condion
    #Get control value by : frm.vars.ControlName
    #If validate fail : frm.errors.ControlName = some message
    pass

def call():
    return service()

################################################################################
# @decor.requires_login()
def index():
    return locals()

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'areas')))
def get_list_areas(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        s_search = request.vars.sSearch 
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
    
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
        list_data = db(conditions).select(  db.areas.id, 
                                            db.areas.area_code,
                                            db.areas.area_name,
                                            db.areas.order_no,
                                            orderby = db.areas.order_no,
                                            limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            aaData.append([
                str(iDisplayStart + 1 + i),
                item.area_code,
                item.area_name,
                item.order_no,
                INPUT(_name='select_item', _class='select_item', _type='checkbox', _value=item.id,
                      data=dict(value=item.id, display=item.area_name), _group=0),
                '%s%s%s%s%s%s' % ( \
                '<a href="javascript: void(0);" class="btnAddNew" title="',
                T('Edit area'),
                    '" data-for="#hfAreaId"  data-callback="reloadDatatable()"',
                    'data-url="', URL('areas', 'popup_add', args=[item.id]), '"> \
                    <i class="fa fa-edit"></i> \
                </a>'),
                str(item.id),
            ])
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'stations')))
def get_list_station_by_area(*args, **kwargs):
    try:
        area_id = request.vars.area_id
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)
        conditions = (db.stations.area_id == area_id)
        list_data = db(conditions).select(db.stations.id, db.stations.station_name,
                                          db.stations.station_type, db.stations.order_in_area,
                                          orderby = db.stations.order_in_area, limitby=limitby)
        iTotalRecords = db(conditions).count(db.stations.id)

        if iTotalRecords:
            iRow = 1 + iDisplayStart
            station_type = dict()
            for key, item in const.STATION_TYPE.iteritems():
                station_type[str(item['value'])] = T(item['name'])
            # Duyet tung phan tu trong mang du lieu vua truy van duoc
            for item in list_data:
                listA = [
                    str(iRow),
                    item.station_name,
                    station_type[str(item.station_type)],
                    item.order_in_area,
                    INPUT(_name = 'select_item', _class = 'select_item', _type = 'checkbox', _value = item.id,
                        data = dict(value = item.id, display = item.station_name), _group=1),
                    item.id,
                ]
                aaData.append(listA)
                iRow += 1
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'areas')))
def popup_add():
    record = db.areas(request.args(0)) or None
    
    table = request.vars.table
    field = request.vars.field
    frm = SQLFORM(db.areas, record, _method = 'POST', hideerror = True, showid = False)
    return  dict(frm = frm, table = table, field = field)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'areas') or auth.has_permission('edit', 'master_area')))
def ajax_save_area(*args, **kwargs):
    try:
        is_manager = auth.has_membership(const.GROUP_MANAGER)
        if current_user and is_manager == False:
            row = db(db.auth_group.manager == current_user.id).select(db.auth_group.id).first()
            if row:
                is_manager = True
        value = display = None
        data = dict()
        area_code = request.vars.area_code
        order_no = request.vars.order_no
        area_name = request.vars.area_name
        description = request.vars.description
        
        if request.vars.id:
            value = db(db.areas.id == request.vars.id).update(area_code = area_code, area_name = area_name, order_no = order_no, description = description)
        else:
            value = db.areas.insert(area_code = area_code, area_name = area_name, order_no = order_no, description = description)
            if is_manager == True:
                db.manager_areas.insert(user_id=current_user.id,areas_id=value.id)
        display = area_name
        return dict(success = True, value = value, display = display, data = data)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'areas')))
def del_records(*args, **kwargs):
    try:
        value = display = None
        data = dict()
        ids = request.vars.ids.split(',')
        db(db.stations.id.belongs(ids)).update(area_id=None)
        return dict(success = True, value = value, display = display, data = data)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'areas')))
def del_area_records(*args, **kwargs):
    try:
        value = display = None
        data = dict()
        ids = request.vars.ids.split(',')
        db(db.areas.id.belongs(ids)).delete()
        return dict(success = True, value = value, display = display, data = data)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))
