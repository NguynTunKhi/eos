# -*- coding: utf-8 -*-
###############################################################################
# Author :
# Date   :
#
# Description :
#
###############################################################################
from applications.eos.modules import common, const
from datetime import datetime, timedelta
import json
from gluon.tools import prettydate

T.force('vn-vi')


def call():
    return service()


def get_station_status():
    ret = dict()
    for idx, value in enumerate(station_status_value):
        ret[str(value)] = {'value': value, 'name': str(station_status_disp[idx]), 'color': station_status_color[idx]}
    return ret


def get_all_records(table):
    ret = dict()
    rows = db(db[table].id > 0).select(db[table].ALL)
    for row in rows:
        ret[str(row.id)] = row.as_dict()
    return ret


################################################################################


def get_indicators_by_station_ids(ids, indicators=None):
    if indicators is None:
        indicators = get_all_records('indicators')
    condition_indicator = (db.station_indicator.station_id.belongs(ids)) & (
        db.station_indicator.is_public == True) & (
                              db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    rows = db(condition_indicator).select(db.station_indicator.indicator_id,
                                           db.station_indicator.station_id,
                                           distinct=True)
    rs = dict()
    for r in rows:
        if not rs.has_key(r.station_id):
            rs[r.station_id] = []
        if indicators.has_key(r.indicator_id):
            rs[r.station_id].append(indicators[r.indicator_id])
    return rs


def set_where_tb_table(tb, conds, station_id, qi_time):
    cons = db[tb].station_id == station_id
    cons &= db[tb].get_time == qi_time
    if conds is None:
        conds = cons
    else:
        conds |= cons
    return conds


def get_data_by_conds(conds, tb):
    rs = dict()
    if conds is not None:
        rows_tm = db(conds).select(
            db[tb].get_time,
            db[tb].station_id,
            db[tb].data,
            orderby=~db[tb].get_time
        )
        for r in rows_tm:
            rs[r.station_id] = r
    return rs


def data_lastest_to_dic_by(station_ids):
    # Lay du lieu moi nhat
    data_rows = db(db.data_lastest.station_id.belongs(station_ids)).select(db.data_lastest.data,
                                                                           db.data_lastest.station_id,
                                                                           orderby=~db.data_lastest.get_time
                                                                           )
    data_dic = dict()
    for r in data_rows:
        data_dic[r.station_id] = r.data
    return data_dic
###############################################################################
@service.json
def history_aqi(*args, **kwargs):
  conditions = (db.data_hour_status_history.id > 0)
  time = request.vars.time
  if time:
    datetime_object = datetime.strptime(time, '%Y/%m/%d %H:%M')
    conditions &= (db.data_hour_status_history.time == datetime_object)
  # eip_config = db(db.eip_config.name == 'eip_config').select().first()
  # try:
  #   p_now = datetime.now() - timedelta(hours=eip_config.time_public)
  # except:
  #   p_now = datetime.now() - timedelta(hours=3)
  rows = db(conditions).select(db.data_hour_status_history.ALL)
  rows = rows[0]['data']
  stations = []
  dt_format = '%H:%M %d/%m/%Y'
  for key in rows:
    if rows[key]['station_type'] == 4 and rows[key]['is_public'] == True:
      if rows[key]['status'] == const.STATION_STATUS['OFFLINE']['value']:
        s = const.STATION_STATUS['OFFLINE']['value']
      else:
        s = const.STATION_STATUS['GOOD']['value']
      station = {
        'station_id' : key,
        'station_type': rows[key]['station_type'],
        'station_name': rows[key]['station_name'],
        'station_code' : '',
        'province_id': rows[key]['province_id'],
        'area_id': rows[key]['area_id'],
        'address': rows[key]['address'],
        'status': rows[key]['status'],
        'lonlat': [rows[key]['longitude'], rows[key]['latitude']],
        'province_name': '',
        'status_disp': const.STATION_STATUS['OFFLINE']['name'] if (
                s == const.STATION_STATUS['OFFLINE']['value']) else const.STATION_STATUS['GOOD']['name'],
        # 'index': random.randint(30, 450),
        'index': round(rows[key]['qi']) if rows[key]['qi'] is not None and rows[key]['qi'] else '-',
        'bgColor': '#0FF0FF',
        'color': '#FFFFFF',
        'status_text': '',
        'parameters': [],
        'qi_time': rows[key]['qi_time'].strftime(dt_format) if rows[key]['qi_time'] else '',
        'qi': rows[key]['qi'],
        'indicator_list': []
      }

      for key in sorted(const.AQI_COLOR):
        if station['index'] <= key:
          station['bgColor'] = const.AQI_COLOR[key]['bgColor']
          station['color'] = const.AQI_COLOR[key]['color']
          station['status_text'] = '(' + const.AQI_COLOR[key]['text'] + ')'
          break

      stations.append(station)


  json_stations = json.dumps(stations)

  return dict(json_stations=json_stations, success=True)
###############################################################################
def index():
    eip_config = db(db.eip_config.name == 'eip_config').select().first()
    try:
        p_now = datetime.now() - timedelta(hours=eip_config.time_public)
    except:
        p_now = datetime.now() - timedelta(hours=3)
    data = db(db.manager_owner_information.id > 0).select().first()
    session.ownerName = unicode(data.name, "utf-8")
    session.ownerDivision = unicode(data.division, "utf-8")
    import random
    station_status = get_station_status()
    provinces = common.get_province_have_station()
    for idx in station_status:
        status = station_status[idx]
        conditions = (db.stations.status == status['value'])
        status['num'] = db(conditions).count(db.stations.id)
        station_status[idx] = status
    json_station_status = json.dumps(station_status)
    indicators = get_all_records('indicators')
    json_indicators = json.dumps(indicators)
    index_items = const.AQI_COLOR
    for k in index_items:
        index_items[k]['text'] = str(T(index_items[k]['text']))
    index_items = json.dumps(index_items)
    # Wqi
    index_items_wqi = const.WQI_COLOR
    for k in index_items_wqi:
        index_items_wqi[k]['text'] = str(T(index_items_wqi[k]['text']))
    index_items_wqi = json.dumps(index_items_wqi)

    conditions = (db.stations.id > 0)
    # conditions &= (db.stations.is_qi == True)
    conditions &= (db.stations.is_public == True)

    # conditions = ((db.stations.id > 0) & (db.stations.is_public == True) & (db.stations.qi_time > p_now))
    # conditions |= ((db.stations.id > 0) & (db.stations.is_public == True) & (db.stations.qi_adjsut_time > p_now))

    # Get all
    rows = db(conditions).select(db.stations.ALL)

    stations = []
    dt_format = '%H:%M %d/%m/%Y'
    dt_format2 = '%H:%M %d/%m'
    aqi_conds = None
    aqi_adj_conds = None
    wqi_conds = None
    wqi_adj_conds = None
    station_ids = []
    # duyet dieu kien
    for r in rows:
        station_id = str(r.id)

        try:
          is_public_data_type = r.is_public_data_type
        except:
          is_public_data_type = 2
        if r.station_type == 4:
            if is_public_data_type == 3:
                if not r.qi_time or r.qi_time < p_now:
                    continue
                aqi_conds = set_where_tb_table('aqi_data_hour', aqi_conds, station_id, r.qi_time)
            else:
                if not r.qi_adjsut_time or r.qi_adjsut_time < p_now:
                    continue
                aqi_adj_conds = set_where_tb_table('aqi_data_adjust_hour', aqi_adj_conds, station_id, r.qi_adjsut_time)
        else:
            if is_public_data_type == 3:
                wqi_conds = set_where_tb_table('wqi_data_hour', wqi_conds, station_id, r.qi_time)
            else:
                wqi_adj_conds = set_where_tb_table('wqi_data_adjust_hour', wqi_adj_conds, station_id, r.qi_adjsut_time)
    station_ids.append(station_id)

    # Get data AQI & WQI
    aqi_dic = get_data_by_conds(aqi_conds, 'aqi_data_hour')
    aqi_adj_dic = get_data_by_conds(aqi_adj_conds, 'aqi_data_adjust_hour')
    wqi_dic = get_data_by_conds(wqi_conds, 'wqi_data_hour')
    wqi_adj_dic = get_data_by_conds(wqi_adj_conds, 'wqi_data_adjust_hour')

    # Lay du lieu moi nhat
    data_dic = data_lastest_to_dic_by(station_ids)

    # lay danh sach thong so thuoc station
    station_indicator_dic = get_indicators_by_station_ids(station_ids, indicators)
    for row in rows:
        qi_time = ''
        station_id = str(row.id)
        try:
            is_public_data_type = row.is_public_data_type
        except:
            is_public_data_type = 2
        if row.status == const.STATION_STATUS['OFFLINE']['value']:
            s = const.STATION_STATUS['OFFLINE']['value']
        else:
            s = const.STATION_STATUS['GOOD']['value']
        # s = str(row.status)

        qi_value = None
        if row.station_type == 4:
            if is_public_data_type == 3:
                if not row.qi_time or row.qi_time < p_now:
                    continue
                aqis = aqi_dic[station_id] if aqi_dic.has_key(station_id) else dict()
            else:
                if not row.qi_adjsut_time or row.qi_adjsut_time < p_now:
                    continue
                aqis = aqi_adj_dic[station_id] if aqi_adj_dic.has_key(station_id) else dict()

            if aqis.has_key('data'):
                item = aqis.data
                if item.has_key('aqi') and qi_value is None:
                    qi_value = item['aqi']
                if qi_time == '' and aqis.has_key('get_time'):
                    qi_time = aqis.get_time
        else:
            if is_public_data_type == 3:
                wqis = wqi_dic[station_id] if wqi_dic.has_key(station_id) else dict()
            else:
                wqis = wqi_adj_dic[station_id] if wqi_adj_dic.has_key(station_id) else dict()

            if wqis.has_key('data'):
                item = wqis.data
                if qi_value is None and item.has_key('wqi'):
                    qi_value = item.get('wqi')
                if qi_time == '' and wqis.has_key('get_time'):
                    qi_time = wqis.get_time

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
            'province_name': provinces[row['province_id']]['province_name'] if provinces.has_key(
                row['province_id']) else '',
            'status_disp': const.STATION_STATUS['OFFLINE']['name'] if (
                    s == const.STATION_STATUS['OFFLINE']['value']) else const.STATION_STATUS['GOOD']['name'],
            # 'index': random.randint(30, 450),
            'index': round(qi_value) if qi_value is not None and qi_value else '-',
            'bgColor': '#0FF0FF',
            'color': '#FFFFFF',
            'status_text': '',
            'parameters': [],
            'qi_time': qi_time.strftime(dt_format) if qi_time else '',
            'qi': qi_value,
            'indicator_list': []
        }

        if row.station_type == const.STATION_TYPE['AMBIENT_AIR']['value']:
            for key in sorted(const.AQI_COLOR):
                if station['index'] <= key:
                    station['bgColor'] = const.AQI_COLOR[key]['bgColor']
                    station['color'] = const.AQI_COLOR[key]['color']
                    station['status_text'] = '(' + const.AQI_COLOR[key]['text'] + ')'
                    break

        else:
            for key in sorted(const.WQI_COLOR):
                if station['index'] <= key:
                    station['bgColor'] = const.WQI_COLOR[key]['bgColor']
                    station['color'] = const.WQI_COLOR[key]['color']
                    station['status_text'] = const.WQI_COLOR[key]['text']
                    break

        # conditions = (db.station_indicator.station_id == station_id)
        # station_indicators = db(conditions).select(db.station_indicator.ALL)
        # for si in station_indicators:
        # Todo: Remove this hardcode for prod
        idx = 0
        for k in indicators:
            si = indicators[k]
            if si['indicator_type'] != row.station_type:
                continue
            idx += 1
            if idx > 5:
                break
            parameter = {
                'id': si['id'],
                # 'key': indicators[str(si.indicator_id)]['indicator'],
                'key': si['indicator'],
                'value': random.randint(1, 10),  # Todo: Hardcode value
                'unit': si['unit'],
            }
            station['parameters'].append(parameter)

        data_indicaticator_last = data_dic[station_id] if data_dic.has_key(station_id) else []

        if station_indicator_dic.has_key(station_id):
            indicators2 = station_indicator_dic[station_id]
            for indicator in indicators2:
                indicator_label = indicator.get('indicator')
                if data_indicaticator_last.has_key(indicator_label):
                    if data_indicaticator_last[indicator_label] != 'NULL':
                        # indicator_label = "<span style='color: #149C20'>" + indicator_label + "</span>"
                        parameter = {
                            'value': indicator_label,
                            'color': '#149C20',
                        }
                    else:
                        # indicator_label = "<span style='color: #C5C5C5'>" + indicator_label + "</span>"
                        parameter = {
                            'value': indicator_label,
                            'color': '#C5C5C5',
                        }

                    if row.status == const.STATION_STATUS['OFFLINE']['value']:
                        indicator_label = indicator['indicator']
                        # indicator_label = "<span style='color: #C5C5C5'>" + indicator_label + "</span>"
                        parameter = {
                            'value': indicator_label,
                            'color': '#C5C5C5',
                        }

                # if (indicator_list_code == '-'):
                #     indicator_list_code = indicator_label
                # else:
                #     indicator_list_code = indicator_list_code + ', ' + indicator_label

                # station['indicator_list'] = indicator_list_code
                station['indicator_list'].append(parameter)

        stations.append(station)
    json_stations = json.dumps(stations)
    # Group by station type
    rows = db(db.stations.is_public == True).select(db.stations.ALL, orderby=db.stations.station_type | db.stations.station_name)
    station_group_by_type = dict()
    ids1, ids2 = [], []
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
            'status_disp': station_status[s]['name'] if station_status.has_key(s) else ''
        }
        station_group_by_type[st].append(item)
        if row.station_type == const.STATION_TYPE['AMBIENT_AIR']['value']:
            ids1.append(str(row.id))
        if row.station_type == const.STATION_TYPE['STACK_EMISSION']['value']:
            ids2.append(str(row.id))

    areas = [] #get_all_records('areas')

    # Nuoc thai
    province_with_station_type_0 = common.get_province_have_station_with_station_type(0)
    province_have_station = dict()
    for province in provinces:
        if province_with_station_type_0.has_key(str(province)):
            if not province_have_station.has_key(province):
                province_have_station[province] = []
            item_province = {
                'id': str(province),
                'province_name': provinces[province]['province_name'],
                'count_stations': province_with_station_type_0[province]
            }
            province_have_station[province].append(item_province)

    json_area = json.dumps(areas)
    json_provinces = json.dumps(provinces)
    #json_province_with_station_type_0 = json.dumps(province_with_station_type_0)
    # conditions1 = (db.station_indicator.station_id.belongs(ids1))
    # conditions1 &= (db.station_indicator.is_public == True)
    # total_ambient_air = db(conditions1).count(db.station_indicator.id)
    # conditions2 = (db.station_indicator.station_id.belongs(ids2))
    # conditions2 &= (db.station_indicator.is_public == True)
    # total_stack_emission = db(conditions2).count(db.station_indicator.id)
    eip_faq = db(db.eip_faq.id > 0).select(db.eip_faq.ALL).first()

    return dict(json_stations=json_stations, provinces=provinces,
                station_status=station_status, json_station_status=json_station_status,
                json_indicators=json_indicators, json_area=json_area, json_provinces=json_provinces,
                stations=stations, areas=areas, index_items=index_items, index_items_wqi=index_items_wqi,
                eip_config=eip_config,
                json_province_with_station_type_0=[],
                province_have_station=province_have_station,
                eip_faq=eip_faq)

################################################################################
@service.json
def get_aqi_data(*args, **kwargs):
    try:
        date = request.vars.date
        aqi_type = int(request.vars.aqi_type)
        station_id = request.vars.station_id
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1)

        station = db.stations(station_id) or None
        station_type = 1
        dt = datetime.now()
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        if not station:
            return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message="Not found!", success=True)
        station_type = station.station_type

        try:
            is_public_data_type = station.is_public_data_type
        except:
            is_public_data_type = 2

        added_columns = request.vars.added_columns or ''
        if added_columns:
            added_columns = added_columns.split(',')

        # Lay du lieu AQI hour
        from_day = request.now
        if aqi_type == 1:
            # if date :
            #     from_day = request.now - timedelta(hours=25)

            if int(station_type) == 1:
                if is_public_data_type == 3:
                    last_record = db(db.wqi_data_hour.station_id == station_id).select().last() or None

                    conditions = (db.wqi_data_hour.station_id == station_id)
                    if date and last_record is not None:
                        from_day = last_record.get_time - timedelta(hours=25)
                        conditions &= (db.wqi_data_hour.get_time >= from_day)
                    aqi_hours = db(conditions).select(db.wqi_data_hour.ALL, orderby=~db.wqi_data_hour.get_time,
                                                      limitby=limitby)
                else:
                    last_record = db(db.wqi_data_adjust_hour.station_id == station_id).select().last() or None

                    conditions = (db.wqi_data_adjust_hour.station_id == station_id)
                    if date and last_record is not None:
                        from_day = last_record.get_time - timedelta(hours=25)
                        conditions &= (db.wqi_data_adjust_hour.get_time >= from_day)
                    aqi_hours = db(conditions).select(db.wqi_data_adjust_hour.ALL,
                                                      orderby=~db.wqi_data_adjust_hour.get_time,
                                                      limitby=limitby)
            else:
                if is_public_data_type == 3:
                    last_record = db(db.aqi_data_hour.station_id == station_id).select().last() or None

                    conditions = (db.aqi_data_hour.station_id == station_id)
                    if date and last_record is not None:
                        from_day = last_record.get_time - timedelta(hours=25)
                        conditions &= (db.aqi_data_hour.get_time >= from_day)
                    aqi_hours = db(conditions).select(db.aqi_data_hour.ALL, orderby=~db.aqi_data_hour.get_time,
                                                      limitby=limitby)
                else:
                    last_record = db(db.aqi_data_adjust_hour.station_id == station_id).select().last() or None

                    conditions = (db.aqi_data_adjust_hour.station_id == station_id)
                    if date and last_record is not None:
                        from_day = last_record.get_time - timedelta(hours=25)
                        conditions &= (db.aqi_data_adjust_hour.get_time >= from_day)
                    aqi_hours = db(conditions).select(db.aqi_data_adjust_hour.ALL,
                                                      orderby=~db.aqi_data_adjust_hour.get_time,
                                                      limitby=limitby)

            aaData = []
            iTotalRecords = db(conditions).count()

            # get dict ('indicator_id' : indicator_name)
            indicators_dict = common.get_indicator_dict()

            # Lay nhung indicator duoc public
            conditions = (db.station_indicator.station_id == station_id)
            conditions &= (db.station_indicator.is_public == True)
            indicators_public = db(conditions).select(db.station_indicator.indicator_id)
            indicators = [indicators_dict.get(item.indicator_id) for item in indicators_public]

            for i, item in enumerate(aqi_hours):
                qi = '-'

                if int(station_type) == 1:
                    if item.data.has_key('wqi'):
                        qi = "{0:.0f}".format(item.data['wqi']) if item.data['wqi'] else '-'
                else:
                    if item.data.has_key('aqi'):
                        qi = "{0:.0f}".format(item.data['aqi']) if item.data['aqi'] else '-'

                row = [
                    str(iDisplayStart + 1 + i),
                    item.get_time.strftime('%d/%m/%Y %H:%M') if item.get_time else '-',
                    qi,
                ]

                added_item = dict()
                # if item.data:
                if indicators:
                    for data_key in sorted(indicators):
                        i_name = str(data_key)
                        v = ''
                        v = item.data[i_name] if item.data.has_key(i_name) else ''
                        if not v:
                            added_item[i_name] = '-'
                        else:
                            v = float(v)
                            added_item[i_name] = "{0:.0f}".format(v)
                for column in sorted(indicators):
                    if column and added_item.has_key(column):
                        if added_item[column] != '-':
                            row.append(added_item[column])
                        # TODO
                        # if (column == 'PM-2-5'):
                        #     column = 'PM-2.5'
                        # if (column in ['O3', 'CO', 'PM-2-5', 'PM-10', 'NO2']) :
                        # if added_item[column] == '-':
                        else:
                            row.append(added_item[column])
                aaData.append(row)
        else:
            # if date :
            #     from_day = request.now - timedelta(days=int(date))

            aaData = []
            iTotalRecords = 0

            if int(station_type) == 4:
                if is_public_data_type == 3:
                    last_record = db(db.aqi_data_24h.station_id == station_id).select().last() or None

                    conditions = (db.aqi_data_24h.station_id == station_id)
                    conditions &= (db.aqi_data_24h.get_time < dt)
                    if date and (last_record != None):
                        from_day = last_record.get_time - timedelta(days=int(date))
                        conditions &= (db.aqi_data_24h.get_time >= from_day)
                    aqi = db(conditions).select(db.aqi_data_24h.ALL, orderby=~db.aqi_data_24h.get_time, limitby=limitby)
                else:
                    last_record = db(db.aqi_data_adjust_24h.station_id == station_id).select().last() or None

                    conditions = (db.aqi_data_adjust_24h.station_id == station_id)
                    conditions &= (db.aqi_data_adjust_24h.get_time < dt)
                    if date and (last_record != None):
                        from_day = last_record.get_time - timedelta(days=int(date))
                        conditions &= (db.aqi_data_adjust_24h.get_time >= from_day)
                    aqi = db(conditions).select(db.aqi_data_adjust_24h.ALL, orderby=~db.aqi_data_adjust_24h.get_time,
                                                limitby=limitby)

                iTotalRecords = db(conditions).count()
                # get dict ('indicator_id' : indicator_name)
                indicators_dict = common.get_indicator_dict()

                # Lay nhung indicator duoc public
                conditions = (db.station_indicator.station_id == station_id)
                conditions &= (db.station_indicator.is_public == True)
                indicators_public = db(conditions).select(db.station_indicator.indicator_id)
                indicators = [indicators_dict.get(item.indicator_id) for item in indicators_public]

                for i, item in enumerate(aqi):
                    qi = '-'
                    if item.data_1d.has_key('aqi'):
                        qi = "{0:.0f}".format(item.data_1d['aqi']) if item.data_1d['aqi'] else '-'

                    row = [
                        str(iDisplayStart + 1 + i),
                        item.get_time.strftime('%d/%m/%Y') if item.get_time else '-',
                        qi,
                    ]

                    added_item = dict()
                    if item.data_1d:
                        if indicators:
                            for data_key in sorted(indicators):
                                i_name = str(data_key)
                                v = ''
                                v = item.data_1d[i_name] if item.data_1d.has_key(i_name) else ''
                                if not v:
                                    u = 1
                                    added_item[i_name] = '-'
                                else:
                                    v = float(v)
                                    added_item[i_name] = "{0:.0f}".format(v)
                    for column in sorted(indicators):
                        if column and added_item.has_key(column):
                            if added_item[column] != '-':
                                row.append(added_item[column])
                            # TODO
                            # if (column == 'PM-2-5'):
                            #     column = 'PM-2.5'
                            # if (column in ['O3', 'CO', 'PM-2-5', 'PM-10', 'NO2']) :
                            # if added_item[column] == '-':
                            else:
                                row.append(added_item[column])
                    aaData.append(row)

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, aoColumns=[],
                    success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


###############################################################################
@service.json
def get_chart_for_widget_aqi(*args, **kwargs):
    try:
        chart = dict()
        aqi = ''
        at_time = ''
        at_date = ''
        station_id = request.vars.station_id
        from_public = request.vars.from_public
        station_type = request.vars.station_type
        get_time = datetime.now()

        # Create blank data for chart
        chart['categories'] = []
        station = db.stations(station_id) or None
        chart['title'] = dict(text='<b>%s</b>' % (station.station_name if station else ''))
        chart['chart'] = {'height': 500}
        chart['xAxis'] = {'type': 'datetime', 'dateTimeLabelFormats': {'minute': '%H:%M'}}
        chart['subtitle'] = dict(text='')
        chart['series'] = [dict(data=[])]
        lat = 0
        lon = 0
        if station:
            lon = station.longitude
            lat = station.latitude
            # Get indicator
            try:
                is_public_data_type = station.is_public_data_type
            except:
                is_public_data_type = 2
            conditions = (db.station_indicator.station_id == station_id)
            if from_public:
                conditions &= (db.station_indicator.is_public == True)
            rows2 = db(conditions).select(db.station_indicator.indicator_id, distinct=True)
            indicators_id = []
            for row in rows2:
                indicators_id.append(row.indicator_id)
            indicators = db(db.indicators.id.belongs(indicators_id)).select(db.indicators.indicator)
            # Build data for all indicators
            data = dict()
            # for indicator in indicators:
            #     data[str(indicator.indicator)] = {'value': 0}
            # Get data from db (table aqi_data_hour)
            if is_public_data_type == 3:
                aqi_data_hour = db(db.aqi_data_hour.station_id == station_id).select(db.aqi_data_hour.ALL,
                                                                                     limitby=(0, 2),
                                                                                     orderby=~db.aqi_data_hour.get_time).first()
            else:
                aqi_data_hour = db(db.aqi_data_adjust_hour.station_id == station_id).select(db.aqi_data_adjust_hour.ALL,
                                                                                            limitby=(0, 2),
                                                                                            orderby=~db.aqi_data_adjust_hour.get_time).first()
            if not aqi_data_hour:
                chart['subtitle']['text'] = T('No data found!')
                for k in data:
                    chart['categories'].append(k)
                    chart['series'][0]['data'].append(0)
            else:
                # get_time
                get_time = aqi_data_hour.get_time
                at_time = '%s %s' % (T('Updated time:'), get_time.strftime('%d/%m/%Y %H:%M'))
                at_date = get_time.strftime('%Y-%m-%d')
                data_json = aqi_data_hour.data
                for i in indicators:
                    if data_json.has_key(i.indicator):
                        for k in (data_json):
                            y = float(data_json[k])
                            if (not data.has_key(k)) & (k != 'aqi'):
                                data[str(k)] = {'value': 0}
                            if data.has_key(k):
                                data[k]['value'] = y
                            if k == 'aqi':
                                aqi = int(round(y))

                        for k in sorted(data):
                            chart['categories'].append(k)
                            chart['series'][0]['data'].append(data[k]['value'])
                            # chart['series'][0]['data'].append(0)
        else:
            chart['subtitle']['text'] = T('No data found!')
        try:
            aqi = int(aqi)
            pass
        except Exception as ex:
            aqi = '-'
            pass
        aqi_detail_info = {}
        for key in sorted(const.AQI_COLOR):
            if aqi <= key:
                aqi_detail_info = const.AQI_COLOR[key]
                break

        if int(station_type) == 1:
            aqi = 'wqi'
        return dict(success=True, chart=chart, aqi=aqi, at_time=at_time, at_date=at_date,
                    aqi_detail_info=aqi_detail_info,
                    lat=lat, lon=lon)
    except Exception as ex:
        return dict(success=False, message=str(ex), chart=dict(), aqi='', at_time=at_time, at_date=at_date)


def sortSecond(val):
    return val[1]


################################################################################
@service.json
def get_station_by_conditions(*args, **kwargs):
    try:
        station_type = request.vars.station_type
        longitude_min = False
        longitude_max = False
        latitude_min = False
        latitude_max = False
        find_log = False
        find_lat = False
        provinces = common.get_province_have_station(station_type)

        html = '<option value="">%s</option>' % (T('-- Select an option --'))
        # Get variables from request
        area_id = request.vars.area_id
        province_id = request.vars.province_id
        # station_type = request.vars.station_type
        from_public = request.vars.from_public

        eip_config = db(db.eip_config.name == 'eip_config').select().first()
        try:
            p_now = datetime.now() - timedelta(hours=eip_config.time_public)
        except:
            p_now = datetime.now() - timedelta(hours=3)

        # Create conditions
        conditions = (db.stations.id > 0)
        if area_id:
            conditions &= (db.stations.area_id == area_id)
        if province_id:
            conditions &= (db.stations.province_id == province_id)
        if station_type:
            conditions &= (db.stations.station_type == station_type)
            if int(station_type) == 4 or int(station_type) == 1:
                conditions &= (db.stations.is_qi == True)
        if from_public:
            conditions &= (db.stations.is_public == True)
        # conditions &= (db.stations.is_qi == True)
        # Get data by conditions
        rows = db(conditions).select(db.stations.id, db.stations.station_name,
                                     db.stations.longitude, db.stations.latitude, db.stations.province_id,
                                     db.stations.address,
                                     db.stations.station_type, db.stations.is_public_data_type,
                                     db.stations.status,
                                     db.stations.qi_time,
                                     db.stations.qi_adjsut_time,
                                     orderby=db.stations.order_no)
        aqi_conds = None
        aqi_adj_conds = None
        wqi_conds = None
        wqi_adj_conds = None
        for r in rows:
            station_id = str(r.id)
            try:
                is_public_data_type = r.is_public_data_type
            except:
                is_public_data_type = 2
                if is_public_data_type == 3:
                    if not r.qi_time or r.qi_time < p_now:
                        continue
                    aqi_conds = set_where_tb_table('aqi_data_hour', aqi_conds, station_id, r.qi_time)
                else:
                    if not r.qi_adjsut_time or r.qi_adjsut_time < p_now:
                        continue
                    aqi_adj_conds = set_where_tb_table('aqi_data_adjust_hour', aqi_adj_conds, station_id,
                                                       r.qi_adjsut_time)
            else:
                if is_public_data_type == 3:
                    wqi_conds = set_where_tb_table('wqi_data_hour', wqi_conds, station_id, r.qi_time)
                else:
                    wqi_adj_conds = set_where_tb_table('wqi_data_adjust_hour', wqi_adj_conds, station_id,
                                                       r.qi_adjsut_time)

        # Du lieu AQI & WQI
        aqi_dic = get_data_by_conds(aqi_conds, 'aqi_data_hour')
        aqi_adj_dic = get_data_by_conds(aqi_adj_conds, 'aqi_data_adjust_hour')
        wqi_dic = get_data_by_conds(wqi_conds, 'wqi_data_hour')
        wqi_adj_dic = get_data_by_conds(wqi_adj_conds, 'wqi_data_adjust_hour')

        # Create options from result and append to html
        for row in rows:
            province_name = provinces[row['province_id']]['province_name'] if provinces.has_key(
                row['province_id']) else ''

            station_id = str(row.id)
            try:
                is_public_data_type = row.is_public_data_type
            except:
                is_public_data_type = 2
            s = str(row.status)

            qi_value = ''

            if row.station_type == 4:
                if is_public_data_type == 3:
                    if not row.qi_time or row.qi_time < p_now:
                        continue
                    aqis = aqi_dic[station_id] if aqi_dic.has_key(station_id) else dict()
                else:
                    if not row.qi_adjsut_time or row.qi_adjsut_time < p_now:
                        continue
                    aqis = aqi_adj_dic[station_id] if aqi_adj_dic.has_key(station_id) else dict()

                if aqis.has_key('data'):
                    data = aqis['data']
                    if data.has_key('aqi') and qi_value == '':
                        qi_value = data['aqi']
            else:
                if is_public_data_type == 3:
                    wqis = wqi_dic[station_id] if wqi_dic.has_key(station_id) else dict()
                else:
                    wqis = wqi_adj_dic[station_id] if wqi_adj_dic.has_key(station_id) else dict()

                if wqis.has_key('data'):
                    data = wqis['data']
                    if data.has_key('wqi') and qi_value == '':
                        qi_value = data['wqi']
            html += '<option value="%s" data-id="%s" data-lat="%s" data-lon="%s" data-province="%s" data-address="%s" data-qi_value="%s">%s</option>' \
                    % (station_id, station_id, row.latitude, row.longitude, province_name, row.address, str(qi_value),
                       row.station_name)
            if row.longitude:
                if longitude_min == False:
                    longitude_min = row.longitude
                    longitude_max = row.longitude
                    find_log = True
                else:
                    if longitude_min > row.longitude:
                        longitude_min = row.longitude
                    if longitude_max < row.longitude:
                        longitude_max = row.longitude
            if row.latitude:
                if latitude_min == False:
                    latitude_min = row.latitude
                    latitude_max = row.latitude
                    find_lat = True
                else:
                    if latitude_min > row.latitude:
                        latitude_min = row.latitude
                    if latitude_max < row.latitude:
                        latitude_max = row.latitude
        longitude_average = (longitude_max + longitude_min) / 2 if find_log and find_lat else 105.80
        latitude_average = (latitude_max + latitude_min) / 2 if find_log and find_lat else 17.03
        return dict(success=True, html=html, longitude_average=longitude_average, latitude_average=latitude_average)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
def get_indicators(*args, **kwargs):
    try:
        html = ''
        station_id = request.vars.station_id
        from_public = request.vars.from_public
        conditions = (db.station_indicator.station_id == station_id)
        if from_public:
            conditions &= (db.station_indicator.is_public == True)
        rows = db(conditions).select(db.station_indicator.indicator_id)
        indicators = []
        for row in rows:
            indicators.append(row.indicator_id)
        rows = db(db.indicators.id.belongs(indicators)).select(db.indicators.ALL)
        for row in rows:
            html += '<option value="%(value)s" selected>%(name)s (%(unit)s)</option>' % dict(value=row.indicator,
                                                                                             name=row.indicator,
                                                                                             unit=row.unit)
        return dict(success=True, html=html)
    except Exception as ex:
        return dict(success=False, message=str(ex))


@service.json
def get_indicators_have_data(*args, **kwargs):
    try:
        html = ''
        station_id = request.vars.station_id
        from_public = request.vars.from_public
        station_type = request.vars.station_type
        iDisplayStart = int(0)
        iDisplayLength = int(20)
        conditions = (db.station_indicator.station_id == station_id)
        if from_public:
            conditions &= (db.station_indicator.is_public == True)
        rowsIndicators = db(conditions).select(db.station_indicator.indicator_id)
        indicators = []
        for row in rowsIndicators:
            indicators.append(row.indicator_id)
        rowsIndicators = db(db.indicators.id.belongs(indicators)).select(db.indicators.ALL)
        # print(rowsIndicators)
        # Lay du lieu AQI hour 7 ngay gan nhat
        from_day = request.now - timedelta(days=7)
        station = db.stations(station_id) or None
        try:
            if station:
                is_public_data_type = station.is_public_data_type
        except:
            is_public_data_type = 2

        if int(station_type) == 1:
            if is_public_data_type == 3:
                conditions = (db.wqi_data_hour.station_id == station_id)
                conditions &= (db.wqi_data_hour.get_time >= from_day)
                aqi_hours = db(conditions).select(db.wqi_data_hour.ALL, orderby=~db.wqi_data_hour.get_time)
            else:
                conditions = (db.wqi_data_adjust_hour.station_id == station_id)
                conditions &= (db.wqi_data_adjust_hour.get_time >= from_day)
                aqi_hours = db(conditions).select(db.wqi_data_adjust_hour.ALL,
                                                  orderby=~db.wqi_data_adjust_hour.get_time)
        else:
            if is_public_data_type == 3:
                conditions = (db.aqi_data_hour.station_id == station_id)
                conditions &= (db.aqi_data_hour.get_time >= from_day)
                aqi_hours = db(conditions).select(db.aqi_data_hour.ALL, orderby=~db.aqi_data_hour.get_time)
            else:
                conditions = (db.aqi_data_adjust_hour.station_id == station_id)
                conditions &= (db.aqi_data_adjust_hour.get_time >= from_day)
                aqi_hours = db(conditions).select(db.aqi_data_adjust_hour.ALL,
                                                  orderby=~db.aqi_data_adjust_hour.get_time)

        aaData = []
        iTotalRecords = db(conditions).count()

        # get dict ('indicator_id' : indicator_name)
        indicators_dict = common.get_indicator_dict()

        # Lay nhung indicator duoc public
        conditions = (db.station_indicator.station_id == station_id)
        conditions &= (db.station_indicator.is_public == True)
        indicators_public = db(conditions).select(db.station_indicator.indicator_id)
        indicators = [indicators_dict.get(item.indicator_id) for item in indicators_public]

        if aqi_hours:

            iRow = 1
            rowHeader = [
                T('LBL_STT'),
                T('Datetime'),
                T('AQI hour'),
            ]
            columnShow = dict()
            for i, item in enumerate(aqi_hours):
                qi = '0'

                if int(station_type) == 1:
                    if item.data.has_key('wqi'):
                        qi = "{0:.0f}".format(item.data['wqi']) if item.data['wqi'] else '0'
                else:
                    if item.data.has_key('aqi'):
                        qi = "{0:.0f}".format(item.data['aqi']) if item.data['aqi'] else '0'

                row = [
                    str(iDisplayStart + 1 + i),
                    item.get_time,
                    qi
                ]

                added_item = dict()
                if item.data:
                    if indicators:
                        for data_key in sorted(indicators):
                            i_name = str(data_key)
                            v = ''
                            v = item.data[i_name] if item.data.has_key(i_name) else ''
                            if not v:
                                u = 1
                                # added_item[i_name] = '-'
                            else:
                                v = float(v)
                                added_item[i_name] = "{0:.0f}".format(v)
                for column in sorted(indicators):
                    try:
                        if column:
                            # if column and added_item.has_key(column):
                            # if (column == 'PM-2-5') :
                            #     column = 'PM-2.5'

                            # if added_item[column] != '-':
                            if iRow == 1:
                                # Write header
                                # print(column)
                                columnShow[column] = column
                                rowHeader.append(column)
                            row.append(added_item[column])
                    except Exception as ex:
                        excep = [ex]
                    finally:
                        pass
                iRow += 1

            # for i, indicator in enumerate(rowHeader):
            #     ws[chr(ord('A') + i) + '1'] = indicator.upper()

            for rowColumnShow in sorted(columnShow):
                # print(rowColumnShow)
                for row in rowsIndicators:
                    if rowColumnShow == row.indicator:
                        indicatorShow = row.indicator
                        # if (rowColumnShow == 'PM-2-5'):
                        # indicatorShow = 'PM-2.5'
                        html += '<option value="%(value)s" selected>%(name)s</option>' % dict(value=row.indicator,
                                                                                              name=indicatorShow)

        return dict(success=True, html=html)
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
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
        rows = db(conditions).select(db.stations.id)
        ids = []
        for row in rows:
            ids.append(str(row.id))
        return dict(success=True, ids=ids)
    except Exception as ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
def get_data_for_block_chart(*args, **kwargs):
    try:
        dt = datetime.now()
        last_check = dt.strftime('%Y-%m-%d %H:%M:%S')
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        station_id = request.vars.station_id
        from_public = request.vars.from_public
        station_name = ''
        is_public_data_type = 2
        station = db.stations(station_id)
        if station:
            station_name = station.station_name
            try:
                is_public_data_type = station.is_public_data_type
            except:
                is_public_data_type = 2
        conditions = (db.station_indicator.station_id == station_id)
        if from_public:
            conditions &= (db.station_indicator.is_public == from_public)
        rows2 = db(conditions).select(db.station_indicator.indicator_id, distinct=True)
        indicators_id = []
        for row in rows2:
            indicators_id.append(row.indicator_id)
        indicators = db(db.indicators.id.belongs(indicators_id)).select(db.indicators.ALL)
        # print(indicators)
        data = dict()
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

        from_time = dt - timedelta(days=7)
        if is_public_data_type == 3:
            rows = db((db.aqi_data_24h.station_id == station_id) &
                      (db.aqi_data_24h.get_time >= from_time)).select(db.aqi_data_24h.ALL,
                                                                      orderby=db.aqi_data_24h.get_time)
        else:
            rows = db((db.aqi_data_adjust_24h.station_id == station_id) &
                      (db.aqi_data_adjust_24h.get_time >= from_time)).select(db.aqi_data_adjust_24h.ALL,
                                                                             orderby=db.aqi_data_adjust_24h.get_time)

        for row in rows:
            for k in data:
                if row.data_1d.has_key(k):
                    for idx, item in enumerate(data[k]):
                        if row.get_time == item['name']:
                            data[k][idx]['y'] = round(float(row.data_1d[k]), 2)
                            # print(row.data_1d[k])
                            break

        # print(data)
        # for k in data:
        #     for idx, item in enumerate(data[k]):
        #         data[k][idx]['name'] = int(1000 * (data[k][idx]['name'] - datetime(1970, 1, 1)).total_seconds())
        # data[k][idx][0] = (data[k][idx][0]).strftime('%d-%m-%Y')
        return dict(charts=data, station_name=station_name, last_check=last_check)
    except Exception as ex:
        return dict(charts=[], station_name='', last_check=last_check)


def export_csv():
    import os.path
    import csv
    station_name = T('Stations list')
    file_name = request.now.strftime(station_name + '_%Y%m%d_%H%M%S.csv')
    file_path = os.path.join(request.folder, 'static', 'export', file_name)
    # get search parameters

    station_id = "28560877461938780203765592307"
    iDisplayStart = int(0)
    iDisplayLength = int(20)
    limitby = (iDisplayStart, iDisplayLength + 1)
    added_columns = request.vars.added_columns or ''

    if added_columns:
        added_columns = added_columns.split(',')
    print(added_columns);
    # Lay du lieu AQI hour 7 ngay gan nhat
    from_day = request.now - timedelta(days=7)
    is_public_data_type = 2
    station = db.stations(station_id)
    if station:
        try:
            is_public_data_type = station.is_public_data_type
        except:
            is_public_data_type = 2

    if is_public_data_type == 3:
        conditions = (db.aqi_data_hour.station_id == station_id)
        conditions &= (db.aqi_data_hour.get_time >= from_day)
        aqi_hours = db(conditions).select(db.aqi_data_hour.ALL, orderby=~db.aqi_data_hour.get_time, limitby=limitby)
    else:
        conditions = (db.aqi_data_adjust_hour.station_id == station_id)
        conditions &= (db.aqi_data_adjust_hour.get_time >= from_day)
        aqi_hours = db(conditions).select(db.aqi_data_adjust_hour.ALL, orderby=~db.aqi_data_adjust_hour.get_time,
                                          limitby=limitby)
    aaData = []
    iTotalRecords = db(conditions).count()

    # get dict ('indicator_id' : indicator_name)
    indicators_dict = common.get_indicator_dict()

    # Lay nhung indicator duoc public
    conditions = (db.station_indicator.station_id == station_id)
    conditions &= (db.station_indicator.is_public == True)
    indicators_public = db(conditions).select(db.station_indicator.indicator_id)
    indicators = [indicators_dict.get(item.indicator_id) for item in indicators_public]

    if aqi_hours:
        with open(file_path, mode='wb') as out_file:
            out_file.write(u'\ufeff'.encode('utf8'))
            writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            iRow = 1
            for i, item in enumerate(aqi_hours):
                rowHeader = [
                    T('LBL_STT'),
                    T('Datetime'),
                    T('AQI hour'),
                ]
                row = [
                    str(iDisplayStart + 1 + i),
                    item.get_time,
                    "{0:.2f}".format(item.data['aqi']) if item.data['aqi'] else '0',
                ]

                added_item = dict()
                if item.data:
                    if indicators:
                        for data_key in indicators:
                            i_name = str(data_key)
                            v = ''
                            v = item.data[i_name] if item.data.has_key(i_name) else ''
                            if not v:
                                u = 1
                                # added_item[i_name] = '-'
                            else:
                                v = float(v)
                                added_item[i_name] = "{0:.2f}".format(v)
                for column in indicators:
                    if column and added_item.has_key(column):
                        if added_item[column] != '-':
                            if iRow == 1:
                                # Write header
                                rowHeader.append(column)
                            row.append(added_item[column])

                # Write header
                if iRow == 1:
                    writer.writerow(rowHeader)
                writer.writerow(row)
                iRow += 1

        data = open(file_path, "rb").read()
        os.unlink(file_path)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

        return data
    else:
        return T('export data empty')


def export_excel():
    import os.path, openpyxl

    try:
        aqi_type = int(request.vars.aqi_type)
        station_id = request.vars.station_id
        station_name = ''
        is_public_data_type = 2
        station = db.stations(station_id)
        if station:
            station_name = station.station_name
            station_type = station.station_type
            try:
                is_public_data_type = station.is_public_data_type
            except:
                is_public_data_type = 2

        iDisplayStart = int(0)
        iDisplayLength = int(20)
        limitby = (iDisplayStart, iDisplayLength + 1)
        added_columns = request.vars.added_columns or ''

        if added_columns:
            added_columns = added_columns.split(',')
        # Lay du lieu AQI hour
        date = request.vars.date
        from_day = request.now

        if aqi_type == 1:
            # if date:
            #     from_day = request.now - timedelta(hours=25)

            if int(station_type) == 1:
                qi_title = 'VN_WQI'
                if is_public_data_type == 3:
                    last_record = db(db.wqi_data_hour.station_id == station_id).select().last() or None

                    conditions = (db.wqi_data_hour.station_id == station_id)
                    if date and (last_record != None):
                        from_day = last_record.get_time - timedelta(hours=25)
                        conditions &= (db.wqi_data_hour.get_time >= from_day)
                    aqi_hours = db(conditions).select(db.wqi_data_hour.ALL, orderby=~db.wqi_data_hour.get_time)
                else:
                    last_record = db(db.wqi_data_adjust_hour.station_id == station_id).select().last() or None

                    conditions = (db.wqi_data_adjust_hour.station_id == station_id)
                    if date and (last_record != None):
                        from_day = last_record.get_time - timedelta(hours=25)
                        conditions &= (db.wqi_data_adjust_hour.get_time >= from_day)
                    aqi_hours = db(conditions).select(db.wqi_data_adjust_hour.ALL,
                                                      orderby=~db.wqi_data_adjust_hour.get_time)
            else:
                qi_title = 'VN_AQI'
                if is_public_data_type == 3:
                    last_record = db(db.aqi_data_hour.station_id == station_id).select().last() or None

                    conditions = (db.aqi_data_hour.station_id == station_id)
                    if date and (last_record != None):
                        from_day = last_record.get_time - timedelta(hours=25)
                        conditions &= (db.aqi_data_hour.get_time >= from_day)
                    aqi_hours = db(conditions).select(db.aqi_data_hour.ALL, orderby=~db.aqi_data_hour.get_time)
                else:
                    last_record = db(db.aqi_data_adjust_hour.station_id == station_id).select().last() or None

                    conditions = (db.aqi_data_adjust_hour.station_id == station_id)
                    if date and last_record is not None:
                        from_day = last_record.get_time - timedelta(hours=25)
                        conditions &= (db.aqi_data_adjust_hour.get_time >= from_day)
                    aqi_hours = db(conditions).select(db.aqi_data_adjust_hour.ALL,
                                                      orderby=~db.aqi_data_adjust_hour.get_time)
            aaData = []
            iTotalRecords = db(conditions).count()

            # get dict ('indicator_id' : indicator_name)
            indicators_dict = common.get_indicator_dict()

            # Lay nhung indicator duoc public
            conditions = (db.station_indicator.station_id == station_id)
            conditions &= (db.station_indicator.is_public == True)
            indicators_public = db(conditions).select(db.station_indicator.indicator_id)
            indicators = [indicators_dict.get(item.indicator_id) for item in indicators_public]

            if aqi_hours:
                wb = openpyxl.load_workbook(
                    filename=os.path.join(request.folder, 'static', 'export', 'Historical_data.xlsx'))
                ws = wb.get_sheet_by_name('Sheet1')

                iRow = 1
                rowHeader_1 = [
                    T('LBL_STT'),
                    T('Datetime'),
                    T('AQI hour'),
                ]
                rowHeader_2 = []
                for i, item in enumerate(aqi_hours):
                    qi = '-'
                    if item.data.has_key('aqi'):
                        qi = "{0:.0f}".format(item.data['aqi']) if item.data['aqi'] else '-'

                    if item.data.has_key('wqi'):
                        qi = "{0:.0f}".format(item.data['wqi']) if item.data['wqi'] else '-'

                    row = [
                        str(iDisplayStart + 1 + i),
                        item.get_time,
                        qi,
                    ]

                    added_item = dict()
                    if item.data:
                        if indicators:
                            for data_key in indicators:
                                i_name = str(data_key)
                                v = ''
                                v = item.data[i_name] if item.data.has_key(i_name) else ''
                                if not v:
                                    u = 1
                                    added_item[i_name] = '-'
                                else:
                                    v = float(v)
                                    added_item[i_name] = "{0:.0f}".format(v)
                    for column in sorted(indicators):
                        if column and added_item.has_key(column):
                            if added_item[column] != '-':
                                if iRow == 1:
                                    # Write header
                                    if (column == 'PM-2-5'):
                                        rowHeader_2.append('PM-2.5')
                                    else:
                                        rowHeader_2.append(column)
                                row.append(added_item[column])
                            # TODO
                            if (column in ['O3', 'CO', 'PM-2-5', 'PM-10', 'NO2']):
                                if added_item[column] == '-':
                                    row.append(added_item[column])
                    # print(i)
                    # Write header
                    # if iRow == 1:
                    # Write header
                    # ws['A1'] = 'Datetime'

                    # Write data
                    for j, indicator in enumerate(row):
                        ws[chr(ord('A') + j) + str(2 + i)] = indicator
                    ws[chr(ord('A') + 1) + str(2 + i)] = item.get_time.strftime(datetime_format_vn)

                    iRow += 1

                for i, indicator in enumerate(sorted(rowHeader_2)):
                    ws[chr(ord('A') + i + 3) + '1'] = indicator.upper()
                ws[chr(ord('A')) + '1'] = 'No'
                ws[chr(ord('A') + 1) + '1'] = 'Ngày giờ'
                ws[chr(ord('A') + 2) + '1'] = qi_title + ' giờ'

                file_name = request.now.strftime(
                    qi_title + ' Gio Trong 7 Ngay_Tram ' + no_accent_vietnamese(station_name) + '_%Y%m%d_%H%M%S.xlsx')
                file_path = os.path.join(request.folder, 'static', 'export', str(file_name.encode("utf-8")))
                wb.save(file_path)

                data = open(file_path, "rb").read()
                os.unlink(file_path)
                response.headers['Content-Type'] = 'application/vnd.ms-excel'
                response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

                return data
            else:
                return T('export data empty')
        else:
            # if date:
            #     from_day = request.now - timedelta(days=int(date))

            if int(station_type) == 1:  # khong xu ly do khong co WQI ngay
                qi_title = 'VN_WQI'
                conditions = (db.data_min.station_id == station_id)
                conditions &= (db.data_min.get_time >= from_day)
                aqi = db(conditions).select(db.data_min.ALL, orderby=~db.data_min.get_time)
            else:
                qi_title = 'VN_AQI'
                if is_public_data_type == 3:
                    last_record = db(db.aqi_data_24h.station_id == station_id).select().last() or None

                    conditions = (db.aqi_data_24h.station_id == station_id)
                    if date and (last_record != None):
                        from_day = last_record.get_time - timedelta(days=int(date))
                        conditions &= (db.aqi_data_24h.get_time >= from_day)
                    aqi = db(conditions).select(db.aqi_data_24h.ALL, orderby=~db.aqi_data_24h.get_time)
                else:
                    last_record = db(db.aqi_data_adjust_24h.station_id == station_id).select().last() or None

                    conditions = (db.aqi_data_adjust_24h.station_id == station_id)
                    if date and (last_record != None):
                        from_day = last_record.get_time - timedelta(days=int(date))
                        conditions &= (db.aqi_data_adjust_24h.get_time >= from_day)
                    aqi = db(conditions).select(db.aqi_data_adjust_24h.ALL, orderby=~db.aqi_data_adjust_24h.get_time)

            aaData = []
            iTotalRecords = db(conditions).count()

            # get dict ('indicator_id' : indicator_name)
            indicators_dict = common.get_indicator_dict()

            # Lay nhung indicator duoc public
            conditions = (db.station_indicator.station_id == station_id)
            conditions &= (db.station_indicator.is_public == True)
            indicators_public = db(conditions).select(db.station_indicator.indicator_id)
            indicators = [indicators_dict.get(item.indicator_id) for item in indicators_public]

            if aqi:
                wb = openpyxl.load_workbook(
                    filename=os.path.join(request.folder, 'static', 'export', 'Historical_data.xlsx'))
                ws = wb.get_sheet_by_name('Sheet1')

                iRow = 1
                rowHeader_1 = [
                    T('LBL_STT'),
                    T('Date'),
                    T('AQI day'),
                ]
                rowHeader_2 = []
                for i, item in enumerate(aqi):
                    qi = '-'
                    if item.data_1d.has_key('aqi'):
                        qi = "{0:.0f}".format(item.data_1d['aqi']) if item.data_1d['aqi'] else '-'

                    row = [
                        str(iDisplayStart + 1 + i),
                        item.get_time.strftime('%d/%m/%Y') if item.get_time else '-',
                        qi,
                    ]

                    added_item = dict()
                    if item.data_1d:
                        if indicators:
                            for data_key in indicators:
                                i_name = str(data_key)
                                v = ''
                                v = item.data_1d[i_name] if item.data_1d.has_key(i_name) else ''
                                if not v:
                                    u = 1
                                    added_item[i_name] = '-'
                                else:
                                    v = float(v)
                                    added_item[i_name] = "{0:.0f}".format(v)
                    for column in sorted(indicators):
                        if column and added_item.has_key(column):
                            if added_item[column] != '-':
                                if iRow == 1:
                                    # Write header
                                    if column == 'PM-2-5':
                                        rowHeader_2.append('PM-2.5')
                                    else:
                                        rowHeader_2.append(column)
                                row.append(added_item[column])
                            # TODO
                            if column in ['O3', 'CO', 'PM-2-5', 'PM-10', 'NO2']:
                                if added_item[column] == '-':
                                    row.append(added_item[column])
                    # print(i)
                    # Write header
                    # if iRow == 1:
                    # Write header
                    # ws['A1'] = 'Datetime'

                    # Write data
                    for j, indicator in enumerate(row):
                        ws[chr(ord('A') + j) + str(2 + i)] = indicator
                    ws[chr(ord('A') + 1) + str(2 + i)] = item.get_time.strftime('%d/%m/%Y')

                    iRow += 1

                for i, indicator in enumerate(sorted(rowHeader_2)):
                    ws[chr(ord('A') + i + 3) + '1'] = indicator.upper()
                ws[chr(ord('A')) + '1'] = 'No'
                ws[chr(ord('A') + 1) + '1'] = 'Ngày'
                ws[chr(ord('A') + 2) + '1'] = qi_title + ' ngày'

                file_name = request.now.strftime(
                    qi_title + ' Ngay Trong 30 Ngay_Tram ' + no_accent_vietnamese(station_name) + '_%Y%m%d_%H%M%S.xlsx')
                file_path = os.path.join(request.folder, 'static', 'export', unicode(file_name, "utf-8"))
                wb.save(file_path)

                data = open(file_path, "rb").read()
                os.unlink(file_path)
                response.headers['Content-Type'] = 'application/vnd.ms-excel'
                response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

                return data
            else:
                return T('export data empty')
    except Exception as ex:
        return dict(success=False, message=str(ex))


################################################################################
@service.json
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
                'station_name': row.station_name,
                'qi_time': row.qi_time.strftime("%H:%M %m/%d") if row.qi_time else '-',
                'qi': "{0:.0f}".format(row.qi) if row.qi else '-',
                'status': str(T(status_icon['name']))
            })
        content = json.dumps(aaData)
        return dict(content=content, success=True)
    except Exception, ex:
        return dict(message=str(ex), success=False)


################################################################################
@service.json
def get_stations_by_province(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1)

        station_type = request.vars.station_type
        status = request.vars.status
        province_id = request.vars.province_id

        stations = []
        conditions = (db.stations.id > 0) & (db.stations.is_public == True)
        if province_id:
            conditions &= (db.stations.province_id == str(province_id))
        if station_type:
            conditions &= (db.stations.station_type == station_type)
        if status:
            status = status.split(',')
            conditions &= (db.stations.status.belongs(status))
        rows = db(conditions).select(db.stations.ALL, orderby=db.stations.order_no, limitby=limitby)

        dt_format = '%Y-%m-%d %H:%M:%S'
        dt_format2 = '%H:%M %d/%m'

        aaData = []
        iTotalRecords = db(conditions).count()
        iCount = 0
        ids = [str(it.id) for it in rows]
        # Lay du lieu moi nhat
        data_dic = data_lastest_to_dic_by(ids)
        # Thong so cua tram
        indicator_dic = get_indicators_by_station_ids(ids)
        for row in rows:
            station_id = str(row.id)
            iCount += 1
            station_color = '#333333'
            station_status = ''
            icon = ''
            try:
                is_public_data_type = row.is_public_data_type
            except:
                is_public_data_type = 2

            show_off_time = False
            if row.status in [const.STATION_STATUS['OFFLINE']['value'], const.STATION_STATUS['ADJUSTING']['value'],
                              const.STATION_STATUS['ERROR']['value']]:
                if row.off_time:
                    show_off_time = True
            if row.status == const.STATION_STATUS['OFFLINE']['value']:
                icon = T(const.STATION_STATUS['OFFLINE']['icon'])
                station_color = const.STATION_STATUS['OFFLINE']['color']
            else:
                icon = T(const.STATION_STATUS['GOOD']['icon'])
                station_color = const.STATION_STATUS['GOOD']['color']
            # for k in const.STATION_STATUS:
            #     if const.STATION_STATUS[k]['value'] == row.status:
            #         station_color = const.STATION_STATUS[k]['color']
            #         station_status = T(const.STATION_STATUS[k]['name'])
            # icon = T(const.STATION_STATUS[k]['icon'])
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
                'longitude': row.longitude
            })

            data_indicaticator_last = []
            if data_dic.has_key(station_id):
                data_indicaticator_last = data_dic[station_id]

            indicator_list_code = '-'
            seperator = ', '

            if indicator_dic.has_key(station_id):
                indicators = indicator_dic[station_id]
                for indicator in indicators:
                    indicator_label = indicator.get('indicator')
                    if data_indicaticator_last.has_key(indicator_label):
                        if data_indicaticator_last[indicator_label] != 'NULL':
                            indicator_label = '<span style="color: #1dce6c">' + indicator_label + '</span>'
                        else:
                            indicator_label = '<span style="color: #999999">' + indicator_label + '</span>'

                        if row.status == const.STATION_STATUS['OFFLINE']['value']:
                            indicator_label = indicator_label
                            indicator_label = '<span style="color: #999999">' + indicator_label + '</span>'

                    if indicator_list_code == '-':
                        indicator_list_code = indicator_label
                    else:
                        indicator_list_code = indicator_list_code + ', ' + indicator_label
            station_name_with_status = '<div class="station-status-icon"><i class="' + icon + ' text-primary" style="color:' + station_color + '!important"></i>&nbsp; <a data-id="' + str(
                row.id) + '" data-lat="' + str(row.latitude) + '" data-lon="' + str(
                row.longitude) + '" href="javascript: void(0);">' + row.station_name + '</a></div>'
            aaData.append([str(iDisplayStart + iCount), station_name_with_status, indicator_list_code])
        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, aoColumns=[],
                    success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
def get_province_have_station(*args, **kwargs):
    try:
        station_type = request.vars.station_type
        provinces = common.get_province_have_station(station_type)

        html = '<option value="">%s</option>' % (T('Select a province'))

        # Nuoc thai
        province_with_station_type_0 = common.get_province_have_station_with_station_type(station_type)
        province_have_station = dict()
        for province in provinces:
            if province_with_station_type_0.has_key(str(province)):
                if not province_have_station.has_key(province):
                    province_have_station[province] = []
                item_province = {
                    'id': str(province),
                    'province_name': provinces[province]['province_name'],
                    'count_stations': province_with_station_type_0[province]
                }
                province_have_station[province].append(item_province)

                html += '<option value="%s">%s (%s)</option>' \
                        % (str(province), str(provinces[province]['province_name']),
                           str(province_with_station_type_0[province]))

        return dict(success=True, html=html)
    except Exception as ex:
        return dict(success=False, message=str(ex))


import re
import unicodedata

def no_accent_vietnamese(s):
    s = s.decode('utf-8')
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')
