# -*- coding: utf-8 -*-

from gluon import current
import const


################################################################################
def get_lastest_files_dict():
    db = current.db
    
    rows = db(db.last_data_files.id > 0).select(
        db.last_data_files.filename,
        db.last_data_files.station_id,
    )
    res = {}
    for item in rows:
        res[str(item.station_id)] = item.filename

    return res
    
################################################################################
def get_usr_dict():
    db = current.db

    rows = db(db.auth_user.id > 0).select(db.auth_user.id, db.auth_user.fullname, db.auth_user.image)
    res_name = {}
    res_avatar = {}
    
    for item in rows:
        res_name[str(item.id)] = item.fullname
        res_avatar[str(item.id)] = item.image
    
    return res_name, res_avatar
    
################################################################################
def get_group_dict():
    db = current.db

    rows = db(db.auth_group.id > 0).select()
    res = {}
    for item in rows:
        res[str(item.id)] = item.role

    return res    
    
################################################################################
def get_province_dict():
    db = current.db
    
    provinces = db(db.provinces.id > 0).select()
    res = {}
    for item in provinces:
        res[str(item.id)] = item.province_name
        
    return res

################################################################################


def get_province_have_station(station_type=None):
    db = current.db
    ret = dict()
    conds = db.stations.id > 0
    if station_type is not None:
        conds &= db.stations.station_type == station_type
    stations = db(conds).select(db.stations.province_id)
    province_ids = [station.province_id for station in stations]
    
    provinces = db(db.provinces.id.belongs(province_ids)).select(db.provinces.ALL, distinct=True)
            
    for row in provinces:
        ret[str(row.id)] = row.as_dict()
    return ret
    
################################################################################
'''
Get station_indicator by station_id or station_type
Return dict with format: {indicator_id: row.as_dict()}
'''
def get_station_indicator_by_station(station_id='', station_type=''):
    db = current.db
    try:
        si_dict = dict()
        conditions = (db.station_indicator.id > 0)
        if station_type:
            db.station_indicator.station_type == station_type
        if station_id:
            db.station_indicator.station_id == station_id
        rows = db(conditions).select(db.station_indicator.ALL)
        for row in rows:
            si_dict[str(row.indicator_id)] = row.as_dict()
        return  si_dict
    except Exception as ex:
        return dict()

################################################################################
'''
Get station_indicator by station_id or station_type
Return dict with format: {indicator_id: row.as_dict()}
'''
def get_station_indicator_by_station_2(station_indicator_rows, station_id=''):
    db = current.db
    try:
        si_dict = dict()
        for row in station_indicator_rows:
            si_dict[str(row.indicator_id)] = row.as_dict()
        return  si_dict
    except Exception as ex:
        return dict()

################################################################################
'''
# Get indicator by station_id
station_indicators_rows: ROWS of station_indicator
indicators_rows: ROWS of indicators
Return ROWS of indicators
'''
def get_indicators_by_station_id(station_indicators_rows, indicators_rows, station_id=''):
    try:
        rows = []
        old_station_id = str(station_id)
        indicator_ids = []
        for si_row in station_indicators_rows:
            new_station_id = str(si_row.station_id)
            if new_station_id == old_station_id:
                indicator_id = str(si_row.indicator_id)
                indicator_ids.append(indicator_id)

        for i_row in indicators_rows:
            new_indicator_id = str(i_row.id)
            if new_indicator_id in indicator_ids:
                rows.append(i_row)
        return  rows
    except Exception as ex:
        return []


################################################################################
# Get all indicator for station
# Return ROWS indicators
def get_indicator_station_info():
    try:
        db = current.db
        # Get list indicator_id from mapping table
        conditions = (db.station_indicator.station_id > 0)
        # rows = db(conditions).select(db.station_indicator.indicator_id)
        rows = db(conditions).select(db.station_indicator.ALL)

        # Get list indicator_id used
        indicator_ids = []
        for row in rows:
            if row.indicator_id not in indicator_ids:
                indicator_ids.append(row.indicator_id)
            
        # Get indicator_dict {indicator_id : indicator_name}
        indicators = db(db.indicators.id.belongs(indicator_ids)).select(
            db.indicators.id,
            db.indicators.indicator
        )
        indicator_dict = {}
        for item in indicators:
            indicator_dict[str(item.id)] = item.indicator
            
        station_indicator_dict = {}
        for row in rows:
            if row.station_id not in station_indicator_dict:
                station_indicator_dict[row.station_id] = {}
            
            indicator = indicator_dict.get(row.indicator_id)
            station_indicator_dict[row.station_id][indicator] = {
                'id' : str(row.id),
                'equipment_id' : row.equipment_id,
                'equal0' : row.equal0,
                'negative_value' : row.negative_value,
                'out_of_range' : row.out_of_range,
                'out_of_range_min' : row.out_of_range_min,
                'out_of_range_max' : row.out_of_range_max,
                'continous_equal' : row.continous_equal,
                'continous_equal_value' : row.continous_equal_value,
                'continous_times' : row.continous_times,
                'mapping_name' : row.mapping_name,
                'convert_rate' : row.convert_rate,
            }
            
        exceed_dict = {}
        preparing_dict = {}
        tendency_dict = {}
        for item in rows:
            indicator = indicator_dict.get(item.indicator_id).upper()   # ten chi so
            
            if item.station_id in exceed_dict:
                exceed_dict[item.station_id][indicator] = item.exceed_value
                preparing_dict[item.station_id][indicator] = item.preparing_value
                tendency_dict[item.station_id][indicator] = item.tendency_value
            else:
                exceed_dict[item.station_id] = {indicator : item.exceed_value}
                preparing_dict[item.station_id] = {indicator : item.preparing_value}
                tendency_dict[item.station_id] = {indicator : item.tendency_value}
                
        return station_indicator_dict, indicators, exceed_dict, preparing_dict, tendency_dict
    except Exception as ex:
        return [], [], []
        
################################################################################
# Get all station_indicator
# Return ROWS station_indicator
# def get_station_indicator_value():
#     try:
#         db = current.db
#         # Get list indicator_id from mapping table
#         # conditions = (db.station_indicator.station_id > 0)
#         # conditions &= (db.station_indicator.indicator_id > 0)
#         conditions = (db.station_indicator.indicator_id > 0)
#         rows = db(conditions).select(db.station_indicator.ALL)
#         return rows
#     except Exception as ex:
#         return []

################################################################################
# Get color for indicator of Station
# si_dict: dict station_indicator {indicator_name: row.as_dict()}
# id: id of indicator
# value: value of indicator
def getColorByIndicator(si_dict, id, value):
    try:
        c = '#c9c9c9'
        if si_dict.has_key(id):
            data = si_dict[id]
            tendency = data['tendency_value']
            preparing = data['preparing_value']
            exceed = data['exceed_value']
            if value >= exceed:
                c = const.STATION_STATUS['EXCEED']['color']
            elif value >= preparing:
                c = const.STATION_STATUS['PREPARING']['color']
            elif value >= tendency:
                c = const.STATION_STATUS['TENDENCY']['color']
            else:
                c = const.STATION_STATUS['GOOD']['color']

        return c
    except Exception as ex:
        return '#c9c9c9'

################################################################################
# Get latest data for station
# Return json data
def get_data_lastest_by_station(station_id):
    try:
        db = current.db
        conditions = (db.data_lastest.station_id == station_id)
        if station_id == "":
            conditions = (db.data_lastest.station_id > 0)
        record = db(conditions).select(db.data_lastest.data).first()
        if record:
            return record.data
        return dict()
    except Exception as ex:
        return dict()

################################################################################
''' Get latest data for station
    Return json data, format {station_id :
                                {indicator : value, ...}
                             }
'''
def get_all_data_lastest():
    data_lastest_dict = {}
    try:
        db = current.db
        conditions = (db.data_lastest.station_id > 0)
        rows = db(conditions).select(db.data_lastest.station_id, db.data_lastest.data)
        
        for item in rows:
            data_dict = {}
            for indicator in item.data:
                data_dict[indicator] = item.data[indicator]
            data_lastest_dict[item.station_id] = data_dict
            
        return data_lastest_dict
    except Exception as ex:
        return data_lastest_dict

################################################################################
# Get latest data for station
# Return json data
def get_data_lastest_by_station_id(data_lastest_rows, station_id):
    try:
        for row in data_lastest_rows:
            if row.station_id == station_id:
                return row.data
        return dict()
    except Exception as ex:
        return dict()

################################################################################
# Get station info
# Return json data
def get_all_station_ftp_info():
    try:
        db = current.db
        field = [
            db.stations.id,
            db.stations.station_code,
            db.stations.data_server,
            db.stations.data_server_port,
            db.stations.data_folder,
            db.stations.username,
            db.stations.pwd,
            db.stations.file_mapping,
            db.stations.scan_failed,
            db.stations.retry,
        ]
        conditions = (db.stations.id > 0)
        conditions &= (db.stations.station_code != None)
        conditions &= (db.stations.data_server != None)
        conditions &= (db.stations.data_folder != None)
        rows = db(conditions).select(*field)
        
        res_ip = {}
        res_data_folder = {}
        res_username = {}
        res_pwd = {}
        res_port = {}
        res_file_mapping = {}
        res_scan_failed = {}
        res_retry = {}

        for item in rows:
            res_ip[item.station_code] = item.data_server
            res_data_folder[item.station_code] = item.data_folder
            res_username[item.station_code] = item.username
            res_pwd[item.station_code] = item.pwd
            res_port[item.station_code] = item.data_server_port
            res_scan_failed[item.station_code] = item.scan_failed
            res_retry[item.station_code] = item.retry
            if item.file_mapping:
                res_file_mapping[item.file_mapping] = str(item.id)
            
        return res_ip, res_data_folder, res_username, res_pwd, res_port, res_file_mapping, res_scan_failed, res_retry
    except Exception as ex:
        return dict()

################################################################################
def get_indicator_dict():
    db = current.db

    rows = db(db.indicators.id > 0).select()
    res = {}
    for item in rows:
        res[str(item.id)] = item.indicator

    return res

################################################################################
def get_station_dict():
    db = current.db
    field = [
        db.stations.id,
        db.stations.station_code,
        db.stations.station_name,
        db.stations.station_type,
        db.stations.status,
    ]
    
    stations = db(db.stations.id > 0).select(*field)
    res_name = {}
    res_type = {}
    res_status = {}
    res_code = {}
    
    for item in stations:
        res_name[str(item.id)] = item.station_name
        res_type[str(item.id)] = item.station_type
        res_status[str(item.id)] = item.status
        res_code[item.station_code] = str(item.id)

    return res_name, res_type, res_status, res_code

################################################################################
'''
    Description : Lay dict() cac tram voi nguong qua han cua tung chi so
    Return      : dict(station_id : dict(indicator : exceed value))
'''
# def get_station_indicator_thresdhold_dict(): 
    # db = current.db
    # logger = current.logger
    
    # fields = [  db.station_indicator.station_id,
                # db.station_indicator.indicator_id,
                # db.station_indicator.exceed_value]
                
    # rows = db(db.station_indicator.id > 0).select(*fields)
    
    
    # indicator_dict = get_indicator_dict()
    # res = {}
    # for item in rows:
        # indicator = indicator_dict.get(item.indicator_id).upper()   # ten chi so
        
        # if item.station_id in res:
            # res[item.station_id][indicator] = item.exceed_value
        # else:
            # res[item.station_id] = {indicator : item.exceed_value}

    # return res
    
################################################################################
def get_area_by_station_dict():
    '''
    Return : dict(key  : station_id, 
                  value: all areas which station belonged (separated by comma))
    '''
    db = current.db
    field = [
        db.areas.id,
        db.areas.area_name,
    ]
    
    records = db(db.areas.id > 0).select(*field)
    res_name = {}
    
    for item in records:
        if item.id not in res_name:
            res_name[str(item.id)] = item.area_name
        else:
            res_name[str(item.id)] = '%s, %s' % (res_name[str(item.id)], item.area_name)
        
    return res_name

################################################################################
def get_stations_belong_current_user():
    '''
    Return : list(station_ids)
    '''
    db = current.db
    session = current.session
    station_ids = db(db.station_role.role_id.belongs(session.user.role_ids)).select(db.station_role.station_id)
    station_ids = [item.station_id for item in station_ids]
    
    return station_ids
            
################################################################################    
def format_passed_time(seconds = 0):
    if not seconds: return ''
    
    T = current.T
    if seconds >= 86400:  # Ngay
        return '%d %s %d %s' % (seconds / 86400, T('day'), (seconds % 86400) / 3600, T('hour'))
    elif seconds >= 3600: # Gio
        return '%d %s %d %s' % (seconds / 3600, T('hour'), (seconds % 3600) / 60, T('minute'))
    elif seconds >= 60: # Phut
        return '%d %s %d %s' % (seconds / 60, T('minute'), seconds % 60, T('second'))
    else:
        return '%d %s' % (seconds, T('second'))

################################################################################
def send_mail(mail_to='', mail_cc='', subject='Subject', message='Content'):
    try:
        myconf = current.myconf
        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(message, 'html', 'UTF-8')
        msg['Subject'] = subject
        msg["From"] = myconf.get('smtp.sender')
        msg["To"] = mail_to
        msg["Cc"] = mail_cc

        server = smtplib.SMTP()
        mail_server = myconf.get('smtp.server')
        mail_port = myconf.get('smtp.port')
        server.connect(mail_server, mail_port)
        mail_user = myconf.get('smtp.login')
        mail_pwd = myconf.get('smtp.pwd')
        server.login(mail_user, mail_pwd)
        server.sendmail(msg["From"], msg["To"].split(','), msg.as_string())
        return True
    except Exception as ex:
        current.logger.error('Send email error')
        current.logger.error(str(ex))
        return False

################################################################################
def send_mail2(mail_to='', mail_cc='', subject='Subject', message='Content'):
    try:
        import smtplib #Sử dụng module smtp của Python
        from email.mime.text import MIMEText
        
        #Khai báo username và pass
        username = 'c0909i1240'
        password = 'chinguyen12345' 
        #Tạo đối tượng làm việc với smtp của gmail 
        server = smtplib.SMTP('smtp.gmail.com:587') # Tạo một kết nối đến SMTP của gmail
        server.starttls() #Khởi tạo kết nối TLS SMTP
        server.login(username, password) # Đăng nhập user, pass

        msg = MIMEText(message, 'html', 'UTF-8')
        msg['Subject'] = subject 
        msg["To"] = mail_to
        msg["Cc"] = mail_cc 
        server.sendmail(msg["From"], msg["To"].split(','), msg.as_string()) # Gửi email từ hocbaomat@gmail.com đến maivanthang@gmail.com
         
        server.close() # Kết thúc
    except Exception as ex:
        current.logger.error('Send email error')
        current.logger.error(str(ex))
        return False
################################################################################
def convert_to_unsigned(text):
    import re
    import sys
    patterns = {
        '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
        '[đ]': 'd',
        '[èéẻẽẹêềếểễệ]': 'e',
        '[ìíỉĩị]': 'i',
        '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        '[ùúủũụưừứửữự]': 'u',
        '[ỳýỷỹỵ]': 'y'
    }
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

################################################################################
def display_list_integer(resource, numbers):
    try:
        ret = ''
        for number in numbers:
            name = resource.get(str(number))
            if name:
                if ret: ret += ', '
                ret += name
        return  ret
    except Exception as ex:
        return  numbers

################################################################################
def get_info_from_const(data, value):
    try:
        ret = []
        for key, item in data.iteritems():
            if item['value'] == value:
                return item
        return  ret
    except Exception as ex:
        return []

################################################################################
# Format of item in dict: 'KEY1': {'value': 0, 'name': 'name1', 'seq': 1}
def sort_dict_const_by_value(dict_const):
    key_field = 'value'
    ret = dict_const.items()
    total = len(ret)
    if total > 0:
        item = ret[0][1]
        if item.has_key('seq'):
            key_field = 'seq'
    for i in range(0, total - 1):
        for j in range(i + 1, total):
            if ret[j][1][key_field] < ret[i][1][key_field]:
                temp = ret[j]
                ret[j] = ret[i]
                ret[i] = temp
    return  ret

################################################################################
def get_const_by_value(dict_const, value):
    ret = []
    for k in dict_const:
        if str(dict_const[k]['value']) == str(value):
            return  dict_const[k]
    return  ret