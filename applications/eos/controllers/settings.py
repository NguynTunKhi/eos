# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
import json
from applications.eos.modules import const, common

#@auth.requires_membership('manager')
#@auth.requires_login()
#@decor.requires_permission()
def index():
    # If in Update mode, get equivallent record
    # Get first row of settings table and working on this
    for row in db(db.settings.id > 0).select():
        first_row = row
    record = db.settings(first_row.id) or None
    msg = ''
    frm = SQLFORM(db.settings, record, _method = 'POST', hideerror = True, showid = False, _id = 'frmMain')
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

    frm.custom.widget.lack_data_value['_style'] = "width:90%"
    frm.custom.widget.paging['_style'] = "width:90%"
    frm.custom.widget.online_refresh_timing['_style'] = "width:90%"
    frm.custom.widget.server_input_ip['_style'] = "width:90%"
    frm.custom.widget.server_input_port['_style'] = "width:90%"
    frm.custom.widget.get_data_interval['_style'] = "width:90%"
    frm.custom.widget.server_output_ip['_style'] = "width:90%"
    frm.custom.widget.server_output_port['_style'] = "width:90%"
    frm.custom.widget.recent_notification_day['_style'] = "width:90%"
    frm.custom.widget.recent_alarm_day['_style'] = "width:90%"
    return dict(frm = frm, msg = XML(msg))

################################################################################
def validate(frm):
    #Check condion
    #Get control value by : frm.vars.ControlName
    #If validate fail : frm.errors.ControlName = some message
    pass
################################################################################
def call():
    return service()
@service.json
# @decor.requires_permission('ip_manager|delete')
def ajax_save_settings(*args, **kwargs):
    try:
        lack_data_value = request.vars.lack_data_value
        paging = request.vars.paging
        online_refresh_timing = request.vars.online_refresh_timing
        server_input_ip = request.vars.server_input_ip
        server_input_port = request.vars.server_input_port
        get_data_interval = request.vars.get_data_interval
        server_output_ip = request.vars.server_output_ip
        server_output_port = request.vars.server_output_port
        recent_notification_day = request.vars.recent_notification_day
        recent_alarm_day = request.vars.recent_alarm_day
        # Check if have any record, if existed get first row to working
        for row in db(db.settings.id > 0).select():
            first_row = row
        if first_row.id:
            db(db.settings.id == first_row.id).update(
                lack_data_value=lack_data_value,
                paging = paging,
                online_refresh_timing = online_refresh_timing,
                server_input_ip = server_input_ip,
                server_input_port = server_input_port,
                get_data_interval = get_data_interval,
                server_output_ip = server_output_ip,
                server_output_port = server_output_port,
                recent_notification_day = recent_notification_day,
                recent_alarm_day = recent_alarm_day,
            )
        else:
            db.settings.insert(
                lack_data_value=lack_data_value,
                paging=paging,
                online_refresh_timing=online_refresh_timing,
                server_input_ip=server_input_ip,
                server_input_port=server_input_port,
                get_data_interval=get_data_interval,
                server_output_ip=server_output_ip,
                server_output_port=server_output_port,
                recent_notification_day=recent_notification_day,
                recent_alarm_day=recent_alarm_day,
            )
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

################################################################################
