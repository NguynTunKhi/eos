# -*- coding: utf-8 -*-
import json
from datetime import datetime

from applications.eos.modules import const, common


################################################################################
# @auth.requires_membership('manager')
# @auth.requires_permission('view', 'stations')
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def stations():
    # Cai nay de test tinh toan du lieu hour, day, month
    # get_data()
    # calc_data_hour(datetime.strptime('20180801 000000', '%Y%m%d %H%M%S'))
    # calc_data_day(datetime.strptime('20180801 000000', '%Y%m%d %H%M%S'))
    # # calc_data_month(datetime.strptime('20180801 000000', '%Y%m%d %H%M%S'))
    # calc_aqi_data_hour(datetime.strptime('20180801 000000', '%Y%m%d %H%M%S'))
    # calc_aqi_data_24h(datetime.strptime('20180801 000000', '%Y%m%d %H%M%S'))

    # db.data_hour.insert(
    # station_id = '28416451415407416826266497775',       # Long Thanh
    # get_time = datetime.now().replace(minute = 0, second = 0, microsecond = 0),
    # data = {
    # 'BOD5':  5,
    # 'COD':   17,
    # 'N-NH4': 0.7,
    # 'P-PO4': 7,
    # 'Turbidity': 4,
    # 'TSS':      45,
    # 'Coliform': 3500,
    # 'DO': 4.9,
    # 'pH' : 6.5,
    # 'Temp' : 28
    # })
    # calc_wqi_data_hour(datetime.strptime('20180801 000000', '%Y%m%d %H%M%S'))
    # Tinh ra gtri wqi = 71
    selected_st = request.vars.station_type or const.STATION_TYPE['SURFACE_WATER']['value']
    selected_st = int(selected_st)
    selected_st_name = common.get_info_from_const(const.STATION_TYPE, selected_st)[
        'name'].upper() if common.get_info_from_const(const.STATION_TYPE, selected_st) else ''
    station_type = request.vars.station_type or 0
    # Select provinces to fill in dropdown box
    provinces = common.get_province_have_station()
    # Select stations to fill in dropdown box
    areas = db(db.areas.id > 0).select()

    conditions = (db.stations.station_type == station_type)
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))

    stations = db(conditions).select(db.stations.id, db.stations.station_name)
    default_provinces = db(db.provinces.default == 1).select()
    return dict(provinces=provinces, areas=areas, station_type=station_type, stations=stations,
                default_provinces=default_provinces, selected_st_name=T(selected_st_name), selected_st=selected_st)


################################################################################
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def map():
    station_id = request.vars.station_id
    if not station_id:
        station_id = request.args(0)
    record = db.stations(station_id) or None

    # Count qty of stations by status
    station_status2 = get_station_status()
    new_group = [const.STATION_STATUS['TENDENCY']['value'], const.STATION_STATUS['PREPARING']['value']]
    total_group = 0
    station_status = {}
    for idx in station_status2:
        status = station_status2[idx]
        conditions = (db.stations.status == status['value'])
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        num = db(conditions).count(db.stations.id)
        if status['value'] not in new_group:
            status['num'] = num
            station_status[idx] = status
        else:
            total_group += num
    for idx in station_status:
        status = station_status[idx]
        if status['value'] == const.STATION_STATUS['GOOD']['value']:
            if status['num']:
                status['num'] += total_group
            else:
                status['num'] = total_group

    json_station_status = json.dumps(station_status)
    # provinces = get_all_records('provinces')
    provinces = common.get_province_have_station_for_envisoft()
    indicators = get_all_records('indicators')
    json_indicators = json.dumps(indicators)

    # Get all stations to display on map
    conditions = (db.stations.id > 0)
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))

    # rows = db(conditions).select(db.stations.ALL, orderby = db.stations.station_type | db.stations.station_name)
    rows = db(conditions).select(db.stations.ALL, orderby=db.stations.order_no)
    total_station = len(rows)
    stations = []
    if False:
        conditions1 = (db.station_indicator.id > 0)
        conditions1 &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        station_indicators_rows = db(conditions1).select(db.station_indicator.ALL)
        indicators = db(db.indicators.id > 0).select(db.indicators.ALL)
        data_lastest_rows = db(db.data_lastest.id > 0).select(db.data_lastest.ALL)
        for row in rows:
            station_id = str(row.id)
            if row.status in new_group:
                row.status = const.STATION_STATUS['GOOD']['value']
            s = str(row.status)
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
                'province_name': provinces[row.province_id]['province_name'] if provinces.has_key(
                    row.province_id) else '',
                'status_disp': station_status[s]['name'] if station_status.has_key(s) else '',
                'parameters': []
            }
            station_indicators = common.get_indicators_by_station_id(station_indicators_rows, indicators, station_id)
            latest_data = common.get_data_lastest_by_station_id(data_lastest_rows, station_id)
            idx = 0
            si_dict = common.get_station_indicator_by_station_2(station_indicators_rows, station_id)
            for row2 in station_indicators:
                idx += 1
                v = 0
                if latest_data.has_key(row2.indicator):
                    try:
                        v = float(latest_data[row2.indicator])
                    except:
                        v = 0
                parameter = {
                    'id': str(row2.id),
                    'key': row2.indicator,
                    'value': '%0.2f' % v,
                    'unit': row2.unit,
                    'color': common.getColorByIndicator(si_dict, str(row2.id), v),
                    'exceed_value': si_dict[str(row2.id)]['exceed_value'],
                }
                station['parameters'].append(parameter)

            stations.append(station)

    json_stations = json.dumps(stations)

    # Group by station type
    station_group_by_type = dict()
    for row in rows:
        st = str(row.station_type)
        if row.status in new_group:
            row.status = const.STATION_STATUS['GOOD']['value']
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
            'status_disp': station_status[s]['name'] if station_status.has_key(s) else ''
        }
        station_group_by_type[st].append(item)
    default_provinces = db(db.provinces.default == 1).select()
    areas = get_all_records_for_area('areas');
    json_area = json.dumps(areas)
    json_provinces = json.dumps(provinces)
    return dict(station_group_by_type=station_group_by_type, json_stations=json_stations, provinces=provinces,
                station_status=station_status, json_station_status=json_station_status,
                json_indicators=json_indicators, areas=areas, json_area=json_area, json_provinces=json_provinces,
                stations=stations, record=record, total_station=total_station, default_provinces=default_provinces)


def map_public():
    station_status2 = get_station_status()
    new_group = [const.STATION_STATUS['TENDENCY']['value'], const.STATION_STATUS['PREPARING']['value']]
    total_group = 0
    station_status = {}
    for idx in station_status2:
        status = station_status2[idx]
        conditions = (db.stations.status == status['value'])
        num = db(conditions).count(db.stations.id)
        if status['value'] not in new_group:
            status['num'] = num
            station_status[idx] = status
        else:
            total_group += num
    for idx in station_status:
        status = station_status[idx]
        if status['value'] == const.STATION_STATUS['GOOD']['value']:
            if status['num']:
                status['num'] += total_group
            else:
                status['num'] = total_group

    json_station_status = json.dumps(station_status)
    conditions = (db.stations.id > 0)
    rows = db(conditions).select(db.stations.ALL, orderby=db.stations.order_no)
    total_station = len(rows)
    stations = []

    return dict(station_group_by_type=[], json_stations=[], provinces=[],
                station_status=[], json_station_status=json_station_status,
                json_indicators=[], areas=[], json_area=[], json_provinces=[],
                stations=stations, total_station=total_station, default_provinces=[])


################################################################################
@service.json
def get_station_for_map(*args, **kwargs):
    if request.vars.dsp_start:
        dsp_start = int(request.vars.dsp_start)
    else:
        dsp_start = 0
    if request.vars.dsp_len:
        dsp_len = int(request.vars.dsp_len)
    else:
        dsp_len = dsp_start + 10

    station_codes = []
    if request.vars.station_codes:
        station_codes = request.vars.station_codes.split(",")
    else:
        station_codes = []

    limitby = (dsp_start, dsp_len)
    station_status = get_station_status()
    provinces = common.get_province_have_station()
    conditions = (db.stations.id > 0)
    if request.vars.station_codes:
        conditions &= (db.stations.station_code.belongs(station_codes))
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))

    station_id = request.vars.station_id
    new_group = [const.STATION_STATUS['TENDENCY']['value'], const.STATION_STATUS['PREPARING']['value']]
    if station_id:
        conditions &= (db.stations.id == station_id)
        limitby = [0, 1]
    rows = db(conditions).select(db.stations.ALL, limitby=limitby, orderby=db.stations.order_no)
    station_ids = []
    for row in rows:
        station_ids.append(str(row.id))
    conditions = (db.station_indicator.id > 0)
    conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    conditions &= (db.station_indicator.station_id.belongs(station_ids))
    station_indicators_rows = db(conditions).select(db.station_indicator.ALL)
    indicator_ids = []
    for row in station_indicators_rows:
        indicator_ids.append(row.indicator_id)
    conditions = (db.indicators.id > 0)
    # conditions &= (db.indicators.id.belongs(station_ids))
    indicators = db(conditions).select(db.indicators.ALL)
    conditions = (db.data_lastest.id > 0)
    conditions &= (db.data_lastest.station_id.belongs(station_ids))
    data_lastest_rows = db(conditions).select(db.data_lastest.ALL)
    stations = []
    for row in rows:
        station_id = str(row.id)
        if row.status in new_group:
            row.status = const.STATION_STATUS['GOOD']['value']
        s = str(row.status)
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
            'province_name': provinces[row.province_id]['province_name'] if provinces.has_key(row.province_id) else '',
            'status_disp': station_status[s]['name'] if station_status.has_key(s) else '',
            'parameters': []
        }
        station_indicators = common.get_indicators_by_station_id(station_indicators_rows, indicators, station_id)
        latest_data = common.get_data_lastest_by_station_id(data_lastest_rows, station_id)
        data_status = common.get_data_status_by_station_id(data_lastest_rows, station_id)
        idx = 0
        si_dict = common.get_station_indicator_by_station_2(station_indicators_rows, station_id)
        for row2 in station_indicators:
            is_exceed = True
            cmax = 0
            cmin = 0
            if data_status.has_key(row2.indicator):
                # try:
                cmax = data_status[row2.indicator]['station_qcvn_max']
                cmin = data_status[row2.indicator]['station_qcvn_min']
                is_exceed = data_status[row2.indicator]['is_exceed']
                # except:
                #     cmax = 0
                #     cmin = 0
                #     is_exceed = True
            idx += 1
            v = 0
            if latest_data.has_key(row2.indicator):
                try:
                    v = float(latest_data[row2.indicator])
                except:
                    v = 0
            parameter = {
                'id': str(row2.id),
                'key': row2.indicator,
                'value': common.convert_data(v),
                'unit': row2.unit,
                'color': common.getColorByIsExceed(is_exceed),
                # 'exceed_value': si_dict[str(row2.id)]['exceed_value'],
                'cmax': cmax,
                'cmin': cmin
            }
            station['parameters'].append(parameter)

        stations.append(station)
    return dict(success=True, data=stations, dsp_next=dsp_start + 10)


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'datalogger')) or (auth.has_permission('view', 'manager_station_type')))
def get_chart_for_station(*args, **kwargs):
    try:
        station_id = request.vars.stationId
        charts = dict()
        import random
        indicators = get_all_records('indicators')
        idx = 0
        chart = dict()
        chart['title'] = dict(text='<b>Formosa Hà Tĩnh</b>')
        chart['chart'] = {'height': 500}
        chart['subtitle'] = {'text': 'Quality index in xx days'}
        chart['xAxis'] = {'categories': range(1, 100)}
        chart['series'] = []
        for key in indicators:
            indicator = indicators[key]
            idx += 1
            if idx > 5:  # Todo: Remove hardcord for prod
                break
            data = []
            for j in range(0, 100):
                x = j
                y = random.randint(8, 10) * idx
                data.append([x, y])
            chart['series'].append({
                'name': '%s(%s)' % (indicator['indicator'], indicator['unit']),
                'data': data,
            })
        charts['all'] = chart
        return dict(success=True, charts=charts)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'datalogger')) or (auth.has_permission('view', 'manager_station_type')))
def get_chart_for_station2(*args, **kwargs):
    try:
        station_id = request.vars.stationId
        charts = dict()
        import random
        for i in range(1, 5):
            chart = dict()
            chart['title'] = dict(text='<b>Cái Đá</b>')
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
                'data': data,
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
            charts['index2_%s' % i] = chart
        return dict(success=True, charts=charts)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def search_on_map(*args, **kwargs):
    try:
        area_id = request.vars.area_id
        province_id = request.vars.province_id
        station_name = request.vars.station_name
        conditions = (db.stations.id > 0)
        if station_name:
            conditions &= (db.stations.station_name.contains(station_name))
        if area_id:
            conditions &= (db.stations.area_id == area_id)
        if province_id:
            conditions &= (db.stations.province_id == province_id)
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        rows = db(conditions).select(db.stations.id)
        ids = []
        for row in rows:
            ids.append(str(row.id))
        return dict(success=True, ids=ids)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'datalogger')) or (auth.has_permission('view', 'manager_station_type')))
def get_list_station(*args, **kwargs):
    try:
        station_type = request.vars.station_type or 0
        sometext = request.vars.sometext
        province_id = request.vars.province_id
        area_id = request.vars.area_id
        station_id = request.vars.station_id
        aaData = []

        conditions = (db.stations.id > 0)
        if station_type:
            conditions &= (db.stations.station_type == station_type)
        if province_id:
            conditions &= (db.stations.province_id == province_id)
        if area_id:
            conditions &= (db.stations.area_id == area_id)
        if station_id:
            conditions &= (db.stations.id == station_id)
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        list_data = db(conditions).select(db.stations.id,
                                          db.stations.station_name,
                                          db.stations.status,
                                          db.stations.off_time)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = len(list_data)

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            sStatus = common.get_station_status_by(station_status_dic, item.status, 'name')
            sColor = common.get_station_status_by(station_status_dic, item.status, 'color')
            off_text = ''
            if item.status == const.STATION_STATUS['OFFLINE']['value']:
                # off_text = '(%s)' %(item.off_time.strftime('%d-%m-%Y %H:%M')) if item.off_time else '1111'
                off_text = '(%s)' % (item.off_time.strftime(datetime_format_vn)) if item.off_time else ''
            aaData.append([
                # str(i+1),
                XML(item.station_name) + SPAN(off_text, _class='off_text'),
                SPAN(sStatus, _style="color: %s" % sColor),
                str(item.id)
            ])

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
# @service.json
# def get_load_station_graph(*args, **kwargs):
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def get_load_station_graph():
    try:
        station_id = request.vars.station_id
        show_by = request.vars.show_by

        LOAD('load_import', 'graph_detail', args=[station_id, show_by], target='graph_detail')
        print
        request.function
        print
        request.action

        return dict(success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
@service.json
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
            row = [str(i + 1), 'Tram khi thai %s' % i, T('LBL_DANG_HOAT_DONG')]
            rows.append(row)
        return dict(iTotalRecords=total_records, iTotalDisplayRecords=total_records, aaData=rows, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def link_area_to_station(*args, **kwargs):
    try:
        areaId = request.vars.areaId
        stationIds = request.vars.stationId.split(',')
        db(db.stations.id.belongs(stationIds)).update(area_id=areaId)
        return dict(success=True)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
# @decor.requires_login()
# @decor.requires_permission('sms|master|customers|list')
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def popup_picklist():
    table = request.vars.table
    field = request.vars.field
    extend = request.vars.extend
    return dict(table=table, field=field, extend=extend)


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def get_list_for_popup_picklist(*args, **kwargs):
    try:
        aaData = []  # Du lieu json se tra ve

        station_type = request.vars.station_type or const.STATION_TYPE['WASTE_WATER']['value']
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        s_search = request.vars.sSearch2  # Chuoi tim kiem nhap tu form
        aaData = []  # Du lieu json se tra ve
        list_data = None  # Du lieu truy van duoc
        iTotalRecords = 0  # Tong so ban ghi
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        # Thu tu ban ghi
        idx = iDisplayStart + 1
        conditions = db.stations.id > 0
        if station_type:
            conditions &= (db.stations.station_type == station_type)
        if request.vars.province_id:
            conditions &= (db.stations.province_id == request.vars.province_id)
        if s_search:
            conditions &= ((db.stations.station_code.contains(s_search)) |
                           (db.stations.station_name.contains(s_search)))

        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))

        list_data = db(conditions).select(db.stations.id, db.stations.station_code, db.stations.station_name,
                                          limitby=limitby
                                          )
        iTotalRecords = db(conditions).count(db.stations.id)
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            listA = [
                idx,
                item.station_code,
                item.station_name,
                INPUT(_name='select_item', _class='select_item', _type='checkbox', _value=item.id,
                      data=dict(value=item.id, display=item.station_name)),
                str(item.id)
            ]
            aaData.append(listA)
            idx += 1
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=ex.message, success=False)


################################################################################
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def popup_adjust():
    station_id = request.vars.station_id
    indicator_id = request.vars.indicator
    from_time = request.vars.from_time
    to_time = request.vars.to_time
    indicator = db.indicators(indicator_id)
    conditions = (db.station_indicator.id > 0)
    conditions &= (db.station_indicator.station_id == station_id)
    conditions &= (db.station_indicator.indicator_id == indicator_id)
    conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    station_indicator = db(conditions).select(db.station_indicator.exceed_value, db.station_indicator.unit,
                                              limitby=(0, 1)).first()
    exceed_value = T('N/A')
    unit = T('N/A')
    if station_indicator:
        exceed_value = station_indicator.exceed_value
        unit = station_indicator.unit
    else:
        indicator = db.indicators(indicator_id)
        if indicator:
            exceed_value = indicator.exceed_value
            unit = indicator.unit
    return dict(station_id=station_id, indicator=indicator, from_time=from_time, to_time=to_time,
                exceed_value=exceed_value, unit=unit)


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def get_data_popup_adjust(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        indicator_id = request.vars.indicator
        from_time = request.vars.from_time
        to_time = request.vars.to_time
        rec = db.indicators(indicator_id)
        indicator = rec.indicator

        aaData, aaData2 = [], []

        format = '%d/%m/%Y %H:%M'
        # format = '%d/%m/%Y'
        from_time = datetime.strptime(from_time, format)
        to_time = datetime.strptime(to_time, format)

        # Get indicator's data from "data_min" table
        items = db((db.data_min.station_id == station_id) &
                   (db.data_min.get_time >= from_time) &
                   (db.data_min.get_time <= to_time)).select(db.data_min.ALL, orderby=~db.data_min.get_time)
        idx = 0
        row = []
        for item in items:
            if not row:
                idx += 1
                row = [idx]
            if item.data.has_key(indicator):
                try:
                    v = float(item.data[indicator])
                except:
                    v = '-'
                row.append(SPAN(item.get_time.strftime(format), _class="adjust_time"))
                html = INPUT(_type="hidden", _name="record_id", _value=item.id) + \
                       INPUT(_type="hidden", _name="current_value", _value=v) + \
                       INPUT(_name="adjust_value", _class="form-control adjust-control", value="%s" % v,
                             data=dict(id=item.id))
                row.append(html)
            if len(row) == 7:
                aaData.append(row)
                row = []
        if row:
            while len(row) < 7:
                row.append('')
                row.append('')
            aaData.append(row)

        return dict(iTotalRecords=idx, iTotalDisplayRecords=idx, success=True, aaData=aaData)
    except Exception, ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(
    lambda: (auth.has_permission('view', 'stations')) or (auth.has_permission('view', 'manager_station_type')))
def ajax_save_adjust(*args, **kwargs):
    try:
        indicator = request.vars.indicator
        record_ids = request.vars.record_id
        if not record_ids:
            return dict(success=True)
        current_values = request.vars.current_value
        adjust_values = request.vars.adjust_value
        total = len(record_ids)
        for i in range(0, total):
            try:
                old_value = float(current_values[i])
            except:
                old_value = None
            try:
                new_value = float(adjust_values[i])
            except:
                new_value = None
            if old_value != new_value:  # Todo: Add 'or True' this line in order to save all
                rec = db.data_min(record_ids[i]) or None
                if rec:
                    conditions = (db.data_adjust.station_id == rec.station_id)
                    conditions &= (db.data_adjust.get_time == rec.get_time)
                    rec2 = db(conditions).select(db.data_adjust.ALL).first()
                    data2 = dict()
                    if rec2:
                        data2 = rec2.data
                    data2[indicator] = new_value
                    db.data_adjust.update_or_insert(conditions, station_id=rec.station_id, get_time=rec.get_time,
                                                    data=data2)
        return dict(success=True)
    except Exception, ex:
        return dict(message=str(ex), success=False)


################################################################################
def call():
    return service()
