# -*- coding: utf-8 -*-
from applications.eos.modules import const, common
from gluon.tools import prettydate
import json

################################################################################
def waste_water():
    return dict()

################################################################################
def stack_emission():
    return dict()

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'aqi')))
def air():
    import random
    station_status = get_station_status()
    provinces = common.get_province_have_station_for_envisoft()

    index_items = const.AQI_COLOR
    for k in index_items:
        index_items[k]['text'] = str(T(index_items[k]['text']))
    index_items = json.dumps(index_items)

    for idx in station_status:
        status = station_status[idx]
        conditions = (db.stations.status == status['value'])
        status['num'] = db(conditions).count(db.stations.id)
        station_status[idx] = status
    json_station_status = json.dumps(station_status)
    indicators = get_all_records('indicators')
    json_indicators = json.dumps(indicators)
    conditions = (db.stations.id > 0)
    conditions &= (db.stations.is_qi == True)
    conditions &= (db.stations.station_type == const.STATION_TYPE['AMBIENT_AIR']['value'])
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))

    rows = db(conditions).select(db.stations.ALL)
    stations = []
    dt_format = '%Y-%m-%d %H:%M:%S'
    dt_format2 = '%H:%M %d/%m'
    for row in rows:
        station_id = str(row.id)
        s = str(row.status)
        try:
            is_public_data_type = row.is_public_data_type
        except:
            is_public_data_type = 2
        qi_value = ''
        qi_time = ''

        if row.station_type == 4:
            if is_public_data_type == 3:
                if qi_value == '':
                    qi_value = row.qi
                    qi_time = row.qi_time
            else:
                if qi_value == '':
                    qi_value = row.qi_adjust
                    qi_time = row.qi_adjsut_time

            if qi_time == '':
                qi_time = item.get_time

        station = {
            'station_id': station_id,
            'station_type': row.station_type,
            'station_name': row.station_name,
            'station_code': row.station_code,
            'province_id': row.province_id,
            'area_id': row.area_id,
            'address': row.address,
            'status': s,
            'lonlat': [row.longitude, row.latitude],
            'province_name': provinces[row['province_id']]['province_name'] if provinces.has_key(row['province_id']) else '',
            'status_disp': station_status[s]['name'] if station_status.has_key(s) else '',
            # 'index': random.randint(30, 450),
            'index': round(qi_value) if qi_value and qi_value != None else '-',
            'qi_time': qi_time.strftime(dt_format) if qi_time else '',
            'qi_time2': qi_time.strftime(dt_format2) if qi_time else '',
            'qi_time3': str(prettydate(qi_time, T)) if qi_time else '',
            'parameters': [],
        }

        if row.station_type == const.STATION_TYPE['AMBIENT_AIR']['value']:
            for key in sorted(const.AQI_COLOR):
                if station['index'] <= key:
                    station['bgColor'] = const.AQI_COLOR[key]['bgColor']
                    station['color'] = const.AQI_COLOR[key]['color']
                    station['status_text'] = '(' + const.AQI_COLOR[key]['text'] + ')'
                    break

        # conditions = (db.station_indicator.station_id == station_id)
        # station_indicators = db(conditions).select(db.station_indicator.ALL)
        # for si in station_indicators:
        # Todo: Remove this hardcode for prod
        idx = 0
        for k in indicators:
            si = indicators[k]
            if si['indicator_type']!=row.station_type:
                continue
            idx += 1
            if idx> 5:
                break
            parameter = {
                'id': si['id'],
                # 'key': indicators[str(si.indicator_id)]['indicator'],
                'key': si['indicator'],
                'value': random.randint(1, 10), # Todo: Hardcode value
                'unit': si['unit'],
            }
            station['parameters'].append(parameter)

        stations.append(station)
    json_stations = json.dumps(stations)
    # Group by station type
    # rows = db(db.stations.id > 0).select(db.stations.ALL, orderby=db.stations.station_type | db.stations.station_name)#hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    condition_new = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            condition_new &= (db.stations.id.belongs(station_ids))
    rows = db(condition_new).select(db.stations.ALL, orderby = db.stations.station_type | db.stations.station_name)
    areas = ''
    station_group_by_type = dict()
    for row in rows:
        st = str(row.station_type)
        s = str(row.status)
        if not station_group_by_type.has_key(st):
            station_group_by_type[st] = []
        item = {
            'id': str(row.id),
            'station_type': st,
            'station_name': row.station_name,
            'status': row.status,
            'latitude': row.latitude,
            'longitude': row.longitude,
            'status_disp': station_status[s]['name'] if station_status.has_key(s) else '',
            'qi_time': row.qi_time.strftime(dt_format) if row.qi_time else '',
            'qi_time2': row.qi_time.strftime(dt_format2) if row.qi_time else '',
            'qi_time3': str(prettydate(row.qi_time, T)) if row.qi_time else '',
        }
        station_group_by_type[st].append(item)
        areas = get_all_records_for_area('areas')
    json_area = json.dumps(areas)
    json_provinces = json.dumps(provinces)
    default_provinces = db(db.provinces.default == 1).select()
    return dict(station_group_by_type=station_group_by_type, json_stations=json_stations, provinces=provinces,
                station_status=station_status, json_station_status=json_station_status,
                json_indicators=json_indicators, json_area=json_area, json_provinces=json_provinces,
                stations=stations, areas=areas, default_provinces=default_provinces, index_items=index_items)

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'wqi')))
def wqi():
    import random
    station_status = get_station_status()
    provinces = common.get_province_have_station()
    for idx in station_status:
        status = station_status[idx]
        conditions = (db.stations.status == status['value'])
        status['num'] = db(conditions).count(db.stations.id)
        station_status[idx] = status

    index_items = const.WQI_COLOR
    for k in index_items:
        index_items[k]['text'] = str(T(index_items[k]['text']))
    index_items = json.dumps(index_items)

    json_station_status = json.dumps(station_status)
    indicators = get_all_records('indicators')
    json_indicators = json.dumps(indicators)
    conditions = (db.stations.id > 0)
    conditions &= (db.stations.is_qi == True)
    conditions &= (db.stations.station_type.belongs([const.STATION_TYPE['WASTE_WATER']['value'],
                                                     const.STATION_TYPE['SURFACE_WATER']['value'],
                                                     const.STATION_TYPE['UNDERGROUND_WATER']['value']]))
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))

    rows = db(conditions).select(db.stations.ALL)
    stations = []
    dt_format = '%Y-%m-%d %H:%M:%S'
    dt_format2 = '%H:%M %d/%m'
    for row in rows:
        station_id = str(row.id)
        s = str(row.status)

        try:
            is_public_data_type = row.is_public_data_type
        except:
            is_public_data_type = 2
        qi_value = ''
        qi_time = ''

        if (row.station_type != 4):
            if is_public_data_type == 3:
                conditionsaqi = (db.wqi_data_hour.station_id == station_id)
                wqi = db(conditionsaqi).select(
                    db.wqi_data_hour.get_time,
                    db.wqi_data_hour.data,
                    orderby=~db.wqi_data_hour.get_time,
                    limitby=(0, 1)
                )
            else:
                conditionsaqi = (db.wqi_data_adjust_hour.station_id == station_id)
                wqi = db(conditionsaqi).select(
                    db.wqi_data_adjust_hour.get_time,
                    db.wqi_data_adjust_hour.data,
                    orderby=~db.wqi_data_adjust_hour.get_time,
                    limitby=(0, 1)
                )

            for item in wqi:
                data = item.data
                for indicator in data:
                    if indicator == 'wqi':
                        if qi_value == '':
                            qi_value = data[indicator]
                            # if qi_value:
                            #     qi_value = "{0:.0f}".format(qi_value)
                        continue
                if qi_time == '':
                    qi_time = item.get_time

        station = {
            'station_id': station_id,
            'station_type': row.station_type,
            'station_name': row.station_name,
            'station_code': row.station_code,
            'province_id': row.province_id,
            'area_id': row.area_id,
            'address': row.address,
            'status': s,
            'lonlat': [row.longitude, row.latitude],
            'province_name': provinces[row['province_id']]['province_name'] if provinces.has_key(row['province_id']) else '',
            'status_disp': station_status[s]['name'] if station_status.has_key(s) else '',
            # 'index': random.randint(30, 450), # Todo: remove random
            'index': round(qi_value) if qi_value and qi_value != None else '-',
            'qi_time': qi_time.strftime(dt_format) if qi_time else '',
            'qi_time2': qi_time.strftime(dt_format2) if qi_time else '',
            'qi_time3': str(prettydate(qi_time, T)) if qi_time else '',
            'parameters': []
        }

        if row.station_type != const.STATION_TYPE['AMBIENT_AIR']['value']:
            for key in sorted(const.WQI_COLOR):
                if station['index'] <= key:
                    station['bgColor'] = const.WQI_COLOR[key]['bgColor']
                    station['color'] = const.WQI_COLOR[key]['color']
                    station['status_text'] = '(' + const.WQI_COLOR[key]['text'] + ')'
                    break

        # conditions = (db.station_indicator.station_id == station_id)
        # station_indicators = db(conditions).select(db.station_indicator.ALL)
        # for si in station_indicators:
        # Todo: Remove this hardcode for prod
        idx = 0
        for k in indicators:
            si = indicators[k]
            if si['indicator_type']!=row.station_type:
                continue
            idx += 1
            if idx> 5:
                break
            parameter = {
                'id': si['id'],
                # 'key': indicators[str(si.indicator_id)]['indicator'],
                'key': si['indicator'],
                'value': random.randint(1, 10), # Todo: Hardcode value
                'unit': si['unit'],
            }
            station['parameters'].append(parameter)

        stations.append(station)
    json_stations = json.dumps(stations)
    # Group by station type
    # rows = db(db.stations.id > 0).select(db.stations.ALL, orderby = db.stations.station_type | db.stations.station_name) #hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    condition_new = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            condition_new &= (db.stations.id.belongs(station_ids))
    rows = db(condition_new).select(db.stations.ALL, orderby = db.stations.station_type | db.stations.station_name)
    areas = ''
    station_group_by_type = dict()
    for row in rows:
        st = str(row.station_type)
        s = str(row.status)
        if not station_group_by_type.has_key(st):
            station_group_by_type[st] = []
        item = {
            'id': str(row.id),
            'station_type': st,
            'station_name': row.station_name,
            'status': row.status,
            'latitude': row.latitude,
            'longitude': row.longitude,
            'status_disp': station_status[s]['name'] if station_status.has_key(s) else '',
            'qi_time': row.qi_time.strftime(dt_format) if row.qi_time else '',
            'qi_time2': row.qi_time.strftime(dt_format2) if row.qi_time else '',
            'qi_time3': str(prettydate(row.qi_time, T)) if row.qi_time else '',
        }
        station_group_by_type[st].append(item)
        areas = get_all_records('areas')
    json_area = json.dumps(areas)
    json_provinces = json.dumps(provinces)
    default_provinces = db(db.provinces.default == 1).select()
    return dict(station_group_by_type=station_group_by_type, json_stations=json_stations, provinces=provinces,
                station_status=station_status, json_station_status=json_station_status,
                json_indicators=json_indicators, json_area=json_area, json_provinces=json_provinces,
                stations=stations, areas=areas, default_provinces=default_provinces, index_items=index_items)

################################################################################
@service.json 
def get_chart_for_station(*args, **kwargs):
    try:
        station_id = request.vars.stationId
        charts = dict()
        import random
        for i in range(1, 5):
            chart = dict()
            chart['title'] = dict(text = '<b>Formosa Hà Tĩnh</b>')
            chart['subtitle'] = {'text': 'Fe(mg/l)'}
            chart['xAxis'] = {'categories': range(1, 100)}
            data = []
            data1 = []
            data2 = []
            data3 = []
            for j in range(0, 100):
                x = j
                y = random.randint(950, 1000)
                data.append([x, y])
                data1.append([x, 940])
                data2.append([x, 965])
                data3.append([x, 1000])
            chart['series'] = [{
                'name': 'Fe(mg/l)',
                'data':  data,
            }, {
                'name': 'Exceeded tendency',
                'data': data1,
                'color': 'green'
            }, {
                'name': 'Exceeded preparing',
                'data': data2,
                'color': 'orange'
            }, {
                'name': 'Exceeded',
                'data': data3,
                'color': 'red '
            }]
            charts['index_%s' %i] = chart
        return dict(success = True, charts=charts)
    except Exception as ex:
        return dict(success = False, message = str(ex))

################################################################################
@service.json
def get_chart_for_station2(*args, **kwargs):
    try:
        station_id = request.vars.stationId
        charts = dict()
        import random
        for i in range(1, 5):
            chart = dict()
            chart['title'] = dict(text = '<b>Cái Đá</b>')
            chart['subtitle'] = {'text': 'Fe(mg/l)'}
            chart['xAxis'] = {'categories': range(1, 100)}
            data = []
            data1 = []
            data2 = []
            data3 = []
            for j in range(0, 100):
                x = j
                y = random.randint(950, 1000)
                data.append([x, y])
                data1.append([x, 940])
                data2.append([x, 965])
                data3.append([x, 1000])
            chart['series'] = [{
                'name': 'Fe(mg/l)',
                'data':  data,
            }, {
                'name': 'Exceeded tendency',
                'data': data1,
                'color': 'green'
            }, {
                'name': 'Exceeded preparing',
                'data': data2,
                'color': 'orange'
            }, {
                'name': 'Exceeded',
                'data': data3,
                'color': 'red '
            }]
            charts['index2_%s' %i] = chart
        return dict(success = True, charts=charts)
    except Exception as ex:
        return dict(success = False, message = str(ex))

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'qi')))
def get_list_station(*args, **kwargs):
    try:
        s_echo = request.vars.sEcho
        display_start = int(request.vars.iDisplayStart)
        display_length = int(request.vars.iDisplayLength)
        department_id = request.vars.department_id
        s_search = request.vars.sSearch
        rows = []
        list_data = None
        total_records = 100
        for i in range(0, total_records):
            row = [str(i+1), 'Tram nuoc thai %s' %i, T('LBL_DANG_HOAT_DONG')]
            rows.append(row)
        return dict(iTotalRecords = total_records, iTotalDisplayRecords = total_records, aaData = rows, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'qi')))
def get_list_station2(*args, **kwargs):
    try:
        s_echo = request.vars.sEcho
        display_start = int(request.vars.iDisplayStart)
        display_length = int(request.vars.iDisplayLength)
        department_id = request.vars.department_id
        s_search = request.vars.sSearch
        rows = []
        list_data = None
        total_records = 100
        for i in range(0, total_records):
            row = [str(i+1), 'Tram khi thai %s' %i, T('LBL_DANG_HOAT_DONG')]
            rows.append(row)
        return dict(iTotalRecords = total_records, iTotalDisplayRecords = total_records, aaData = rows, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'qi')))
def link_area_to_station(*args, **kwargs):
    try:
        areaId = request.vars.areaId
        stationId = request.vars.stationId
        stationType = request.vars.stationType or const.STATION_TYPE['WASTE_WATER']['value']
        conditions = ((db.area_station.area_id == areaId) |
                      (db.area_station.station_id == stationId) |
                      (db.area_station.station_type == stationType))
        is_existed = db(conditions).count(db.area_station.id)
        if is_existed:
            return dict(message=T('The record is existed!'), success=False)
        area = db.areas(areaId)
        area_name = area.area_name if area else ''
        station = db.stations(stationId)
        station_name = station.station_name if station else ''
        db.area_station.insert(area_id = areaId, area_name=area_name, station_id = stationId, station_name=station_name, station_type = stationType)
        return dict(success = True)
    except Exception as ex:
        return dict(message = str(ex), success = False)

################################################################################
# @decor.requires_login()
# @decor.requires_permission('sms|master|customers|list')
def popup_picklist():
    table = request.vars.table
    field = request.vars.field
    extend = request.vars.extend
    return  dict(table = table, field = field, extend = extend)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'qi')))
def get_list_for_popup_picklist(*args, **kwargs):
    try:
        aaData = []  # Du lieu json se tra ve

        station_type = request.vars.station_type or const.STATION_TYPE['WASTE_WATER']['value']
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength) # So luong ban ghi se lay toi da
        s_search = request.vars.sSearch2 # Chuoi tim kiem nhap tu form
        aaData = [] # Du lieu json se tra ve
        list_data = None # Du lieu truy van duoc
        iTotalRecords = 0 # Tong so ban ghi
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
        # Thu tu ban ghi
        idx = iDisplayStart + 1
        conditions = (db.stations.station_type == station_type)
        if s_search:
            conditions &= ((db.stations.station_code.contains(s_search)) |
                           (db.stations.station_name.contains(s_search)))
        list_data = db(conditions).select(  db.stations.id,
                                            db.stations.station_code,
                                            db.stations.station_name,
                                            limitby = limitby)
        iTotalRecords = db(conditions).count(db.stations.id)
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            listA = [
                    idx,
                    item.station_code,
                    item.station_name,
                    INPUT(_name = 'select_item', _class = 'select_item', _type = 'checkbox', _value = item.id,
                        data = dict(value = item.id, display = item.station_name)),
                    str(item.id)
            ]
            aaData.append(listA)
            idx += 1
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'qi')))
def get_data_for_block_chart(*args, **kwargs):
    try:
        dt = datetime.now()
        # last_check = dt.strftime('%Y-%m-%d %H:%M:%S')
        last_check = dt.strftime(datetime_format_vn)
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        station_id = request.vars.station_id
        from_public = request.vars.from_public
        station_name = ''
        station = db.stations(station_id)
        if station:
            station_name = station.station_name
        conditions = (db.station_indicator.station_id == station_id)
        conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        conditions &= (db.station_indicator.is_public == True)

        rows2 = db(conditions).select(db.station_indicator.indicator_id, distinct = True)

        indicators_id = []
        for row in rows2:
            indicators_id.append(row.indicator_id)
        indicators = db(db.indicators.id.belongs(indicators_id)).select(db.indicators.indicator)

        #Not
        conditions_not = (db.station_indicator.station_id == station_id)
        conditions_not &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        conditions_not &= (db.station_indicator.is_public == False)

        rows3 = db(conditions_not).select(db.station_indicator.indicator_id, distinct=True)

        indicators_id_not = []
        for row in rows3:
            indicators_id_not.append(row.indicator_id)
        indicators_not = db(db.indicators.id.belongs(indicators_id_not)).select(db.indicators.indicator)

        data = dict()

        from_time = dt - timedelta(days=7)
        to_time = dt
        # rows = db((db.aqi_data_24h.station_id == station_id) &
        #           (db.aqi_data_24h.get_time >= from_time)).select(db.aqi_data_24h.ALL, orderby = db.aqi_data_24h.get_time)

        try:
            is_public_data_type = station.is_public_data_type
        except:
            is_public_data_type = 2

        qi_value = ''
        qi_time = ''
        aqis = None

        if (station.station_type != 4):
            for indicator in indicators:
                item = []
                for i in range(7, 0, -1):
                    x = dt - timedelta(hours=i)
                    item.append({
                        "name": x,
                        "color": '#4dce6e',
                        "y": 0,
                    })
                data[str(indicator.indicator)] = item

            from_time = dt - timedelta(hours=7)
            if is_public_data_type == 3:
                conditions = (db.wqi_data_hour.station_id == station_id) & (db.wqi_data_hour.get_time >= from_time) & (db.wqi_data_hour.get_time < to_time)
                aqis = db(conditions).select(
                    db.wqi_data_hour.ALL,
                    orderby=~db.wqi_data_hour.get_time,
                    limitby=(0, 15)
                )
            else:
                conditions = (db.wqi_data_adjust_hour.station_id == station_id) & (db.wqi_data_adjust_hour.get_time >= from_time) & (db.wqi_data_adjust_hour.get_time < to_time)
                aqis = db(conditions).select(
                    db.wqi_data_adjust_hour.ALL,
                    orderby=~db.wqi_data_adjust_hour.get_time,
                    limitby=(0, 15)
                )

            for row in aqis:
                for k in data:
                    if row.data.has_key(k):
                        for idx, item in enumerate(data[k]):
                            if row.get_time == item['name']:
                                print(row.data[k])
                                data[k][idx]['y'] = round(float(row.data[k]), 0)
                                break
            for k in data:
                for idx, item in enumerate(data[k]):
                    data[k][idx]['name'] = int(1000 * (data[k][idx]['name'] - datetime(1970, 1, 1)).total_seconds())
                    # data[k][idx][0] = (data[k][idx][0]).strftime('%d-%m-%Y')
            res = {}
            for item in aqis:
                data2 = item.data

                for i in indicators_not:
                    if data2.has_key(i.indicator):
                        del data2[i.indicator]

                for indicator in data2:
                    if indicator == 'wqi': continue
                    if not res.has_key(indicator):
                        res[indicator] = {
                            'values': [],
                            'min': data2[indicator],
                            'max': data2[indicator],
                        }
                    # O day mang 'values' dang duoc luu gtri theo tgian tu gan --> xa
                    # nen tren html se phai dao nguoc lai (reversed)
                    res[indicator]['values'].append(str(int(round(data2[indicator]))))
                    if res[indicator]['min'] > data2[indicator]:
                        res[indicator]['min'] = data2[indicator]
                    if res[indicator]['max'] < data2[indicator]:
                        res[indicator]['max'] = data2[indicator]

        else:
            for indicator in indicators:
                item = []
                for i in range(7, 0, -1):
                    x = dt - timedelta(days=i)
                    item.append({
                        "name": x,
                        "color": '#4dce6e',
                        "y": 0,
                    })
                data[str(indicator.indicator)] = item

            if is_public_data_type == 3:
                conditions = (db.aqi_data_24h.station_id == station_id) & (db.aqi_data_24h.get_time >= from_time) & (db.aqi_data_adjust_24h.get_time < to_time)
                aqis = db(conditions).select(
                    db.aqi_data_24h.ALL,
                    orderby=~db.aqi_data_24h.get_time,
                    limitby=(0, 15)
                )
            else:
                conditions = (db.aqi_data_adjust_24h.station_id == station_id) & (db.aqi_data_adjust_24h.get_time >= from_time) & (db.aqi_data_adjust_24h.get_time < to_time)
                aqis = db(conditions).select(
                    db.aqi_data_adjust_24h.ALL,
                    orderby=~db.aqi_data_adjust_24h.get_time,
                    limitby=(0, 15)
                )

            for row in aqis:
                for k in data:
                    if row.data_1d.has_key(k):
                        for idx, item in enumerate(data[k]):
                            if row.get_time == item['name']:
                                data[k][idx]['y'] = round(float(row.data_1d[k]), 0)
                                break
            for k in data:
                for idx, item in enumerate(data[k]):
                    data[k][idx]['name'] = int(1000 * (data[k][idx]['name'] - datetime(1970, 1, 1)).total_seconds())
                    # data[k][idx][0] = (data[k][idx][0]).strftime('%d-%m-%Y')
            res = {}
            for item in aqis:
                data2 = item.data_1d

                for i in indicators_not:
                    if data2.has_key(i.indicator):
                        del data2[i.indicator]

                for indicator in data2:
                    if indicator == 'aqi': continue
                    if not res.has_key(indicator):
                        res[indicator] = {
                            'values': [],
                            'min': data2[indicator],
                            'max': data2[indicator],
                        }
                    # O day mang 'values' dang duoc luu gtri theo tgian tu gan --> xa
                    # nen tren html se phai dao nguoc lai (reversed)
                    res[indicator]['values'].append(str(int(round(data2[indicator]))))
                    if res[indicator]['min'] > data2[indicator]:
                        res[indicator]['min'] = data2[indicator]
                    if res[indicator]['max'] < data2[indicator]:
                        res[indicator]['max'] = data2[indicator]

        return dict(charts = data, station_name=station_name, last_check=last_check, res=res)
    except Exception as ex:
        return dict(charts=[], station_name='', last_check=last_check)

################################################################################
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


