# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from datetime import datetime, timedelta

from applications.eos.modules import common
from applications.eos.modules.w2pex import date_util
from gluon.tools import prettydate
import json


@auth.requires_login()
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def form():
    record = db.adjustments(request.args(0)) or None
    msg = ''

    form = SQLFORM
    frm = SQLFORM(db.adjustments, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' % (item, frm.errors[item])
    else:
        pass

    frm.custom.widget.title['_maxlength'] = '256'
    frm.custom.widget.content['_rows'] = '3'
    frm.custom.widget.from_date['_class'] = 'form-control valid datetime_iso'
    frm.custom.widget.to_date['_class'] = 'form-control valid datetime_iso'

    stations = None
    indicator_id = ''
    indicator_name = ''
    created_date = ''
    logger_id = ''
    title = ''
    list_indicators = []
    list_status_edit = []
    can_update_status = '0'
    current_status = 4
    current_status_name = ''

    if record:
        usr_dict = common.get_usr_dict()[0]
        fullname = usr_dict.get(record.created_by)
        frm.custom.widget.station_name['_readonly'] = 'true'
        indicator_id = record.indicator_id
        indicator_name = record.indicator_name
        created_date = record.created_date
        logger_id = record.logger_id
        title = record.title
        # Get all indicators to fill in dropdown

        current_status = record.status
        if current_status == 0:
            current_status_name = 'Draft'
        elif current_status == 2:
            current_status_name = 'Wait for approve'
        elif current_status == 4:
            current_status_name = 'Accepted'
        elif current_status == 5:
            current_status_name = 'Cancelled'
        elif current_status == 3:
            current_status_name = 'Rejected'

        list_status_edit.append({'value': current_status, 'name': current_status_name})

        if current_status < 3:
            can_update_status = '1'
            list_status_edit.append({'value': 3, 'name': 'Rejected'})
            list_status_edit.append({'value': 4, 'name': 'Accepted'})
            list_status_edit.append({'value': 5, 'name': 'Cancelled'})

        list_indicators = db(
            (db.station_indicator.station_id == record.station_id) & (db.station_indicator.status == 1)).select()

        for i in range(len(list_indicators)):
            list_indicators[i].id = str(list_indicators[i].id)

            if list_indicators[i].indicator_id:
                indicator_details = db.indicators(list_indicators[i].indicator_id) or None

                if indicator_details:
                    if list_indicators[i].mapping_name == '':
                        list_indicators[i].mapping_name = str(indicator_details.source_name)
                else:
                    list_indicators[i].mapping_name = ''

    else:
        fullname = ''
        # stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44
        # hungdx phan quyen quan ly trạm theo user issue 44
        conditions = (db.stations.id > 0)
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))
        stations = db(conditions).select(db.stations.id, db.stations.station_name)

    return dict(frm=frm, fullname=fullname, msg=XML(msg), stations=stations, list_indicators=list_indicators,
                indicator_id=indicator_id, indicator_name=indicator_name, title=title, list_status_edit=list_status_edit,
                logger_id=logger_id, current_status=current_status, can_update_status=can_update_status,
                current_status_name=current_status_name)


################################################################################
def validate(frm):
    # Check condion
    # Get control value by : frm.vars.ControlName
    # If validate fail : frm.errors.ControlName = some message
    pass


def call():
    return service()


################################################################################
@service.json
def get_list_indicator_by_station(*args, **kwargs):
    try:
        station_id = request.vars.station_id  # Chuoi tim kiem nhap tu form
        # Get all
        station_indicator_list = db(
            (db.station_indicator.station_id == station_id) & (db.station_indicator.status == 1)).select()

        for i in range(len(station_indicator_list)):
            station_indicator_list[i].id = str(station_indicator_list[i].id)

            if station_indicator_list[i].indicator_id:
                indicator_details = db.indicators(station_indicator_list[i].indicator_id) or None
                if indicator_details:
                    station_indicator_list[i].indicators_name = str(indicator_details.source_name)
                else:
                    station_indicator_list[i].indicators_name = ''

        return dict(station_indicator_list=station_indicator_list, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def index():
    types = db.adjustments.adjustment_type.requires.options()
    status = db.adjustments.status.requires.options()
    # stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)
    return locals()

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def get_list_adjustments(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        type = request.vars.adjustment_type
        sometext = request.vars.sometext
        status = request.vars.status
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        station_id = request.vars.station_id
        is_process = request.vars.is_process

        aaData = []
        conditions = (db.adjustments.id > 0)
        if sometext:
            conditions &= ((db.adjustments.title.contains(sometext)) | (db.adjustments.content.contains(sometext)))
        if type:
            conditions &= (db.adjustments.adjustment_type == type)
        if status:
            conditions &= (db.adjustments.status == status)

        if from_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
            except:
                from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            conditions &= (db.adjustments.from_date >= from_date)
        if to_date:
            try:
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
            except:
                to_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            conditions &= (db.adjustments.to_date <= to_date + timedelta(days=1))

        if station_id:
            conditions &= (db.adjustments.station_id == station_id)
        if is_process:
            conditions &= (db.adjustments.is_process == is_process)

        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).\
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.adjustments.station_id.belongs(station_ids))

        list_data = db(conditions).select(db.adjustments.id,
                                          db.adjustments.title,
                                          db.adjustments.content,
                                          db.adjustments.created_by,
                                          db.adjustments.station_name,
                                          db.adjustments.from_date,
                                          db.adjustments.to_date,
                                          db.adjustments.content,
                                          db.adjustments.adjustment_type,
                                          db.adjustments.status,
                                          db.adjustments.is_process,
                                          db.adjustments.created_date,
                                          orderby=~db.adjustments.created_date | db.adjustments.status,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        # Thu tu ban ghi
        iRow = iDisplayStart + 1
        usr_dict = common.get_usr_dict()[0]
        types = dict(db.adjustments.adjustment_type.requires.options())
        status = dict(db.adjustments.status.requires.options())
        colors = ['green', 'green', 'orange', 'red', 'gray', 'gray']
        print(list_data)
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            url_issue_adjustment = URL('issue_adjustment', args=[item.id])
            icon_send = "<i class='fa fa-send'></i>"
            if item.status != 2:
                icon_send = ""

            is_process = '-'
            if (item.is_process == 1):
                is_process = T('IS_Process_done')
            elif (item.is_process == 0):
                is_process = T('IS_Process_waiting')
            aaData.append([
                str(iRow + i),
                A(item.title, _href=URL('form', args=[item.id])),
                item.station_name,
                usr_dict.get(item.created_by),
                item.from_date,
                item.to_date,
                types[str(item.adjustment_type)],
                SPAN(status[str(item.status)], _style="background:%s; color:white" % colors[item.status],
                     _class="badge"),
                # item.created_date.strftime('%H:%M %d/%m'),
                "%s%s%s%s%s%s%s%s" % ( \
                "<a href='javascript: void(0);' class='btnAddNew' title='",
                T('Issue this command'),
                "' data-for='#hfAdjustmentId' data-callback='reloadDatatable_Adjustment()' data-url='",
                url_issue_adjustment, "'> ",
                "", icon_send, "</a>"),
                is_process,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
            ])

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def calendar():
    # lay nhung Adjustments co ngay bat dau trong 7 ngay gan nhat
    common_cd = (db.adjustments.from_date >= request.now - timedelta(days=7))
    # va co status 'Wait for approve', 'Rejected'
    conditions = common_cd & (db.adjustments.status <= 4)
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.adjustments.station_id.belongs(station_ids))

    rows = db(conditions).select(db.adjustments.id,
                                 db.adjustments.status,
                                 db.adjustments.title,
                                 orderby=~db.adjustments.from_date | ~db.adjustments.status)

    rows_wait, rows_not_submit, rows_finished = [], [], []
    for row in rows:
        if row.status in [2, 3]:
            rows_wait.append(row)
        elif row.status in [0, 1]:
            rows_not_submit.append(row)
        elif row.status == 4:
            rows_finished.append(row)
        else:
            pass

    return dict(rows_wait=rows_wait, rows_not_submit=rows_not_submit, rows_finished=rows_finished)


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def get_adjustments_calendar():
    try:
        # Get parameter (this is auto parameter by calendar control)
        start = request.vars.start
        end = request.vars.end

        conditions = (db.adjustments.id > 0)
        if start:
            conditions &= (db.adjustments.from_date >= date_util.string_to_date(start))
        if end:
            conditions &= (db.adjustments.to_date <= date_util.string_to_date(end))
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.adjustments.station_id.belongs(station_ids))

        rows = db(conditions).select(db.adjustments.id,
                                     db.adjustments.created_by,
                                     db.adjustments.created_date,
                                     db.adjustments.from_date,
                                     db.adjustments.to_date,
                                     db.adjustments.title,
                                     db.adjustments.content,
                                     db.adjustments.status)
        array_object = []
        usr_dict = common.get_usr_dict()[0]
        types = dict(db.adjustments.adjustment_type.requires.options())
        status = dict(db.adjustments.status.requires.options())
        colors = ['green', 'green', 'orange', 'red', 'gray', 'gray']

        for row in rows:
            schedule = {
                'id': str(row.id),
                'title': row.title,
                'content': row.content,
                'created_by': usr_dict.get(row.created_by),
                'created_date': str(row.created_date),
                'start': '%s' % row.from_date,
                'end': '%s' % row.to_date,
                'allDay': True,
                'color': colors[row.status],
                'textColor': '#fff',
                # 'url'       : URL('adjustments', 'form', args=[row.id]),
            }
            array_object.append(schedule)
        return json.dumps(array_object, ensure_ascii=False)
    except Exception as ex:
        return json.dumps([])


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def issue_adjustment():
    list_status_edit = []
    record = db.adjustments(request.args(0)) or None
    current_status = record.status
    if current_status < 3:
        list_status_edit.append({'value': 3, 'name': 'Rejected'})
        list_status_edit.append({'value': 4, 'name': 'Accepted'})
    if not record:
        redirect(URL('adjustments', 'index'))

    frm = SQLFORM(db.adjustments, record, _method='POST', hideerror=True, showid=False)


    frm.custom.widget.station_name['_readonly'] = 'true'
    frm.custom.widget.title['_readonly'] = 'true'
    frm.custom.widget.content['_readonly'] = 'true'

    return dict(frm=frm, list_status_edit=list_status_edit, current_status=current_status)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def ajax_issue_adjustment(*args, **kwargs):
    try:
        db(db.adjustments.id == request.vars.id).update(
            status=request.vars.status,
        )

        return dict(success=True)
    except Exception as ex:
        logger.error(str(ex))

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def index_alert():
    types = db.adjustments.adjustment_type.requires.options()
    status = db.adjustments.status.requires.options()
    # stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)
    return locals()

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def get_list_adjustments_alert(*args, **kwargs):
    try:
        s_search = request.vars.sSearch
        # sometext = request.vars.sometext
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        station_id = request.vars.station_id
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.sensor_trouble_history.id > 0)
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

        list_data = db(conditions).select(orderby=db.sensor_trouble_history.get_time,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        iRow = iDisplayStart + 1
        stations_dict = common.get_station_dict()[0]
        indicator_dict = common.get_indicator_dict()

        status = dict(db.adjustments.status.requires.options())
        colors = ['green', 'green', 'orange', 'red', 'gray', 'gray']
        for i, item in enumerate(list_data):
            row = [
                str(iDisplayStart + 1 + i),
                # A(item.station_id, _href = URL('', args = [item.id])),
                stations_dict[str(item.station_id)],
                SPAN(status[str(item.status)], _style="background:%s; color:white" % colors[item.status],
                     _class="badge"),
                item.get_time,
                indicator_dict[str(item.indicator_id)],
                item.value,
                item.unit,
                item.file_name,
            ]


            aaData.append(row)

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)
