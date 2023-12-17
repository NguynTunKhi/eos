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


def call():
    return service()

################################################################################
def page():
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
    conditions = (db.stations.id > 0)
    conditions &= (db.stations.is_qi == True)
    conditions &= (db.stations.is_public == True)
    index_items = const.AQI_COLOR
    for k in index_items:
        index_items[k]['text'] = str(T(index_items[k]['text']))
    index_items = json.dumps(index_items)
    # Get all
    # conditions &= (db.stations.station_type.belongs([const.STATION_TYPE['STACK_EMISSION']['value'], const.STATION_TYPE['AMBIENT_AIR']['value']]))
    rows = db(conditions).select(db.stations.ALL)
    stations = []
    for row in rows:
        station_id = str(row.id)
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
            'province_name': provinces[row['province_id']]['province_name'] if provinces.has_key(row['province_id']) else '',
            'status_disp': station_status[s]['name'] if station_status.has_key(s) else '',
            # 'index': random.randint(30, 450),
            'index': round(row.qi) if row.qi else 0,
            'parameters': []
        }
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
    rows = db(db.stations.id > 0).select(db.stations.ALL, orderby = db.stations.station_type | db.stations.station_name)
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
            'status_disp': station_status[s]['name'] if station_status.has_key(s) else ''
        }
        station_group_by_type[st].append(item)

        areas = get_all_records('areas');
    json_area = json.dumps(areas)
    json_provinces = json.dumps(provinces)
    return dict(station_group_by_type=station_group_by_type, json_stations=json_stations, provinces=provinces,
                station_status=station_status, json_station_status=json_station_status,
                json_indicators=json_indicators, json_area=json_area, json_provinces=json_provinces,
                stations=stations, areas=areas, index_items=index_items)

################################################################################
# @decor.requires_login()
def index():
    # Select all AQI stations
    conditions = (db.stations.is_qi == True)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    #conditions &= (db.stations.station_type.belongs([const.STATION_TYPE['STACK_EMISSION']['value'], const.STATION_TYPE['AMBIENT_AIR']['value']]))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)

    eip_config = db(db.eip_config.name == 'eip_config').select().first()

    return dict(stations = stations, eip_config = eip_config)

################################################################################
@service.json
def get_list_stations_public(*args, **kwargs):
    try:
        sometext = request.vars.sometext
        station_id = request.vars.station_id
        station_type = request.vars.station_type
        is_public = request.vars.is_public
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
        aaData = []

        conditions = (db.stations.id > 0)
        if station_type:
            conditions &= (db.stations.station_type == station_type)
            if ((int(station_type) == 4) or (int(station_type) == 1)):
                conditions &= (db.stations.is_qi == True)
        if station_id:
                conditions &= (db.stations.id == station_id)

        if is_public:
                conditions &= (db.stations.is_public == is_public)
        # Get all station_ids which belonged to current login user (group)
        #if not 'admin' in current_user.roles:
        #    station_ids = common.get_stations_belong_current_user()
        #    conditions &= (db.stations.id.belongs(station_ids))
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.stations.id.belongs(station_ids))
        stations = db(conditions).select(db.stations.id, db.stations.station_name, db.stations.is_public_data_type, db.stations.is_public)
        ids = []
        station_dic = dict()
        for item in stations:
          ids.append(str(item.id))
          station_dic[str(item.id)] = item['station_name']

        resStations = {}
        for item in stations:
            if not resStations.has_key(str(item.id)):
                resStations[str(item.id)] = {}
            resStations[str(item.id)]['is_public_data_type'] = item.is_public_data_type
            resStations[str(item.id)]['is_public'] = item.is_public

        # Get dict(indicator_id : indicator_name)
        indicators_dict = common.get_indicator_dict()
        # Get all indicators of AQI stations
        conds = db.station_indicator.station_id.belongs(ids)
        conds &= db.station_indicator.status == const.SI_STATUS['IN_USE']['value']
        station_indicators = db(conds).select(
            db.station_indicator.id,
            db.station_indicator.station_id,
            db.station_indicator.station_name,
            db.station_indicator.station_type,
            db.station_indicator.indicator_id,
            db.station_indicator.is_public,
        )
        # build dict(station_id : {indicator_id: indicator_name,...})
        res = {}
        for item in station_indicators:
            if not res.has_key(item.station_id):
              res[item.station_id] = {}
              res[item.station_id]['indicator'] = []
              if station_dic.has_key(item.station_id):
                res[item.station_id]['station_name'] = station_dic[item.station_id]
            indicator = item.as_dict()
            indicator['indicator_code'] = indicators_dict.get(item.indicator_id)
            res[item.station_id]['indicator'].append(indicator)
            #res[item.station_id]['station_name'] = item.station_name

            # for item2 in stations:
            #     if str(item2.id) == str(item.station_id):
            #         res[item.station_id]['station_name'] = item2.station_name
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = len(res.keys())
        i = 0
        for station_id in sorted(res)[iDisplayStart : iDisplayStart + iDisplayLength + 1]:     # Thuc hien paging
            i += 1
            indicator_str = ''
            for indicator in res[station_id]['indicator']:
                if indicator['is_public']:
                    indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id'], _checked=True), indicator['indicator_code'])
                else:
                    indicator_str += '<label data-station="%s" class=\'check_public\'>%s&nbsp;%s</label>' % (indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['id']), indicator['indicator_code'])

            data_type = '';
            if resStations[str(station_id)]['is_public_data_type'] :
                if (resStations[str(station_id)]['is_public_data_type'] == const.DATA_TYPE['APPROVED']['value']) :
                    data_type += '<label data-station="%s" class=\'data_type\'>%s&nbsp;%s</label>' % (
                        station_id, INPUT(_type="radio", _name="%s" % station_id, _value="%s" % const.DATA_TYPE['APPROVED']['value'], _checked="checked"), T(const.DATA_TYPE['APPROVED']['name']))
                else :
                    data_type += '<label data-station="%s" class=\'data_type\'>%s&nbsp;%s</label>' % (
                        station_id, INPUT(_type="radio", _name="%s" % station_id, _value="%s" % const.DATA_TYPE['APPROVED']['value']), T(const.DATA_TYPE['APPROVED']['name']))

                # if (resStations[str(station_id)]['is_public_data_type'] == const.DATA_TYPE['YET_APPROVED']['value']):
                #     data_type += '<label data-station="%s" class=\'data_type\'>%s&nbsp;%s</label>' % (
                #     station_id, INPUT(_type="radio", _name="%s" % station_id, _value="%s" % const.DATA_TYPE['YET_APPROVED']['value'],  _checked="checked"), T(const.DATA_TYPE['YET_APPROVED']['name']))
                # else :
                #     data_type += '<label data-station="%s" class=\'data_type\'>%s&nbsp;%s</label>' % (
                #         station_id, INPUT(_type="radio", _name="%s" % station_id, _value="%s" % const.DATA_TYPE['YET_APPROVED']['value']),
                #         T(const.DATA_TYPE['YET_APPROVED']['name']))
                if (resStations[str(station_id)]['is_public_data_type'] == const.DATA_TYPE['ORIGINAL_DATA']['value']):
                    data_type += '<label data-station="%s" class=\'data_type\'>%s&nbsp;%s</label>' % (
                    station_id, INPUT(_type="radio", _name="%s" % station_id, _checked="checked", _value="%s" % const.DATA_TYPE['ORIGINAL_DATA']['value']),
                    T(const.DATA_TYPE['ORIGINAL_DATA']['name']))
                else :
                    data_type += '<label data-station="%s" class=\'data_type\'>%s&nbsp;%s</label>' % (
                        station_id, INPUT(_type="radio", _name="%s" % station_id, _value="%s" % const.DATA_TYPE['ORIGINAL_DATA']['value']),
                        T(const.DATA_TYPE['ORIGINAL_DATA']['name']))
            else :
                data_type += '<label data-station="%s" class=\'data_type\'>%s&nbsp;%s</label>' % (station_id, INPUT(_type="radio", _name="%s" % station_id, _value="%s"  % const.DATA_TYPE['APPROVED']['value'], _checked="checked"), T(const.DATA_TYPE['APPROVED']['name']))
                # data_type += '<label data-station="%s" class=\'data_type\'>%s&nbsp;%s</label>' % (station_id, INPUT(_type="radio",_name="%s" % station_id,  _value="%s" % const.DATA_TYPE['YET_APPROVED']['value']), T(const.DATA_TYPE['YET_APPROVED']['name']))
                data_type += '<label data-station="%s" class=\'data_type\'>%s&nbsp;%s</label>' % (station_id, INPUT(_type="radio",  _name="%s" % station_id, _value="%s" % const.DATA_TYPE['ORIGINAL_DATA']['value']), T(const.DATA_TYPE['ORIGINAL_DATA']['name']))

            if (resStations[str(station_id)]['is_public'] == True):
                is_public = '<label data-station="%s" class=\'is_public\'>%s&nbsp;</label>' % (
                    indicator['station_id'], INPUT(_type="checkbox", _checked="checked", _id="%s" % indicator['station_id']))
            else:
                is_public = '<label data-station="%s" class=\'is_public\'>%s&nbsp;</label>' % (
                    indicator['station_id'], INPUT(_type="checkbox", _id="%s" % indicator['station_id']))

            aaData.append([
                str(iDisplayStart + i),
                is_public,
                res[station_id]['station_name'],
                data_type,
                indicator_str,
                station_id
            ])
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@service.json
# # @decor.requires_login()
# @decor.requires_permission('eos|areas|form')
def ajax_save(*args, **kwargs):
    try:
        checked = request.vars.checked.split(',')
        unchecked = request.vars.unchecked.split(',')
        station_public = request.vars.station_public.split(',')
        station_unpublic = request.vars.station_unpublic.split(',')
        is_publics_checked = request.vars.is_publics_checked.split(',')
        is_publics_unchecked = request.vars.is_publics_unchecked.split(',')

        station_style_0 = request.vars.station_style_0
        waste_water_is_public = True
        if int(station_style_0) == 0:
            waste_water_is_public = False

        surface_water_is_public = True
        station_style_1 = request.vars.station_style_1
        if int(station_style_1) == 0:
            surface_water_is_public = False

        stack_emission_is_public = True
        station_style_3 = request.vars.station_style_3
        if int(station_style_3) == 0:
            stack_emission_is_public = False

        ambient_air_is_public = True
        station_style_4 = request.vars.station_style_4
        if int(station_style_4) == 0:
            ambient_air_is_public = False

        time = datetime.now()
        db(db.station_indicator.id.belongs(checked)).update(is_public=True)
        db(db.station_indicator.id.belongs(unchecked)).update(is_public=False)
        db(db.stations.id.belongs(is_publics_checked) and db.stations.is_public==False).update(is_public=True , public_time=time)
        db(db.stations.id.belongs(is_publics_unchecked)).update(is_public=False)

        db.eip_config.update_or_insert(
            (db.eip_config.name == 'eip_config'),
            name='eip_config',
            waste_water_is_public=waste_water_is_public,
            surface_water_is_public=surface_water_is_public,
            stack_emission_is_public=stack_emission_is_public,
            ambient_air_is_public=ambient_air_is_public
        )

        station_data_type = request.vars.station_data_type.split(',')
        try:
            for item in station_data_type:
                id = item.split('_')[0]
                data_type = item.split('_')[1]

                db(db.stations.id == id).update(
                    is_public_data_type=data_type,
                )
        except :
            pass

        return dict(success = True)
    except Exception as ex:
        logger.error(str(ex))
        return dict(success = False, message = str(ex))


def test():
    return dict()

################################################################################
@service.json
# # @decor.requires_login()
# @decor.requires_permission('eos|areas|form')
def get_aqi_data(*args, **kwargs):
    try:
        station_id = request.vars.station_id
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
        added_columns = request.vars.added_columns or ''
        if added_columns:
            added_columns = added_columns.split(',')

        # Lay du lieu AQI hour 7 ngay gan nhat
        from_day = request.now - timedelta(days=7)
        conditions = (db.aqi_data_hour.station_id == station_id)
        conditions &= (db.aqi_data_hour.get_time >= from_day)
        aqi_hours = db(conditions).select(db.aqi_data_hour.ALL, limitby = limitby)

        aaData = []
        iTotalRecords = db(conditions).count()

        # get dict ('indicator_id' : indicator_name)
        indicators_dict = common.get_indicator_dict()

        # Lay nhung indicator duoc public
        conditions = (db.station_indicator.station_id == station_id)
        conditions &= (db.station_indicator.is_public == True)
        conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        indicators_public = db(conditions).select(db.station_indicator.indicator_id)
        indicators = [indicators_dict.get(item.indicator_id) for item in indicators_public]

        for i, item in enumerate(aqi_hours):
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
                            added_item[i_name] = '-'
                        else:
                            try:
                                v = float(v)
                                added_item[i_name] = "{0:.2f}".format(v)
                            except:
                                added_item[i_name] = '-'
            for column in indicators:
                if column and added_item.has_key(column):
                    row.append(added_item[column])
            aaData.append(row)

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception, ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)

################################################################################
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

        if command_id:
            command_content = db(db.datalogger_command.id == command_id). \
                select(db.datalogger_command.command_content).first().command_content
        if station_id:
            logger_id = db(db.adjustments.station_id == station_id).select().first()
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

        return dict(success=True, html=html, logger_id=logger_id, command_content=command_content)
    except Exception as ex:
        return dict(success=False, message=str(ex))

#####################################################################################
@service.json
def popup_config():
    try:
        record = db(db.eip_config).select().first() or None
        frm = SQLFORM(db.eip_config, record, _method='POST', hideerror=True, showid=False)
    except Exception as ex:
        return dict(success=False, message=str(ex))

    return dict(frm=frm)
#######################################################################
@service.json
def ajax_add_config_public(*args, **kwargs):
    try:
        time_public = request.vars.time_public
        db(db.eip_config.name == 'eip_config').update(time_public=time_public)
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

def sort_func(e):
    return e['from']

#######################################################################
@service.json
def get_data_public(*args, **kwargs):
    try:
        html = ''
        time_public = request.vars.public
        if time_public:
            time_public = int(time_public)
        conditions = (db.stations.is_public == True)
        conditions &= (db.stations.station_type == 4)
        if current_user:
          if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
              db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
        row = db(conditions).select(db.stations.qi_time, db.stations.qi_adjsut_time,
                                    db.stations.qi_adjust, db.stations.qi,
                                    db.stations.is_public_data_type)
        time_now = datetime.now()
        total = 0
        rs = dict()
        for k in const.AQI_COLOR:
            val = const.AQI_COLOR[k]
            rs[str(val['from'])] = val
            rs[str(val['from'])]['total'] = 0
        for item in row:
            public_type = item['is_public_data_type']
            k_time = 'qi_adjsut_time'
            k_value = 'qi_adjust'
            if public_type == 3:
                k_time = 'qi_time'
                k_value = 'qi'

            value = item[k_value]
            time = item[k_time]
            # if value in range(0, 50):
            if value is not None and time > time_now - timedelta(hours=time_public):
                for k in rs:
                    val = rs[k]
                    if round(value) in range(val['from'], val['to'] + 1):
                        total += 1
                        rs[k]['total'] += 1
                        break
        html = "<table class='table table-striped table-bordered table-hover table-responsive no-footer'><thead><tr><th>{}</th><th>{} ({})</th></tr></thead><tbody>".format(T('Status'), T('Tổng số trạm'), total)
        ls = rs.values()
        ls.sort(key=sort_func)
        _clss = 'odd'
        for item in ls:
            if _clss == 'odd':
                _clss = 'even'
            html += "<tr class={}>".format(_clss) \
                    + "<td class='text-left' style='font-weight: 600;'>{}</td>".format(T(item['text'])) \
                    + "<td><span style='background-color: {}; color: {}' class='badge badge-light'>{}</span></td></tr>"\
                    .format(item['bgColor'], item['color'],  item['total'])
        # for key in rs:
        #

        return dict(success=True, html=html+"</tbody></table>")
    except Exception as ex:
        return dict(success=False, message=str(ex))