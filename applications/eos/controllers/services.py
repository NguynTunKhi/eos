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

myjwt = AuthJWT(auth, secret_key='secret@259', expiration=60 * 60)

#auth.settings.allow_basic_login = True
#@auth.requires_login()
auth.settings.allow_basic_login = True

def call():
    session.forget()
    response.headers["Access-Control-Allow-Origin"] = '*'
    return service()

################################################################################
@service.json
def getAppSetting(*args, **kwargs):
    settings = db().select(db.app_settings.ALL).first()
    return dict(success=True, data=settings)

@service.json
@auth.requires_login()
def login(*args, **kwargs):
    #return dict(success=True, token=myjwt.jwt_token_manager().token)
    #return {'success': True}
    token = myjwt.jwt_token_manager()
    json_object = json.loads(token)
    return dict(success=True, token=json_object['token'])

@service.json
@myjwt.allows_jwt()
def getInfo():
    user = db.auth_user(auth.user_id)
    return dict(success=True, data=user)

@service.json
@myjwt.allows_jwt()
def changePassword(*args, **kwargs):
    user = db.auth_user(auth.user_id)
    result = False
    print request.post_vars
    if CRYPT(digest_alg = 'sha512', salt = True)(request.vars.old_password)[0] == user.password:
        user.password =  CRYPT(digest_alg = 'sha512', salt = True)(request.vars.password)[0]
    #    # db.usr[user.id] = dict(password = user.password)
        db.auth_user[user.id] = dict(password = user.password)
        result = True
    return dict(success=result)

@service.json
#@myjwt.allows_jwt()
def get_common_settings(*args, **kwargs):
    try:
        # aqi_colors
        aqi_colors = []
        for k in sorted(const.AQI_COLOR):
            name = ''
            if const.AQI_COLOR[k]['to']:
                name = '%s-%s (%s)' %(const.AQI_COLOR[k]['from'], const.AQI_COLOR[k]['to'], T(const.AQI_COLOR[k]['text']))
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
        return dict(success=True, qi_colors = aqi_colors, aqi_colors = aqi_colors, wqi_colors = wqi_colors, status=status,
                    provinces=provinces, station_type=station_type)
    except Exception as ex:
        return dict(success=False, message=str(ex))

###############################################################################
@service.json
def get_stations_by_province(*args, **kwargs):
    province_id_list = request.vars.limit_province_id
    if province_id_list:
        province_id_list = province_id_list.split(',')

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
            },
            {
                'name': T('Offline'),
                'type': 'areaspline',
                'color': '#544e4f',
                'data': [],
                'marker': {'enabled': False},
            },
            {
                'name': T('Adjust'),
                'type': 'areaspline',
                'color': '#8322d8',
                'data': [],
                'marker': {'enabled': False},
            },
            {
                'name': T('Equipment error'),
                'type': 'areaspline',
                'color': '#d84622',
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
        if province_id_list :
            conditions &= (db.stations.province_id.contains(province_id_list, all=False))
        else :
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
                    'qty_offline': 0,
                    'qty_adjust': 0,
                    'qty_error': 0
                }
            categories[province_id]['qty'] += 1
            if row.status == const.STATION_STATUS['EXCEED']['value']:
                categories[province_id]['qty_exceed'] += 1
                pass
            elif row.status == const.STATION_STATUS['GOOD']['value'] or\
                    row.status == const.STATION_STATUS['TENDENCY']['value'] or\
                    row.status == const.STATION_STATUS['PREPARING']['value']:
                categories[province_id]['qty_good'] += 1
            elif row.status == const.STATION_STATUS['OFFLINE']['value']:
                categories[province_id]['qty_offline'] += 1
            elif row.status == const.STATION_STATUS['ADJUSTING']['value']:
                categories[province_id]['qty_adjust'] += 1
            elif row.status == const.STATION_STATUS['ERROR']['value']:
                categories[province_id]['qty_error'] += 1
        for item in categories:
            data['categories'].append(categories[item]['name'])
            data['series'][0]['data'].append(categories[item]['qty'])
            data['series'][1]['data'].append(categories[item]['qty_good'])
            data['series'][2]['data'].append(categories[item]['qty_exceed'])
            data['series'][3]['data'].append(categories[item]['qty_offline'])
            data['series'][4]['data'].append(categories[item]['qty_adjust'])
            data['series'][5]['data'].append(categories[item]['qty_error'])

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
#@myjwt.allows_jwt()
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
                                     orderby=db.stations.order_no)

        dt_format = '%Y-%m-%d %H:%M:%S'
        dt_format2 = '%H:%M %d/%m'
        for row in rows:
            station_color = '#333333'
            station_status = ''
            icon = ''
            try:
                is_public_data_type = row.is_public_data_type
            except:
                is_public_data_type = 2

            show_off_time = False
            if row.status in [const.STATION_STATUS['OFFLINE']['value'], const.STATION_STATUS['ADJUSTING']['value'], const.STATION_STATUS['ERROR']['value']]:
                if row.off_time:
                    show_off_time = True
            for k in const.STATION_STATUS:
                if const.STATION_STATUS[k]['value'] == row.status:
                    station_color = const.STATION_STATUS[k]['color']
                    station_status = T(const.STATION_STATUS[k]['name'])
                    icon = T(const.STATION_STATUS[k]['icon'])
            qi_detail_info = {}
            if row.station_type in [const.STATION_TYPE['WASTE_WATER']['value'],
                                        const.STATION_TYPE['SURFACE_WATER']['value'],
                                        const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
                colors = const.WQI_COLOR
            else:
                colors = const.AQI_COLOR
            for key in sorted(colors):
                if is_public_data_type == 3:
                    if row.qi <= key:
                        qi_detail_info = colors[key]
                        break
                else:
                    if row.qi_adjust <= key:
                        qi_detail_info = colors[key]
                        break

            if is_public_data_type == 3:
                qi = row.qi if row.qi else '-'
                qi_time = row.qi_time.strftime(dt_format) if row.qi_time else ''
                qi_time2 = row.qi_time.strftime(dt_format2) if row.qi_time else ''
                qi_time3 = prettydate(row.qi_time, T) if row.qi_time else ''
                status = T(qi_detail_info['text']) if row.qi else '-'
                color = qi_detail_info['bgColor'] if row.qi else '-'
            else:
                qi = row.qi_adjust if row.qi_adjust else '-'
                qi_time = row.qi_adjsut_time.strftime(dt_format) if row.qi_adjsut_time else ''
                qi_time2 = row.qi_adjsut_time.strftime(dt_format2) if row.qi_adjsut_time else ''
                qi_time3 = prettydate(row.qi_adjsut_time, T) if row.qi_adjsut_time else ''
                status = T(qi_detail_info['text']) if row.qi_adjust else '-'
                color = qi_detail_info['bgColor'] if row.qi_adjust else '-'

            stations.append({
                'id': str(row.id),
                'station_name': row.station_name,
                'longitude': row.longitude,
                'latitude': row.latitude,
                'address': row.address,
                'qi': qi,
                'qi_time': qi_time,
                'qi_time2': qi_time2,
                'qi_time3': qi_time3,
                'off_time': row.off_time.strftime(dt_format) if show_off_time else '',
                'off_time2': row.off_time.strftime(dt_format2) if show_off_time else '',
                'off_time3': prettydate(row.off_time, T) if show_off_time else '',
                'status': status,
                'color': color,
                'station_status': station_status,
                'station_color': station_color,
                'icon': icon
            })
        return dict(success=True, stations = stations)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
def qi_detail(*args, **kwargs):
    try:
        station_id = request.vars.station_id

        qi_time = request.vars.qi_time
        get_aqi_type = 1

        station = db.stations(station_id) or None
        qi_detail_info = {}
        qi_value = ''
        station_name = ''
        is_public_data_type = 2
        qi_time_1, qi_time_2 = '', ''

        if not station:
            return dict(success=False, message=T('Not found!'))

        # qi_value = int(round(station.qi)) if station.qi else '-'
        station_name = station.station_name
        try:
            is_public_data_type = station.is_public_data_type
        except:
            is_public_data_type = 2
        qi_time_1 = prettydate(station.qi_time, T) if station.qi_time else '-'
        # qi_time_2 = stations.qi_time.strftime('%d/%m/%Y %H:%S') if stations.qi_time else '-'
        # qi_time_2 = station.qi_time.strftime(datetime_format_vn_2) if station.qi_time else '-'
        if station.station_type in [const.STATION_TYPE['WASTE_WATER']['value'], const.STATION_TYPE['SURFACE_WATER']['value'], const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
            colors = const.WQI_COLOR
        else:
            colors = const.AQI_COLOR

        ### Lay phan du lieu chi so AQI detail
        aqis = []

        if station.station_type in [const.STATION_TYPE['WASTE_WATER']['value'], const.STATION_TYPE['SURFACE_WATER']['value'], const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
            if qi_time:
                get_aqi_type = qi_time
            if get_aqi_type == 1:
                if is_public_data_type == 3:
                    conditions = (db.wqi_data_hour.station_id == station_id)
                    aqis = db(conditions).select(
                        db.wqi_data_hour.get_time,
                        db.wqi_data_hour.data,
                        orderby=~db.wqi_data_hour.get_time,
                        limitby=(0, 49)
                    )
                else:
                    conditions = (db.wqi_data_adjust_hour.station_id == station_id)
                    aqis = db(conditions).select(
                        db.wqi_data_adjust_hour.get_time,
                        db.wqi_data_adjust_hour.data,
                        orderby=~db.wqi_data_adjust_hour.get_time,
                        limitby=(0, 49)
                    )
            else:  # hungdx khong co wqi 24h nen khong xu ly
                conditions = (db.wqi_data_24h.station_id == station_id)
                aqis = db(conditions).select(
                    db.wqi_data_24h.get_time,
                    db.wqi_data_24h.data,
                    orderby=~db.wqi_data_24h.get_time,
                    limitby=(0, 49)
                )
        else:
            if qi_time:
                get_aqi_type = qi_time
            if get_aqi_type == 1:
                if is_public_data_type == 3:
                    conditions = (db.aqi_data_hour.station_id == station_id)
                    aqis = db(conditions).select(
                        db.aqi_data_hour.get_time,
                        db.aqi_data_hour.data,
                        orderby=~db.aqi_data_hour.get_time,
                        limitby=(0, 49)
                    )
                else:
                    conditions = (db.aqi_data_adjust_hour.station_id == station_id)
                    aqis = db(conditions).select(
                        db.aqi_data_adjust_hour.get_time,
                        db.aqi_data_adjust_hour.data,
                        orderby=~db.aqi_data_adjust_hour.get_time,
                        limitby=(0, 49)
                    )
            else:
                if is_public_data_type == 3:
                    conditions = (db.aqi_data_24h.station_id == station_id)
                    aqis = db(conditions).select(
                        db.aqi_data_24h.get_time,
                        db.aqi_data_24h.data,
                        orderby=~db.aqi_data_hour.get_time,
                        limitby=(0, 49)
                    )
                else:
                    conditions = (db.aqi_data_adjust_24h.station_id == station_id)
                    aqis = db(conditions).select(
                        db.aqi_data_adjust_24h.get_time,
                        db.aqi_data_adjust_24h.data,
                        orderby=~db.aqi_data_adjust_24h.get_time,
                        limitby=(0, 49)
                    )

        res = {}
        conditions = (db.station_indicator.station_id == station_id) & (db.station_indicator.is_public == False)
        rows2 = db(conditions).select(db.station_indicator.indicator_id, distinct=True)
        indicators_id = []
        for row in rows2:
            indicators_id.append(row.indicator_id)
        indicators = db(db.indicators.id.belongs(indicators_id)).select(db.indicators.indicator)
        for item in aqis:
            if qi_time_1 == '':
                qi_time_1 = prettydate(item.get_time, T) if item.get_time else '-'
            if qi_time_2 == '':
                qi_time_2 = item.get_time.strftime(datetime_format_vn_2) if item.get_time else '-'
            data2 = dict()
            data = item.data
            for i in indicators:
                # print data.has_key(i.indicator)
                if data.has_key(i.indicator):
                    del data[i.indicator]
                    # data2 = data.fromkeys([i.indicator], data.get(i.indicator))
                    # data2.update(data2)
                # print data2
            for indicator in data:
                if indicator == 'aqi':
                    if qi_value == '':
                        qi_value = data[indicator]
                        if qi_value:
                            qi_value = int(round(qi_value)) if qi_value else '-'
                    continue

                if indicator == 'wqi':
                    if qi_value == '':
                        qi_value = data[indicator]
                        if qi_value:
                            qi_value = int(round(qi_value)) if qi_value else '-'
                    continue

                if not res.has_key(indicator):
                    res[indicator] = {
                        'values': [],
                        'min': data[indicator],
                        'max': data[indicator],
                        'current': data[indicator]
                    }

                # O day mang 'values' dang duoc luu gtri theo tgian tu gan --> xa
                # nen tren html se phai dao nguoc lai (reversed)
                res[indicator]['values'].append({str(int(round(data[indicator]))): item.get_time.strftime(datetime_format_vn_2)})
                if res[indicator]['min'] > data[indicator]:
                    res[indicator]['min'] = data[indicator]
                if res[indicator]['max'] < data[indicator]:
                    res[indicator]['max'] = data[indicator]
        # Lay bang dinh nghia Color cho AQI, de buil colorMap cho client co format:
        # '0 : 50' : 'color1', '51 : 100' : 'color2', ....

        if ((qi_value == '') or (qi_value is None)):
            qi_value = '-'

        if (qi_value != '-'):
            for key in sorted(colors):
                if qi_value <= key:
                    qi_detail_info = colors[key]
                    break

        keys = sorted(colors)  # keys    = [50, 100, 150, 200, 300, 999]
        shift_keys = [-1] + keys[:len(keys) - 1]  # shift_keys = [-1, 50, 100, 150, 200, 300]
        # color_map = ''
        color_map = {}
        for i, key in enumerate(keys):
            # color_map += "'%s : %s' : '%s', " % (shift_keys[i] + 1, keys[i], colors[key]['bgColor'])
            color_map['%s : %s' % (shift_keys[i] + 1, keys[i])] = '%s' % (colors[key]['bgColor'])
        # color_map = json.dumps(color_map)
        if qi_detail_info.has_key('description'):
            qi_detail_info['description'] = str(T(qi_detail_info['description']))

        if qi_value == '-':
            qi_detail_info = {}
        return dict(success=True, qi_value=qi_value, station_name=station_name, res=res, color_map=color_map,
                    qi_time_1=qi_time_1, qi_time_2=qi_time_2, qi_detail_info=qi_detail_info)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
def qi_detail_for_eip(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        station_type = request.vars.station_type

        qi_time = request.vars.qi_time
        get_aqi_type = 1

        station = db.stations(station_id) or None
        qi_detail_info = {}
        qi_value = ''
        station_name = ''
        is_public_data_type = 2
        qi_time_1, qi_time_2 = '', ''

        if not station:
            return dict(success=False, message=T('Not found!'))

        # qi_value = int(round(station.qi)) if station.qi else '-'
        station_name = station.station_name
        try:
            is_public_data_type = station.is_public_data_type
        except:
            is_public_data_type = 2
        qi_time_1 = prettydate(station.qi_time, T) if station.qi_time else '-'
        # qi_time_2 = stations.qi_time.strftime('%d/%m/%Y %H:%S') if stations.qi_time else '-'
        # qi_time_2 = station.qi_time.strftime(datetime_format_vn_2) if station.qi_time else '-'
        if station.station_type in [const.STATION_TYPE['WASTE_WATER']['value'], const.STATION_TYPE['SURFACE_WATER']['value'], const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
            colors = const.WQI_COLOR
        else:
            colors = const.AQI_COLOR

        ### Lay phan du lieu chi so AQI detail
        aqis = []

        if station.station_type in [const.STATION_TYPE['WASTE_WATER']['value'], const.STATION_TYPE['SURFACE_WATER']['value'], const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
            if qi_time:
                get_aqi_type = qi_time
            if get_aqi_type == 1:
                if is_public_data_type == 3:
                    conditions = (db.wqi_data_hour.station_id == station_id)
                    aqis = db(conditions).select(
                        db.wqi_data_hour.get_time,
                        db.wqi_data_hour.data,
                        orderby=~db.wqi_data_hour.get_time,
                        limitby=(0, 25)
                    )
                else:
                    conditions = (db.wqi_data_adjust_hour.station_id == station_id)
                    aqis = db(conditions).select(
                        db.wqi_data_adjust_hour.get_time,
                        db.wqi_data_adjust_hour.data,
                        orderby=~db.wqi_data_adjust_hour.get_time,
                        limitby=(0, 25)
                    )
            else:  #hungdx khong co wqi 24h nen khong xu ly
                conditions = (db.wqi_data_24h.station_id == station_id)
                aqis = db(conditions).select(
                    db.wqi_data_24h.get_time,
                    db.wqi_data_24h.data,
                    orderby=~db.wqi_data_24h.get_time,
                    limitby=(0, 25)
                )
        else :
            if qi_time:
                get_aqi_type = qi_time
            if get_aqi_type == 1:
                if is_public_data_type == 3:
                    conditions = (db.aqi_data_hour.station_id == station_id)
                    aqis = db(conditions).select(
                        db.aqi_data_hour.get_time,
                        db.aqi_data_hour.data,
                        orderby = ~db.aqi_data_hour.get_time,
                        limitby = (0, 25)
                    )
                else:
                    conditions = (db.aqi_data_adjust_hour.station_id == station_id)
                    aqis = db(conditions).select(
                        db.aqi_data_adjust_hour.get_time,
                        db.aqi_data_adjust_hour.data,
                        orderby=~db.aqi_data_adjust_hour.get_time,
                        limitby=(0, 25)
                    )
            else:
                if is_public_data_type == 3:
                    conditions = (db.aqi_data_24h.station_id == station_id)
                    aqis = db(conditions).select(
                        db.aqi_data_24h.get_time,
                        db.aqi_data_24h.data,
                        orderby=~db.aqi_data_hour.get_time,
                        limitby=(0, 25)
                    )
                else:
                    conditions = (db.aqi_data_adjust_24h.station_id == station_id)
                    aqis = db(conditions).select(
                        db.aqi_data_adjust_24h.get_time,
                        db.aqi_data_adjust_24h.data,
                        orderby=~db.aqi_data_adjust_24h.get_time,
                        limitby=(0, 25)
                    )

        res = {}
        conditions = (db.station_indicator.station_id == station_id) & (db.station_indicator.is_public == False)
        rows2 = db(conditions).select(db.station_indicator.indicator_id, distinct=True)
        indicators_id = []
        for row in rows2:
            indicators_id.append(row.indicator_id)
        indicators = db(db.indicators.id.belongs(indicators_id)).select(db.indicators.indicator)
        for item in aqis:
            if qi_time_1 == '':
                qi_time_1 = prettydate(item.get_time, T) if item.get_time else '-'
            if qi_time_2 == '':
                qi_time_2 = item.get_time.strftime(datetime_format_vn_2) if item.get_time else '-'
            data2 = dict()
            data = item.data
            for i in indicators:
                #print data.has_key(i.indicator)
                if data.has_key(i.indicator):
                    del data[i.indicator]
                    #data2 = data.fromkeys([i.indicator], data.get(i.indicator))
                    #data2.update(data2)
                #print data2
            for indicator in data:
                if indicator == 'aqi' :
                    if qi_value == '' :
                        qi_value = data[indicator]
                        if qi_value :
                            qi_value = int(round(qi_value)) if qi_value else '-'
                    continue

                if indicator == 'wqi' :
                    if qi_value == '' :
                        qi_value = data[indicator]
                        if qi_value :
                            qi_value = int(round(qi_value)) if qi_value else '-'
                    continue

                if not res.has_key(indicator):
                    res[indicator] = {
                        'values': [],
                        'min': data[indicator],
                        'max': data[indicator],
                        'current': data[indicator]
                    }

                # O day mang 'values' dang duoc luu gtri theo tgian tu gan --> xa
                # nen tren html se phai dao nguoc lai (reversed)
                res[indicator]['values'].append({str(int(round(data[indicator]))): item.get_time.strftime(datetime_format_vn_2)})
                if res[indicator]['min'] > data[indicator]:
                    res[indicator]['min'] = data[indicator]
                if res[indicator]['max'] < data[indicator]:
                    res[indicator]['max'] = data[indicator]
        # Lay bang dinh nghia Color cho AQI, de buil colorMap cho client co format:
        # '0 : 50' : 'color1', '51 : 100' : 'color2', ....

        if ((qi_value == '') or (qi_value is None)) :
            qi_value = '-'

        if (qi_value != '-') :
            for key in sorted(colors):
                if qi_value <= key:
                    qi_detail_info = colors[key]
                    break

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

        return dict(success=True, qi_value = qi_value, station_name = station_name, res = res, color_map = color_map,
                    qi_time_1 = qi_time_1, qi_time_2 = qi_time_2, qi_detail_info = qi_detail_info)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
def qi_detail_24h(*args, **kwargs):
    try:
        dt = datetime.now()
        station_id = request.vars.station_id
        qi_time = request.vars.qi_time
        get_aqi_type = 2

        station = db.stations(station_id) or None
        qi_detail_info = {}
        qi_value = ''
        station_name = ''
        is_public_data_type = 2
        qi_time_1, qi_time_2, min_date, max_date, qi_time_3 = '', '', '', '', ''
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

        if not station:
            return dict(success=False, message=T('Not found!'))

        # qi_value = int(round(station.qi)) if station.qi else '-'
        station_name = station.station_name
        try:
            is_public_data_type = station.is_public_data_type
        except:
            is_public_data_type = 2
        qi_time_1 = prettydate(station.qi_time, T) if station.qi_time else '-'
        # qi_time_2 = stations.qi_time.strftime('%d/%m/%Y %H:%S') if stations.qi_time else '-'
        #qi_time_2 = station.qi_time.strftime(datetime_format_vn) if station.qi_time else '-'

        ### Lay phan du lieu chi so AQI detail
        aqis = []
        if qi_time:
            get_aqi_type = qi_time
        if get_aqi_type == 1:
            if is_public_data_type == 3:
                conditions = (db.aqi_data_hour.station_id == station_id)
                aqis = db(conditions).select(
                    db.aqi_data_hour.get_time,
                    db.aqi_data_hour.data,
                    orderby = ~db.aqi_data_hour.get_time,
                    limitby = (0, 15)
                )
            else:
                conditions = (db.aqi_data_adjust_hour.station_id == station_id)
                aqis = db(conditions).select(
                    db.aqi_data_adjust_hour.get_time,
                    db.aqi_data_adjust_hour.data,
                    orderby=~db.aqi_data_adjust_hour.get_time,
                    limitby=(0, 15)
                )
        else:
            from_time = dt - timedelta(days=15)
            to_time = dt
            if is_public_data_type == 3:
                conditions = (db.aqi_data_24h.station_id == station_id) & (db.aqi_data_24h.get_time >= from_time) & (db.aqi_data_adjust_24h.get_time < to_time)
                aqis = db(conditions).select(
                    db.aqi_data_24h.get_time,
                    db.aqi_data_24h.data_1d,
                    orderby=~db.aqi_data_24h.get_time,
                    limitby=(0, 15)
                )
            else:
                conditions = (db.aqi_data_adjust_24h.station_id == station_id) & (db.aqi_data_adjust_24h.get_time >= from_time) & (db.aqi_data_adjust_24h.get_time < to_time)
                aqis = db(conditions).select(
                    db.aqi_data_adjust_24h.get_time,
                    db.aqi_data_adjust_24h.data_1d,
                    orderby=~db.aqi_data_adjust_24h.get_time,
                    limitby=(0, 15)
                )
        res = {}
        conditions = (db.station_indicator.station_id == station_id) & (db.station_indicator.is_public == False)
        rows2 = db(conditions).select(db.station_indicator.indicator_id, distinct=True)
        indicators_id = []
        for row in rows2:
            indicators_id.append(row.indicator_id)
        indicators = db(db.indicators.id.belongs(indicators_id)).select(db.indicators.indicator)

        numberData = 0
        for item in aqis:
            data = item.data_1d

            # if numberData == 0:
            #     numberData += 1
            #     continue
            if qi_time_2 == '':
                qi_time_2 = item.get_time.strftime('%d/%m/%Y') if item.get_time else '-'

            if qi_time_3 == '':
                qi_time_3 = item.get_time.strftime(datetime_format_vn_2) if item.get_time else '-'

            if min_date == '':
                min_date = item.get_time
            if max_date == '':
                max_date = item.get_time

            if min_date > item.get_time:
                min_date = item.get_time
            if max_date < item.get_time:
                max_date = item.get_time

            for i in indicators:
                if data.has_key(i.indicator):
                    del data[i.indicator]
                    if data.has_key('O38h') and i.indicator == "O3":
                        try:
                            del data["O38h"]
                        except:
                            pass
            for indicator in data:
                if indicator == 'aqi' :
                    if qi_value == '':
                        qi_value = int(round(data[indicator])) if data[indicator] else '-'
                    continue
                if not res.has_key(indicator):
                    res[indicator] = {
                        'values': [],
                        'min': data[indicator],
                        'max': data[indicator],
                        'current': data[indicator],
                    }
                # O day mang 'values' dang duoc luu gtri theo tgian tu gan --> xa
                # nen tren html se phai dao nguoc lai (reversed)
                res[indicator]['values'].append({str(int(round(data[indicator]))): item.get_time.strftime(' %d/%m/%Y')})
                if res[indicator]['min'] > data[indicator]:
                    res[indicator]['min'] = data[indicator]
                if res[indicator]['max'] < data[indicator]:
                    res[indicator]['max'] = data[indicator]

        if station.station_type in [const.STATION_TYPE['WASTE_WATER']['value'], const.STATION_TYPE['SURFACE_WATER']['value'], const.STATION_TYPE['UNDERGROUND_WATER']['value']]:
            colors = const.WQI_COLOR
        else:
            colors = const.AQI_COLOR
        for key in sorted(colors):
            if qi_value <= key:
                qi_detail_info = colors[key]
                break

        # res = sorted(res)
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

        min_date = min_date.strftime('%d/%m/%Y') if min_date else '-'
        max_date = max_date.strftime('%d/%m/%Y') if max_date else '-'

        if qi_value == '' :
            qi_value = '-'
        return dict(success=True, qi_value = qi_value, station_name = station_name, res = res, color_map = color_map,
                    qi_time_1 = qi_time_1, qi_time_2 = qi_time_2, qi_detail_info = qi_detail_info, qi_time_3 = qi_time_3, min_date = min_date, max_date = max_date)
    except Exception as ex:
        return dict(success=False, message=str(ex))

def sortSecond(val):
    return val[1]

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

 
    