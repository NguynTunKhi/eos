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
@auth.requires(lambda: (auth.has_permission('view', 'ftp_send_receive')))
def index():
    
    agents = db(db.agents.id > 0).select(db.agents.id, db.agents.agent_name)

    return dict(agents = agents)

################################################################################
@service.json
def get_list_ftp_send_receive(*args, **kwargs):
    try:
        sometext = request.vars.sometext
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
    
        conditions = (db.ftp_send_receive.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        # if sometext:
            # conditions &= ((db.ftp_send_receive.station_name.contains(sometext)) | 
                           # (db.ftp_send_receive.content.contains(sometext)) | 
                           # (db.ftp_send_receive.alarm_to.contains(sometext)))
        # if from_date:
            # conditions &= (db.ftp_send_receive.alarm_datetime >= date_util.string_to_datetime(from_date))
        # if to_date:
            # conditions &= (db.ftp_send_receive.alarm_datetime <= date_util.string_to_datetime(to_date))
        
        # Get all station_ids which belonged to current login user (group)
        # if auth.has_membership('admin'):
            # station_ids = common.get_stations_belong_current_user()
            # conditions &= (db.ftp_send_receive.station_id.belongs(station_ids))

        
        list_data = db(conditions).select(  db.ftp_send_receive.id, 
                                            db.ftp_send_receive.send_agent_name,
                                            db.ftp_send_receive.receive_agent_name,
                                            db.ftp_send_receive.file_name,
                                            db.ftp_send_receive.send_time,
                                            db.ftp_send_receive.status,
                                            db.ftp_send_receive.alarm_status,
                                            db.ftp_send_receive.archive_status,
                                            orderby = ~db.ftp_send_receive.send_time,
                                            limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        status = dict(db.ftp_send_receive.status.requires.options())

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            aaData.append([
                str(iDisplayStart + 1 + i),
                item.send_agent_name,
                item.receive_agent_name,
                item.file_name,
                item.send_time,
                status.get(str(item.status)),
                item.alarm_status,
                item.archive_status,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
            ])

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
 
################################################################################
# # @decor.requires_login()
# @decor.requires_permission('eos|areas|form')
def popup_update_status():
    record = db.ftp_send_receive(request.args(0)) or None
    if not record: redirect(URL('ftp_send_receive', 'index'))
    
    frm = SQLFORM(db.ftp_send_receive, record, _method = 'POST', hideerror = True, showid = False)
    frm.custom.widget.content['_row'] = '5'
    frm.custom.widget.content['_readonly'] = 'true'
    frm.custom.widget.station_name['_readonly'] = 'true'
    
    return  dict(frm = frm)
    
################################################################################
@service.json
# # @decor.requires_login()
# @decor.requires_permission('eos|areas|form')
def ajax_save_update_status(*args, **kwargs):
    try:
        if not request.vars.id:
            # db.ftp_send_receive.insert(**dict(request.vars)) 
            pass
        else:
            db(db.ftp_send_receive.id == request.vars.id).update(**dict(request.vars)) 
        
        return dict(success = True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))

################################################################################
def popup_add():
    id = request.vars.id
    station_type = request.vars.station_type
    station_id = request.vars.station_id
    indicator_id = request.vars.indicator_id
    ftp_send_receive = db.ftp_send_receive(id) or None
    if ftp_send_receive:
        station_id = ftp_send_receive.station_id
    station = db.stations(station_id) or None
    station_name = ''
    alarm_to = ''
    alarm_to_phone = ''
    content = ''
    alarm_type = 1 # Indicator alarm
    if station:
        station_name = station.station_name
        alarm_to = station.email
        alarm_to_phone = station.phone
        conditions = (db.station_indicator.id > 0)
        conditions &= (db.station_indicator.station_id == station_id)
        conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        # conditions &= (db.station_indicator.indicator_id == indicator_id)
        station_indicator = db(conditions).select(db.station_indicator.ALL)
        for row in station_indicator:
            content += '%s\n' %(row.equipment_name)
    # Set default value for some fields
    db.ftp_send_receive.station_id.default = station_id
    db.ftp_send_receive.station_name.default = station_name
    db.ftp_send_receive.alarm_type.default = alarm_type
    db.ftp_send_receive.alarm_to.default = alarm_to
    db.ftp_send_receive.alarm_to_phone.default = alarm_to_phone
    db.ftp_send_receive.content.default = content
    # Create form
    try:
        frm = SQLFORM(db.ftp_send_receive, ftp_send_receive, _method = 'POST', hideerror = True, showid = False)
    except Exception as ex:
        # Todo: Can check tai sao chet o day khi mo tu list ftp_send_receive
        frm = SQLFORM(db.ftp_send_receive, None, _method = 'POST', hideerror = True, showid = False)
    frm.custom.widget.content['_rows'] = 3
    frm.custom.widget.alarm_to['_rows'] = 1

    return  dict(frm = frm, ftp_send_receive=ftp_send_receive)

################################################################################
@service.json
def ajax_add_alarm_log(*args, **kwargs):
    try:
        rec_id = db.ftp_send_receive.insert(**dict(request.vars))
        phone = request.vars.alarm_to_phone
        content = request.vars.content
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
def alarm_menu(*args, **kwargs):
    try:
        from gluon.tools import prettydate
        # Loc nhung alarm trong 3 ngay tro lai
        conditions_recent_day = (db.ftp_send_receive.alarm_datetime >= request.now - timedelta(days = 3))
        conditions_belong = True
        station_ids = []
        
        # Get all station_ids which belonged to current login user (group)
        # Todo : tam thoi rao lai vi sua phan phan quyen
        # if auth.has_membership('admin'):
            # station_ids = common.get_stations_belong_current_user()
            # conditions_belong = (db.ftp_send_receive.station_id.belongs(station_ids))
        conditions_belong = (1==1)
        
        # Count for 'Station alarm'
        # conditions = conditions_recent_day & conditions_belong & (db.ftp_send_receive.alarm_type == 0)
        conditions = conditions_recent_day & conditions_belong
        station_alarms = db(conditions).select(
            db.ftp_send_receive.id,
            db.ftp_send_receive.station_name,
            db.ftp_send_receive.alarm_datetime,
            db.ftp_send_receive.content,
        )
        count_station_alarm = len(station_alarms)

        # Count for 'Indicator alarm'
        conditions = (db.data_alarm.get_time >= request.now - timedelta(days = 3))
        conditions &= (conditions_belong)
        count_indicator_alarm = db(conditions).count()
        
        # Count for 'Not solve yet' alarm
        conditions = (conditions_belong & (db.ftp_send_receive.status == 0))
        count_not_solve = db(conditions).count()
        
        # Count for alarm station in-active
        conditions = (db.station_off_log.end_off == None) & (db.station_off_log.station_id.belongs(station_ids))
        count_inactive = db(conditions).count()
        
        count_total = count_station_alarm + count_indicator_alarm + count_not_solve + count_inactive
        
        # Build HTML content to return client
        if count_total == 0:
            html_total, html_station_alarm, html_station_inactive, html_indicator_alarm, html_not_solve_alarm = ''
        else:
            html_total = str(count_total)
            html_station_alarm = str('(%s)' % count_station_alarm) if count_station_alarm else ''
            html_station_inactive = str('(%s)' % count_inactive) if count_inactive else ''
            html_indicator_alarm = str('(%s)' % count_indicator_alarm) if count_indicator_alarm else ''
            html_not_solve_alarm = str('(%s)' % count_not_solve) if count_not_solve else ''

        # Build html for ftp_send_receive in Header
        html = '''
                <a class="dropdown-toggle count-info" data-toggle="dropdown" href="#"> 
                    <i class="fa fa-bell"></i> '''
        if station_alarms:
            html += '<span class="label label-danger">%s</span>' % len(station_alarms)
        html += '''
                </a>
                <ul class="dropdown-menu dropdown-alerts">
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
                        ''' % (item.id, URL('ftp_send_receive', 'popup_add'), icon, item.content[:30] + '...', prettydate(item.alarm_datetime, T))
        html += '''
                    <li>
                        <div class="text-center link-block">
                            <a href="%s">
                                <strong>%s</strong>&nbsp;&nbsp;<i class="fa fa-angle-double-right"></i>
                            </a>
                        </div>
                    </li>
                </ul>  ''' % (URL('ftp_send_receive', 'index'), T('View all'))

        return dict(success = True,
                    html = html,
                    html_total = html_total, 
                    html_station_alarm = html_station_alarm, 
                    html_station_inactive = html_station_inactive, 
                    html_indicator_alarm = html_indicator_alarm, 
                    html_not_solve_alarm = html_not_solve_alarm)
    except Exception, ex:
        return dict(message = str(ex), success = False)
        
        
        