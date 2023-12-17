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
    record = db.adjustments_calendar(request.args(0)) or None
    msg = ''
    frequency = request.vars.repeatMode or None
    frm = SQLFORM(db.adjustments_calendar, record, _method='POST', hideerror=True, showid=False, _id='frmMain')

    frequency_at = ''
    if frequency == 'weekly':
        frequency_at = request.vars.weeklyFrequency
    if frequency == 'monthly':
        frequency_at = request.vars.monthlyFrequency

    start_time = request.vars.start_time
    end_time = request.vars.end_time
    start_hour = int(start_time.split(':')[0]) if start_time else 0
    end_hour = int(end_time.split(':')[0]) if end_time else 0

    if frm.process(onvalidation=validate, detect_record_change=True, hideerror=True).accepted:
        calendar_id = frm.vars.id
        db(db.adjustments_calendar.id ==calendar_id).update(
            start_hour=start_hour,
            end_hour=end_hour,
            frequency=frequency,
            frequency_at=','.join(frequency_at)
        )
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
    list_indicators = []
    list_status_edit = []
    can_update_status = '1'
    current_status = 0
    current_status_name = ''

    if record:
        usr_dict = common.get_usr_dict()[0]
        fullname = usr_dict.get(record.created_by)
        frm.custom.widget.station_name['_readonly'] = 'true'
        indicator_id = record.indicator_id
        list_status_edit.append({'value': 0, 'name': 'Draft'})
        list_status_edit.append({'value': 2, 'name': 'Wait for approve'})
        indicator_name = record.indicator_name
        current_status = record.status

        if ((current_status == 0) | (current_status == 2)):
            can_update_status = '1'
        else:
            can_update_status = '0'

        if current_status == 4:
            current_status_name = 'Accepted'
        elif current_status == 5:
            current_status_name = 'Cancelled'
        elif current_status == 3:
            current_status_name = 'Rejected'
        # Get all indicators to fill in dropdown
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
        list_status_edit.append({'value': 0, 'name': 'Draft'})
        list_status_edit.append({'value': 2, 'name': 'Wait for approve'})
        can_update_status = '1'
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
                list_status_edit=list_status_edit,
                indicator_id=indicator_id, indicator_name=indicator_name, current_status=current_status,
                can_update_status=can_update_status, current_status_name=current_status_name)


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

        logger_id = db(db.datalogger.station_id == station_id).select().first()
        if logger_id is None:
            logger_id = ''
        else:
            logger_id = logger_id.logger_id
        for i in range(len(station_indicator_list)):
            station_indicator_list[i].id = str(station_indicator_list[i].id)

            if station_indicator_list[i].indicator_id:
                indicator_details = db.indicators(station_indicator_list[i].indicator_id) or None
                if indicator_details:
                    station_indicator_list[i].indicators_name = str(indicator_details.source_name)
                else:
                    station_indicator_list[i].indicators_name = ''

        return dict(station_indicator_list=station_indicator_list, logger_id=logger_id, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def index():
    types = db.adjustments_calendar.adjustment_type.requires.options()
    status = db.adjustments_calendar.status.requires.options()
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
        conditions = (db.adjustments_calendar.id > 0)
        if sometext:
            conditions &= ((db.adjustments_calendar.title.contains(sometext)) | (db.adjustments_calendar.content.contains(sometext)))
        if type:
            conditions &= (db.adjustments_calendar.adjustment_type == type)
        if status:
            conditions &= (db.adjustments_calendar.status == status)

        if from_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
            except:
                from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            conditions &= (db.adjustments_calendar.from_date >= from_date)
        if to_date:
            try:
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
            except:
                to_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            conditions &= (db.adjustments_calendar.to_date <= to_date + timedelta(days=1))

        if station_id:
            conditions &= (db.adjustments_calendar.station_id == station_id)
        if is_process:
            conditions &= (db.adjustments_calendar.is_process == is_process)

        # conditions &= (db.adjustments_calendar.created_by == current_user.id)
        #hungdx issue 44 khong can check o day vi create_by la da duoc phan quyen
        list_data = db(conditions).select(db.adjustments_calendar.id,
                                          db.adjustments_calendar.title,
                                          db.adjustments_calendar.content,
                                          db.adjustments_calendar.created_by,
                                          db.adjustments_calendar.station_name,
                                          db.adjustments_calendar.from_date,
                                          db.adjustments_calendar.to_date,
                                          db.adjustments_calendar.content,
                                          db.adjustments_calendar.adjustment_type,
                                          db.adjustments_calendar.status,
                                          db.adjustments_calendar.is_process,
                                          db.adjustments_calendar.created_date,
                                          db.adjustments_calendar.start_hour,
                                          db.adjustments_calendar.end_hour,
                                          db.adjustments_calendar.frequency,
                                          db.adjustments_calendar.frequency_at,
                                          orderby=~db.adjustments_calendar.created_date | db.adjustments_calendar.status,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        # Thu tu ban ghi
        iRow = iDisplayStart + 1
        usr_dict = common.get_usr_dict()[0]
        types = dict(db.adjustments_calendar.adjustment_type.requires.options())
        status = dict(db.adjustments_calendar.status.requires.options())
        colors = ['green', 'green', 'orange', 'red', 'gray', 'gray']
        print(list_data)
        days_of_week = dict()
        for key, item in const.DAYS_OF_WEEK.iteritems():
            days_of_week[str(item['value'])] = T(item['text'])
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            frequency = ''
            hour = ''
            days = []
            if item.frequency_at:
                for j in item.frequency_at.split(','):
                    if item.frequency == 'weekly':
                        days.append(days_of_week[str(j)])
                    if item.frequency == 'monthly':
                        days.append(T('day') + ' ' + j)
            else:
                days.append('-')

            if item.start_hour and item.end_hour:
                hour += str(item.start_hour) + ':00' + ' - ' + str(item.end_hour) + ':00'
            elif item.start_hour:
                hour += str(item.start_hour) + ':00'
            elif item.end_hour:
                hour += str(item.end_hour) + ':00'
            else:
                hour = '-'

            if item.frequency == 'daily':
                frequency = T('Every day')
            if item.frequency == 'weekly':
                frequency = T('Every week')
            if item.frequency == 'monthly':
                frequency = T('Every month')
            if not item.frequency:
                frequency = '-'

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
                hour,
                frequency,
                days,
                types[str(item.adjustment_type)],
                SPAN(status[str(item.status)], _style="background:%s; color:white" % colors[item.status],
                     _class="badge"),
                # item.created_date.strftime('%H:%M %d/%m'),
                # is_process,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
            ])

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
def del_records(table, *args, **kwargs):
    try:
        id = request.vars.id  # for single record
        array_data = request.vars.ids  # for list record (dc truyen qua app.executeFunction())
        list_ids = []
        if array_data:  list_ids = array_data.split(',')
        list_ids.append(id) if id else list_ids

        if list_ids:
            db(db[table].id.belongs(list_ids)).delete()
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def calendar():
    # lay nhung adjustments_calendar co ngay bat dau trong 7 ngay gan nhat
    common_cd = (db.adjustments_calendar.from_date >= request.now - timedelta(days=7))
    # va co status 'Wait for approve', 'Rejected'
    conditions = common_cd & (db.adjustments_calendar.status <= 4)
    conditions &= (db.adjustments_calendar.created_by == current_user.id)

    rows = db(conditions).select(db.adjustments_calendar.id,
                                 db.adjustments_calendar.status,
                                 db.adjustments_calendar.title,
                                 orderby=~db.adjustments_calendar.from_date | ~db.adjustments_calendar.status)

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

        conditions = (db.adjustments_calendar.id > 0)
        if start:
            conditions &= (db.adjustments_calendar.from_date >= date_util.string_to_date(start))
        if end:
            conditions &= (db.adjustments_calendar.to_date <= date_util.string_to_date(end))

        conditions &= (db.adjustments_calendar.created_by == current_user.id)

        rows = db(conditions).select(db.adjustments_calendar.id,
                                     db.adjustments_calendar.created_by,
                                     db.adjustments_calendar.created_date,
                                     db.adjustments_calendar.from_date,
                                     db.adjustments_calendar.to_date,
                                     db.adjustments_calendar.title,
                                     db.adjustments_calendar.content,
                                     db.adjustments_calendar.status)
        array_object = []
        usr_dict = common.get_usr_dict()[0]
        types = dict(db.adjustments_calendar.adjustment_type.requires.options())
        status = dict(db.adjustments_calendar.status.requires.options())
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

@service.json
@auth.requires(lambda: (auth.has_permission('view', 'adjust_manager') or auth.has_permission('view', 'adjust_company')))
def ajax_get_adjustments_calendar(*args, **kwargs):
    try:
        calendar_id = request.vars.calendar_id
        datalogger_id = ''
        start_hour = ''
        end_hour = ''
        html = ''
        data = db(db.adjustments_calendar.id == calendar_id).select(
            # db.commands_calendar.command_id,
            # db.commands_calendar.station_id,
            # # station_name = command.station_name,
            # # station_name=station_name,
            # db.commands_calendar.bottle,
            # db.commands_calendar.content,
            # db.commands_calendar.logger_id,
            # db.commands_calendar.title,
            # # execute_datetime = request.now,
            # # status = 1,         # Running
            # db.commands_calendar.start_date,
            # db.commands_calendar.end_date,
            db.adjustments_calendar.start_hour,
            db.adjustments_calendar.end_hour,
            db.adjustments_calendar.frequency,
            db.adjustments_calendar.frequency_at,
        ).first()
        # command = db.datalogger_command(request.vars.command_id)
        if data:
            # datalogger_id = db(db.datalogger.station_id == data.station_id).select(db.datalogger.logger_id).first()['logger_id']
            start_hour = str(data.start_hour) + ':00' if data.start_hour else None
            end_hour = str(data.end_hour) + ':00' if data.end_hour else None
            # start_date = data.start_date.strftime('%Y/%m/%d %H:%M') if data.start_date else None
            # end_date = data.end_date.strftime('%Y/%m/%d %H:%M') if data.end_date else None

            if data.frequency == 'weekly':
                freq = data.frequency_at.split(',')
                if freq.count(str(0))>=1:
                    html+= "<option value='%s' selected >%s</option>" % (str(0), T('Mon'))
                else:
                    html+= "<option value='%s'>%s</option>" % (str(0), T('Mon'))

                if freq.count(str(1))>=1:
                    html+= "<option value='%s' selected >%s</option>" % (str(1), T('Tue'))
                else:
                    html+= "<option value='%s'>%s</option>" % (str(1), T('Tue'))

                if freq.count(str(2))>=1:
                    html+= "<option value='%s' selected >%s</option>" % (str(2), T('Wed'))
                else:
                    html+= "<option value='%s'>%s</option>" % (str(2), T('Wed'))

                if freq.count(str(3))>=1:
                    html+= "<option value='%s' selected >%s</option>" % (str(3), T('Thu'))
                else:
                    html+= "<option value='%s'>%s</option>" % (str(3), T('Thu'))

                if freq.count(str(4))>=1:
                    html+= "<option value='%s' selected >%s</option>" % (str(4), T('Fri'))
                else:
                    html+= "<option value='%s'>%s</option>" % (str(4), T('Fri'))

                if freq.count(str(5))>=1:
                    html+= "<option value='%s' selected >%s</option>" % (str(5), T('Sat'))
                else:
                    html+= "<option value='%s'>%s</option>" % (str(5), T('Sat'))

                if freq.count(str(6))>=1:
                    html+= "<option value='%s' selected >%s</option>" % (str(6), T('Sun'))
                else:
                    html+= "<option value='%s'>%s</option>" % (str(6), T('Sun'))

            if data.frequency == 'monthly':
                freq = data.frequency_at.split(',')
                #<option selected value="1">{{=T('Day')}} 1</option>
                for i in range(1,32):
                    if freq.count(str(i)) >= 1:
                        html += "<option value='%s' selected >%s %s</option>" % (str(i), T('Day'), i)
                    else:
                        html+= "<option value='%s'>%s %s</option>" % (str(i),T('Day'), i)


        return dict(success=True,data=data, datalogger_id = datalogger_id, start_hour = start_hour, end_hour=end_hour, freq_html = html)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success=False, message=str(ex))