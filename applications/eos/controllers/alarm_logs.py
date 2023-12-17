# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from applications.eos.modules.w2pex import date_util
from applications.eos.modules import common
from datetime import timedelta


def call():
    return service()

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def index():
    provinces = common.get_province_have_station()
    not_solve = request.vars.not_solve

    # levels = dict(db.alarm_logs.alarm_level.requires.options())
    levels = db.alarm_logs.alarm_level.requires.options()
    status = db.alarm_logs.status.requires.options()
    conditions = (db.stations.id > 0)
    station_id = request.vars.station_id

    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(orderby=db.stations.order_no)
    return dict(levels=levels, status=status, not_solve=not_solve,provinces=provinces,stations=stations,station_id=station_id)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def get_list_alarm_logs(*args, **kwargs):
    try:
        s_search = request.vars.sSearch
        not_solve = request.vars.not_solve
        sometext = request.vars.sometext
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        alarm_level = request.vars.alarm_level
        status = request.vars.status
        province_id = request.vars.province_id
        station_type = request.vars.station_type
        station_id = request.vars.station_id

        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.alarm_logs.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= ((db.alarm_logs.station_name.contains(sometext)) |
                           (db.alarm_logs.content.contains(sometext)) |
                           (db.alarm_logs.alarm_to.contains(sometext)))
        if status:
            conditions &= (db.alarm_logs.status == status)
        if alarm_level:
            conditions &= (db.alarm_logs.alarm_level == alarm_level)
        if from_date:
            conditions &= (db.alarm_logs.alarm_datetime >= date_util.string_to_datetime(from_date))
        if to_date:
            conditions &= (db.alarm_logs.alarm_datetime < date_util.string_to_datetime(to_date) + timedelta(days = 1))
        if not station_id:
            if station_type:
                type_station_ids = db(db.stations.station_type == station_type).select(db.stations.id)
                type_station_ids = [item.id for item in type_station_ids]
                conditions &= (db.alarm_logs.station_id.belongs(type_station_ids))
            if province_id:
                province_station_ids = db(db.stations.province_id == province_id).select(db.stations.id)
                province_station_ids = [item.id for item in province_station_ids]
                conditions &= (db.alarm_logs.station_id.belongs(province_station_ids))
        else:
            conditions &= (db.alarm_logs.station_id == station_id)

        # Get all station_ids which belonged to current login user (group)
        #if auth.has_membership('admin'):
        # if not 'admin' in current_user.roles: #hungdx comment issue 44
        #     station_ids = common.get_stations_belong_current_user()
        #     conditions &= (db.alarm_logs.station_id.belongs(station_ids))

        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.alarm_logs.station_id.belongs(station_ids))

        if not_solve:
            orderby = db.alarm_logs.status | ~db.alarm_logs.alarm_datetime
        else:
            orderby = ~db.alarm_logs.alarm_datetime

        list_data = db(conditions).select(  db.alarm_logs.id,
                                            db.alarm_logs.station_name,
                                            db.alarm_logs.alarm_datetime,
                                            db.alarm_logs.alarm_level,
                                            db.alarm_logs.content,
                                            db.alarm_logs.alarm_to,
                                            db.alarm_logs.status,
                                            orderby = orderby,
                                            limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        iRow = iDisplayStart + 1
        levels = dict(db.alarm_logs.alarm_level.requires.options())
        status = dict(db.alarm_logs.status.requires.options())

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            # Check status to assign alert badge
            if item.status == 0:    # Not solve yet
                item_status = SPAN(status[str(item.status)], _style="background:red; color:white", _class="badge")
            else:
                item_status = SPAN(status[str(item.status)], _style="background:gray; color:white", _class="badge")

            url = URL('popup_update_status', args=[item.id])

            bg_color = '#FF9900';
            color = '#FFFFFF';
            for al_key in const.ALARM_LOG_LEVEL:
                if item.alarm_level == const.ALARM_LOG_LEVEL[al_key]['value']:
                    bg_color = const.ALARM_LOG_LEVEL[al_key]['color']
                    color = const.ALARM_LOG_LEVEL[al_key]['color2']
                    break

            aaData.append([
                str(iDisplayStart + 1 + i),
                A(item.station_name, _class='show_alarm_log_detail', _href = 'javascript: void(0)', data=dict(id=str(item.id), url=URL('alarm_logs', 'popup_add'))),
                item.alarm_datetime,
                SPAN(levels[str(item.alarm_level)], _style="background:%s; color: %s" % (bg_color, color), _class="badge"),
                item.content,
                item.alarm_to,
                # Todo : neu co quyen thi cho link popup de chinh status, neu ko thi label
                item_status,
                "%s%s%s%s%s" % ( \
                "<a href='javascript: void(0);' class='btnAddNew' title='",
                    T('Update status'),
                    "' data-for='#hfAlarmId'  data-callback='reloadDatatable_alarm_logs()' \
                    data-url='", url, "'> <i class='fa fa-edit'></i></a>",
                ),
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
            ])

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
 
################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def popup_update_status():
    record = db.alarm_logs(request.args(0)) or None
    if not record: redirect(URL('alarm_logs', 'index'))
    
    frm = SQLFORM(db.alarm_logs, record, _method = 'POST', hideerror = True, showid = False)
    frm.custom.widget.content['_row'] = '5'
    frm.custom.widget.content['_readonly'] = 'true'
    frm.custom.widget.station_name['_readonly'] = 'true'
    
    return  dict(frm = frm)
    
################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('edit', 'alarm_log')))
def ajax_save_update_status(*args, **kwargs):
    try:
        if not request.vars.id:
            # db.alarm_logs.insert(**dict(request.vars)) 
            pass
        else:
            db(db.alarm_logs.id == request.vars.id).update(**dict(request.vars)) 
        
        return dict(success = True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def popup_add():
    id = request.vars.id
    station_type = request.vars.station_type
    station_id = request.vars.station_id
    indicator_id = request.vars.indicator_id
    alarm_logs = db.alarm_logs(id) or None
    if alarm_logs:
        station_id = alarm_logs.station_id
    station = db.stations(station_id) or None
    station_name = ''
    alarm_to = ''
    alarm_to_phone = ''
    content = ''
    alarm_type = 1
    # Indicator alarm
    # if station:
    #     station_name = station.station_name
    #     alarm_to = station.email
    #     alarm_to_phone = station.phone
    #     conditions = (db.station_indicator.id > 0)
    #     conditions &= (db.station_indicator.station_id == station_id)
    #     conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    #     # conditions &= (db.station_indicator.indicator_id == indicator_id)
    #     station_indicator = db(conditions).select(db.station_indicator.ALL)
    #     for row in station_indicator:
    #         if row.equipment_name: content += '%s\n' %(row.equipment_name)
    # # Set default value for some fields
    # db.alarm_logs.station_id.default = station_id
    # db.alarm_logs.station_name.default = station_name
    # db.alarm_logs.alarm_type.default = alarm_type
    # db.alarm_logs.alarm_to.default = alarm_to
    # db.alarm_logs.alarm_to_phone.default = alarm_to_phone
    # db.alarm_logs.content.default = content
    if station:
        station_name = station.station_name
        station_alarms = db(db.station_alarm.station_id == station_id).select()
        if station_alarms:
            station_alarm = station_alarms.first()
            alarm_to = station_alarm.exceed_email_list
            alarm_to_phone = station_alarm.exceed_phone_list
            content = station_alarm.exceed_msg
    # Set default value for some fields
    db.alarm_logs.station_id.default = station_id
    db.alarm_logs.station_name.default = station_name
    db.alarm_logs.alarm_type.default = alarm_type
    db.alarm_logs.alarm_to.default = alarm_to
    db.alarm_logs.alarm_to_phone.default = alarm_to_phone
    db.alarm_logs.content.default = content
    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)
    res_id = {}
    for item in stations:
        res_id[str(item.id)] = item.station_name
    db.alarm_logs.station_id.requires = IS_IN_SET(res_id)
    # Create form
    try:
        frm = SQLFORM(db.alarm_logs, alarm_logs, _method = 'POST', hideerror = True, showid = False)
    except Exception as ex:
        return dict(success = False, message = str(ex))
    frm.custom.widget.content['_rows'] = 3
    frm.custom.widget.alarm_to['_rows'] = 1

    return  dict(frm = frm, alarm_logs=alarm_logs)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('create', 'alarm_log')))
def ajax_add_alarm_log(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        station_name = request.vars.station_name
        content = request.vars.content
        alarm_level = request.vars.alarm_level
        alarm_type = request.vars.alarm_type
        alarm_to = request.vars.alarm_to
        alarm_to_phone = request.vars.alarm_to_phone
        status = request.vars.status
        send_sms = request.vars.send_sms
        rec_id = db.alarm_logs.insert(station_id = station_id,station_name = station_name,content= content, alarm_level=alarm_level,alarm_type=alarm_type,
                                        alarm_to = alarm_to, alarm_to_phone=alarm_to_phone, status=status, send_sms=send_sms)
        #rec_id = db.alarm_logs.insert(**dict(request.vars))
        phone = request.vars.alarm_to_phone
        content = request.vars.content

        fmt_new = '%d-%m-%Y %H:%M:%S'
        now = datetime.now()

        subject = '%s %s (%s)' % (station_name, ' lỗi sensor tại thời điểm ', now.strftime(fmt_new))
        try:
            if alarm_to and subject:
                common.send_mail_alarm(mail_to=alarm_to,mail_cc='', subject=subject,message=content)
        except Exception as ex:
            pass

        #i will send my email here
        if request.vars.send_sms and phone:
            phones = phone.split(',')
            from suds.client import Client
            conn = Client('http://124.158.6.45/CMC_BRAND/Service.asmx?WSDL')
            for p in phones:
                p = p.strip()
                # Todo: Uncomment for prod
                ret = conn.service.SendSMSBrandName(phone=p, sms=content, sender='CMC Telecom',
                                                username='hn_telecom', password='telecom@123!')
        return dict(success = True)
    except Exception as ex:
        return dict(success = False, message = str(ex))

################################################################################
@service.json
# @auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def alarm_menu(*args, **kwargs):
    try:
        from gluon.tools import prettydate
        # Loc nhung alarm trong 3 ngay tro lai
        # conditions_recent_day = (db.alarm_logs.alarm_datetime >= request.now - timedelta(days = 3))
        conditions_recent_day = {'alarm_datetime': {'$gte': request.now - timedelta(days=3)}}
        # conditions_belong = True
        station_ids = []
        
        # Get all station_ids which belonged to current login user (group)
        # Todo : tam thoi rao lai vi sua phan phan quyen
        # if auth.has_membership('admin'):
            # station_ids = common.get_stations_belong_current_user()
            # conditions_belong = (db.alarm_logs.station_id.belongs(station_ids))
        # conditions_belong = (1==1)
        
        # Count for 'Station alarm'
        # conditions = conditions_recent_day & conditions_belong & (db.alarm_logs.alarm_type == 0)
        # conditions = conditions_recent_day #& conditions_belong
        # station_alarms = db(conditions).select(
        #     db.alarm_logs.id,
        #     db.alarm_logs.station_name,
        #     db.alarm_logs.alarm_datetime,
        #     db.alarm_logs.content,
        #     orderby=~db.alarm_logs.alarm_datetime
        # )
        station_alarms = pydb.alarm_logs.find(conditions_recent_day, {
            '_id': 1,
            'station_name': 1,
            'alarm_datetime': 1,
            'content': 1
        }).sort('alarm_datetime', -1)
        count_station_alarm = pydb.alarm_logs.count(conditions_recent_day)
        # Count for 'Indicator alarm'

        # conditions = (db.station_indicator_exceed.get_time >= request.now - timedelta(days = 7))
        conditions = {'get_time': {'$gte': request.now - timedelta(days=7)}}
        # conditions &= (conditions_belong)
        count_indicator_alarm = pydb.station_indicator_exceed.count(conditions)
        
        # Count for 'Not solve yet' alarm
        # conditions = (conditions_belong & (db.alarm_logs.status == 0))
        conditions = {'status': 0}
        count_not_solve = pydb.alarm_logs.count(conditions)
        # Count for equipment_error
        # conditions = (db.sensor_trouble_history.get_time >= request.now - timedelta(days = 3))
        conditions = {'get_time': {'$gte': request.now - timedelta(days=3)}}
        # conditions &= (conditions_belong)
        count_equipment_error = pydb.sensor_trouble_history.count(conditions)

        # Count for alarm station in-active
        # conditions = (db.stations.status == 4)
        count_inactive = pydb.stations.count({'status': 4})

        count_total = count_station_alarm + count_indicator_alarm + count_not_solve + count_inactive + count_equipment_error
        
        # Build HTML content to return client
        if count_total == 0:
            html_total, html_station_alarm, html_station_inactive, html_indicator_alarm, html_not_solve_alarm, html_sensor_trouble_history, html_equipment_error = '','','','','','', ''
        else:
            html_total = str(count_total)
            html_station_alarm = str('(%s)' % count_station_alarm) if count_station_alarm else ''
            html_station_inactive = str('(%s)' % count_inactive) if count_inactive else ''
            html_indicator_alarm = str('(%s)' % count_indicator_alarm) if count_indicator_alarm else ''
            html_not_solve_alarm = str('(%s)' % count_not_solve) if count_not_solve else ''
            html_equipment_error = str('(%s)' % count_equipment_error) if count_equipment_error else ''

        # Build html for alarm_logs in Header
        html = '''
                <a class="dropdown-toggle count-info" data-toggle="dropdown" href="#"> 
                    <i class="fa fa-bell"></i> '''
        if count_station_alarm > 0:
            html += '<span class="label label-danger">%s</span>' % count_station_alarm
        html += '''
                </a>
                <ul class="dropdown-menu dropdown-alerts">
                <div class="scroll_alarm_menu">
                '''
        if not station_alarms:
            html += '''
                    <li>
                        <a style="text-center">
                            <div class="" >%s</div>
                        </a>
                    </li>
                    <li class="divider"></li>
                    ''' % T('No alarm!')
        else:
            for item in station_alarms:
                icon = '<i class="fa fa-times-circle text-danger"></i>'
                html += '''
                        <li>
                            <a class="show_alarm_log_detail" href="javascript: void(0);" data-id="%s" data-url="%s">
                                <div> %s  %s
                                    <span class="pull-right text-muted small">%s</span>
                                </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        ''' % (str(item['_id']), URL('alarm_logs', 'popup_add'), icon, item['content'], prettydate(item['alarm_datetime'], T))
        html += '''
                    </div>
                    <li>
                        <div class="text-center link-block">
                            <a href="%s">
                                <strong>%s</strong>&nbsp;&nbsp;<i class="fa fa-angle-double-right"></i>
                            </a>
                        </div>
                    </li>
                </ul>   ''' % (URL('alarm_logs', 'index'), T('View all'))
        html += '''
            <script>
                $('.scroll_alarm_menu').slimscroll({
                    height: '300px'
                });
            </script>
        '''
        return dict(success=True,
                    html=html,
                    html_total=html_total,
                    html_station_alarm=html_station_alarm,
                    html_station_inactive=html_station_inactive,
                    html_indicator_alarm=html_indicator_alarm,
                    html_equipment_error=html_equipment_error)
    except Exception as ex:
        return dict(message=ex.message, success=False)
