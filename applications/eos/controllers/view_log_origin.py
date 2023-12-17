# coding=utf-8
# encoding: utf-8
# encoding=utf8
# -*- coding: utf-8 -*-
###############################################################################
# Author :
# Date   :
#
# Description :
#
###############################################################################

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from applications.eos.modules import common
from w2pex import date_util
from datetime import datetime, timedelta


def call():
    return service()


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'view_log')))
def index():
    view_type = request.vars.view_type
    try:
        view_type = int(view_type)
    except Exception as es:
        view_type = const.VIEW_BY['MINUTE']['value']
    station_id = request.vars.station_id
    provinces = common.get_province_have_station()
    # stations = db(db.stations.id > 0).select() #hungdx comment issue 44
    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(orderby=db.stations.order_no)
    default_provinces = db(db.provinces.default == 1).select()
    return dict(provinces=provinces, stations=stations, view_type=view_type, station_id=station_id,
                default_provinces=default_provinces)


################################################################################
@service.json
def get_list_log(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        station_id = request.vars.station_id
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        data_type = request.vars.data_type
        if data_type:
            data_type = int(data_type)

        duration = request.vars.durationf
        is_exceed = request.vars.is_exceed
        added_columns = request.vars.added_columns or ''
        if added_columns:
            added_columns = added_columns.split(',')
        view_type = request.vars.view_type or const.VIEW_BY['MINUTE']['value']
        if not station_id:
            return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[],
                        message=T('Select a station for viewing data'), success=True)
        aaData = []  # Du lieu json se tra ve
        list_data = None  # Du lieu truy van duoc
        iTotalRecords = 0  # Tong so ban ghi
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        view_by_info = common.get_const_by_value(const.VIEW_BY, view_type)
        table = view_by_info['table']

        if data_type and (
                data_type == const.DATA_TYPE['YET_APPROVED']['value'] or data_type == const.DATA_TYPE['APPROVED'][
            'value']):
            view_by_info_adjust = common.get_const_by_value(const.VIEW_BY_ADJUST, view_type)
            table = view_by_info_adjust['table']
            # table = 'data_adjust'

        conditions = (db[table]['id'] > 0)
        conditions &= (db[table]['station_id'] == station_id)
        if duration:  # Todo: Not clear
            duration = int(duration)
            duration = datetime.now() - timedelta(days=duration)
            conditions &= (db[table]['get_time'] >= duration)
        else:
            if from_date:
                conditions &= (db[table]['get_time'] >= date_util.string_to_datetime(from_date))
            if to_date:
                conditions &= (db[table]['get_time'] < date_util.string_to_datetime(to_date) + timedelta(days=1))
            if not from_date and not to_date:
                to_date = datetime.now()
                from_date = to_date - timedelta(days=365)
                conditions &= (db[table]['get_time'] >= from_date)
                conditions &= (db[table]['get_time'] < to_date)
        if is_exceed and table == 'data_min':
            conditions &= (db[table]['is_exceed'] == True)


        if table != 'aqi_data_24h' and table != 'aqi_data_adjust_24h':
            list_data = db(conditions).select(db[table].id,
                                              db[table].get_time,
                                              db[table].data,
                                              orderby=~db[table].get_time,
                                              limitby=limitby)
        else:
            list_data = db(conditions).select(db[table].id,
                                              db[table].get_time,
                                              db[table].data_24h,
                                              orderby=~db[table].get_time,
                                              limitby=limitby)
        ########

        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count(db[table].id)
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        si_dict = dict()
        conditions = (db.station_indicator.station_id == station_id)
        conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        rows = db().select(db.station_indicator.ALL)
        indicator_ids = []
        for row in rows:
            indicator_ids.append(row.indicator_id)
            si_dict[str(row.indicator_id)] = row.as_dict()
        indicators = db(db.indicators.id.belongs(indicator_ids)).select(db.indicators.id, db.indicators.indicator,
                                                                        db.indicators.unit)

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            added_item = dict()
            if added_columns:
                for indicator in indicators:
                    i_name = str(indicator.indicator)
                    i_name_decode = i_name.decode('utf-8')
                    if table != 'aqi_data_24h' and table != 'aqi_data_adjust_24h':
                        v = item.data[i_name_decode] if item.data.has_key(i_name_decode) else ''
                    else:
                        v = item.data_24h[i_name_decode] if item.data_24h.has_key(i_name_decode) else ''
                    if v == '' or v is None:
                        added_item[i_name] = '-'
                    else:
                        try:
                            v = float(v)
                            added_item[i_name] = "{0:.2f}".format(v)
                        except:
                            added_item[i_name] = '-'
            # if table != 'data_mon':
            if table != 'data_mon' and table != 'data_mon_adjust':
                row = [
                    str(iRow + i),
                    # item.get_time.strftime('%Y-%m-%d %H:%M:%S'),
                    item.get_time.strftime(datetime_format_vn),
                ]
            else:
                list = item.get_time.strftime(datetime_format_vn).split(' ')[1].split('/')
                list.pop(0)
                time = list[0] + '/' + list[1]
                row = [
                    str(iRow + i),
                    # item.get_time.strftime('%Y-%m-%d %H:%M:%S'),
                    time,
                ]
            for column in added_columns:
                if column and added_item.has_key(column):
                    row.append(added_item[column])
            aaData.append(row)

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
def get_list_max_min(*args, **kwargs):
    try:
        from datetime import datetime, timedelta
        from w2pex import date_util
        iDisplayStart = int(request.vars.iDisplayStart)  # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength)  # So luong ban ghi se lay toi da
        station_type = request.vars.station_type
        station_id = request.vars.station_id
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        duration = request.vars.duration
        is_exceed = request.vars.is_exceed
        added_columns = request.vars.added_columns or ''
        if added_columns:
            added_columns = added_columns[0].split(',')

        view_type = request.vars.view_type or const.VIEW_BY['MINUTE']['value']
        if not station_id:
            return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[],
                        message=T('Select a station for viewing data'), success=True)
        aaData = []  # Du lieu json se tra ve
        list_data = None  # Du lieu truy van duoc
        iTotalRecords = 0  # Tong so ban ghi
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        view_by_info = common.get_const_by_value(const.VIEW_BY, view_type)

        table = view_by_info['table']

        # conditions = (db[table]['id'] > 0)
        conditions = (db[table].id > 0)

        # if from_date:
        # conditions &= (db[table]['get_time'] >= date_util.string_to_datetime(from_date))
        # if to_date:
        # conditions &= (db[table]['get_time'] < date_util.string_to_datetime(to_date) + timedelta(days = 1))

        if duration:  # Neu co duration thi 2 dk from/to bi discard
            duration = int(duration)
            duration = datetime.now() - timedelta(days=duration)
            conditions = (db[table]['get_time'] >= duration)
        else:
            # Chi xuat toi da 30 ngay du lieu gan nhat
            if from_date and to_date:
                from_date = date_util.string_to_datetime(from_date)
                to_date = date_util.string_to_datetime(to_date)
                if (to_date - from_date).days > 30:
                    to_date = from_date + timedelta(days=30)
            elif from_date:
                from_date = date_util.string_to_datetime(from_date)
                if (request.now - from_date).days > 30:
                    to_date = from_date + timedelta(days=30)
                else:
                    to_date = request.now
            elif to_date:
                to_date = date_util.string_to_datetime(to_date)
                from_date = to_date - timedelta(days=30)
            else:
                to_date = request.now
                from_date = to_date - timedelta(days=30)

            conditions &= (db[table]['get_time'] >= from_date)
            conditions &= (db[table]['get_time'] < to_date + timedelta(days=1))

        if is_exceed and table == 'data_min':
            conditions &= (db[table]['is_exceed'] == True)

        conditions2 = (db.station_indicator.id > 0)
        conditions2 &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        if station_id:
            conditions2 &= (db.station_indicator.station_id == station_id)
        if station_type:
            conditions2 &= (db.station_indicator.station_type == station_type)
        #lấy id của added_columns
        rows = db(conditions2).select(db.station_indicator.ALL)
        id_indicators = db(conditions2).select(db.station_indicator.indicator_id)
        id_indicator_station = []
        for id in id_indicators:
            id_indicator_station.append(id.indicator_id)
        query = (db.indicators.id.belongs(id_indicator_station))
        query &= (db.indicators.indicator.belongs(added_columns))
        indicatorOrigin = db(query).select(db.indicators.id)
        id_addcolumns = []
        for item in indicatorOrigin:
            id_addcolumns.append(item.id)

        indicator_ids = id_addcolumns
        station_ids = []
        for row in rows:
            if row.station_id not in station_ids:
                station_ids.append(row.station_id)
            # if row.indicator_id not in indicator_ids:
            #     indicator_ids.append(row.indicator_id)

        if station_ids:
            # conditions &= (db[table]['station_id'].belongs(station_ids))
            conditions &= (db[table].station_id.belongs(station_ids))

        if table != 'aqi_data_24h':
            list_data = db(conditions).select(db[table].id, db[table].get_time, db[table].data)
        else:
            list_data = db(conditions).select(db[table].id, db[table].get_time, db[table].data_24h)
        rows = db(db.indicators.id.belongs(indicator_ids)).select(db.indicators.id, db.indicators.indicator,
                                                                  db.indicators.unit)

        indicators = dict()
        for row in rows:
            indicators[u'{}'.format(row.indicator)] = {
                'min_value': 999999999,
                'min_time': '',
                'has_min': False,
                'max_value': -999999999,
                'max_time': '',
                'has_max': False,
                'total': 0,
                'qty': 0,
                'unit': row.unit,
            }


        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            if table != 'aqi_data_24h':
                data = item.data
            else:
                data = item.data_24h
            for key_tmp in data:
                k = u'{}'.format(key_tmp)
                if indicators.has_key(k):
                    v = data[k]
                    if v:
                        try:
                            v = float(v)
                            indicators[k]['total'] += v
                            indicators[k]['qty'] += 1
                            if not indicators[k]['has_min'] or indicators[k]['min_value'] > v:
                                indicators[k]['has_min'] = True
                                indicators[k]['min_value'] = v
                                indicators[k]['min_time'] = item.get_time
                            if not indicators[k]['has_max'] or indicators[k]['max_value'] < v:
                                indicators[k]['has_max'] = True
                                indicators[k]['max_value'] = v
                                indicators[k]['max_time'] = item.get_time
                        except:
                            pass

        iTotalRecords = 0
        for k in indicators:
            iTotalRecords += 1
            row = [
                str(iTotalRecords),
                '%s(%s)' % (k, indicators[k]['unit']),
                '%0.2f' % indicators[k]['max_value'] if indicators[k]['has_max'] else '',
                indicators[k]['max_time'] if indicators[k]['has_max'] else '',
                '%0.2f' % indicators[k]['min_value'] if indicators[k]['has_min'] else '',
                indicators[k]['min_time'] if indicators[k]['has_min'] else '',
                '%0.2f' % (indicators[k]['total'] / indicators[k]['qty']) if indicators[k]['qty'] else '',
            ]
            aaData.append(row)

        return dict(iTotalRecords=iTotalRecords, iTotalDisplayRecords=iTotalRecords, aaData=aaData, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
# @decor.requires_login()
def export_csv():
    import os.path
    # get search parameters
    station_id = request.vars.station_id
    from_date = request.vars.from_date
    to_date = request.vars.to_date
    data_type = request.vars.data_type
    if data_type:
        data_type = int(data_type)

    duration = request.vars.duration
    is_exceed = request.vars.is_exceed
    view_type = request.vars.view_type or const.VIEW_BY['MINUTE']['value']

    if not station_id:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[],
                    message=T('Select a station for export data'), success=True)

    view_by_info = common.get_const_by_value(const.VIEW_BY, view_type)
    table = view_by_info['table']

    conditions = (db[table]['station_id'] == station_id)
    if duration:  # Duration duoc uu tien nhat so voi from/to
        duration = int(duration)
        # duration = datetime.now() - timedelta(days=duration)
        # Chi xuat toi da 7 ngay du lieu
        if duration == 1:
            duration = datetime.now() - timedelta(days=1)
        elif duration == 7:
            duration = datetime.now() - timedelta(days=7)
        else:
            duration = datetime.now() - timedelta(days=15)
        # duration = datetime.now() - timedelta(days=7)
        conditions &= (db[table]['get_time'] >= duration)
    else:
        # Chi xuat toi da 7 ngay du lieu
        if from_date and to_date:
            from_date = date_util.string_to_datetime(from_date)
            to_date = date_util.string_to_datetime(to_date)
        # if (to_date - from_date).days > 7:
        #    to_date = from_date + timedelta(days=7)
        elif from_date:
            from_date = date_util.string_to_datetime(from_date)
            if (request.now - from_date).days > 7:
                to_date = from_date + timedelta(days=30)
            else:
                to_date = request.now
        elif to_date:
            to_date = date_util.string_to_datetime(to_date)
            from_date = to_date - timedelta(days=30)
        else:
            if table == 'data_mon':
                to_date = request.now
                from_date = to_date - timedelta(days=365)
            else:
                to_date = request.now
                from_date = to_date - timedelta(days=30)

        conditions &= (db[table]['get_time'] >= from_date)
        conditions &= (db[table]['get_time'] <= to_date)

    if is_exceed and table == 'data_min':
        conditions &= (db[table]['is_exceed'] == True)

    if data_type:
        if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
            conditions &= (db[table]['is_approved'] == False)
        elif data_type == const.DATA_TYPE['APPROVED']['value']:
            conditions &= (db[table]['is_approved'] == True)

    list_data = db(conditions).select(db[table].id,
                                      db[table].get_time,
                                      db[table].data,
                                      orderby=db[table].get_time)

    conditions = (db.station_indicator.station_id == station_id)
    conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    # conditions &= (db.station_indicator.is_public == True)
    indicator_ids_data = db(conditions).select(db.station_indicator.indicator_id)
    indicator_ids = []
    for row in indicator_ids_data:
        indicator_ids.append(row.indicator_id)
    indicators_header = db(db.indicators.id.belongs(indicator_ids)).select(db.indicators.id, db.indicators.indicator,
                                                                           db.indicators.unit)

    import csv
    # Get station name
    station = db.stations(station_id)
    station_name = station.station_name if station else ''
    file_name = request.now.strftime(station_name + '_%Y%m%d_%H%M%S.csv')
    file_path = os.path.join(request.folder, 'static', 'export', file_name)

    with open(file_path, mode='wb') as out_file:
        writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if list_data.first() is None:
            raise HTTP(400, "Không đủ dữ liệu xuất CSV, vui lòng thử lại!")
        else:
            row = ['Datetime']
            # Write header
            for indicator in indicators_header:
                row.append(indicator.indicator)
            writer.writerow(row)

            # Write data
            for i, item in enumerate(list_data):
                row = []
                row.append(item.get_time.strftime(datetime_format_vn))
                for indicator in indicators_header:
                    try:
                        row_value = "{0:.4f}".format(float(item.data[indicator.indicator])) if item.data.has_key(
                            indicator.indicator) else '-'
                    except:
                        row_value = '-'

                    row.append(row_value)

                writer.writerow(row)

    data = open(file_path, "rb").read()
    os.unlink(file_path)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

    return data


################################################################################
# @decor.requires_login()
def export_csv_min_max():
    import os.path
    # get search parameters
    station_id = request.vars.station_id
    from_date = request.vars.from_date
    to_date = request.vars.to_date
    data_type = request.vars.data_type
    if data_type:
        data_type = int(data_type)

    duration = request.vars.duration
    is_exceed = request.vars.is_exceed
    view_type = request.vars.view_type or const.VIEW_BY['MINUTE']['value']

    if not station_id:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[],
                    message=T('Select a station for export data'), success=True)

    view_by_info = common.get_const_by_value(const.VIEW_BY, view_type)
    table = view_by_info['table']

    conditions = (db[table]['station_id'] == station_id)
    if duration:  # Duration duoc uu tien nhat so voi from/to
        duration = int(duration)
        # duration = datetime.now() - timedelta(days=duration)
        # Chi xuat toi da 7 ngay du lieu
        if duration == 1:
            duration = datetime.now() - timedelta(days=1)
        elif duration == 7:
            duration = datetime.now() - timedelta(days=7)
        else:
            duration = datetime.now() - timedelta(days=15)
        # duration = datetime.now() - timedelta(days=7)
        conditions &= (db[table]['get_time'] >= duration)
    else:
        # Chi xuat toi da 7 ngay du lieu
        if from_date and to_date:
            from_date = date_util.string_to_datetime(from_date)
            to_date = date_util.string_to_datetime(to_date)
        # if (to_date - from_date).days > 7:
        #    to_date = from_date + timedelta(days=7)
        elif from_date:
            from_date = date_util.string_to_datetime(from_date)
            if (request.now - from_date).days > 7:
                to_date = from_date + timedelta(days=30)
            else:
                to_date = request.now
        elif to_date:
            to_date = date_util.string_to_datetime(to_date)
            from_date = to_date - timedelta(days=30)
        else:
            if table == 'data_mon':
                to_date = request.now
                from_date = to_date - timedelta(days=365)
            else:
                to_date = request.now
                from_date = to_date - timedelta(days=30)

        conditions &= (db[table]['get_time'] >= from_date)
        conditions &= (db[table]['get_time'] <= to_date)

    if is_exceed and table == 'data_min':
        conditions &= (db[table]['is_exceed'] == True)

    if data_type:
        if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
            conditions &= (db[table]['is_approved'] == False)
        elif data_type == const.DATA_TYPE['APPROVED']['value']:
            conditions &= (db[table]['is_approved'] == True)

    list_data = db(conditions).select(db[table].id,
                                      db[table].get_time,
                                      db[table].data,
                                      orderby=db[table].get_time)

    conditions = (db.station_indicator.station_id == station_id)
    conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    # conditions &= (db.station_indicator.is_public == True)
    indicator_ids_data = db(conditions).select(db.station_indicator.indicator_id)
    indicator_ids = []
    for row in indicator_ids_data:
        indicator_ids.append(row.indicator_id)
    indicators_header = db(db.indicators.id.belongs(indicator_ids)).select(db.indicators.id, db.indicators.indicator,
                                                                           db.indicators.unit)

    import csv
    # Get station name
    station = db.stations(station_id)
    station_name = station.station_name if station else ''
    file_name = request.now.strftime(station_name + '_%Y%m%d_%H%M%S.csv')
    file_path = os.path.join(request.folder, 'static', 'export', file_name)

    with open(file_path, mode='wb') as out_file:
        writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if list_data.first() is None:
            raise HTTP(400, "Không đủ dữ liệu xuất CSV, vui lòng thử lại!")
        else:
            row = []
            headers = [T('#'), T('Indicator'), T('Max value'), T('Max time'), T('Min value'), T('Min time'),
                       T('Average value')]
            for header in headers:
                row.append(header)
            writer.writerow(row)

            indicators = dict()
            for row in indicators_header:
                indicators[str(row.indicator)] = {
                    'min_value': 999999999,
                    'min_time': '',
                    'has_min': False,
                    'max_value': -999999999,
                    'max_time': '',
                    'has_max': False,
                    'total': 0,
                    'qty': 0,
                    'unit': row.unit,
                }

            # Duyet tung phan tu trong mang du lieu vua truy van duoc
            for item in list_data:
                data = item.data
                for k in data:
                    if indicators.has_key(k):
                        v = data[k]
                        if v:
                            try:
                                v = float(v)
                                indicators[k]['total'] += v
                                indicators[k]['qty'] += 1
                                if not indicators[k]['has_min'] or indicators[k]['min_value'] > v:
                                    indicators[k]['has_min'] = True
                                    indicators[k]['min_value'] = v
                                    indicators[k]['min_time'] = item.get_time
                                if not indicators[k]['has_max'] or indicators[k]['max_value'] < v:
                                    indicators[k]['has_max'] = True
                                    indicators[k]['max_value'] = v
                                    indicators[k]['max_time'] = item.get_time
                            except:
                                pass

            iTotalRecords = 0
            for k in indicators:
                iTotalRecords += 1
                row = [
                    str(iTotalRecords),
                    '%s(%s)' % (k, indicators[k]['unit']),
                    '%0.2f' % indicators[k]['max_value'] if indicators[k]['has_max'] else '',
                    indicators[k]['max_time'] if indicators[k]['has_max'] else '',
                    '%0.2f' % indicators[k]['min_value'] if indicators[k]['has_min'] else '',
                    indicators[k]['min_time'] if indicators[k]['has_min'] else '',
                    '%0.2f' % (indicators[k]['total'] / indicators[k]['qty']) if indicators[k]['qty'] else '',
                ]
                writer.writerow(row)

    data = open(file_path, "rb").read()
    os.unlink(file_path)
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

    return data


# ################################################################################
# @decor.requires_login()
def export_excel():
    import os.path, openpyxl
    # get search parameters
    ######################################
    start =  datetime.now()
    station_id = request.vars.station_id
    from_date = request.vars.from_date
    to_date = request.vars.to_date
    data_type = request.vars.data_type
    added_columns = request.vars.added_columns or ''
    if added_columns:
        added_columns = added_columns.split(',')
    if data_type:
        data_type = int(data_type)
    added_columns_decode = []
    for name in added_columns:
        name_decode = name.decode('utf-8')
        added_columns_decode.append(name_decode)


    duration = request.vars.duration
    is_exceed = request.vars.is_exceed
    view_type = request.vars.view_type or const.VIEW_BY['MINUTE']['value']

    if not station_id:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[],
                    message=T('Select a station for export data'), success=True)
    aaData = []  # Du lieu json se tra ve
    view_by_info = common.get_const_by_value(const.VIEW_BY, view_type)
    table = view_by_info['table']

    if data_type and (
            data_type == const.DATA_TYPE['YET_APPROVED']['value'] or data_type == const.DATA_TYPE['APPROVED'][
        'value']):
        view_by_info_adjust = common.get_const_by_value(const.VIEW_BY_ADJUST, view_type)
        table = view_by_info_adjust['table']

    conditions = (db[table]['station_id'] == station_id)
    if duration:  # Duration duoc uu tien nhat so voi from/to
        duration = int(duration)
        # duration = datetime.now() - timedelta(days=duration)
        # Chi xuat toi da 7 ngay du lieu
        # duration = datetime.now() - timedelta(days=7)
        if duration == 1:
            duration = datetime.now() - timedelta(days=1)
        elif duration == 7:
            duration = datetime.now() - timedelta(days=7)
        else:
            duration = datetime.now() - timedelta(days=15)
        conditions &= (db[table]['get_time'] >= duration)
    else:
        # Chi xuat toi da 7 ngay du lieu
        if from_date and to_date:
            from_date = date_util.string_to_datetime(from_date)
            to_date = date_util.string_to_datetime(to_date) + timedelta(days=1)
        # if (to_date - from_date).days > 7:
        #    to_date = from_date + timedelta(days=7)
        elif from_date:
            from_date = date_util.string_to_datetime(from_date)
            if table != 'data_min' or table != 'data_adjust':
                to_date = from_date + timedelta(days=365)
            else:
                if (request.now - from_date).days > 7:
                    to_date = from_date + timedelta(days=30)
        elif to_date:
            to_date = date_util.string_to_datetime(to_date)
            if table != 'data_min' or table != 'data_adjust':
                from_date = to_date - timedelta(days=365)
            else:
                from_date = to_date - timedelta(days=30)
        else:
            if table == 'data_mon' or table == 'data_adjust':
                to_date = request.now
                from_date = to_date - timedelta(days=365)
            else:
                to_date = request.now
                from_date = to_date - timedelta(days=30)

        conditions &= (db[table]['get_time'] >= from_date)
        conditions &= (db[table]['get_time'] <= to_date)

    if is_exceed and table == 'data_min':
        conditions &= (db[table]['is_exceed'] == True)

    if data_type:
        if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
            if table != 'data_hour_adjust' and table != 'data_day_adjust' and table != 'data_mon_adjust':
                conditions &= (db[table]['is_approved'] == False)
        elif data_type == const.DATA_TYPE['APPROVED']['value']:
            if table != 'data_hour_adjust' and table != 'data_day_adjust' and table != 'data_mon_adjust':
                conditions &= (db[table]['is_approved'] == True)
    print "truoc select", datetime.now() - start
    start = datetime.now()
    if table != 'aqi_data_24h' and table != 'aqi_data_adjust_24h':
        list_data = db(conditions).select(db[table].id,
                                          db[table].get_time,
                                          db[table].data,
                                          orderby=db[table].get_time)
    else:
        list_data = db(conditions).select(db[table].id,
                                          db[table].get_time,
                                          db[table].data_24h,
                                          orderby=db[table].get_time)

    si_dict = dict()
    conditions = (db.station_indicator.station_id == station_id)
    conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    rows = db(conditions).select(db.station_indicator.ALL)
    indicator_ids = []
    for row in rows:
        indicator_ids.append(row.indicator_id)
        si_dict[str(row.indicator_id)] = row.as_dict()
    indicators = db(db.indicators.id.belongs(indicator_ids)).select(db.indicators.id, db.indicators.indicator,
                                                                    db.indicators.unit)
    print "data select", datetime.now() - start
    start = datetime.now()
    for i, item in enumerate(list_data):
        added_item = dict()
        if added_columns:
            for indicator in indicators:
                i_name = str(indicator.indicator)
                i_name_decode = i_name.decode('utf-8')
                v = item.data[i_name_decode] if item.data.has_key(i_name_decode) else ''
                if v == '' or v is None:
                    added_item[i_name] = '-'
                else:
                    try:
                        v = float(v)
                        added_item[i_name] = "{0:.2f}".format(v)
                    except:
                        added_item[i_name] = '-'


    print "process data", datetime.now() - start
    start = datetime.now()
    wb2 = openpyxl.Workbook(write_only=True)
    ws2 = wb2.create_sheet()
    if list_data.first() is None:
        raise HTTP(400, "Không đủ dữ liệu xuất excel, vui lòng thử lại!")
    else:
        # Write header
        # ws['A1'] = 'Datetime'
        temp_headers = []
        headers = []
        temp_headers.append('Datetime')
        for i, indicator in enumerate(added_columns):
            # ws[chr(ord('A') + i + 1) + '1'] = indicator.upper()
            temp_headers.append(indicator.upper())
        headers.append(temp_headers)
        for header in headers:
            ws2.append(header)

        # Write data
        temp_datas = []
        datas = []

        for i, item in enumerate(list_data):  # bo dem
                if table == 'data_mon':
                    list = item.get_time.strftime(datetime_format_vn).split(' ')[1].split('/')
                    list.pop(0)
                    # ws['A' + str(2 + i)] = list[0] + '/' + list[1]
                    temp_datas.append(list[0] + '/' + list[1])
                else:
                    # ws['A' + str(2 + i)] = item.get_time.strftime(datetime_format_vn)
                    temp_datas.append(item.get_time.strftime(datetime_format_vn))
                for j,indicator in enumerate(added_columns_decode):
                        if table != 'aqi_data_24h' and table != 'aqi_data_adjust_24h':
                            if item.data.has_key(indicator):
                                if item.data[indicator] is None or item.data[indicator] == 'NULL':
                                    # ws[chr(ord('A') + j + 1) + str(2 + i)] = '-'
                                    temp_datas.append('-')
                                else:
                                    # ws[chr(ord('A') + j + 1) + str(2 + i)] = item.data[indicator]
                                    temp_datas.append(item.data[indicator])
                            else:
                                # ws[chr(ord('A') + j + 1) + str(2 + i)] = '-'
                                temp_datas.append('-')
                        else:
                            if item.data_24h.has_key(indicator):
                                if item.data_24h[indicator] is None or item.data_24h[indicator] == 'NULL':
                                    # ws[chr(ord('A') + j + 1) + str(2 + i)] = '-'
                                    temp_datas.append('-')
                                else:
                                    # ws[chr(ord('A') + j + 1) + str(2 + i)] = item.data[indicator]
                                    temp_datas.append(item.data_24h[indicator])
                            else:
                                # ws[chr(ord('A') + j + 1) + str(2 + i)] = '-'
                                temp_datas.append('-')

                datas.append(temp_datas)
                temp_datas = []
        print "sau for ", datetime.now() - start
        start = datetime.now()
        for data in datas:
            ws2.append(data)

    # Get station name
    station = db.stations(station_id)
    station_name = station.station_name if station else ''
    if "," in station_name:
        station_name = station_name.replace("," , " ")
    file_name = request.now.strftime(station_name + '_%Y%m%d_%H%M%S.xlsx')
    file_path = os.path.join(request.folder, 'static', 'export', file_name)
    # wb.save(file_path)
    wb2.save(file_path)

    data = open(file_path, "rb").read()
    print "sau doc", datetime.now() - start
    start = datetime.now()
    os.unlink(file_path)
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

    return data


# ################################################################################
# @decor.requires_login()
def export_excel_min_max():
    import os.path, openpyxl
    # get search parameters
    station_id = request.vars.station_id
    from_date = request.vars.from_date
    to_date = request.vars.to_date
    data_type = request.vars.data_type
    if data_type:
        data_type = int(data_type)

    duration = request.vars.duration
    is_exceed = request.vars.is_exceed
    view_type = request.vars.view_type or const.VIEW_BY['MINUTE']['value']
    added_columns = request.vars.added_columns or ''
    if added_columns:
        added_columns = added_columns.split(',')

    if not station_id:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[],
                    message=T('Select a station for export data'), success=True)

    view_by_info = common.get_const_by_value(const.VIEW_BY, view_type)
    table = view_by_info['table']

    conditions = (db[table]['station_id'] == station_id)
    if duration:  # Duration duoc uu tien nhat so voi from/to
        duration = int(duration)
        # duration = datetime.now() - timedelta(days=duration)
        # Chi xuat toi da 7 ngay du lieu
        # duration = datetime.now() - timedelta(days=7)
        if duration == 1:
            duration = datetime.now() - timedelta(days=1)
        elif duration == 7:
            duration = datetime.now() - timedelta(days=7)
        else:
            duration = datetime.now() - timedelta(days=15)
        conditions &= (db[table]['get_time'] >= duration)
    else:
        # Chi xuat toi da 7 ngay du lieu
        if from_date and to_date:
            from_date = date_util.string_to_datetime(from_date)
            to_date = date_util.string_to_datetime(to_date) + timedelta(days=1)
        # if (to_date - from_date).days > 7:
        #    to_date = from_date + timedelta(days=7)
        elif from_date:
            from_date = date_util.string_to_datetime(from_date)
            if (request.now - from_date).days > 7:
                to_date = from_date + timedelta(days=30)
            else:
                if table == 'data_mon':
                    to_date = request.now
                else:
                    to_date = request.now
        elif to_date:
            to_date = date_util.string_to_datetime(to_date)
            from_date = to_date - timedelta(days=30)
        else:
            if table == 'data_mon':
                to_date = request.now
                from_date = to_date - timedelta(days=365)
            else:
                to_date = request.now
                from_date = to_date - timedelta(days=30)

        conditions &= (db[table]['get_time'] >= from_date)
        conditions &= (db[table]['get_time'] <= to_date)

    if is_exceed and table == 'data_min':
        conditions &= (db[table]['is_exceed'] == True)

    if data_type:
        if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
            conditions &= (db[table]['is_approved'] == False)
        elif data_type == const.DATA_TYPE['APPROVED']['value']:
            conditions &= (db[table]['is_approved'] == True)

    if table != 'aqi_data_24h' and table != 'aqi_data_adjust_24h':
        list_data = db(conditions).select(db[table].id,
                                          db[table].get_time,
                                          db[table].data,
                                          orderby=db[table].get_time)
    else:
        list_data = db(conditions).select(db[table].id,
                                          db[table].get_time,
                                          db[table].data_24h,
                                          orderby=db[table].get_time)

    conditions = (db.station_indicator.station_id == station_id)
    conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])


    # wb = openpyxl.load_workbook(
    #     filename=os.path.join(request.folder, 'static', 'export', 'Historical_data.xlsx'))
    # ws = wb.get_sheet_by_name('Sheet1')
    # sheet = wb.active

    wb2 = openpyxl.Workbook(write_only=True)
    ws2 = wb2.create_sheet()

    if list_data.first() is None:
        raise HTTP(400, "Không đủ dữ liệu xuất excel, vui lòng thử lại!")
    else:
        #lấy id của added_columns
        indicator_ids_data = db(conditions).select(db.station_indicator.indicator_id)
        id_indicator_station = []
        for id in indicator_ids_data:
            id_indicator_station.append(id.indicator_id)
        query = (db.indicators.id.belongs(id_indicator_station))
        query &= (db.indicators.indicator.belongs(added_columns))
        indicatorOrigin = db(query).select(db.indicators.id)
        id_addcolumns = []
        for item in indicatorOrigin:
            id_addcolumns.append(item.id)

        indicator_ids = id_addcolumns
        # for row in indicator_ids_data:
        #     indicator_ids.append(row.indicator_id)
        rows = db(db.indicators.id.belongs(indicator_ids)).select(db.indicators.id,
                                                                               db.indicators.indicator,
                                                                               db.indicators.unit)
        indicators = dict()
        for row in rows:
            name_str = str(row.indicator)
            name_decode = name_str.decode('utf-8')
            indicators[name_decode] = {
                'min_value': 999999999,
                'min_time': '',
                'has_min': False,
                'max_value': -999999999,
                'max_time': '',
                'has_max': False,
                'total': 0,
                'qty': 0,
                'unit': row.unit,
            }

            # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            if table != 'aqi_data_24h' and table != 'aqi_data_adjust_24h':
                data = item.data
            else:
                data = item.data_24h
            for k in data:
                if indicators.has_key(k):
                    v = data[k]
                    if v:
                        try:
                            v = float(v)
                            indicators[k]['total'] += v
                            indicators[k]['qty'] += 1
                            if not indicators[k]['has_min'] or indicators[k]['min_value'] > v:
                                indicators[k]['has_min'] = True
                                indicators[k]['min_value'] = v
                                indicators[k]['min_time'] = item.get_time
                            if not indicators[k]['has_max'] or indicators[k]['max_value'] < v:
                                indicators[k]['has_max'] = True
                                indicators[k]['max_value'] = v
                                indicators[k]['max_time'] = item.get_time
                        except:
                            pass

        iTotalRecords = 0
        # Write header
        headers = ['No.', 'Thông số', 'Giá trị Max', 'Thời gian Max', 'Giá trị Min', 'Thời gian Min',
                   'Giá trị trung bình']
        ws2.append(headers)
        for header in headers:
            pass

        # Write data

        for k in indicators:
            iTotalRecords += 1
            row = [
                str(iTotalRecords),
                '%s(%s)' % (k, indicators[k]['unit']),
                '%0.2f' % indicators[k]['max_value'] if indicators[k]['has_max'] else '',
                indicators[k]['max_time'] if indicators[k]['has_max'] else '',
                '%0.2f' % indicators[k]['min_value'] if indicators[k]['has_min'] else '',
                indicators[k]['min_time'] if indicators[k]['has_min'] else '',
                '%0.2f' % (indicators[k]['total'] / indicators[k]['qty']) if indicators[k]['qty'] else '',
            ]

            ws2.append(row)

    # Get station name
    station = db.stations(station_id)
    station_name = station.station_name if station else ''
    if "," in station_name:
        station_name = station_name.replace("," , " ")

    file_name = request.now.strftime(station_name + '_%Y%m%d_%H%M%S.xlsx')
    file_path = os.path.join(request.folder, 'static', 'export', file_name)
    wb2.save(file_path)

    data = open(file_path, "rb").read()
    os.unlink(file_path)
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

    return data


################################################################################
# hungdx issue 44 add (co the ap dung cho cac chon tinh, vung ... fix sau
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

        records = db(conditions).select(db[table][get_value_field], db[table][get_dsp_field],
                                        orderby=db[table].order_no)

        if records:
            html1 = "<option value=''>%s</option>" % T('-- Select an option --')
            html = ["<option value='%s'>%s</option>" % (item[get_value_field], item[get_dsp_field]) for item in records]
            html = html1 + ''.join(html)
        else:
            html = "<option value=''>%s</option>" % T('-- No data --')

        return dict(success=True, html=html)
    except Exception as ex:
        return dict(success=False, message=str(ex))
