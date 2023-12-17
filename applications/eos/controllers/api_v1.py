# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
from datetime import datetime, timedelta 
from applications.eos.modules import const
from gluon.tools import prettydate
import json
from gluon.tools import AuthJWT
import datetime

myjwt = AuthJWT(auth, secret_key='secret@259', expiration=60*60*24*365)

#auth.settings.allow_basic_login = True
#@auth.requires_login()
auth.settings.allow_basic_login = True

def call():
    session.forget()
    response.headers["Access-Control-Allow-Origin"] = '*'
    return service()

################################################################################

@service.json
def test_01(*args, **kwargs):
    return dict(success=True, k=True)

@service.json
def getAppSetting(*args, **kwargs):
    settings = db().select(db.app_settings.ALL).first()
    return dict(success=True, data=settings)

# @service.json
# @auth.requires_login()
# def login(*args, **kwargs):
#     #return dict(success=True, token=myjwt.jwt_token_manager().token)
#     #return {'success': True}
#     token = myjwt.jwt_token_manager()
#     json_object = json.loads(token)
#     return dict(success=True, token=json_object['token'])

@service.json
def login(*args, **kwargs):
    #return dict(success=True, token=myjwt.jwt_token_manager().token)
    #return {'success': True}
    token = myjwt.jwt_token_manager()
    json_object = json.loads(token)
    return dict(success=True, token=json_object['token'])

@service.json
@myjwt.allows_jwt()
def getUserInfo():
    user = db.auth_user(auth.user_id)
    return dict(success=True, data=user)

@service.json
@myjwt.allows_jwt()
def changePassword(*args, **kwargs):
    user = db.auth_user(auth.user_id)
    result = False
    tokenValue = ''
    print request.post_vars
    if CRYPT(digest_alg = 'sha512', salt = True)(request.vars.old_password)[0] == user.password:
        user.password =  CRYPT(digest_alg = 'sha512', salt = True)(request.vars.password)[0]
    #    # db.usr[user.id] = dict(password = user.password)
        db.auth_user[user.id] = dict(password = user.password)
        request.vars.username = user.username
        request.vars.password = request.vars.password
        token = myjwt.jwt_token_manager()
        json_object = json.loads(token)
        tokenValue = json_object['token']
        result = True
    return dict(success=result, token=tokenValue)

@service.json
def get_common_settings(*args, **kwargs):
    try:
        # aqi_colors
        aqi_colors = []
        for k in sorted(const.AQI_COLOR):
            name = ''
            if const.AQI_COLOR[k]['to']:
                name = '%s - %s (%s)' %(const.AQI_COLOR[k]['from'], const.AQI_COLOR[k]['to'], T(const.AQI_COLOR[k]['text']))
            else:
                name = '%s %s (%s)' %(T('Greater'), const.AQI_COLOR[k]['from'] - 1, T(const.AQI_COLOR[k]['text']))

            aqi_colors.append({
                'name': name,
                'from': const.AQI_COLOR[k]['from'],
                'to': const.AQI_COLOR[k]['to'] if const.AQI_COLOR[k]['to'] != None else 600,
                'color': const.AQI_COLOR[k]['bgColor'],
            })
            pass

        # wqi_colors
        wqi_colors = []
        for k in sorted(const.WQI_COLOR):
            name = ''
            if const.WQI_COLOR[k]['to']:
                name = '%s - %s (%s)' %(const.WQI_COLOR[k]['from'], const.WQI_COLOR[k]['to'], T(const.WQI_COLOR[k]['text']))
            else:
                name = '%s %s (%s)' %(T('Greater'), const.WQI_COLOR[k]['from'] - 1, T(const.WQI_COLOR[k]['text']))

            wqi_colors.append({
                'name': name,
                'from': const.WQI_COLOR[k]['from'],
                'to': const.WQI_COLOR[k]['to'] if const.WQI_COLOR[k]['to'] != None else 600,
                'color': const.WQI_COLOR[k]['bgColor'],
            })
            pass

        # status
        status = []
        status_good = ''
        for k in const.STATION_STATUS:
            if k in ['GOOD', 'TENDENCY', 'PREPARING']:
                if status_good:
                    status_good += ','
                status_good += str(const.STATION_STATUS[k]['value'])
                continue
            status.append({
                'value': const.STATION_STATUS[k]['value'],
                'name': T(const.STATION_STATUS[k]['name'])
            })
            pass
        status.append({
            'value': status_good,
            'name': T(const.STATION_STATUS['GOOD']['name'])
        })

        # STATION_TYPE
        station_type = []
        for k in const.STATION_TYPE:
            station_type.append({
                'value': const.STATION_TYPE[k]['value'],
                'name': T(const.STATION_TYPE[k]['name'])
            })
            pass

        # provinces
        provinces = []
        conditions = (db.provinces.id > 0)
        rows = db(conditions).select(db.provinces.id,
                                     db.provinces.province_name,
                                     orderby=db.provinces.province_name)
        for row in rows:
            provinces.append({
                'id': str(row.id),
                'name': row.province_name,
            })

        # areas
        areas = []
        conditions = (db.areas.id > 0)
        rows = db(conditions).select(db.areas.id,
                                     db.areas.area_code,
                                     db.areas.area_name,
                                     orderby=db.areas.area_name)
        for row in rows:
            areas.append({
                'id': str(row.id),
                'area_code': row.area_code,
                'area_name': row.area_name,
            })

        return dict(success=True, qi_colors = aqi_colors, aqi_colors = aqi_colors, wqi_colors = wqi_colors, status=status,
                    provinces=provinces, station_type=station_type, areas=areas)
    except Exception as ex:
        return dict(success=False, message=str(ex))

###############################################################################
@service.json
def get_stations_by_province(*args, **kwargs):
    try:
        data = dict()
        data['categories'] = []
        data['series'] = [{
            'name': T('Station'),
            'type': 'column',
            'color': '#1ab394',
            'data': [],
        }, {
            'name': T('Good'),
            'type': 'areaspline',
            'marker': {'enabled': False},
            'data': [],
            'fillOpacity': 0.3,
        }
            , {
            'name': T('Exceed'),
            'type': 'areaspline',
            'color': 'red',
            'data': [],
            'marker': {'enabled': False},
            }
        ]
        data['title'] = T('Stations distributed by Province')
        data['subtitle'] = ''
        rows = db(db.provinces.id > 0).select(db.provinces.id, db.provinces.province_name, orderby = db.provinces.order_no)
        provinces = dict()
        for row in rows:
            provinces[str(row.id)] = row.province_name

        conditions = (db.stations.id > 0)
        conditions &= (db.stations.province_id != None)
        rows = db(conditions).select(db.stations.province_id, db.stations.status, limitby=(0,100))
        categories = dict()
        if not rows:
            data['subtitle'] = T('No data found!')
        for row in rows:
            province_id = str(row.province_id)
            if not categories.has_key(province_id):
                categories[province_id] = {
                    'name': provinces[province_id],
                    'qty': 0,
                    'qty_good': 0,
                    'qty_exceed': 0,
                }
            categories[province_id]['qty'] += 1
            if row.status == const.STATION_STATUS['EXCEED']['value']:
                categories[province_id]['qty_exceed'] += 1
                pass
            elif row.status == const.STATION_STATUS['GOOD']['value'] or\
                    row.status == const.STATION_STATUS['TENDENCY']['value'] or\
                    row.status == const.STATION_STATUS['PREPARING']['value']:
                categories[province_id]['qty_good'] += 1

        for item in categories:
            data['categories'].append(categories[item]['name'])
            data['series'][0]['data'].append(categories[item]['qty'])
            data['series'][1]['data'].append(categories[item]['qty_good'])
            data['series'][2]['data'].append(categories[item]['qty_exceed'])

        return dict(success=True, data=data)
    except Exception as ex:
        return dict(success=False, data=data)

###############################################################################
@service.json
def get_stations_by_area(*args, **kwargs):
    try:
        data = dict()
        data['categories'] = []
        data['series'] = [{
            'name': T('Station'),
            'type': 'column',
            'color': '#1ab394',
            'data': [],
        }, {
            'name': T('Good'),
            'type': 'areaspline',
            'marker': {'enabled': False},
            'data': [],
            'fillOpacity': 0.3,
        }
        ]
        data['title'] = T('Stations distributed by Area')
        data['subtitle'] = ''
        rows = db(db.areas.id > 0).select(db.areas.id, db.areas.area_name, orderby = db.areas.order_no)
        areas = dict()
        for row in rows:
            areas[str(row.id)] = row.area_name
        conditions = (db.stations.id > 0)
        conditions &= (db.stations.area_id != None)
        rows = db(conditions).select(db.stations.area_id, db.stations.status, limitby=(0, 100))
        categories = dict()
        if not rows:
            data['subtitle'] = T('No data found!')
        for row in rows:
            area_id = str(row.area_id)
            if not categories.has_key(area_id):
                categories[area_id] = {
                    'name': areas[area_id],
                    'qty': 0,
                    'qty_good': 0,
                    # 'qty_exceed': 0,
                }
            categories[area_id]['qty'] += 1
            if row.status == const.STATION_STATUS['EXCEED']['value']:
                # categories[area_id]['qty_exceed'] += 1
                pass
            elif row.status == const.STATION_STATUS['GOOD']['value'] or\
                    row.status == const.STATION_STATUS['TENDENCY']['value'] or\
                    row.status == const.STATION_STATUS['PREPARING']['value']:
                categories[area_id]['qty_good'] += 1

        for item in categories:
            data['categories'].append(categories[item]['name'])
            data['series'][0]['data'].append(categories[item]['qty'])
            data['series'][1]['data'].append(categories[item]['qty_good'])
            # data['series'][2]['data'].append(categories[item]['qty_exceed'])

        return dict(success=True, data=data)
    except Exception as ex:
        return dict(success=True, data=data)


################################################################################
@service.json
@myjwt.allows_jwt()
def get_stations(*args, **kwargs):
    try:
        is_qi = request.vars.is_qi
        is_public = request.vars.is_public
        station_type = request.vars.station_type
        qi_type = request.vars.qi_type
        status = request.vars.status
        station_name = request.vars.station_name
        province_id = request.vars.province_id

        stations = []
        conditions = (db.stations.id > 0)
        if province_id:
            conditions &= (db.stations.province_id == province_id)
        if is_qi:
            conditions &= (db.stations.is_qi == is_qi)
        if is_public:
            conditions &= (db.stations.is_public == is_public)
        if station_type:
            conditions &= (db.stations.station_type == station_type)
        if status:
            status = status.split(',')
            conditions &= (db.stations.status.belongs(status))
        if station_name:
            conditions &= (db.stations.station_name.contains(station_name))
        if qi_type:
            qi_type = qi_type.lower()
            if qi_type == 'aqi':
                conditions &= (db.stations.station_type.belongs([const.STATION_TYPE['STACK_EMISSION']['value'], const.STATION_TYPE['AMBIENT_AIR']['value']]))
            elif qi_type == 'wqi':
                conditions &= (db.stations.station_type.belongs([const.STATION_TYPE['WASTE_WATER']['value'], const.STATION_TYPE['SURFACE_WATER']['value'], const.STATION_TYPE['UNDERGROUND_WATER']['value']]))
        rows = db(conditions).select(db.stations.ALL,
                                     orderby=db.stations.station_name)
        dt_format = '%Y-%m-%d %H:%M:%S'
        dt_format2 = '%H:%M %d/%m'
        for row in rows:
            color = '#333333'
            status = ''
            icon = ''
            show_off_time = False
            if row.status in [const.STATION_STATUS['OFFLINE']['value'], const.STATION_STATUS['ADJUSTING']['value'], const.STATION_STATUS['ERROR']['value']]:
                if row.off_time:
                    show_off_time = True
            for k in const.STATION_STATUS:
                if const.STATION_STATUS[k]['value'] == row.status:
                    color = const.STATION_STATUS[k]['color']
                    status = T(const.STATION_STATUS[k]['name'])
                    icon = T(const.STATION_STATUS[k]['icon'])
            qi_detail_info = {}
            if row.station_type in [const.STATION_TYPE['WASTE_WATER']['value'],
                                        const.STATION_TYPE['SURFACE_WATER']['value'],
                                        const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
                colors = const.WQI_COLOR
            else:
                colors = const.AQI_COLOR
            for key in sorted(colors):
                if row.qi <= key:
                    qi_detail_info = colors[key]
                    break
            if qi_detail_info.has_key('description'):
                qi_detail_info['description'] = str(T(qi_detail_info['description']))
            if qi_detail_info.has_key('text'):
                qi_detail_info['text'] = str(T(qi_detail_info['text']))

            stations.append({
                'id': str(row.id),
                'station_name': row.station_name,
                'station_code': row.station_code,
                'station_type': row.station_type,
                'qi_detail_info': qi_detail_info,
                'longitude': row.longitude,
                'latitude': row.latitude,
                'qi': row.qi if row.qi else 0,
                'qi_time': row.qi_time.strftime(dt_format) if row.qi_time else '',
                'qi_time2': row.qi_time.strftime(dt_format2) if row.qi_time else '',
                'qi_time3': prettydate(row.qi_time, T) if row.qi_time else '',
                'off_time': row.off_time.strftime(dt_format) if show_off_time else '',
                'off_time2': row.off_time.strftime(dt_format2) if show_off_time else '',
                'off_time3': prettydate(row.off_time, T) if show_off_time else '',
                'status': status,
                'color': color,
                'icon': icon,
                'province_id': row.province_id,
                'area_id': row.area_id,
                'address': row.address,
            })
        return dict(success=True, total= len(stations), stations = stations)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################

@service.json
@myjwt.allows_jwt()
def get_station_type():
    area_id = request.vars.area_id
    province_id = request.vars.province_id

    # Select stations to fill in dropdown box
    fields = [
        db.stations.id,
        db.stations.station_name,
        db.stations.station_type,
        db.stations.status,
    ]

    conditions = (db.stations.id > 0)
    if area_id:
        conditions &= (db.stations.area_id == area_id)
    if province_id:
        conditions &= (db.stations.province_id == province_id)
    # stations = db(conditions).select(db.stations.id, db.stations.status, db.stations.station_type)
    stations = db(conditions).select(*fields)

    # Get qty online/total for each station
    
    station_type_online = dict()
    for st in const.STATION_TYPE:
        if not station_type_online.has_key(st):
            station_type_online[st] = dict()
            station_type_online[st]['value'] = const.STATION_TYPE[st]['value']
            station_type_online[st]['name'] = const.STATION_TYPE[st]['name']
            station_type_online[st]['name_vn'] = T(const.STATION_TYPE[st]['name'])
            station_type_online[st]['image'] = const.STATION_TYPE[st]['image']
            station_type_online[st]['online'] = 0
            station_type_online[st]['total'] = 0
            station_type_online[st]['offline'] = 0
            station_type_online[st]['adjust'] = 0
            station_type_online[st]['error'] = 0

    total_online, total_adjust, total_offline, total_error = 0, 0, 0, 0

    for station in stations:
        for st in station_type_online:
            if station.station_type == station_type_online[st]['value']:
                if station.status == const.STATION_STATUS['ADJUSTING']['value']:
                    station_type_online[st]['adjust'] += 1
                    total_adjust += 1
                elif station.status == const.STATION_STATUS['OFFLINE']['value']:
                    station_type_online[st]['offline'] += 1
                    total_offline += 1
                elif station.status == const.STATION_STATUS['ERROR']['value']:
                    station_type_online[st]['error'] += 1
                    total_error += 1
                else:
                    station_type_online[st]['online'] += 1
                    total_online += 1

                station_type_online[st]['total'] += 1
                break
    station_type = []
    for st in station_type_online:
        station_type.append(station_type_online[st])
    time_count = datetime.datetime.now()
    return dict(time_count=time_count, station_type=station_type, total_error = total_error,
                total_station=len(stations), total_online=total_online, total_offline=total_offline, total_adjust=total_adjust)

################################################################################
@service.json
@myjwt.allows_jwt()
def get_qi_detail(*args, **kwargs):
    try:
        station_id = request.vars.station_id

        station = db.stations(station_id) or None
        qi_detail_info = {}
        qi_value = ''
        station_name = ''
        qi_time_1, qi_time_2 = '', ''

        if not station:
            return dict(success=False, message=T('Not found!'))

        qi_value = int(round(station.qi)) if station.qi else '-'
        station_name = station.station_name
        address = station.address
        qi_time_1 = prettydate(station.qi_time, T) if station.qi_time else '-'
        # qi_time_2 = stations.qi_time.strftime('%d/%m/%Y %H:%S') if stations.qi_time else '-'
        qi_time_2 = station.qi_time.strftime(datetime_format_vn) if station.qi_time else '-'
        if station.station_type in [const.STATION_TYPE['WASTE_WATER']['value'], const.STATION_TYPE['SURFACE_WATER']['value'], const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
            colors = const.WQI_COLOR
        else:
            colors = const.AQI_COLOR
        for key in sorted(colors):
            if station.qi <= key:
                qi_detail_info = colors[key]
                break

        ### Lay phan du lieu chi so AQI detail
        conditions = (db.aqi_data_hour.station_id == station_id)
        aqis = db(conditions).select(
            db.aqi_data_hour.get_time,
            db.aqi_data_hour.data,
            orderby = ~db.aqi_data_hour.get_time,
            limitby = (0, 48)
        )

        res = {}
        for item in aqis:
            data = item.data
            for indicator in data:
                if indicator == 'aqi' : continue
                if not res.has_key(indicator):
                    res[indicator] = {
                        'values': [],
                        'min': data[indicator],
                        'max': data[indicator],
                    }
                # O day mang 'values' dang duoc luu gtri theo tgian tu gan --> xa
                # nen tren html se phai dao nguoc lai (reversed)
                res[indicator]['values'].append(str(int(round(data[indicator]))))
                if res[indicator]['min'] > data[indicator]:
                    res[indicator]['min'] = data[indicator]
                if res[indicator]['max'] < data[indicator]:
                    res[indicator]['max'] = data[indicator]
        resArray =[]
        for item in res:
            res[item]['indicator'] = item
            resArray.append(res[item])
        # Lay bang dinh nghia Color cho AQI, de buil colorMap cho client co format:
        # '0 : 50' : 'color1', '51 : 100' : 'color2', ....
        keys = sorted(colors)                     # keys    = [50, 100, 150, 200, 300, 999]
        shift_keys = [-1] + keys[:len(keys)-1] # shift_keys = [-1, 50, 100, 150, 200, 300]
        # color_map = ''
        color_map = {}
        for i, key in enumerate(keys):
            # color_map += "'%s : %s' : '%s', " % (shift_keys[i] + 1, keys[i], colors[key]['bgColor'])
            color_map['%s : %s' % (shift_keys[i] + 1, keys[i])] = '%s' %(colors[key]['bgColor'])
        # color_map = json.dumps(color_map)
        if qi_detail_info.has_key('description'):
            qi_detail_info['description'] = str(T(qi_detail_info['description']))
        if qi_value == '-':
            qi_detail_info = {}
        return dict(success=True, qi_value = qi_value, station_name = station_name, res = resArray, color_map = color_map,
                    qi_time_1 = qi_time_1, qi_time_2 = qi_time_2, qi_detail_info = qi_detail_info, address = address)
    except Exception as ex:
        return dict(success=False, message=str(ex))

################################################################################
@service.json
@myjwt.allows_jwt()
def get_qi_detail_with_day_hour(*args, **kwargs):
    try:
        station_id = request.vars.station_id

        station = db.stations(station_id) or None
        qi_detail_info = {}
        qi_value = ''
        station_name = ''
        qi_time_1, qi_time_2 = '', ''

        if not station:
            return dict(success=False, message=T('Not found!'))

        qi_value = int(round(station.qi)) if station.qi else '-'
        station_name = station.station_name
        address = station.address
        qi_time_1 = prettydate(station.qi_time, T) if station.qi_time else '-'
        # qi_time_2 = stations.qi_time.strftime('%d/%m/%Y %H:%S') if stations.qi_time else '-'
        qi_time_2 = station.qi_time.strftime(datetime_format_vn) if station.qi_time else '-'
        if station.station_type in [const.STATION_TYPE['WASTE_WATER']['value'], const.STATION_TYPE['SURFACE_WATER']['value'], const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
            colors = const.WQI_COLOR
        else:
            colors = const.AQI_COLOR
        for key in sorted(colors):
            if station.qi <= key:
                qi_detail_info = colors[key]
                break

        ### Lay phan du lieu chi so AQI detail
        conditions = (db.aqi_data_hour.station_id == station_id)
        aqis = db(conditions).select(
            db.aqi_data_hour.get_time,
            db.aqi_data_hour.data,
            orderby = ~db.aqi_data_hour.get_time,
            limitby = (0, 48)
        )

        res = {}
        for item in aqis:
            data = item.data
            for indicator in data:
                if indicator == 'aqi' : continue
                if not res.has_key(indicator):
                    res[indicator] = {
                        'values_hour': [],
                        'min_hour': data[indicator],
                        'max_hour': data[indicator],
                    }
                # O day mang 'values' dang duoc luu gtri theo tgian tu gan --> xa
                # nen tren html se phai dao nguoc lai (reversed)
                res[indicator]['values_hour'].append(str(int(round(data[indicator]))))
                if res[indicator]['min_hour'] > data[indicator]:
                    res[indicator]['min_hour'] = data[indicator]
                if res[indicator]['max_hour'] < data[indicator]:
                    res[indicator]['max_hour'] = data[indicator]
        resArray =[]
        for item in res:
            res[item]['indicator'] = item
            resArray.append(res[item])

        # Lay chi so theo ngay
        ### Lay phan du lieu chi so AQI detail
        conditions = (db.aqi_data_24h.station_id == station_id)
        aqis = db(conditions).select(
            db.aqi_data_24h.get_time,
            db.aqi_data_24h.data_1d,
            orderby=~db.aqi_data_24h.get_time,
            limitby=(0, 48)
        )

        res = {}
        for item in aqis:
            data = item.data_1d
            for indicator in data:
                if indicator == 'aqi': continue
                if not res.has_key(indicator):
                    res[indicator] = {
                        'values_day': [],
                        'min_day': data[indicator],
                        'max_day': data[indicator],
                    }
                # O day mang 'values' dang duoc luu gtri theo tgian tu gan --> xa
                # nen tren html se phai dao nguoc lai (reversed)
                res[indicator]['values_day'].append(str(int(round(data[indicator]))))
                if res[indicator]['min_day'] > data[indicator]:
                    res[indicator]['min_day'] = data[indicator]
                if res[indicator]['max_day'] < data[indicator]:
                    res[indicator]['max_day'] = data[indicator]
        resDayArray = []
        for item in res:
            res[item]['indicator'] = item
            resDayArray.append(res[item])

        # Lay bang dinh nghia Color cho AQI, de buil colorMap cho client co format:
        # '0 : 50' : 'color1', '51 : 100' : 'color2', ....
        keys = sorted(colors)                     # keys    = [50, 100, 150, 200, 300, 999]
        shift_keys = [-1] + keys[:len(keys)-1] # shift_keys = [-1, 50, 100, 150, 200, 300]
        # color_map = ''
        color_map = {}
        for i, key in enumerate(keys):
            # color_map += "'%s : %s' : '%s', " % (shift_keys[i] + 1, keys[i], colors[key]['bgColor'])
            color_map['%s : %s' % (shift_keys[i] + 1, keys[i])] = '%s' %(colors[key]['bgColor'])
        # color_map = json.dumps(color_map)
        if qi_detail_info.has_key('description'):
            qi_detail_info['description'] = str(T(qi_detail_info['description']))
        if qi_value == '-':
            qi_detail_info = {}
        return dict(success=True, qi_value = qi_value, station_name = station_name, res_hour = resArray, res_day = resDayArray, color_map = color_map,
                    qi_time_1 = qi_time_1, qi_time_2 = qi_time_2, qi_detail_info = qi_detail_info, address = address)
    except Exception as ex:
        return dict(success=False, message=str(ex))

################################################################################
@service.json
@myjwt.allows_jwt()
def get_details_station(*args, **kwargs):
    try:
        station_id = request.vars.station_id

        station = db.stations(station_id) or None
        province = db.provinces(station.province_id) or None

        station.province_name = province.province_name

        status = ''
        for k in const.STATION_STATUS:
            if const.STATION_STATUS[k]['value'] == station.status:
                status = T(const.STATION_STATUS[k]['name'])
        station.status = str(status)
        station.id = str(station.id)            
        conditions = (db.station_indicator.id > 0)
        if station_id:
            conditions &= (db.station_indicator.station_id == station_id)
        list_data = db(conditions).select(  db.station_indicator.ALL)
        if station_id:
            conditions = (db.data_lastest.station_id == station_id)
        data_lastest = db(conditions).select(db.data_lastest.data, db.data_lastest.get_time,
                                         limitby=(0, 1),
                                         orderby=~db.data_lastest.get_time).first() or None
        si_dict = common.get_station_indicator_by_station_2(list_data, station_id)
        for i in range(len(list_data)):
            indicator = db.indicators(list_data[i].indicator_id) or None
            list_data[i].indicator = indicator.indicator
            if data_lastest:
                if data_lastest.data[indicator.indicator]:
                    try:
                        list_data[i].value = float(data_lastest.data[indicator.indicator])
                    except:
                        list_data[i].value = '-'
                    list_data[i].color = common.getColorByIndicator(si_dict, indicator.indicator, list_data[i].value)
        return dict(success=True, station=station, station_indicator=list_data)
    except Exception as ex:
        return dict(success=False, message=str(ex))

################################################################################
@service.soap('getAqiWqi',
            returns = [{'station_name': str,#Trạm
                   'qi_time': str, #Thời gian
                   'qi': str, #Giá trị
                   'status': str, #Trạng thái 
                   }],
            args = {'province_id': str, #Mã tỉnh(option)
                   'area_id': str # Mã vùng(option)
                    }) 
def get_aqi_wqi(province_id, area_id):
    try:  
        conditions = (db.stations.is_qi == True)
        # Todo : lay 30 tram co chi so QI cao nhat --> xem ve sau cho ra Setting
        conditions &= (db.stations.station_type.belongs([const.STATION_TYPE['STACK_EMISSION']['value'],
                                                         const.STATION_TYPE['AMBIENT_AIR']['value']]))
        if area_id:
            conditions &= (db.stations.area_id == area_id)
        if province_id:
            conditions &= (db.stations.province_id == province_id)

        fields = ['id', 'station_name', 'qi', 'qi_time', 'status']
        fields = [db.stations[field] for field in fields]

        rows = db(conditions).select(*fields, orderby=~db.stations.qi, limitby=(0, 30))
        aaData = []
        for row in rows:
            status_icon = const.STATION_STATUS['GOOD']
            for ss in const.STATION_STATUS:
                if row.status == const.STATION_STATUS[ss]['value']:
                    status_icon = const.STATION_STATUS[ss]

            aaData.append({ 
                'station_name':row.station_name,
                'qi_time': row.qi_time.strftime("%H:%M %m/%d") if row.qi_time else '-',
                'qi':"{0:.0f}".format(row.qi) if row.qi else '-',
                'status': str(T(status_icon['name']))
            })
        content = json.dumps(aaData)
        return dict(content = content, success = True)   
    except Exception, ex:
        return dict(message = str(ex), success = False)

 
    