# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################


def call():
    return service()

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'command_schedule')))
def index():
    stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name)
    commands = db(db.commands.id > 0).select(db.commands.id, db.commands.title)
    return locals()

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'command_schedule')))
def get_list_schedule(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        station_id = request.vars.station_id
        command_id = request.vars.command_id
        frequency = request.vars.frequency

        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.commands_calendar.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if station_id:
            conditions &= (db.commands_calendar.station_id == station_id)
        if command_id:
            conditions &= (db.commands_calendar.command_id == command_id)
        if frequency:
            conditions &= (db.commands_calendar.frequency == frequency)

        list_data = db(conditions).select(db.commands_calendar.id,
                                          db.commands_calendar.command_id,
                                          db.commands_calendar.title,
                                          db.commands_calendar.station_name,
                                          db.commands_calendar.bottle,
                                          db.commands_calendar.start_date,
                                          db.commands_calendar.end_date,
                                          db.commands_calendar.start_hour,
                                          db.commands_calendar.end_hour,
                                          db.commands_calendar.frequency,
                                          db.commands_calendar.frequency_at,
                                          limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        days_of_week = dict()
        for key, item in const.DAYS_OF_WEEK.iteritems():
            days_of_week[str(item['value'])] = T(item['text'])

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            frequency = ''
            hour = ''
            days = []
            if item.frequency_at:
                for i in item.frequency_at.split(','):
                    if item.frequency == 'weekly':
                        days.append(days_of_week[str(i)])
                    if item.frequency == 'monthly':
                        days.append(T('day')+' '+i)
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

            aaData.append([
                A(str(iRow), _href=URL('commands', 'form', args=[item.command_id])),
                A(item.title, _href=URL('command_schedule', 'form', args=[item.id])),
                # '',
                item.station_name if item.station_name else '-',
                item.bottle if item.bottle else '-',
                item.start_date if item.start_date else '-',
                item.end_date if item.end_date else '-',
                # hour,
                # frequency,
                # days,
                INPUT(_group='0', _class='select_item', _type='checkbox', _value=item.id),
                item.id
            ])

            iRow += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'command_schedule')))
def del_command_schedule(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db.commands_calendar.id.belongs(list_ids)).delete()
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'command_schedule')))
def form():
    command_id = request.vars.command_id or ''

    conditions = (db.datalogger_command.station_id > 0)

    # Get command to fill dropdown
    commands = db(conditions).select(
        db.datalogger_command.id,
        db.datalogger_command.command_id,
        db.datalogger_command.station_id,
        db.datalogger_command.command_name,
        db.datalogger_command.command_content,
    )
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)

    return dict(stations = stations, commands=commands, command_id=command_id)

################################################################################
@service.json 
@auth.requires(lambda: (auth.has_permission('schedule', 'command_schedule')))
def ajax_set_command_schedule(*args, **kwargs):
    try:
        command_id = request.vars.command_id
        command = db.datalogger_command(request.vars.command_id)
        bottle = request.vars.bottle
        content = request.vars.content
        station_id = None
        if command:
            station_id = command.station_id

        station_name = db(db.stations.id == station_id).select(db.stations.station_name).first()['station_name']
        datalogger_id = db(db.datalogger.station_id == station_id).select(db.datalogger.logger_id).first()['logger_id']

        frequency = request.vars.repeat_mode
        start_time = request.vars.start_time
        end_time   = request.vars.end_time
        start_date = datetime.strptime(request.vars.start_date,'%Y/%m/%d %H:%M')
        end_date = datetime.strptime(request.vars.end_date,'%Y/%m/%d %H:%M')
        start_hour = int(start_time.split(':')[0]) if start_time else 0
        end_hour = int(end_time.split(':')[0]) if end_time else 0
        frequency_at = ''
        if frequency == 'weekly':
            frequency_at = request.vars.weeklyFrequency
        if frequency == 'monthly':
            frequency_at = request.vars.monthlyFrequency
        if not command:
            return dict(success = False, message = T('No command id!'))

        # Luu command nay vao bang 'commands_calendar'
        calendar_id = request.vars.calendar_id
        if calendar_id == 'form': calendar_id = None

        db.commands_calendar.update_or_insert(
            db.commands_calendar.id == calendar_id,
            command_id = command_id,
            station_id = station_id,
            # station_name = command.station_name,
            station_name = station_name,
            bottle = bottle,
            content = content,
            logger_id = datalogger_id,
            title = command.command_name,
            # execute_datetime = request.now,
            # status = 1,         # Running
            start_date = start_date,
            end_date = end_date,
            start_hour = start_hour,
            end_hour = end_hour,
            frequency=frequency,
            frequency_at=frequency_at,
        )
        return dict(success = True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))

@service.json
def ajax_get_command_calendar(*args, **kwargs):
    try:
        calendar_id = request.vars.calendar_id
        datalogger_id = ''
        start_hour = ''
        end_hour = ''
        html = ''
        data = db(db.commands_calendar.id == calendar_id).select(
            db.commands_calendar.command_id,
            db.commands_calendar.station_id,
            # station_name = command.station_name,
            # station_name=station_name,
            db.commands_calendar.bottle,
            db.commands_calendar.content,
            db.commands_calendar.logger_id,
            db.commands_calendar.title,
            # execute_datetime = request.now,
            # status = 1,         # Running
            db.commands_calendar.start_date,
            db.commands_calendar.end_date,
            db.commands_calendar.start_hour,
            db.commands_calendar.end_hour,
            db.commands_calendar.frequency,
            db.commands_calendar.frequency_at,
        ).first()
        # command = db.datalogger_command(request.vars.command_id)
        if data:
            datalogger_id = db(db.datalogger.station_id == data.station_id).select(db.datalogger.logger_id).first()['logger_id']
            start_hour = str(data.start_hour) + ':00' if data.start_hour else None
            end_hour = str(data.end_hour) + ':00' if data.end_hour else None
            start_date = data.start_date.strftime('%Y/%m/%d %H:%M') if data.start_date else None
            end_date = data.end_date.strftime('%Y/%m/%d %H:%M') if data.end_date else None

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


        return dict(success=True,data=data, datalogger_id = datalogger_id, start_hour = start_hour, end_hour=end_hour, freq_html = html,
                    start_date = start_date, end_date = end_date)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success=False, message=str(ex))
        ################################################################################
@service.json 
@auth.requires(lambda: (auth.has_permission('view', 'command_schedule')))
def get_command_by_id(*args, **kwargs):
    try:
        command = db.datalogger_command(request.vars.command_id) or None
        station_id = None
        datalogger_id = ''
        if command:
            station_id = command.station_id
            # station_name = command.station_name
            if station_id:
                station_name = db(db.stations.id == station_id).select(db.stations.station_name).first()['station_name']
                dataloggers = db(db.datalogger.station_id == station_id).select(db.datalogger.logger_id)
                if dataloggers:
                    datalogger_id = dataloggers.first()['logger_id']
            command = command.command_content
            # command = station_name + ":\n" + command
            # stations_html = "<option value=''>%s</option>" % T('-- Select an option --')
            # stations = db(db.stations.id > 0).select(db.stations.id, db.stations.station_name)
            # for item in stations:
            #     html = "<option value='%s'>%s</option>" % (item.id, item.station_name)
            #     if item.id == station_id:
            #         html = "<option value='%s'>%s</option> selected" % (item.id, item.station_name)
            #     stations_html = stations_html + ''.join(html)
        return dict(success = True, command = command, station_id=station_id, datalogger_id = datalogger_id)
        # return dict(success = True, command = command, station_id=station_id, datalogger_id = datalogger_id, stations_html = stations_html)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))

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

        if records:
            html1 = "<option value=''>%s</option>" % T('-- Select an option --')
            html = ["<option value='%s'>%s</option>" % (item[get_value_field], item[get_dsp_field]) for item in records]
            html = html1 + ''.join(html)
        else:
            html = "<option value=''>%s</option>" % T('-- No data --')

        return dict(success=True, html=html)
    except Exception as ex:
        return dict(success=False, message=str(ex))
