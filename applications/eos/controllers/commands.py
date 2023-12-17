# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from applications.eos.modules import common
from applications.eos.modules.w2pex import date_util
from datetime import datetime, timedelta
from applications.eos.modules import const

################################################################################
@auth.requires(lambda: (auth.has_permission('create', 'control') or auth.has_permission('edit', 'control')))
def form():
    # If in Update mode, get equivallent record
    record = db.commands(request.args(0)) or None
    msg = ''
    
    frm = SQLFORM(db.commands, record, _method = 'POST', hideerror = True, showid = False, _id = 'frmMain')
    
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
    lst_quiqment =[]
    equipmentId =''
    if record:
        equipmentId = record.equipment_id
        frm.custom.widget.station_name['_readonly'] = 'true'
        lst_quiqment = db(db.equipments.station_id == record.station_id).select(db.equipments.id, db.equipments.equipment)
        
    return dict(frm = frm, msg = XML(msg), lst_quiqment = lst_quiqment,type_datalogger=const.TYPE_SAMPLING, equipmentId = equipmentId)

################################################################################
def validate(frm):
    #Check condion
    #Get control value by : frm.vars.ControlName
    #If validate fail : frm.errors.ControlName = some message
    pass

def call():
    return service()

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'control')))
def index():
    # stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)

    return dict(stations = stations)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'control')))
def get_list_commands(*args, **kwargs):
    try:
        sometext = request.vars.sometext
        station_id = request.vars.station_id
        station_type = request.vars.station_type
        
        aaData = []
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
        
        conditions = (db.commands.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= ( (db.commands.command.contains(sometext)) | 
                            (db.commands.title.contains(sometext)) |
                            (db.commands.station_name.contains(sometext)))
        if station_id:
            conditions &= (db.commands.station_id == station_id)
        if station_type:
            conditions &= (db.commands.station_type == station_type)
        conditions &= (db.commands.is_calendar == False)
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.commands.station_id.belongs(station_ids))

        list_data = db(conditions).select(db.commands.id,
                                          db.commands.station_id,
                                          db.commands.station_name,
                                          db.commands.station_type,
                                          db.commands.created_date,
                                          db.commands.title,
                                          db.commands.is_process,
                                          db.commands.status,
                                          db.commands.send_data_logger_time,
                                          orderby=~db.commands.created_date,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        station_type = dict()
        for key, item in const.STATION_TYPE.iteritems():
            station_type[str(item['value'])] = T(item['name'])
        
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            url_issue_command = URL('issue_command', args=[item.id])
            icon_send = "<i class='fa fa-send'></i>"
            if (item.is_process == 1) & (item.status == 1):
                icon_send = ""
            history = ''
            # if item.is_process == 1:
            #     history = A(I(_class='fa fa-archive'), _href=URL('commands_history', vars={'command_id': item.id}))

            is_process = '-'
            if (item.is_process == 1):
                is_process = T('CMD_complete')
            elif (item.is_process == 0):
                is_process = T('CMD_unfulfilled')

            aaData.append([
                str(iDisplayStart + i + 1),
                A(item.station_name, _href = URL('form', args = [item.id])),
                station_type[str(item.station_type)],
                item.title,
                item.created_date,
                item.send_data_logger_time.strftime("%H:%M %d-%m-%Y") if item.send_data_logger_time else '',
                # Issue command
                "%s%s%s%s%s%s%s%s" % ( \
                "<a href='javascript: void(0);' class='btnAddNew' title='", 
                    T('Issue this command'),
                    "' data-for='#hfCommandId' data-callback='reloadDatatable_Command()' data-url='", 
                    url_issue_command, "'> ",
                "", icon_send, "</a>"),
                is_process,
                # A(I(_class='fa fa-calendar'), _href = URL('command_schedule', 'index', vars={'command_id': item.id})),
                # A(I(_class='fa fa-archive'), _href = URL('commands_history', vars={'command_id' : item.id})),
                # history,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id), item.id
            ])
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
    
################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'control')))
def commands_history():
    command_id = request.vars.command_id or ''
    # stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)

    status = db.commands_schedule.status.requires.options()
    
    return dict(stations = stations, status = status, command_id = command_id)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'command_schedule')))
def get_list_history_commands(*args, **kwargs):
    try:
        sometext = request.vars.sometext
        station_id = request.vars.station_id
        command_id = request.vars.command_id
        status = request.vars.status
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        
        aaData = []
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
        
        conditions = (db.commands_schedule.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= ( (db.commands_schedule.title.contains(sometext)) | 
                            (db.commands_schedule.station_name.contains(sometext)))
        if station_id:
            conditions &= (db.commands_schedule.station_id == station_id)
        if command_id:
            conditions &= (db.commands_schedule.command_id == command_id)
        if status:
            conditions &= (db.commands_schedule.status == status)
        if from_date:
            conditions &= (db.commands_schedule.issue_datetime >= date_util.string_to_datetime(from_date))
        if to_date:
            conditions &= (db.commands_schedule.issue_datetime < date_util.string_to_datetime(to_date) + timedelta(days = 1))

        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.commands_schedule.station_id.belongs(station_ids))

        list_data = db(conditions).select(  db.commands_schedule.id, 
                                            db.commands_schedule.station_name,
                                            db.commands_schedule.command_id,
                                            db.commands_schedule.issue_datetime,
                                            db.commands_schedule.execute_datetime,
                                            db.commands_schedule.title,
                                            db.commands_schedule.status,
                                            orderby = ~db.commands_schedule.issue_datetime | db.commands_schedule.status,
                                            limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        status = dict(db.commands_schedule.status.requires.options())
        
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            aaData.append([
                str(iDisplayStart + i + 1),
                item.station_name,
                item.title,
                item.issue_datetime,
                item.execute_datetime,
                status[str(item.status)],
                A(I(_class='fa fa-archive'), _href = URL('commands_results', vars={'command_schedule_id' : item.id})),
            ])
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
     
################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'control')))
def commands_results():
    command_schedule_id = request.vars.command_schedule_id or ''
    # stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)

    status = db.commands_schedule.status.requires.options()
    
    return dict(stations = stations, status = status, command_schedule_id = command_schedule_id)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'control')))
def get_list_commands_result(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        command_id = request.vars.command_id
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        command_schedule_id = request.vars.command_schedule_id
        
        aaData = []
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
        
        conditions = (db.command_results.id > 0)
        if command_schedule_id:
            conditions &= (db.command_results.command_schedule_id == command_schedule_id)
        if station_id:
            conditions &= (db.command_results.station_id == station_id)
        if command_id:
            conditions &= (db.command_results.command_id == command_id)
        if from_date:
            conditions &= (db.command_results.issue_datetime >= date_util.string_to_datetime(from_date))
        if to_date:
            conditions &= (db.command_results.issue_datetime < date_util.string_to_datetime(to_date) + timedelta(days = 1))
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.command_results.station_id.belongs(station_ids))

        list_data = db(conditions).select(  db.command_results.id, 
                                            db.command_results.station_name,
                                            db.command_results.issue_datetime,
                                            db.command_results.title,
                                            orderby = ~db.command_results.issue_datetime | db.command_results.command_id,
                                            limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            url_result = URL('view_results', args=[item.id])
            
            aaData.append([
                str(iDisplayStart + i + 1),
                item.station_name,
                item.title,
                item.issue_datetime,
                "%s%s%s%s%s%s" % ( \
                "<a href='javascript: void(0);' class='btnAddNew' title='", 
                    T('View results'),
                    "' data-callback='' data-url='", 
                    url_result, "'> ",
                "<i class='fa fa-archive'></i></a>"),
            ])
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
     
################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'control')))
def issue_command():
    record = db.commands(request.args(0)) or None
    if not record:
        redirect(URL('commands', 'index'))
    
    frm = SQLFORM(db.commands, record, _method = 'POST', hideerror = True, showid = False)
    
    frm.custom.widget.command['_rows'] = '8'
    frm.custom.widget.station_name['_readonly'] = 'true'
    frm.custom.widget.title['_readonly'] = 'true'
    frm.custom.widget.command['_readonly'] = 'true'
    
    return dict(frm = frm)

################################################################################
@service.json
# # @decor.requires_login()
@auth.requires(lambda: (auth.has_permission('create', 'control')))
def ajax_issue_command(*args, **kwargs):
    try:
        # Todo : Thuc hien cu the viec lay mau o day
        # ex : tao file excel va save o server nao day
        
        
        # Luu command nay vao bang 'commands_schedule'
        db.commands_schedule.insert(
            command_id = request.vars.id,
            station_id = request.vars.station_id,
            station_name = request.vars.station_name,
            title = request.vars.title,
            execute_datetime = request.now,
            status = 1,         # Running
        )

        db(db.commands.id == request.vars.id).update(
            status=1,
        )
        
        return dict(success = True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))    
    
################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'control')))
def view_results():
    record = db.command_results(request.args(0)) or None
    if not record:
        redirect(URL('commands', 'index'))
    
    return dict(record = record)


################################################################################
#hungdx issue 44 add (co the ap dung cho cac chon tinh, vung ... fix sau
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
        type_logger = ''
        command_name = ''

        if command_id:
            command_content = db(db.datalogger_command.id == command_id).select(db.datalogger_command.command_content).first().command_content
            command_name = db(db.datalogger_command.id == command_id).select(db.datalogger_command.command_name).first().command_name
            type_logger = db(db.datalogger_command.id == command_id).select(db.datalogger_command.type_logger).first().type_logger
        if station_id:
            station_type_logger = db(db.datalogger.station_id == station_id).select().first()
            if station_type_logger is None:
                type_logger = ''
            else:
                type_logger = station_type_logger.type_logger
        if station_id:
            logger_id = db(db.datalogger.station_id == station_id).select().first()
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

        return dict(success=True, html=html,type_logger = type_logger, logger_id=logger_id, command_content=command_content, command_name=command_name)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
def get_list_command_by_station(*args, **kwargs):
    try:
        station_id = request.vars.station_id  # Chuoi tim kiem nhap tu form
        # Get all
        command_list = db(db.datalogger_command.station_id == station_id).select()

        for i in range(len(command_list)):
            command_list[i].id = str(command_list[i].id)

        return dict(command_list=command_list, success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)