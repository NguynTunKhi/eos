# -*- coding: utf-8 -*-
import datetime

###############################################################################
def get_token_with():
    row = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
    if not row:
        return None
    iplocal = row['iplocal']
    last_time_access = row['last_time_access']
    last_time_refresh = row['last_time_refresh']
    access_token_expires = row['access_token_expires']
    refresh_token_expires = row['refresh_token_expires']
    access_token = row['access_token']
    refresh_token = row['refresh_token']
    username = row['username']

    if last_time_access and last_time_refresh:
        now = datetime.utcnow()
        if last_time_access + timedelta(seconds=access_token_expires - (60 * 60)) > now:
            return access_token
        else:
            if last_time_refresh + timedelta(seconds=refresh_token_expires - (60 * 15)) > now:
                req = requests.get('{}/zm/api/host/login.json?token={}'.format(iplocal, refresh_token), verify=False, timeout=5)
                content = req.content
                dic = ast.literal_eval(content)
                db(db.camera_tokens.username == username).update(
                    last_time_access=now,
                    access_token_expires=dic['access_token_expires'],
                    access_token=dic['access_token']
                )
                return dic['access_token']
    try:
        username = row['username']
        password = row['password']
        req = requests.get('{}/zm/api/host/login.json?user={}&pass={}'.format(iplocal, username, password),
                           verify=False)
        content = req.content
        dic = ast.literal_eval(content)
        if not dic['access_token']:
            return None
        now = datetime.utcnow()
        db(db.camera_tokens.username == username).update(
            last_time_access=now,
            last_time_refresh=now,
            access_token_expires=dic['access_token_expires'],
            refresh_token_expires=dic['refresh_token_expires'],
            access_token=dic['access_token'],
            refresh_token=dic['refresh_token']
        )
        return dic['access_token']
    except Exception as ex:
        return dict(message=str(ex), success=False)
   
################################################################################
def get_function_code_by_table(table):
    func_code = {
        'station_role': 'master_station',
        'alarm_levels': 'master_station',
        'station_types': 'master_station',
        'stations': 'master_station',
        'camera_links': 'master_station',
        'station_indicator': 'master_station',
        'station_alarm': 'master_station',
        'station_off_log': 'master_station',
        'provinces': 'master_province',
        'areas': 'master_area',
        'area_station': 'master_area',
        'indicators': 'master_indicator',
        'aqi_indicators': 'master_indicator',
        'equipments': 'master_equipment',
        'qcvn': 'master_qcvn',
        'qcvn_detail': 'master_qcvn',
        'agents': 'master_agent',
        'agent_details': 'master_agent',
        'agent_station': 'master_agent',
        'adjustments': 'data_adjust',
        'aqi_data_hour': 'data',
        'aqi_data_24h': 'data',
        'wqi_data_hour': 'data',
        'wqi_data_24h': 'data',
        'last_data_files': 'data',
        'data_lastest': 'data',
        'data_approve': 'data',
        'data_min': 'data',
        'data_hour': 'data',
        'data_day': 'data',
        'data_mon': 'data',
        'ftp_send_receive': 'ftp_transfer',
    }
    if func_code.has_key(table):
        return  func_code[table]
    return  table


################################################################################
@service.json
def del_records(table, *args, **kwargs):
    try:
        id = request.vars.id            # for single record
        array_data = request.vars.ids   # for list record (dc truyen qua app.executeFunction())
        func_code = get_function_code_by_table(table)
        if not auth.has_permission('delete', func_code):
            return dict(success=False, message=T('Access denied!'))
        
        list_ids = []
        if array_data:  list_ids = array_data.split(',')
        list_ids.append(id) if id else list_ids
        
        if list_ids:
            if table == 'camera_links':
                for i in list_ids:
                    row = db(db.camera_tokens.id > 0).select(db.camera_tokens.ALL).first()
                    data = db(db.camera_links.id == i).select(db.camera_links.camera_id)
                    access_token = None
                    if not access_token:
                        access_token = get_token_with()
                    payload = {'token': access_token}
                    url_del = "{host}/zm/api/monitors/{camera_id}.json".format(host=row['iplocal'],
                                                                               camera_id=data[0].camera_id)
                    api_del_camera = requests.delete(url_del, data=payload, verify=False)
                    db(db[table].id.belongs(list_ids)).delete()
            else:
                db(db[table].id.belongs(list_ids)).delete()
        return dict(success = True)
    except Exception as ex:
        return dict(success = False, message = str(ex))

################################################################################
'''
    Return content of dropdown box (html)
'''
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
        records = db(conditions).select(db[table][get_value_field], db[table][get_dsp_field])
        
        if records:
            html1 = "<option value=''>%s</option>" % T('-- Select an option --')
            html = ["<option value='%s'>%s</option>" % (item[get_value_field], item[get_dsp_field]) for item in records]
            html = html1 + ''.join(html)
        else:
            html = "<option value=''>%s</option>" % T('-- No data --')

        return dict(success = True, html = html)
    except Exception as ex:
        return dict(success = False, message = str(ex))

# -------------------------------------------------------------------------
def CUSTOM_SQLFORM(table, record, **attributes):
    frm = SQLFORM(table, record, **attributes)
    for item in frm.custom.widget:
        try:
            if table[item].type in ('string', 'text'):
                maxlength = table[item].length
                if maxlength:
                    frm.custom.widget[item]['_maxlength'] = maxlength
        except Exception as ex:
            pass
    return frm

# -------------------------------------------------------------------------
def format_date(date_str):
    # return date_str.replace('-', '').replace('/', '').replace(' ', '')
    fmt_date = date_str.replace('-', '').replace('/', '').replace(' ', '')
    return '%s%s%s' % (fmt_date[4:8], fmt_date[2:4], fmt_date[:2])
    

# -------------------------------------------------------------------------
def format_date_for_display(date_str, separator = '/'):
    if not date_str or date_str.strip() == '':
        return date_str
        
    return '%s%s%s%s%s' % (date_str[6:], separator, date_str[4:6], separator, date_str[:4])
    
# -------------------------------------------------------------------------
def decode_str(s):
    if not s:
        return ''
    ret = None
    try:
        ret = s.decode('utf8')
    except UnicodeDecodeError:
        try:
            ret = s.decode('latin1')
        except:
            return s
    return ret

# -------------------------------------------------------------------------
def get_station_status():
    ret = dict()
    for idx, value in enumerate(station_status_value):
        ret[str(value)] = {'value': value, 'name': str(station_status_disp[idx]), 'color': station_status_color[idx]}
    return  ret

# -------------------------------------------------------------------------
def get_all_records(table):
    ret = dict()
    rows = db(db[table].id > 0).select(db[table].ALL)
    for row in rows:
        ret[str(row.id)] = row.as_dict()
    return  ret
    

def get_all_records_for_area(table):
    ret = dict()
    conds = db.stations.id >0
    areas_ids = []
    session = current.session
    if session:
        if not 'admin' in session.auth.user_groups.values():
            list_station_manager = db(db.manager_stations.user_id == session.auth.user.user_id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conds &= (db.stations.id.belongs(station_ids))
            row = db(db.stations.id.belongs(station_ids)).select(db.stations.area_id, distinct=True)
            areas_ids = [str(it.area_id) for it in row]
    rows = db(db[table].id.belongs(areas_ids)).select(db[table].ALL)
    for row in rows:
        ret[str(row.id)] = row.as_dict()
    return  ret