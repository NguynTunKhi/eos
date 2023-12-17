# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

if False:
    from gluon import *

    request = current.request
    response = current.response
    session = current.session
    cache = current.cache
    T = current.T
    db = current.db

from applications.eos.modules.w2pex import date_util
from applications.eos.modules import common
from datetime import datetime, timedelta

def call():
    return service()

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'equipments')) or (auth.has_permission('view', 'alarm_log')))
def index():
    conditions = db.stations.id > 0
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)
    status = dict(db.equipments.status.requires.options())

    return dict(stations = stations, status = status)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'equipments')) or (auth.has_permission('view', 'alarm_log')))
def get_list_equipments(*args, **kwargs):
    try:
        s_search = request.vars.sSearch
        type = request.vars.type
        status = request.vars.status
        sometext = request.vars.sometext
        station_id = request.vars.station_id
        aaData = []
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.equipments.id > 0)
        if sometext:
            conditions &= ( (db.equipments.equipment.contains(sometext)) |
                            (db.equipments.brandname.contains(sometext)) |
                            (db.equipments.provider.contains(sometext)) |
                            (db.equipments.series.contains(sometext)) |
                            (db.equipments.made_in.contains(sometext)) |
                            (db.equipments.description.contains(sometext)) )
        if type:
            conditions &= (db.equipments.station_type == type)
        if station_id:
            conditions &= (db.equipments.station_id == station_id)
        if status:
            conditions &= (db.equipments.status == status)
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.equipments.station_id.belongs(station_ids))
        list_data = db(conditions).select(limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        status = dict(db.equipments.status.requires.options())
        colors = ['', 'blue', 'red', 'green', 'orange']

        stations_dict = common.get_station_dict()[0]

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            url = URL('equipments', 'popup_add_equipment', args=[item.id], vars={'station_id' : item.station_id, 'type' : item.station_type})

            aaData.append([
                str(iDisplayStart + i + 1),
                "%s%s%s%s%s%s%s" % ( \
                "<a href='javascript: void(0);' class='btnAddNew' title='",
                    T('Equipment information'),
                    "' data-for='#hfEquipmentId'  data-callback='reloadDatatable_Equipment()' \
                    data-url='", url, "'> ",
                    item.equipment,
                "</a>"),
                stations_dict[item.station_id] if stations_dict.has_key(item.station_id) else '',
                item.start_date,
                item.brandname,
                item.made_in,
                item.series,
                SPAN(status[str(item.status)], _class="badge", _style="background:%s; color:white" % colors[item.status]),
                INPUT(_group = '0', _class = 'select_item', _type = 'checkbox', _value = item.id),
                item.id
            ])
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'equipments')) or (auth.has_permission('view', 'alarm_log')))
def get_equipments_by_station(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        type = request.vars.type
        view_only = request.vars.view_only
        aaData = []

        conditions = (db.equipments.id > 0) & (db.equipments.station_id == station_id)
                           
        list_data = db(conditions).select()
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = len(list_data)
        iRow = 1
        status = dict(db.equipments.status.requires.options())
        colors = ['', 'blue', 'red', 'green', 'orange']

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            url = URL('equipments', 'popup_add_equipment', args=[item.id], vars={'station_id' : station_id, 'type' : type})
            link = "%s%s%s%s%s%s%s" % ( \
                "<a href='javascript: void(0);' class='btnAddNew' title='",
                    T('Equipment information'),
                    "' data-for='#hfEquipmentId'  data-callback='reloadDatatable_Equipment()' \
                    data-url='", url, "'> ",
                    item.equipment,
                "</a>")
            aaData.append([
                str(iRow),
                item.equipment if view_only else link,
                item.start_date,
                item.brandname,
                item.provider,
                item.series,
                item.lrv,
                item.urv,
                SPAN(status[str(item.status)], _class="badge", _style="background:%s; color:white" % colors[item.status]) ,
            ])

            iRow += 1
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)


@service.json
def get_equipments_by_request_create_station(*args, **kwargs):
    try:
        request_create_station_id = request.vars.request_create_station_id
        type = request.vars.type
        view_only = request.vars.view_only
        aaData = []

        conditions = (db.request_create_station_equipments.id > 0) & (db.request_create_station_equipments.request_create_station_id == request_create_station_id)

        list_data = db(conditions).select()
        iTotalRecords = len(list_data)
        iRow = 1
        status = dict(db.request_create_station_equipments.status.requires.options())
        colors = ['', 'blue', 'red', 'green', 'orange']

        for item in list_data:
            url = URL('equipments', 'popup_add_request_create_station_equipment', args=[item.id],
                      vars={'request_create_station_id': request_create_station_id, 'type': type})
            link = "%s%s%s%s%s%s%s" % ( \
                "<a href='javascript: void(0);' class='btnAddNew' title='",
                T('Equipment information'),
                "' data-for='#hfRequestCreateStationEquipmentId'  data-callback='reloadDatatable_Equipment()' \
                data-url='", url, "'> ",
                item.equipment,
                "</a>")
            aaData.append([
                str(iRow),
                item.equipment if view_only else link,
                item.start_date,
                item.brandname,
                item.provider,
                item.series,
                item.lrv,
                item.urv,
                SPAN(status[str(item.status)], _class="badge",
                     _style="background:%s; color:white" % colors[item.status]),
            ])

            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)

################################################################################
# # @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'equipments')) or (auth.has_permission('view', 'alarm_log')))
def popup_add_equipment():

    record = db.equipments(request.args(0)) or None
    station_id = request.vars.station_id
    station = db.stations(station_id)
    type = request.vars.type

    frm = SQLFORM(db.equipments, record, _method = 'POST', hideerror = True, showid = False)
    frm.custom.widget.description['_rows'] = '2'
    frm.custom.widget.station_id['_readonly'] = True

    if station_id:
        db.equipments.station_id.requires = IS_IN_DB(db(db.stations.id == station_id), db.stations.id, db.stations.station_name)
        # update history
        db.manager_stations_history.insert(station_id=station_id,
                                           action='Update',
                                           username=current_user.fullname or None,
                                           description='Them_Chinh_sua_thiet_bi',
                                           update_time=datetime.now())
        ###
    return  dict(frm = frm, station = station, type = type)


@auth.requires(lambda: (auth.has_permission('view', 'equipments')) or (auth.has_permission('view', 'alarm_log')))
def popup_add_request_create_station_equipment():

    record = db.request_create_station_equipments(request.args(0)) or None
    request_create_station_id = request.vars.request_create_station_id
    request_create_station = db.request_create_stations(request_create_station_id)
    type = request.vars.type

    frm = SQLFORM(db.request_create_station_equipments, record, _method = 'POST', hideerror = True, showid = False)
    frm.custom.widget.description['_rows'] = '2'
    frm.custom.widget.request_create_station_id['_readonly'] = True

    if request_create_station_id:
        db.request_create_station_equipments.request_create_station_id.requires = IS_IN_DB(db(db.request_create_stations.id == request_create_station_id), db.request_create_stations.id, db.request_create_stations.station_name)
        # update history
        # db.manager_stations_history.insert(station_id=station_id,
        #                                    action='Update',
        #                                    username=current_user.fullname or None,
        #                                    description='Them_Chinh_sua_thiet_bi',
        #                                    update_time=datetime.now())
        ###
    return  dict(frm = frm, request_create_station = request_create_station, type = type)

################################################################################
@service.json
# # @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('create', 'equipments') or (auth.has_permission('view', 'alarm_log')) or auth.has_permission('edit', 'equipments')) & (auth.has_permission('edit', 'stations')))
def ajax_save_equipment(*args, **kwargs):
    try:
        # convert date manually
        if request.vars.start_date : request.vars.start_date = date_util.string_to_datetime(request.vars.start_date)
        if request.vars.warranty_start : request.vars.warranty_start = date_util.string_to_datetime(request.vars.warranty_start)
        if request.vars.warranty_end : request.vars.warranty_end = date_util.string_to_datetime(request.vars.warranty_end)
        if request.vars.implement_date : request.vars.implement_date = date_util.string_to_datetime(request.vars.implement_date)
        if request.vars.produce_date : request.vars.produce_date = date_util.string_to_datetime(request.vars.produce_date)
        if request.vars.certification_deadline : request.vars.certification_deadline = date_util.string_to_datetime(request.vars.certification_deadline)

        if not request.vars.id:
            db.equipments.insert(**dict(request.vars))
        else:
            db(db.equipments.id == request.vars.id).update(**dict(request.vars))

        if request.vars.id == db.station_indicator.equipment_id:
            db(db.station_indicator.equipment_id == request.vars.id).update(equipment_urv=request.vars.urv,
                                                                            equipment_lrv=request.vars.lrv)
        return dict(success = True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))


@service.json
# # @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('create', 'equipments') or (auth.has_permission('view', 'alarm_log')) or auth.has_permission('edit', 'equipments')) & (auth.has_permission('edit', 'request_create_stations')))
def ajax_save_request_create_station_equipments(*args, **kwargs):
    try:
        # convert date manually
        if request.vars.start_date : request.vars.start_date = date_util.string_to_datetime(request.vars.start_date)
        if request.vars.warranty_start : request.vars.warranty_start = date_util.string_to_datetime(request.vars.warranty_start)
        if request.vars.warranty_end : request.vars.warranty_end = date_util.string_to_datetime(request.vars.warranty_end)
        if request.vars.implement_date : request.vars.implement_date = date_util.string_to_datetime(request.vars.implement_date)
        if request.vars.produce_date : request.vars.produce_date = date_util.string_to_datetime(request.vars.produce_date)
        if request.vars.certification_deadline : request.vars.certification_deadline = date_util.string_to_datetime(request.vars.certification_deadline)

        if not request.vars.id:
            db.request_create_station_equipments.insert(**dict(request.vars))
        else:
            db(db.request_create_station_equipments.id == request.vars.id).update(**dict(request.vars))

        if request.vars.id == db.request_create_station_indicator.equipment_id:
            db(db.request_create_station_indicator.equipment_id == request.vars.id).update(equipment_urv=request.vars.urv,
                                                                            equipment_lrv=request.vars.lrv)
        return dict(success = True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'equipments')) or (auth.has_permission('view', 'alarm_log')))
def index_alert():
    types = db.adjustments.adjustment_type.requires.options()
    status = db.adjustments.status.requires.options()
    # stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    areas = db(db.areas.id > 0).select()
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
            row = db(db.stations.id.belongs(station_ids)).select(db.stations.area_id, distinct=True)
            areas_ids = [str(it.area_id) for it in row]
            areas = db(db.areas.id.belongs(areas_ids)).select(db.areas.area_name,
                                                              db.areas.id)
    stations = db(conditions).select(db.stations.id, db.stations.station_name)
    provinces = common.get_province_have_station_for_envisoft()
    default_provinces = db(db.provinces.default == 1).select()
    return locals()

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'equipments')) or (auth.has_permission('view', 'alarm_log')))
def get_list_equipments_alert(*args, **kwargs):
    try:
        s_search = request.vars.sSearch
        # sometext = request.vars.sometext
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        status = request.vars.status
        area_id = request.vars.area_id
        province_id = request.vars.province_id
        station_type = request.vars.station_type
        station_id = request.vars.station_id
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.sensor_trouble_history.id > 0)
        conditions2 = (db.stations.id > 0)
        if status:
            conditions &= (db.sensor_trouble_history.status == status)
        if area_id:
            conditions2 &= (db.stations.area_id == area_id)
        if province_id:
            conditions2 &= (db.stations.province_id == province_id)
        if station_type:
            conditions2 &= (db.stations.station_type == station_type)
        if station_id:
            conditions2 &= (db.stations.id == station_id)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        # if sometext:
        # conditions &= (db.data_alarm.station_id.contains(sometext))
        #if station_id:
            #conditions &= (db.sensor_trouble_history.station_id == station_id)
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.sensor_trouble_history.station_id.belongs(station_ids))
                conditions2 &= (db.stations.id.belongs(station_ids))

        rows = db(conditions2).select(db.stations.id)
        station_ids = ['']
        for row in rows:
            station_ids.append(str(row.id))
        conditions &= (db.sensor_trouble_history.station_id.belongs(station_ids))
        if from_date != ['', '']:
            conditions &= (db.sensor_trouble_history.get_time >= date_util.string_to_datetime(from_date[1]))
        if to_date != ['', '']:
            conditions &= (db.sensor_trouble_history.get_time <= date_util.string_to_datetime(to_date[1]).replace(hour=23, minute=59))
        if from_date == ['', ''] and to_date == ['', '']:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=14)
            conditions &= (db.sensor_trouble_history.get_time >= from_date)
            conditions &= (db.sensor_trouble_history.get_time <= to_date)
        # Gioi han so luong ban ghi xuat ra
        #limitation = datetime.now() - timedelta(days=14)
        #conditions &= (db.sensor_trouble_history.get_time > limitation)
        list_data = db(conditions).select(orderby=~db.sensor_trouble_history.get_time,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        iRow = iDisplayStart + 1
        stations_dict = common.get_station_dict()[0]
        indicator_dict = common.get_indicator_dict()

        status = dict(db.sensor_trouble_history.status.requires.options())
        colors = ['', 'green', 'red']
        for i, item in enumerate(list_data):
            row = [
                str(iDisplayStart + 1 + i),
                # A(item.station_id, _href = URL('', args = [item.id])),
                stations_dict[str(item.station_id)],
                SPAN(status[str(item.status)], _class="badge", _style="background:%s; color:white" % colors[item.status]),
                item.get_time,
                indicator_dict[str(item.indicator_id)] if (item.indicator_id is not None and item.indicator_id != '') else '---',
                item.value if (item.value is not None and item.value != 'NULL') else '---',
                item.unit if item.unit is not None else '---',
                A(item.file_name,_target ='_blank', _href = URL('equipments','get_text',args = [item.id])) if item.file_name is not None else '---',
            ]

            aaData.append(row)

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


def get_text():
    try:
        id = request.args[0] or None
        item = db(db.sensor_trouble_history.id == id).select(db.sensor_trouble_history.file_content,db.sensor_trouble_history.file_name).first()
        content = item.file_content
        file_name = item.file_name
        filename = os.path.join(request.folder, 'static', 'export', file_name)
        f = open(filename, "w+")
        f.write(content);
        f.close()
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name
        data = open(filename, "rb").read()
        return data
    except Exception as ex:
        return T('Error text export')


################################################################################
@service.json
def dropdown_content(table, filter_field, get_value_field, get_dsp_field, *args, **kwargs):
    try:
        filter_value = request.vars.filter_value
        filter_value = filter_value.split(';')
        filter_field = filter_field.split('-')
        conditions = (db[table]['id'] > 0)
        t1 = len(filter_field)
        t2 = len(filter_value)
        if t1 == t2:
            for i in range(0, t1):
                if filter_field[i] and filter_value[i] != '':
                    conditions &= (db[table][filter_field[i]] == filter_value[i])
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db[table]['id'].belongs(station_ids))

        records = db(conditions).select(db[table][get_value_field], db[table][get_dsp_field])
        station_id = request.vars.station_id
        command_id = request.vars.command_id
        logger_id = ''
        command_content = ''

        if command_id:
            command_content = db(db.datalogger_command.id == command_id). \
                select(db.datalogger_command.command_content).first().command_content
        if station_id:
            logger_id = db(db.adjustments.station_id == station_id).select().first()
            if logger_id is None:
                logger_id = ''
            else:
                logger_id = logger_id.logger_id
        if records:
            html1 = "<option value=''>%s</option>" % T('-- Select an option --')
            html = ["<option value='%s'>%s</option>" % (item[get_value_field], item[get_dsp_field]) for item in records]
            html = html1 + ''.join(html)
        else:
            html = "<option value=''>%s</option>" % T('-- No data --')

        return dict(success=True, html=html, logger_id=logger_id, command_content=command_content)
    except Exception as ex:
        return dict(success=False, message=str(ex))


# ################################################################################
@service.json
def export_excel():
    import os.path, openpyxl
    s_search = request.vars.sSearch
    # sometext = request.vars.sometext
    from_date = request.vars.from_date
    to_date = request.vars.to_date
    status = request.vars.status
    area_id = request.vars.area_id
    province_id = request.vars.province_id
    station_type = request.vars.station_type
    station_id = request.vars.station_id
    aaData = []

    conditions = (db.sensor_trouble_history.id > 0)
    conditions2 = (db.stations.id > 0)
    if status:
        conditions &= (db.sensor_trouble_history.status == status)
    if area_id:
        conditions2 &= (db.stations.area_id == area_id)
    if province_id:
        conditions2 &= (db.stations.province_id == province_id)
    if station_type:
        conditions2 &= (db.stations.station_type == station_type)
    if station_id:
        conditions2 &= (db.stations.id == station_id)
    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    # if sometext:
    # conditions &= (db.data_alarm.station_id.contains(sometext))
    # if station_id:
    # conditions &= (db.sensor_trouble_history.station_id == station_id)
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.sensor_trouble_history.station_id.belongs(station_ids))
            conditions2 &= (db.stations.id.belongs(station_ids))

    rows = db(conditions2).select(db.stations.id)
    station_ids = ['']
    for row in rows:
        station_ids.append(str(row.id))
    conditions &= (db.sensor_trouble_history.station_id.belongs(station_ids))
    if from_date != ['', '']:
        conditions &= (db.sensor_trouble_history.get_time >= date_util.string_to_datetime(from_date))
    if to_date != ['', '']:
        conditions &= (db.sensor_trouble_history.get_time <= date_util.string_to_datetime(to_date).replace(hour=23,
                                                                                                              minute=59))
    # if from_date == ['', ''] and to_date == ['', '']:
    #     to_date = datetime.now()
    #     from_date = to_date - timedelta(days=14)
    #     conditions &= (db.sensor_trouble_history.get_time >= from_date)
    #     conditions &= (db.sensor_trouble_history.get_time <= to_date)
    # Gioi han so luong ban ghi xuat ra
    # limitation = datetime.now() - timedelta(days=14)
    # conditions &= (db.sensor_trouble_history.get_time > limitation)
    table = 'sensor_trouble_history'
    list_data = db(conditions).select(orderby=~db.sensor_trouble_history.get_time)
    # Tong so ban ghi khong thuc hien phan trang
    iTotalRecords = db(conditions).count()
    stations_dict = common.get_station_dict()[0]
    indicator_dict = common.get_indicator_dict()

    status = dict(db.sensor_trouble_history.status.requires.options())
    for i, item in enumerate(list_data):
        if item.status == 1 :
            status_name = 'Hiệu chuẩn'
        if item.status == 2 :
            status_name = 'Lỗi thiết bị'
        row = [
            str(1 + i),
            stations_dict[str(item.station_id)],
            item.get_time,
            status_name,
            indicator_dict[str(item.indicator_id)] if (item.indicator_id is not None and item.indicator_id != '') else '---',
            item.value if (item.value is not None and item.value != 'NULL') else '---',
            item.unit if item.unit is not None else '---',
            item.file_name if item.file_name is not None else '---',
        ]

        aaData.append(row)

    #EXPORT_EXCEL
    wb2 = openpyxl.Workbook(write_only=True)
    ws2 = wb2.create_sheet()

    temp_headers = ['#','Tên trạm','Ngày giờ','Trạng thái','Tên thông số','Giá trị','Đơn vị','Tên file']
    headers = []
    headers.append(temp_headers)
    for header in headers:
        ws2.append(header)
    # Write data
    for row in aaData:
        ws2.append(row)

    # Get station name

    file_name = request.now.strftime('Thietbido_%Y%m%d_%H%M%S.xlsx')
    file_path = os.path.join(request.folder, 'static', 'export', file_name)
    # wb.save(file_path)
    wb2.save(file_path)

    data = open(file_path, "rb").read()
    os.unlink(file_path)
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

    return data


##################################################################################