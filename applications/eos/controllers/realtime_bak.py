# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

from applications.eos.modules import common
from datetime import datetime, timedelta

BP_AQI = {
    "I": {"1": 0.0, "2": 50.0, "3": 100.0, "4": 150.0, "5": 200.0, "6": 300.0, "7": 400.0, "8": 500.0},
    "O3": {"1": 0.0, "2": 160.0, "3": 200.0, "4": 300.0, "5": 400.0, "6": 800.0, "7": 1000.0, "8": 1200.0},
    "O38": {"1": 0.0, "2": 100.0, "3": 120.0, "4": 170.0, "5": 210.0, "6": 400.0, "7": None, "8": None},
    "CO": {"1": 0.0, "2": 10000.0, "3": 30000.0, "4": 45000.0, "5": 60000.0, "6": 90000.0, "7": 120000.0,
           "8": 150000.0},
    "SO2": {"1": 0.0, "2": 125, "3": 350.0, "4": 550.0, "5": 800.0, "6": 1600.0, "7": 2100.0, "8": 2630.0},
    "NO2": {"1": 0.0, "2": 100.0, "3": 200.0, "4": 700.0, "5": 1200.0, "6": 2350.0, "7": 3100.0, "8": 3850.0},
    "PM-10": {"1": 0.0, "2": 50.0, "3": 150.0, "4": 250.0, "5": 350.0, "6": 420.0, "7": 500.0, "8": 600.0},
    "PM-2-5": {"1": 0.0, "2": 25, "3": 50.0, "4": 80.0, "5": 150.0, "6": 250.0, "7": 350.0, "8": 500.0}
}

def call():
    return service()

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'realtime')))
def station():
    selected_st = request.vars.station_type or const.STATION_TYPE['SURFACE_WATER']['value']
    selected_st = int(selected_st)
    selected_st_name = common.get_info_from_const(const.STATION_TYPE, selected_st)['name'].upper() if common.get_info_from_const(const.STATION_TYPE, selected_st) else ''
    # indicators = db(db.indicators.indicator_type == selected_st).select(db.indicators.indicator, db.indicators.unit)
    default_provinces = db(db.provinces.default == 1).select()
    # stations = db(db.stations.station_type == selected_st).select(db.stations.id, db.stations.station_name) #hungdx comment issue 44

    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    conditions &= (db.stations.station_type == selected_st)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(db.stations.id, db.stations.station_name)
    # Select provinces to fill in dropdown box
    provinces = common.get_province_have_station()
    # Select stations to fill in dropdown box
    areas = db(db.areas.id > 0).select()
    # Trung Pham: filter indicators follow issue 210
    station_ids = [str(item.id) for item in stations]  # id các trạm
    rowsIndicators = db(db.station_indicator.station_id.belongs(station_ids)).select(db.station_indicator.indicator_id)  # id các indicator
    indicator_ids = [str(item.indicator_id) for item in rowsIndicators]  # id các indicator
    conditions = db.indicators.id.belongs(indicator_ids)
    conditions &= db.indicators.indicator_type == selected_st
    indicators = db(conditions).select(db.indicators.indicator, db.indicators.unit, db.indicators.id)
    # end issue 210

    return dict(indicators=indicators, selected_st=selected_st, selected_st_name=T(selected_st_name), stations=stations,
                provinces = provinces, areas = areas, default_provinces=default_provinces)


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'realtime')) or (auth.has_permission('view', 'qa_qc')))
def qa_qc():
    # Select areas to fill in dropdown box
    areas = db(db.areas.id > 0).select()
    # Select provinces to fill in dropdown box
    provinces = common.get_province_have_station()
    # Select stations to fill in dropdown box
    #stations = db(db.stations.id > 0).select(orderby=~db.stations.station_name)#hungdx comment issue 44

    # hungdx phan quyen quan ly trạm theo user issue 44
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
    stations = db(conditions).select(orderby=~db.stations.station_name)

    to_date = request.now
    from_date = to_date - timedelta(days=3)
    from_date = from_date.strftime('%Y-%m-%d')
    to_date = to_date.strftime('%Y-%m-%d')

    return dict(provinces = provinces, areas = areas, stations = stations, from_date=from_date, to_date=to_date)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'realtime')))
def get_list_log_lastest(*args, **kwargs):
    try:
        from datetime import datetime, timedelta
        from w2pex import date_util
        dictStation = {}
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        selected_st = request.vars.station_type
        station_id = str(request.vars.station_id)
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        area_id = request.vars.area_id
        province_id = request.vars.province_id
        data_type = request.vars.data_type
        if data_type:
            data_type = int(data_type)
        data_filter_by = request.vars.data_filter_by
        if data_filter_by:
            data_filter_by = data_filter_by.split(';')
        is_qa_qc = request.vars.is_qa_qc

        status = request.vars.alarm_level
        s_search = request.vars.sometext
        added_columns = request.vars.added_columns or ''
        if added_columns:
            added_columns = added_columns.split(',')
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
        table = 'data_lastest'
        if is_qa_qc:
            if not station_id:
                return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], success=True)
            table = 'data_min'
            if data_type and (data_type == const.DATA_TYPE['YET_APPROVED']['value'] or data_type == const.DATA_TYPE['APPROVED']['value']):
                table = 'data_adjust'
        conditions = (db[table]['id'] > 0)
        if data_type:
            if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
                conditions &= (db[table]['is_approved'] == False)
            elif data_type == const.DATA_TYPE['APPROVED']['value']:
                conditions &= (db[table]['is_approved'] == True)
        if from_date:
            conditions &= (db[table]['get_time'] >= date_util.string_to_datetime(from_date))
        if to_date:
            conditions &= (db[table]['get_time'] < date_util.string_to_datetime(to_date) + timedelta(days = 1))

        station_status = dict()
        if selected_st:
            conditions2 = (db.stations.station_type == selected_st)
            if status:
                #if station_status in ['1', '2', '0']:
                if status in ['1', '2', '0']:
                    conditions2 &= (db.stations.status.belongs([1, 2, 0]))
                else:
                    conditions2 &= (db.stations.status == status)
            if area_id:
                conditions2 &= (db.stations.area_id == area_id)
            if province_id:
                conditions2 &= (db.stations.province_id == province_id)
            # hungdx phan quyen quan ly trạm theo user issue 44
            if current_user:
                if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                    list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                        db.manager_stations.station_id)
                    station_ids = [str(item.station_id) for item in list_station_manager]
                    conditions2 &= (db.stations.id.belongs(station_ids))

            rows = db(conditions2).select(db.stations.id, db.stations.status, db.stations.order_no, orderby=db.stations.order_no)
            station_ids = ['']
            for row in rows:
                dictStation[str(row.id)] = row.order_no
                station_ids.append(str(row.id))
                station_status[str(row.id)] = row.status
            conditions &= (db[table]['station_id'].belongs(station_ids))

        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if s_search:
            conditions &= ((db[table]['station_id'].contains(s_search)) |
                           (db[table]['data'].contains(s_search)))
        if station_id:
            conditions &= (db[table]['station_id'] == station_id)

        time = db(conditions).select(db[table]['get_time'])
        # times = db(conditions).select(db.data_lastest.get_time)
        # if times:
        #     for i in times:
        #         get_time  = i.get_time

        list_data = db(conditions).select(  db[table]['id'],
                                            db[table]['station_id'],
                                            db[table]['get_time'],
                                            db[table]['is_exceed'],
                                            db[table]['data'],
                                            db[table]['data_status'],
                                            limitby = limitby,
                                            orderby=~db[table]['get_time']
                                            )
        # for item in get_time:
        #     list_data.append(item.data_lastest.get_time)

        if data_type == const.DATA_TYPE['ORIGINAL_DATA']['value']:
            # If is Original Data, load data_adjust in order to compare on list
            table2 = 'data_adjust'
            conditions2 = (db[table2]['id'] > 0)
            conditions2 &= (db[table2]['station_id'] == station_id)
            list_data2 = db(conditions2).select(  db[table2]['id'],
                                                db[table2]['station_id'],
                                                db[table2]['get_time'],
                                                db[table2]['is_exceed'],
                                                db[table2]['data'],
                                                db[table]['data_status'],
                                                limitby = limitby)

        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        iRow = iDisplayStart + 1
        res = common.get_station_dict()
        station_dict_name = res[0]
        station_dict_status = res[2]

        si_dict =  dict()
        conditions = (db.station_indicator.id > 0)
        conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        if selected_st:
            conditions &= (db.station_indicator.station_type == selected_st)
        rows = db(conditions).select(db.station_indicator.ALL)
        for row in rows:
            si_dict[str(row.station_id), str(row.indicator_id)] = row.as_dict()
        indicators = db(db.indicators.indicator_type == selected_st).select(db.indicators.id, db.indicators.indicator, db.indicators.unit)
        icon = BR() + I('',_class = "fa fa-times-circle-o",_style="color: red")

        # add order
        for i, item in enumerate(list_data):
            if dictStation[item.station_id]:
                item['order_no'] = dictStation[item.station_id]
            else:
                item['order_no'] = i

                # sort by order no

        list_data = sorted(list_data, key=lambda x: x.order_no, reverse=False)
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
        # for i, item in enumerate(sorted(list_data, key=list_data.__getitem__, reverse=True)):
            added_item = dict()
            if added_columns:
                for indicator in indicators:
                    i_id = str(indicator.id)
                    i_name = str(indicator.indicator)
                    i_name_decode = i_name.decode('utf-8')
                    v = ''
                    data_status = ''
                    if item.data:
                        v = item.data[i_name_decode] if item.data.has_key(i_name_decode) else ''
                    if item.data_status:
                        data_status = item.data_status[i_name_decode]['status'] if item.data_status.has_key(i_name_decode) else ''
                    if v or v == 0:
                        try:
                            v = float(v)
                            if data_filter_by:
                                is_valid = False
                                for data_filter in data_filter_by:
                                    if str(const.DATA_FILTER_BY['IS_ZERO']['value']) == data_filter:
                                        if v == 0:
                                            is_valid = True
                                            break
                                    elif str(const.DATA_FILTER_BY['NEGATIVE']['value']) == data_filter:
                                        if v < 0:
                                            is_valid = True
                                            break
                                    elif str(const.DATA_FILTER_BY['OUT_OF_RANGE']['value']) == data_filter:
                                        pass
                                if not is_valid:
                                    html = '-' # Todo: Gia tri k theo dung dieu kien loc thi cung khong cho phep thay doi
                                    added_item[i_name] = html
                                    continue
                            # Lay thong tin cac nguong de display title khi hover len gtri
                            title = ''
                            station_id = str(item['station_id'])
                            key = (station_id,i_id)
                            if si_dict.has_key(key):
                                data = si_dict[station_id,i_id]
                                qcvn_detail_min_value = data['qcvn_detail_min_value']
                                qcvn_detail_max_value = data['qcvn_detail_max_value']

                                if qcvn_detail_min_value and qcvn_detail_max_value:
                                    # So sanh <= ... <=
                                    title = 'QCVN Min: %s' % qcvn_detail_min_value
                                    title = title + ' - QCVN Max: %s' % qcvn_detail_max_value
                                else:
                                    if qcvn_detail_max_value:
                                        title = 'QCVN Max: %s' % qcvn_detail_max_value
                                    elif qcvn_detail_min_value:
                                        title = 'QCVN Min: %s' % qcvn_detail_min_value

                                # if v <= si_dict[i_id]['tendency_value']:
                                #     title = 'Tendency value : %s' % si_dict[i_id]['tendency_value']
                                # elif v <= si_dict[i_id]['preparing_value']:
                                #     title = 'Preparing value : %s' % si_dict[i_id]['preparing_value']
                                # else:
                                #     title = 'Limit value : %s' % si_dict[i_id]['exceed_value']

                            c = common.getColorByIndicatorQcvn2(v, qcvn_detail_min_value, qcvn_detail_max_value)
                            html = SPAN("{0:.2f}".format(v), _style="background:%s; color:white" %c, _class="badge", _title= title)
                            if (data_status == 2):
                                html += icon
                            if is_qa_qc:
                                if data_type == const.DATA_TYPE['ORIGINAL_DATA']['value'] or data_type == const.DATA_TYPE['YET_APPROVED']['value']:
                                    html += INPUT(_class='inline_adjust', _style="display: none;", _value=v, data=dict(table=table, indicator=i_name, id=item.id, oldValue=v))
                            # adjust_data
                            if data_type == const.DATA_TYPE['ORIGINAL_DATA']['value']:
                                adjust_data = get_adjust_value_by_original_record(item, list_data2, i_name)
                                if adjust_data != False:
                                    try:
                                        adjust_data = float(adjust_data)
                                        html += SPAN('({0:.2f})'.format(adjust_data))
                                    except:
                                        pass
                            added_item[i_name] = html
                        except:
                            html = SPAN('-')
                            if (data_status == 2):
                                html += icon
                            if is_qa_qc:
                                if data_type == const.DATA_TYPE['ORIGINAL_DATA']['value'] or data_type == \
                                        const.DATA_TYPE['YET_APPROVED']['value']:
                                    html += INPUT(_class='inline_adjust', _style="display: none;", _value=v,
                                                  data=dict(table=table, indicator=i_name, id=item.id, oldValue=''))
                            added_item[i_name] = html
                    else:
                        html = SPAN('-')
                        if (data_status == 2):
                            html += icon
                        if is_qa_qc:
                            if data_type == const.DATA_TYPE['ORIGINAL_DATA']['value'] or data_type == \
                                    const.DATA_TYPE['YET_APPROVED']['value']:
                                html += INPUT(_class='inline_adjust', _style="display: none;", _value=v,
                                              data=dict(table=table, indicator=i_name, id=item.id, oldValue=''))
                        added_item[i_name] = html

            # Get status info for item
            status_info = const.STATION_STATUS['GOOD']
            for ss in const.STATION_STATUS:
                if station_status.has_key(str(item.station_id)):
                    if station_status[str(item.station_id)] == const.STATION_STATUS[ss]['value']:
                        status_info = const.STATION_STATUS[ss]
            # hungdx comment 28/5/2019
            # if item.get_time > request.now:
            #     item.get_time = request.now
            row = [
                str(iRow + i),
            ]
            if is_qa_qc:
                row.append(INPUT(_type='checkbox', _class='select_item', _group=0, _value=item.id))
                pass
            else:
                # row.append(A(I(_class=status_info['icon'],_style=' font-size: 16px !important; color: %s' % (status_info['color'])),_href=URL('detail', args=[item.station_id])))
                row.append(A(I(_class=status_info['icon'], _style=' font-size: 16px !important; color: %s' %(status_info['color']))))

            row.append(station_dict_name.get(str(item.station_id)))
            # row.append(item.get_time.strftime('%Y-%m-%d %H-%M'))
            if item.get_time :
                row.append(item.get_time.strftime(datetime_format_vn))
            else :
                row.append("-")
            for column in added_columns:
                if column and added_item.has_key(column):
                    row.append(added_item[column])

            row.append(A(I(_class='fa fa-bar-chart-o text-info'), _href=URL('detail_graph', args=[item.station_id])))
            row.append(A(I(_class='fa fa-video-camera text-success'),_href=URL('realtime', 'detail_camera', args=[item.station_id])))
            row.append(A(I(_class='fa fa-map-marker text-danger'), _href=URL('station', 'map', args=[item.station_id])))
            aaData.append(row)

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'realtime')))
def approve_data_adjust(*args, **kwargs):
    try:
        import json
        array_data = request.vars.data
        array_data = json.loads(array_data)
        list_ids = []
        for k in array_data:
            list_ids.append(k)
            array_data[k] = array_data[k].split(';')
        conditions = (db.data_adjust.id.belongs(list_ids))
        db(conditions).update(is_approved=True)
        # Insert or update to data_approve
        rows = db(conditions).select(db.data_adjust.ALL, orderby=db.data_adjust.get_time)
        for row in rows:
            conditions = (db.data_approve.station_id == row.station_id)
            conditions &= (db.data_approve.get_time == row.get_time)
            data = {}
            for k in array_data[str(row.id)]:
                if row.data.has_key(k):
                    data[k] = row.data[k]
            db.data_approve.update_or_insert(conditions, station_id=row.station_id, get_time=row.get_time, data=data)
            try:
                calcu_update(row.station_id, row.get_time)
            except Exception as ex:
                logger.info('hungdx except %s', str(ex))
            db.commit()
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'realtime')) or (auth.has_permission('view', 'qa_qc')))
def get_list_qa_qc(*args, **kwargs):
    try:
        from datetime import datetime, timedelta
        from w2pex import date_util
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        selected_st = request.vars.station_type
        station_id = request.vars.station_id
        from_date = request.vars.from_date
        to_date = request.vars.to_date
        area_id = request.vars.area_id
        province_id = request.vars.province_id
        data_type = request.vars.data_type
        if data_type:
            data_type = int(data_type)
        data_filter_by = request.vars.data_filter_by
        if data_filter_by:
            data_filter_by = data_filter_by.split(';')
        is_qa_qc = request.vars.is_qa_qc

        status = request.vars.alarm_level
        s_search = request.vars.sometext
        added_columns = request.vars.added_columns or ''
        if added_columns:
            added_columns = added_columns.split(',')
        aaData = []
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
        table = 'data_lastest'
        if is_qa_qc:
            if not station_id:
                return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], success=True)
            table = 'data_min'
            if data_type:
                if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
                    table = 'data_adjust'
                elif data_type == const.DATA_TYPE['APPROVED']['value']:
                    table = 'data_approve'
        conditions = (db[table]['id'] > 0)
        if data_type:
            if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
                conditions &= (db[table]['is_approved'] == False)
        if from_date:
            conditions &= (db[table]['get_time'] >= date_util.string_to_datetime(from_date))
        if to_date:
            conditions &= (db[table]['get_time'] < date_util.string_to_datetime(to_date) + timedelta(days = 1))

        station_status = dict()
        if selected_st:
            conditions2 = (db.stations.station_type == selected_st)
            if status:
                conditions2 &= (db.stations.status == status)
            if area_id:
                conditions2 &= (db.stations.area_id == area_id)
            if province_id:
                conditions2 &= (db.stations.province_id == province_id)

            rows = db(conditions2).select(db.stations.id, db.stations.status)
            station_ids = ['']
            for row in rows:
                station_ids.append(str(row.id))
                station_status[str(row.id)] = row.status
            conditions &= (db[table]['station_id'].belongs(station_ids))

        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if s_search:
            conditions &= ((db[table]['station_id'].contains(s_search)) |
                           (db[table]['data'].contains(s_search)))
        if station_id:
            conditions &= (db[table]['station_id'] == station_id)
        if table == 'data_adjust':
            conditions &= (db[table]['del_flag'] != True)

        list_data = db(conditions).select( db[table]['id'],
                                            db[table]['station_id'],
                                            db[table]['get_time'],
                                            db[table]['is_exceed'],
                                            db[table]['data'],
                                            orderby=~db[table]['get_time'],
                                            limitby = limitby)
        if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
            # If is 'YET_APPROVED', load data_adjust in order to compare on list
            # Todo: Toi uu de lay dung nhung ban ghi nhu list_data
            table2 = 'data_min'
            conditions2 = (db[table2]['id'] > 0)
            conditions2 &= (db[table2]['station_id'] == station_id)
            if from_date:
                conditions2 &= (db[table2]['get_time'] >= date_util.string_to_datetime(from_date))
            if to_date:
                conditions2 &= (db[table2]['get_time'] < date_util.string_to_datetime(to_date) + timedelta(days = 1))
            list_data2 = db(conditions2).select(  db[table2]['id'],
                                                db[table2]['station_id'],
                                                db[table2]['get_time'],
                                                db[table2]['is_exceed'],
                                                db[table2]['data'],
                                                orderby=~db[table]['get_time'])

        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count()
        iRow = iDisplayStart + 1
        res = common.get_station_dict()
        station_dict_name = res[0]
        station_dict_status = res[2]

        si_dict =  dict()
        conditions = (db.station_indicator.id > 0)
        conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
        if selected_st:
            conditions &= (db.station_indicator.station_type == selected_st)
        if station_id:
            conditions &= (db.station_indicator.station_id == station_id)
        rows = db(conditions).select(db.station_indicator.ALL)
        si_ids = [] # list of indicators id
        for row in rows:
            si_dict[str(row.indicator_id)] = row.as_dict()
            si_ids.append(row.indicator_id)
        conditions = (db.indicators.id > 0)
        if selected_st:
            conditions &= (db.indicators.indicator_type == selected_st)
        if si_ids:
            conditions &= (db.indicators.id.belongs(si_ids))
        indicators = db(conditions).select(db.indicators.id, db.indicators.indicator, db.indicators.unit)

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            added_item = dict()
            if added_columns:
                for indicator in indicators:
                    i_id = str(indicator.id)
                    i_name = str(indicator.indicator)
                    i_name_decode = i_name.decode('utf-8')
                    if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
                        v = ''
                        adjust_data = get_adjust_value_by_original_record(item, list_data2, i_name_decode)
                        if adjust_data != False:
                            try:
                                v = float(adjust_data)
                            except:
                                v = ''
                    else:
                        v = item.data[i_name_decode] if item.data.has_key(i_name_decode) else ''
                    if not v:
                        html = SPAN('-')
                        if is_qa_qc:
                            if data_type == const.DATA_TYPE['ORIGINAL_DATA']['value'] or data_type == const.DATA_TYPE['YET_APPROVED']['value']:
                                html += INPUT(_class='inline_adjust', _style="display: none;", _value=v, data=dict(table=table, indicator=i_name, id=item.id, oldValue=''))
                        added_item[i_name] = html
                    else:
                        try:
                            v = float(v)
                            if data_filter_by:
                                is_valid = False
                                for data_filter in data_filter_by:
                                    if str(const.DATA_FILTER_BY['IS_ZERO']['value']) == data_filter:
                                        if v == 0:
                                            is_valid = True
                                            break
                                    elif str(const.DATA_FILTER_BY['NEGATIVE']['value']) == data_filter:
                                        if v < 0:
                                            is_valid = True
                                            break
                                    elif str(const.DATA_FILTER_BY['OUT_OF_RANGE']['value']) == data_filter:
                                        pass
                                if not is_valid:
                                    html = SPAN('-') # Todo: Gia tri k theo dung dieu kien loc thi cung khong cho phep thay doi
                                    added_item[i_name] = html
                                    continue
                            # Lay thong tin cac nguong de display title khi hover len gtri
                            title = ''
                            if si_dict.has_key(i_id):
                                data = si_dict[i_id]
                                qcvn_detail_min_value = data['qcvn_detail_min_value']
                                qcvn_detail_max_value = data['qcvn_detail_max_value']

                                if qcvn_detail_min_value and qcvn_detail_max_value:
                                    # So sanh <= ... <=
                                    title = 'QCVN Min: %s' % si_dict[i_id]['qcvn_detail_min_value']
                                    title = title + ' - QCVN Max: %s' % si_dict[i_id]['qcvn_detail_max_value']
                                else:
                                    if qcvn_detail_max_value:
                                        title = 'QCVN Max: %s' % si_dict[i_id]['qcvn_detail_max_value']
                                    elif qcvn_detail_min_value:
                                        title = 'QCVN Min: %s' % si_dict[i_id]['qcvn_detail_min_value']

                            c = common.getColorByIndicatorQcvn(si_dict, i_id, v)
                            html = SPAN("{0:.2f}".format(v), _style="background:%s; color:white" %c, _class="badge", _title= title)
                            if is_qa_qc:
                                if data_type == const.DATA_TYPE['ORIGINAL_DATA']['value'] or data_type == const.DATA_TYPE['YET_APPROVED']['value']:
                                    html += INPUT(_class='inline_adjust', _style="display: none;", _value=v, data=dict(table=table, indicator=i_name, id=item.id, oldValue=v))
                            # adjust_data
                            if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
                                v = item.data[i_name_decode] if item.data.has_key(i_name_decode) else ''
                                if v:
                                    try:
                                        v = float(v)
                                        html += SPAN('({0:.2f})'.format(v))
                                    except:
                                        pass
                            added_item[i_name] = html
                        except:
                            html = SPAN('-')
                            if is_qa_qc:
                                if data_type == const.DATA_TYPE['ORIGINAL_DATA']['value'] or data_type == \
                                        const.DATA_TYPE['YET_APPROVED']['value']:
                                    html += INPUT(_class='inline_adjust', _style="display: none;", _value=v,
                                                  data=dict(table=table, indicator=i_name, id=item.id, oldValue=''))
                            added_item[i_name] = html

            # Get status info for item
            status_info = const.STATION_STATUS['GOOD']
            for ss in const.STATION_STATUS:
                if station_status.has_key(str(item.station_id)):
                    if station_status[str(item.station_id)] == const.STATION_STATUS[ss]['value']:
                        status_info = const.STATION_STATUS[ss]
            # hungdx comment 28/5/2019
            # if item.get_time > request.now:
            #     item.get_time = request.now
            row = [
                str(iRow + i),
            ]
            if is_qa_qc:
                row.append(INPUT(_type='checkbox', _class='select_item column_item row_all', _row=i, _column=0, _group=0, _value=item.id))
                pass
            else:
                row.append(A(I(_class=status_info['icon'], _style='color: %s' %(status_info['color'])),  _href = URL('detail', args = [item.station_id])))
                row.append(A(I(_class='fa fa-bar-chart-o text-info'), _href = URL('detail_graph', args = [item.station_id])))
                row.append(A(I(_class='fa fa-video-camera text-success'), _href = URL('camera_links', 'index', args = [item.station_id])))
                row.append(A(I(_class='fa fa-map-marker text-danger'), _href = URL('station', 'map', args = [item.station_id])))
            row.append(station_dict_name.get(str(item.station_id)))
            # row.append(item.get_time.strftime('%Y-%m-%d %H-%M'))
            row.append(item.get_time.strftime(datetime_format_vn))
            idx_column = 0
            for column in added_columns:
                if column and added_item.has_key(column):
                    if data_type == const.DATA_TYPE['YET_APPROVED']['value']:
                        idx_column += 1
                        row.append(added_item[column] + INPUT(_type='checkbox', _class='column_item row_item', _row=i, _column=idx_column, _group=0, _value=column))
                    else:
                        row.append(added_item[column])
            aaData.append(row)

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'realtime')))
def remove_data_adjust(*args, **kwargs):
    try:
        import json
        array_data = request.vars.data
        array_data = json.loads(array_data)
        list_ids = []
        for k in array_data:
            list_ids.append(k)
            array_data[k] = array_data[k].split(';')
        conditions = (db.data_adjust.id.belongs(list_ids))
        # issue 209
        #rows = db(conditions).select(db.data_adjust.ALL)
        rows = db(conditions).select(db.data_adjust.ALL, orderby=db.data_adjust.get_time)
        for row in rows:
            data = row.data
            k = str(row.id)
            if array_data.has_key(k):
                for k1 in array_data[k]:
                    if data.has_key(k1):
                        del data[k1]
            row.update_record(data = data)
            try:
                calcu_update(row.station_id, row.get_time)
            except Exception as ex:
                logger.info('hungdx except %s', str(ex))
            db.commit()

        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'realtime')))
def reject_data_adjust(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        conditions = (db.data_approve.id.belongs(list_ids))
        rows = db(conditions).select(db.data_approve.ALL)
        for row in rows:
            conditions2 = (db.data_adjust.station_id == row.station_id)
            conditions2 &= (db.data_adjust.get_time == row.get_time)
            db(conditions2).update(is_approved=False)
        db(conditions).delete()
        # Update flag for data_adjust
        rows = db(conditions).select(db.data_approve.ALL)
        return dict(success=True)
    except Exception as ex:
        return dict(success=False, message=str(ex))

################################################################################
def get_adjust_value_by_original_record(record, rows, indicator):
    try:
        for row in rows:
            if row.station_id == record.station_id and row.get_time == record.get_time:
                return row.data[indicator] if row.data.has_key(indicator) else False
        return False
    except Exception as ex:
        return False

################################################################################
def getPercentByIndicator(si_dict, id, value):
    try:
        p = 0
        if si_dict.has_key(id):
            data = si_dict[id]
            try:
                tendency = float(data['tendency_value'])
                preparing = float(data['preparing_value'])
                exceed = float(data['exceed_value'])
                p = float(value) * 100 / exceed
            except:
                p = 0

        return int(p)
    except Exception as ex:
        return 0

################################################################################
def getLimitValueByIndicator(si_dict, id):
    try:
        exceed = 0
        if si_dict.has_key(id):
            data = si_dict[id]
            exceed = float(data['exceed_value'])

        return exceed
    except Exception as ex:
        return 0

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'realtime')))
def detail():
    station_id = request.args(0)
    station_info = db(db.data_lastest.station_id == station_id).select().first() or None
    station = db.stations(station_id)
    selected_st = station.station_type if station else ''
    selected_st = int(selected_st)
    selected_st_name = common.get_info_from_const(const.STATION_TYPE, selected_st)['name'] if common.get_info_from_const(const.STATION_TYPE, selected_st) else ''
    indicators = db(db.indicators.indicator_type == selected_st).select(db.indicators.id, db.indicators.indicator, db.indicators.unit)
    items = []
    if station_info:
        si_dict =  common.get_station_indicator_by_station(station_type=selected_st)
        for indicator in indicators:
            i_id = str(indicator.id)
            i_name = str(indicator.indicator)
            i_name_decode = i_name.decode('utf-8')
            v = station_info.data[i_name_decode] if station_info.data.has_key(i_name_decode) else ''
            if v:
                try:
                    v = float(v)
                    c = common.getColorByIndicator(si_dict, i_id, v)
                    item = {
                        'name': i_name,
                        'value': "{0:.2f}".format(v),
                        'unit': indicator.unit,
                        'color': c,
                        'percent': getLimitValueByIndicator(si_dict, i_id),
                    }
                    items.append(item)
                except:
                    pass
    return dict(station_info=station_info, selected_st=selected_st, station=station, selected_st_name=selected_st_name, items=items)

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'realtime')))
def detail_graph():
    station_id = request.args(0)
    station_info = db(db.data_lastest.station_id == station_id).select().first() or None
    station = db.stations(station_id)
    selected_st = station.station_type if station else ''
    selected_st = int(selected_st)
    selected_st_name = common.get_info_from_const(const.STATION_TYPE, selected_st)['name'] if common.get_info_from_const(const.STATION_TYPE, selected_st) else ''

    conditions = (db.station_indicator.station_id == station_id)
    conditions &= (db.station_indicator.status == const.SI_STATUS['IN_USE']['value'])
    rows2 = db(conditions).select(db.station_indicator.indicator_id, distinct=True)
    indicators_id = []
    for row in rows2:
        indicators_id.append(row.indicator_id)
    indicators = db(db.indicators.id.belongs(indicators_id)).select(db.indicators.ALL)
    return dict(station_info=station_info, selected_st=selected_st, station=station, selected_st_name=selected_st_name, indicators=indicators)

 ################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'realtime')))
def detail_camera():
    station_id = request.args(0)
    station_info = db(db.data_lastest.station_id == station_id).select().first() or None
    station = db.stations(station_id)
    selected_st = station.station_type if station else ''
    selected_st = int(selected_st)
    selected_st_name = common.get_info_from_const(const.STATION_TYPE, selected_st)['name'] if common.get_info_from_const(const.STATION_TYPE, selected_st) else ''
    cameras = db(db.camera_links.station_id == station_id).select(db.camera_links.ALL, orderby=db.camera_links.order_no)
    return dict(station_info=station_info, station=station, selected_st_name=selected_st_name, cameras=cameras)


################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'realtime')))
def get_list_indicators_by_statios(*args, **kwargs):
    try:
        html = ''
        station_id = request.vars.station_id
        station_type = request.vars.station_type
        iDisplayStart = int(0)
        iDisplayLength = int(20)
        conditions = (db.station_indicator.station_id == station_id)
        rowsIndicators = db(conditions).select(db.station_indicator.indicator_id)
        # if no station_id
        if not station_id:
            conditions = (db.stations.id > 0)
            conditions &= (db.stations.station_type == station_type)
            stations = db(conditions).select(db.stations.id, db.stations.station_name)
            station_ids = [str(item.id) for item in stations]  # id các trạm
            rowsIndicators = db(db.station_indicator.station_id.belongs(station_ids)).select(db.station_indicator.indicator_id)
        #end if
        indicators = []
        for row in rowsIndicators:
            indicators.append(row.indicator_id)
        rowsIndicators = db(db.indicators.id.belongs(indicators)).select(db.indicators.ALL)
        # print(rowColumnShow)
        for row in rowsIndicators:
            indicatorShow = row.indicator
            html += '<option value="%(value)s" selected>%(name)s (%(unit)s)</option>' % dict(value=row.indicator, name=indicatorShow, unit=row.unit)
        return dict(success=True, html=html)
    except Exception as ex:
        return dict(success=False, html=html)

#########################################################################################
#hungdx update data hieu chuan

def calcu_update(station_id, time_cal):
    hour_data_adjust_calc(station_id, time_cal + timedelta(minutes=-1))
    hour_8h_data_adjust_calc(station_id, time_cal)
    day_data_adjust_calc(station_id,time_cal)
    mon_data_adjust_calc(station_id, time_cal)
    calc_aqi_data_adjust_hour_stations(station_id, time_cal)
    calc_aqi_data_adjust_24h_stations(station_id, time_cal)
    calc_wqi_data_adjust_hour_stations(station_id, time_cal)
    return

def hour_data_adjust_calc(station_id, time_hour):
    import datetime
    db = current.db
    data = dict()  # {indicator : sum value}
    count = dict()  # {indicator : count}

    start = time_hour.replace(minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=1)
    if end <= datetime.datetime.now():
        try:
            conditions_delete = (db.data_hour_adjust.station_id == station_id)
            conditions_delete &= (db.data_hour_adjust.get_time == end)
            db(conditions_delete).delete()
            db.commit()
        except:
            logger.info('no data to delete')

        conditions_2 = (db.data_adjust.station_id == station_id)
        conditions_2 &= (db.data_adjust.get_time > start)
        conditions_2 &= (db.data_adjust.get_time <= end)
        data_adjusts = db(conditions_2).select(orderby=db.data_adjust.get_time)

        if data_adjusts:
            for i, row in enumerate(data_adjusts):
                get_data = row.data
                for indicator in get_data.keys():
                    try:
                        if get_data[indicator] is not None and len(str(get_data[indicator])) > 0:
                            if data.has_key(indicator):
                                data[indicator] += float(get_data[indicator])
                                count[indicator] += 1
                            else:
                                data[indicator] = float(get_data[indicator])
                                count[indicator] = 1

                    except Exception as ex:
                        continue
                # Neu la row cuoi thi chot, insert vao db
                if i == len(data_adjusts) - 1:
                    # Neu du lieu dict la empty thi skip, ko luu DB
                    if bool(data):
                        # Calc average
                        for indicator in data.keys():
                            try:
                                data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
                            except:
                                continue

                        try:
                            db.data_hour_adjust.update_or_insert(
                                (db.data_hour_adjust.station_id == station_id) & (
                                        db.data_hour_adjust.get_time == end),
                                station_id=station_id,
                                get_time=end,
                                data=data
                            )
                            db.commit()
                        except:
                            db.rollback()
        return


def hour_8h_data_adjust_calc(station_id, time_hour):
    import datetime
    db = current.db
    data = dict()  # {indicator : sum value}
    count = dict()  # {indicator : count}

    start = time_hour.replace(minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=1)
    if end <= datetime.datetime.now():
        try:
            conditions_delete = (db.data_hour_8h_adjust.station_id == station_id)
            conditions_delete &= (db.data_hour_8h_adjust.get_time == end)
            db(conditions_delete).delete()
            db.commit()
        except:
            logger.info('no data to delete')

        conditions = (db.data_hour_adjust.station_id == station_id)
        conditions &= (db.data_hour_adjust.get_time == end)
        data_hour_curent = db(conditions).select(db.data_hour_adjust.station_id)
        if data_hour_curent:
            conditions_2 = (db.data_hour_adjust.station_id == station_id)
            conditions_2 &= (db.data_hour_adjust.get_time >= end - datetime.timedelta(hours=7))
            data_hour_adjusts = db(conditions_2).select(orderby=db.data_hour_adjust.get_time)
            if data_hour_adjusts:
                for i, row in enumerate(data_hour_adjusts):
                    get_data = row.data
                    for indicator in get_data.keys():
                        try:
                            if get_data[indicator] is not None and len(str(get_data[indicator])) > 0:
                                if data.has_key(indicator):
                                    data[indicator] += float(get_data[indicator])
                                    count[indicator] += 1
                                else:
                                    data[indicator] = float(get_data[indicator])
                                    count[indicator] = 1

                        except Exception as ex:
                            continue
                    # Neu la row cuoi thi chot, insert vao db
                    if i == len(data_hour_adjusts) - 1:
                        # Neu du lieu dict la empty thi skip, ko luu DB
                        if bool(data):
                            # Calc average
                            for indicator in data.keys():
                                try:
                                    data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
                                except:
                                    continue

                            try:
                                db.data_hour_8h_adjust.update_or_insert(
                                    (db.data_hour_8h_adjust.station_id == station_id) & (
                                            db.data_hour_8h_adjust.get_time == end),
                                    station_id=station_id,
                                    get_time=end,
                                    data=data
                                )
                                db.commit()
                            except:
                                db.rollback()
    return
################################################################################
def day_data_adjust_calc(station_id, time_day):
    # import datetime
    db = current.db
    data = dict()  # {indicator : sum value}
    count = dict()  # {indicator : count}
    max_data = dict()
    min_data = dict()
    max_data_time = dict()
    min_data_time = dict()

    start = time_day.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    try:
        conditions_delete = (db.data_day_adjust.station_id == station_id)
        conditions_delete &= (db.data_day_adjust.get_time == start)
        db(conditions_delete).delete()
        db.commit()
    except:
        logger.info('no data to delete')

    conditions_2 = (db.data_hour_adjust.station_id == station_id)
    conditions_2 &= (db.data_hour_adjust.get_time >= start)
    conditions_2 &= (db.data_hour_adjust.get_time < end)
    data_hour_adjusts = db(conditions_2).select(orderby=db.data_hour_adjust.get_time)
    if data_hour_adjusts:
        for i, row in enumerate(data_hour_adjusts):
            get_data = row.data
            for indicator in get_data.keys():
                if get_data[indicator] is not None and len(str(get_data[indicator])) > 0:
                    try:
                        val = float(get_data[indicator])
                        if data.has_key(indicator):
                            data[indicator] += val
                            count[indicator] += 1
                            if val > max_data[indicator]:
                                max_data[indicator] = val
                                max_data_time[indicator] = row.get_time
                            if val < min_data[indicator]:
                                min_data[indicator] = val
                                min_data_time[indicator] = row.get_time
                        else:
                            data[indicator] = val
                            count[indicator] = 1
                            max_data[indicator] = val
                            min_data[indicator] = val
                            max_data_time[indicator] = row.get_time
                            min_data_time[indicator] = row.get_time
                    except:
                        continue

            # Neu la row cuoi thi insert phan da doc vao DB
            if i == len(data_hour_adjusts) - 1:
                if bool(data):
                    # Calc average
                    for indicator in data.keys():
                        try:
                            data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
                        except:
                            continue

                    try:
                        db.data_day_adjust.update_or_insert(
                            (db.data_day_adjust.station_id == station_id) & (db.data_day_adjust.get_time == start),
                            station_id=station_id,
                            get_time=start,
                            data=data,
                            data_min=min_data,
                            data_max=max_data,
                            data_min_time=min_data_time,
                            data_max_time=max_data_time,
                        )
                        db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                    except:
                        db.rollback()

    return
################################################################################
def mon_data_adjust_calc(station_id, time_month):
    import datetime
    db = current.db
    data = dict()  # {indicator : sum value}
    count = dict()  # {indicator : count}
    max_data = dict()
    min_data = dict()
    max_data_time = dict()
    min_data_time = dict()
    start = time_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_month = time_month.replace(day=28, hour=0, minute=0, second=0, microsecond=0)
    result_month_end = end_month + timedelta(days=5)
    end = result_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    try:
        conditions_delete = (db.data_mon_adjust.station_id == station_id)
        conditions_delete &= (db.data_mon_adjust.get_time == start)
        db(conditions_delete).delete()
        db.commit()
    except:
        logger.info('no data to delete')

    conditions_2 = (db.data_day_adjust.station_id == station_id)
    conditions_2 &= (db.data_day_adjust.get_time >= start)
    conditions_2 &= (db.data_day_adjust.get_time < end)
    data_days_adjusts = db(conditions_2).select(orderby=db.data_day_adjust.get_time)
    if data_days_adjusts:
        for i, row in enumerate(data_days_adjusts):
            # Boc du lieu tu row hien tai vao data dict()
            get_data = row.data
            for indicator in get_data.keys():
                if get_data[indicator] is not None and len(str(get_data[indicator])) > 0:
                    try:
                        val = float(get_data[indicator])
                        if data.has_key(indicator):
                            data[indicator] += val
                            count[indicator] += 1
                            if val > max_data[indicator]:
                                max_data[indicator] = val
                                max_data_time[indicator] = datetime.datetime.fromordinal(
                                    row.get_time.toordinal())  # phai convert kieu date ve datetime thi mongo no moi save dc vao DB
                            if val < min_data[indicator]:
                                min_data[indicator] = val
                                min_data_time[indicator] = datetime.datetime.fromordinal(row.get_time.toordinal())
                        else:
                            data[indicator] = val
                            count[indicator] = 1
                            max_data[indicator] = val
                            min_data[indicator] = val
                            max_data_time[indicator] = datetime.datetime.fromordinal(row.get_time.toordinal())
                            min_data_time[indicator] = datetime.datetime.fromordinal(row.get_time.toordinal())
                    except:
                        continue

            # Check if la row cuoi cung, thi insert record vao bang data_mon
            if i == len(data_days_adjusts) - 1:
                # Neu du lieu dict la empty thi skip, ko luu DB
                if bool(data):
                    # Calc average
                    for indicator in data.keys():
                        try:
                            data[indicator] = float("{0:.4f}".format(data[indicator] / count[indicator]))
                        except:
                            continue
                    try:

                        db.data_mon_adjust.update_or_insert(
                            (db.data_mon_adjust.station_id == station_id) & (
                                    db.data_mon_adjust.get_time == start),
                            station_id=station_id,
                            get_time=start,
                            data=data,
                            data_min=min_data,
                            data_max=max_data,
                            data_min_time=min_data_time,
                            data_max_time=max_data_time,
                        )
                        db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                    except:
                        db.rollback()
    return

# ------ AQI 2019 -----
def aqi_2019_cal_nowcast(ls):
    try:
        cmax = max(ls)
        cmin = min(ls)
        w = float(cmin) / float(cmax)

        if w <= 0.5:
            w = 0.5
        nowcast = None
        # Tinh gia tri nowcast
        if w == 0.5:
            for i, item in enumerate(ls, start=1):
                if not nowcast:
                    nowcast = 0
                nowcast += math.pow(float(w), i) * float(item)

        else:
            n1 = 0
            n2 = 0
            for i, item in enumerate(ls, start=0):
                n1 += pow(w, i) * float(item)
                n2 += pow(w, i)
            if n2 != 0:
                nowcast = n1 / n2
            # float(item["data"][key])

        return nowcast
    except:
        return -1

def aqi_2019_get_index(key, value):
    last = BP_AQI[key]["8"]
    if last and value >= last:
        return 8
    for x in range(1, 8):
        vt = BP_AQI[key][str(x)]
        vs = BP_AQI[key][str(x + 1)]
        if vt != None and vs != None and value >= vt and value < vs:
            return x
    return None

# cong thuc tinh AQI moi nhat nam 2019
def aqi_2019_formulas_1(key, cx, o38h=None):
    if o38h:
        i = aqi_2019_get_index(o38h, cx)
    else:
        i = aqi_2019_get_index(key, cx)
    if i:
        if i == 8:
            return 500
        else:
            inx = str(i)
            inxNext = str(i + 1)
            BP_I = BP_AQI["I"]
            if o38h:
                BP = BP_AQI[o38h]
            else:
                BP = BP_AQI[key]
            return (BP_I[inxNext] - BP_I[inx]) / (BP[inxNext] - BP[inx]) * (cx - BP[inx]) + BP_I[inx]

def aqi_2019_cal_adjust_aqi_hour(station_id, indicator, hour_data, time):
    try:
        if hour_data[indicator] is None:
            return None
        if indicator == "PM-10" or indicator == "PM-2-5":
            data12_hour = get_list_log_after_12h_adjust(station_id, indicator, time)
            if len(data12_hour) < 2:
                return None
            cx = aqi_2019_cal_nowcast(station_id, data12_hour)
        else:
            cx = hour_data[indicator]
        return aqi_2019_formulas_1(indicator, cx)
    except:
        return None


def get_max_day_aqi_adjust_O3_8h(station_id, indicator, time):
    try:
        start_date = datetime.datetime(time.year, time.month, time.day)
        end_date = datetime.datetime(time.year, time.month, time.day, 23, 59, 00)
        aaData = []  # Du lieu json se tra ve
        conditions = (db.data_hour_8h_adjust.id > 0)
        conditions &= (db.data_hour_8h_adjust.station_id == station_id)

        if time:
            conditions &= (db.data_hour_8h_adjust.get_time >= start_date)
            conditions &= (db.data_hour_8h_adjust.get_time <= end_date)
        list_data = db(conditions).select(orderby=~db.data_hour_8h_adjust.get_time)
        # Thu tu ban ghi
        iRow = 1
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        if list_data:
            for i, item in enumerate(list_data):
                row = []
                added_item = dict()
                i_name = indicator
                i_name_decode = i_name.decode('utf-8')
                v = item.data[indicator] if item.data.has_key(indicator) else ''
                if v == '':
                    added_item[i_name] = 0
                else:
                    try:
                        v = float(v)
                        added_item[i_name] = float(v)
                    except:
                        added_item[i_name] = 0
                if added_item.has_key(i_name):
                    aaData.append(added_item[i_name])
        max_day_api = 0
        try:
            max_day_api = max(aaData)
        except Exception as ex:
            print ex
        return max_day_api
    except Exception as ex:
        return 0

# ------- END AQI 2019 ----
def calc_aqi_data_adjust_hour_stations(station_id, time_cal):
    # while True:
    db = current.db
    import datetime
    try:
        conditions = (db.stations.station_type.belongs(
            [const.STATION_TYPE['AMBIENT_AIR']['value'], const.STATION_TYPE['STACK_EMISSION']['value']]))
        conditions &= (db.stations.is_qi == True)
        ambients = db(conditions).select(db.stations.id)
        ambients = [str(station.id) for station in ambients]
        time_cal = time_cal.replace(minute=0, second=0, microsecond=0)
        # Get data from 'data_hour' tu cac station o tren de tinh toan
        conditions2 = (db.data_hour_adjust.station_id == station_id)
        # hungdx check id station co can tinh hay khong
        conditions2 &= (db.data_hour_adjust.station_id.belongs(ambients))
        conditions2 &= (db.data_hour_adjust.get_time >= time_cal)
        conditions2 &= (db.data_hour_adjust.get_time <= time_cal + timedelta(hours=48))

        try:
            conditions_delete = (db.aqi_data_adjust_hour.station_id == station_id)
            conditions_delete &= (db.aqi_data_adjust_hour.get_time >= time_cal)
            conditions_delete &= (db.aqi_data_adjust_hour.get_time <= time_cal + timedelta(hours=48))
            db(conditions_delete).delete()
            db.commit()
        except:
            logger.info('no data to delete')

        data_adjust_hours = db(conditions2).select(orderby=db.data_hour_adjust.get_time)

        # Lay cac chi so qui chuan cua cac indicator
        qc = db(db.aqi_indicators.id > 0).select(db.aqi_indicators.indicator, db.aqi_indicators.qc_1h,
                                                 db.aqi_indicators.indicator_id)
        conditions_qc = (db.station_indicator.station_id == station_id)
        conditions_qc &= db.station_indicator.is_calc_qi == True
        qc_stations_id = db(conditions_qc).select(db.station_indicator.indicator_id)
        ambients_qc = [str(qc_stations_.indicator_id) for qc_stations_ in qc_stations_id]
        qc_dict = dict()

        qc_stations_dict = dict()

        for item in qc:
            qc_dict[item.indicator] = item.qc_1h
            if str(item.indicator_id) in ambients_qc:
                qc_stations_dict[item.indicator] = item.qc_1h

        for item in data_adjust_hours:
            data = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_hour'
            hour_data = item.data
            get_time = item.get_time  # Chuan hoa : cat minute, second ve 0 mac dinh cua data hour da chuan hoa roi
            hasPM = False
            # Tinh toan gtri AQI cho tung indicator (dc dinh nghia truoc trong qc_dict)
            for indicator in hour_data.keys():
                # print(indicator)
                # Chi lay nhung chi so AQI
                if qc_dict.has_key(indicator):
                    # Ko tinh toan AQI 1h cho cac chi so ko co gtri qui chuan (PM10, Pb)
                    if qc_dict[indicator]:
                        # print(indicator)
                        if indicator == "PM-2-5" or indicator == "PM-10":
                            hasPM = True
                        aqi = aqi_2019_cal_adjust_aqi_hour(station_id, indicator, hour_data, get_time)
                        if aqi is not None:
                            data[indicator] = aqi
                        # if (indicator == 'PM-10'):
                        #     dataAfter12h = get_list_log_after_12h_adjust(station_id, indicator, get_time)
                        #     aqi = getNowcastConcentration(indicator, dataAfter12h)
                        #     data[indicator] = aqi
                        #
                        # elif (indicator == 'PM-2-5'):
                        #     dataAfter12h = get_list_log_after_12h_adjust(station_id, indicator, get_time)
                        #     aqi = getNowcastConcentration(indicator, dataAfter12h)
                        #     data[indicator] = aqi
                        # else:
                        #     aqi = hour_data[indicator] / qc_dict[
                        #         indicator] * 100  # Theo cong thuc tinh AQI cho tung chi so
                        #     data[indicator] = aqi
                        # if qc_stations_dict.has_key(indicator):
                        #     # So sanh voi chi so AQI chung tong the
                        #     if data['aqi'] < aqi: data['aqi'] = aqi
                        if qc_stations_dict.has_key(indicator):
                            if data['aqi'] < aqi: data['aqi'] = aqi
            # Neu co du lieu thi insert/update bang 'aqi_data_hour'
            # if data['aqi']:
            if hasPM is False:
                data["aqi"] = None
            try:
                db.aqi_data_adjust_hour.update_or_insert(
                    (db.aqi_data_adjust_hour.station_id == item.station_id) & (
                            db.aqi_data_adjust_hour.get_time == get_time),
                    station_id=item.station_id,
                    get_time=get_time,
                    data=data
                )
                db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
            except:
                db.rollback()
            db.commit()
            try:
                if data['aqi']:
                    time_old = db(db.stations.id == item.station_id).select(db.stations.qi_adjsut_time)
                    if time_old:
                        time_cal = time_old[0].qi_adjsut_time
                    if time_cal:
                        if get_time < time_cal:
                            logger.debug('hungdx get_time < time_cal')
                        else:
                            db(db.stations.id == item.station_id).update(qi_adjust=data['aqi'], qi_adjsut_time=get_time)
                            db.commit()
                    else:
                        db(db.stations.id == item.station_id).update(qi_adjust=data['aqi'], qi_adjsut_time=get_time)
                        db.commit()
            except:
                pass
    except Exception as ex:
        return

def calc_aqi_data_adjust_24h_stations(station_id, time_cal):
    # while True:
    import datetime
    db = current.db
    try:
        # Chi loai station_type = 4 and is_qi = True
        conditions = (db.stations.station_type.belongs(
            [const.STATION_TYPE['AMBIENT_AIR']['value'], const.STATION_TYPE['STACK_EMISSION']['value']]))
        conditions &= (db.stations.is_qi == True)
        ambients = db(conditions).select(db.stations.id)
        ambients = [str(station.id) for station in ambients]
        last_days = time_cal.replace(hour=0, minute=0, second=0, microsecond=0)
        # Get data from 'data_day' tu cac station o tren de tinh toan
        conditions2 = (db.data_day_adjust.station_id == station_id)
        conditions2 &= (db.data_day_adjust.station_id.belongs(ambients))
        conditions2 &= (db.data_day_adjust.get_time >= last_days)
        conditions2 &= (db.data_day_adjust.get_time < last_days + timedelta(days=3))
        conditions2 &= (db.data_day_adjust.get_time < datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))

        try:
            conditions_delete = (db.aqi_data_adjust_24h.station_id == station_id)
            conditions_delete &= (db.aqi_data_adjust_24h.get_time >= last_days)
            conditions_delete &= (db.aqi_data_adjust_24h.get_time < last_days + timedelta(days=3))
            db(conditions_delete).delete()
            db.commit()
        except:
            logger.info('no data to delete')

        data_days = db(conditions2).select(orderby=db.data_day_adjust.get_time)

        # Lay cac chi so qui chuan cua cac indicator
        qc = db(db.aqi_indicators.id > 0).select(db.aqi_indicators.indicator, db.aqi_indicators.qc_1h,
                                                 db.aqi_indicators.qc_24h, db.aqi_indicators.indicator_id)

        conditions_qc = (db.station_indicator.station_id == station_id)
        conditions_qc &= db.station_indicator.is_calc_qi == True
        qc_stations_id = db(conditions_qc).select(db.station_indicator.indicator_id)
        ambients_qc = [str(qc_stations_.indicator_id) for qc_stations_ in qc_stations_id]
        qc_stations_dict = dict()
        qc_dict_1h = dict()
        qc_dict_24h = dict()
        for item in qc:
            qc_dict_1h[item.indicator] = item.qc_1h
            qc_dict_24h[item.indicator] = item.qc_24h
            if str(item.indicator_id) in ambients_qc:
                qc_stations_dict[item.indicator] = item.qc_1h

        for item in data_days:
            data_24h = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_24h'
            data_1d = {'aqi': None}  # du lieu AQI se insert/update vao bang 'aqi_data_24h'
            day_data = item.data  # Du lieu quan trac trung binh 1 ngay cua thong so = SUM/count
            max_data = item.data_max

            # Tinh toan gtri AQI cho tung indicator (dc dinh nghia truoc trong qc_dict)
            for indicator in day_data.keys():
                # Chi lay nhung chi so AQI
                if qc_dict_24h.has_key(indicator):
                    if indicator in ["PM-2-5", "PM-10"]:
                        aqi = aqi_2019_formulas_1(indicator, day_data[indicator])
                        data_1d[indicator] = aqi
                    elif indicator in ["SO2", "NO2", "CO"]:
                        aqi = aqi_2019_formulas_1(indicator, max_data[indicator])
                        data_1d[indicator] = aqi
                    elif indicator == "O3":
                        aqi = aqi_2019_formulas_1(indicator, max_data[indicator])
                        data_1d[indicator] = aqi
                        o3_8h = get_max_day_aqi_adjust_O3_8h(station_id, indicator, item.get_time)
                        if o3_8h < 400 and o3_8h != 0:
                            aqi = aqi_2019_formulas_1(indicator, o3_8h, "O38")
                            data_1d["O38h"] = aqi
                    if data_1d['aqi'] < aqi: data_1d['aqi'] = aqi

                    # Ko tinh toan AQI 24h cho chi so ko co gtri qui chuan hoac O3
                    # if qc_dict_24h[indicator] and indicator not in ['O3', 'CO']:
                    #     aqi = day_data[indicator] / qc_dict_24h[
                    #         indicator] * 100  # Theo cong thuc tinh AQI cho tung chi so
                    #     data_24h[indicator] = aqi
                    #
                    #     if qc_stations_dict.has_key(indicator):
                    #         # So sanh voi chi so AQI chung tong the
                    #         if data_24h['aqi'] < aqi:
                    #             data_24h['aqi'] = aqi

            # Neu co du lieu thi insert/update bang 'aqi_data_24h'
            # if data_24h['aqi']:
            #     # So sanh du lieu AQI_24h vua tinh duoc voi gtri max cua AQI_1h de lay gtri AQI_1d
            #     keys = data_24h.keys()
            #     keys.remove('aqi')
            #     for indicator in keys:
            #         get_time = datetime.datetime.fromordinal(item.get_time.toordinal())
            #         if (indicator == 'PM-10'):
            #             aqi_max_indicator = get_max_day_aqi_adjust_pm(station_id, indicator, get_time)
            #             data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else data_24h[indicator]
            #         elif (indicator == 'PM-2-5'):
            #             aqi_max_indicator = get_max_day_aqi_adjust_pm(station_id, indicator, get_time)
            #             data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else \
            #                 data_24h[indicator]
            #         else:
            #             aqi_max_indicator = max_data[indicator] / qc_dict_1h[indicator] * 100 if qc_dict_1h[
            #                 indicator] else 0
            #
            #             data_1d[indicator] = aqi_max_indicator if aqi_max_indicator > data_24h[indicator] else \
            #                 data_24h[indicator]
            #         # Gtri AQI_1d chung cua tram
            #         if qc_stations_dict.has_key(indicator):
            #             if data_1d['aqi'] < data_1d[indicator]:
            #                 data_1d['aqi'] = data_1d[indicator]
            #
            #     # Do qui dinh : AQI_1d cua O3 = max (AQI_1h cua O3)
            #     if max_data.has_key('O3'):
            #         data_1d['O3'] = max_data['O3'] / qc_dict_1h['O3'] * 100  # Gtri AQI_1d cua O3
            #         # Gtri AQI_1d chung cua tram
            #         if qc_stations_dict.has_key('O3'):
            #             if data_1d['aqi'] < data_1d['O3']:
            #                 data_1d['aqi'] = data_1d['O3']
            #
            #     # Do qui dinh : AQI_1d cua CO = max (AQI_1h cua CO)
            #     if max_data.has_key('CO'):
            #         data_1d['CO'] = max_data['CO'] / qc_dict_1h['CO'] * 100  # Gtri AQI_1d cua O3
            #         # Gtri AQI_1d chung cua tram
            #         if qc_stations_dict.has_key('CO'):
            #             if data_1d['aqi'] < data_1d['CO']:
            #                 data_1d['aqi'] = data_1d['CO']

                get_time = datetime.datetime.fromordinal(item.get_time.toordinal())

                try:
                    db.aqi_data_adjust_24h.update_or_insert(
                        (db.aqi_data_adjust_24h.station_id == item.station_id) & (
                                db.aqi_data_adjust_24h.get_time == get_time),
                        station_id=item.station_id,
                        get_time=get_time,
                        data_24h=data_1d,
                        data_1d=data_1d
                    )
                    db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
                except:
                    db.rollback()

        db.commit()
    except Exception as ex:
        return
    finally:
        return

def calc_wqi_data_adjust_hour_stations(station_id, time_cal):
    import datetime
    db = current.db
    try:
        type = [
            const.STATION_TYPE['WASTE_WATER']['value'],
            const.STATION_TYPE['SURFACE_WATER']['value'],
            const.STATION_TYPE['UNDERGROUND_WATER']['value']
        ]
        # Chi loai station_type = 0,1,2 and is_qi = True
        conditions = (db.stations.station_type.belongs(type))
        conditions &= (db.stations.is_qi == True)
        waters = db(conditions).select(db.stations.id)
        waters = [str(station.id) for station in waters]
        time_cal = time_cal.replace(minute=0, second=0, microsecond=0)
        # Get data from 'data_hour' tu cac station o tren de tinh toan
        conditions_2 = (db.data_hour_adjust.station_id.belongs(waters))
        conditions_2 &= (db.data_hour_adjust.station_id == station_id)
        conditions_2 &= (db.data_hour_adjust.get_time >= time_cal)
        conditions_2 &= (db.data_hour_adjust.get_time < time_cal + timedelta(hours=1))
        try:
            conditions_delete = (db.wqi_data_adjust_hour.station_id == station_id)
            conditions_delete &= (db.wqi_data_adjust_hour.get_time == time_cal)
            db(conditions_delete).delete()
            db.commit()
        except:
            logger.info('no data to delete')

        data_hours = db(conditions_2).select(orderby=db.data_hour_adjust.station_id | db.data_hour_adjust.get_time)
        # mang cac thong so co trong cong thuc tinh wqi cua station
        conditions = (db.station_indicator.station_id == station_id)
        conditions &= (db.station_indicator.is_calc_qi == True)
        rows = db(conditions).select(db.station_indicator.ALL)

        # Get list indicator_id used
        indicator_ids = []
        for row in rows:
            if row.indicator_id not in indicator_ids:
                indicator_ids.append(row.indicator_id)

        # Get indicator_dict {indicator_id : indicator_name}
        indicators = db(db.indicators.id.belongs(indicator_ids)).select(db.indicators.indicator)

        ambients_qc = [str(qc_stations_.indicator).upper() for qc_stations_ in indicators]

        for item in data_hours:
            data = {'wqi': None}  # du lieu WQI se insert/update vao bang 'wqi_data_hour'
            hour_data = item.data
            if not hour_data:
                continue
            group_1 = []  # tap cac chi so cua data trong nhom I
            group_2 = []  # tap cac chi so cua data trong nhom II
            group_3 = []  # tap cac chi so cua data trong nhom III
            group_4 = []  # tap cac chi so cua data trong nhom IV

            is_calcu_wqi = False
            is_calc_qi_group_1 = []  # tap cac chi so cua data trong nhom I va co is_calc_qi = True
            is_calc_qi_group_2 = []  # tap cac chi so cua data trong nhom II va co is_calc_qi = True
            is_calc_qi_group_3 = []  # tap cac chi so cua data trong nhom III va co is_calc_qi = True
            is_calc_qi_group_4 = []  # tap cac chi so cua data trong nhom IV va co is_calc_qi = True
            in_gr_1 = 0
            in_gr_2 = 0
            in_gr_3 = 0
            in_gr_4 = 0
            for indicator in hour_data.keys():
                if indicator.upper() in const.WQI_GR_1:
                    group_1 = group_1 + [str(indicator)]
                    if indicator.upper() in ambients_qc:
                        is_calc_qi_group_1 = is_calc_qi_group_1 + [str(indicator)]
                        in_gr_1 = 1
                if indicator.upper() in const.WQI_GR_2:
                    group_2 = group_2 + [str(indicator)]
                    if indicator.upper() in ambients_qc:
                        is_calc_qi_group_2 = is_calc_qi_group_2 + [str(indicator)]
                        in_gr_2 = 1
                if indicator.upper() in const.WQI_GR_3:
                    group_3 = group_3 + [str(indicator)]
                    if indicator.upper() in ambients_qc:
                        is_calc_qi_group_3 = is_calc_qi_group_3 + [str(indicator)]
                        in_gr_3 = 1
                if indicator.upper() in const.WQI_GR_4:
                    group_4 = group_4 + [str(indicator)]
                    if indicator.upper() in ambients_qc:
                        is_calc_qi_group_4 = is_calc_qi_group_4 + [str(indicator)]
                        in_gr_4 = 1

            if in_gr_2 > 0 and (in_gr_1 + in_gr_3 + in_gr_4 >= 1):
                is_calcu_wqi = True

            for indicator in hour_data.keys():
                # Chi lay nhung chi so WQI : BOD5, COD, N-NH4, P-PO4, Turbidity, TSS, Coliform
                if indicator.upper() in const.WQI_INDICATOR_SAME_1:
                    try:
                        if hour_data[indicator] <= const.WQI_BP[indicator.upper()][0]:
                            data[indicator] = const.QI[0]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][1]:
                            data[indicator] = formular_1(const.QI[0], const.QI[1],
                                                         const.WQI_BP[indicator.upper()][0],
                                                         const.WQI_BP[indicator.upper()][1], hour_data[indicator])
                        elif hour_data[indicator] == const.WQI_BP[indicator.upper()][1]:
                            data[indicator] = const.QI[1]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][2]:
                            data[indicator] = formular_1(const.QI[1], const.QI[2],
                                                         const.WQI_BP[indicator.upper()][1],
                                                         const.WQI_BP[indicator.upper()][2], hour_data[indicator])
                        elif hour_data[indicator] == const.WQI_BP[indicator.upper()][2]:
                            data[indicator] = const.QI[2]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][3]:
                            data[indicator] = formular_1(const.QI[2], const.QI[3],
                                                         const.WQI_BP[indicator.upper()][2],
                                                         const.WQI_BP[indicator.upper()][3], hour_data[indicator])
                        elif hour_data[indicator] == const.WQI_BP[indicator.upper()][3]:
                            data[indicator] = const.QI[3]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][4]:
                            data[indicator] = formular_1(const.QI[3], const.QI[4],
                                                         const.WQI_BP[indicator.upper()][3],
                                                         const.WQI_BP[indicator.upper()][4], hour_data[indicator])
                        else:
                            data[indicator] = const.QI[4]
                    except:
                        pass
                elif indicator.upper() in const.WQI_INDICATOR_SAME_2:
                    try:
                        if hour_data[indicator] <= const.WQI_BP[indicator.upper()][0]:
                            data[indicator] = const.QI[0]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][1]:
                            data[indicator] = formular_1(const.QI[0], const.QI[1],
                                                         const.WQI_BP[indicator.upper()][0],
                                                         const.WQI_BP[indicator.upper()][1], hour_data[indicator])
                        elif hour_data[indicator] == const.WQI_BP[indicator.upper()][1]:
                            data[indicator] = const.QI[1]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][2]:
                            data[indicator] = formular_1(const.QI[1], const.QI[2],
                                                         const.WQI_BP[indicator.upper()][1],
                                                         const.WQI_BP[indicator.upper()][2], hour_data[indicator])
                        elif hour_data[indicator] == const.WQI_BP[indicator.upper()][2]:
                            data[indicator] = const.QI[2]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][3]:
                            data[indicator] = formular_1(const.QI[2], const.QI[3],
                                                         const.WQI_BP[indicator.upper()][2],
                                                         const.WQI_BP[indicator.upper()][3], hour_data[indicator])
                        elif hour_data[indicator] == const.WQI_BP[indicator.upper()][3]:
                            data[indicator] = const.QI[3]
                        else:
                            data[indicator] = const.QI[4]
                    except:
                        pass
                elif indicator.upper() in const.WQI_INDICATOR_SAME_3:
                    try:
                        if hour_data[indicator] < const.WQI_BP[indicator.upper()][0]:
                            data[indicator] = const.QI[0]
                        elif hour_data[indicator] == const.WQI_BP[indicator.upper()][1]:
                            data[indicator] = const.QI[1]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][2]:
                            data[indicator] = formular_1(const.QI[1], const.QI[2],
                                                         const.WQI_BP[indicator.upper()][1],
                                                         const.WQI_BP[indicator.upper()][2], hour_data[indicator])
                        elif hour_data[indicator] == const.WQI_BP[indicator.upper()][2]:
                            data[indicator] = const.QI[2]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][3]:
                            data[indicator] = formular_1(const.QI[2], const.QI[3],
                                                         const.WQI_BP[indicator.upper()][2],
                                                         const.WQI_BP[indicator.upper()][3], hour_data[indicator])
                        elif hour_data[indicator] == const.WQI_BP[indicator.upper()][3]:
                            data[indicator] = const.QI[3]
                        elif hour_data[indicator] < const.WQI_BP[indicator.upper()][4]:
                            data[indicator] = formular_1(const.QI[3], const.QI[4],
                                                         const.WQI_BP[indicator.upper()][3],
                                                         const.WQI_BP[indicator.upper()][4], hour_data[indicator])
                        else:
                            data[indicator] = const.QI[4]
                    except:
                        pass

                elif indicator.upper() == 'DO':
                    try:
                    # Tinh DO bao hoa
                        do_bh = do_baohoa(hour_data['Temp'])
                        do_baohoa_percent = hour_data['DO'] / do_bh * 100
                        if do_baohoa_percent < const.DO_BP[0]:  # Neu gtri < 20 : WQI cua DO = 10
                            data['DO'] = const.DO_QI[0]
                        elif do_baohoa_percent == const.DO_BP[1]:
                            data['DO'] = const.DO_QI[1]
                        elif do_baohoa_percent < const.DO_BP[2]:
                            data['DO'] = formular_2(const.DO_QI[1], const.DO_QI[2], const.DO_BP[1],
                                                    const.DO_BP[2], do_baohoa_percent)
                        elif do_baohoa_percent == const.DO_BP[2]:
                            data['DO'] = const.DO_QI[2]
                        elif do_baohoa_percent < const.DO_BP[3]:
                            data['DO'] = formular_2(const.DO_QI[2], const.DO_QI[3], const.DO_BP[2],
                                                    const.DO_BP[3], do_baohoa_percent)
                        elif do_baohoa_percent == const.DO_BP[3]:
                            data['DO'] = const.DO_QI[3]
                        elif do_baohoa_percent < const.DO_BP[4]:
                            data['DO'] = formular_2(const.DO_QI[3], const.DO_QI[4], const.DO_BP[3],
                                                    const.DO_BP[4], do_baohoa_percent)
                        elif do_baohoa_percent <= const.DO_BP[5]:
                            data['DO'] = const.DO_QI[5]
                        elif do_baohoa_percent < const.DO_BP[6]:
                            data['DO'] = formular_1(const.DO_QI[5], const.DO_QI[6], const.DO_BP[5],
                                                    const.DO_BP[6], do_baohoa_percent)
                        elif do_baohoa_percent == const.DO_BP[6]:
                            data['DO'] = const.DO_QI[6]
                        elif do_baohoa_percent < const.DO_BP[7]:
                            data['DO'] = formular_1(const.DO_QI[6], const.DO_QI[7], const.DO_BP[6],
                                                    const.DO_BP[7], do_baohoa_percent)
                        elif do_baohoa_percent == const.DO_BP[7]:
                            data['DO'] = const.DO_QI[7]
                        elif do_baohoa_percent < const.DO_BP[8]:
                            data['DO'] = formular_1(const.DO_QI[7], const.DO_QI[8], const.DO_BP[7],
                                                    const.DO_BP[8], do_baohoa_percent)
                        elif do_baohoa_percent == const.DO_BP[8]:
                            data['DO'] = const.DO_QI[8]
                        else:  # Neu gtri > 200: WQI cua DO = 10
                            data['DO'] = const.DO_QI[9]
                    except:
                        pass

                elif indicator.upper() == 'PH':
                    try:
                        if hour_data['pH'] < const.PH_BP[0]:  # Neu gtri < 5.5 : WQI cua pH = 1
                            data['pH'] = const.PH_QI[0]
                        elif hour_data['pH'] == const.PH_BP[1]:  # Neu gtri = 5.5 : WQI cua pH = 50
                            data['pH'] = const.PH_QI[1]
                        elif hour_data['pH'] < const.PH_BP[2]:  # Neu gtri 5.5 < x < 6
                            data['pH'] = formular_2(const.PH_QI[1], const.PH_QI[2], const.PH_BP[1],
                                                    const.PH_BP[2], hour_data['pH'])
                        elif hour_data['pH'] <= const.PH_BP[3]:  # Neu gtri >= 6  vs <= 8.5 : WQI cua pH = 100
                            data['pH'] = const.PH_QI[3]
                        elif hour_data['pH'] < const.PH_BP[4]:  # Neu gtri >8.5  vs < 9 WQI cua pH
                            data['pH'] = formular_1(const.PH_QI[3], const.PH_QI[4], const.PH_BP[3],
                                                    const.PH_BP[4], hour_data['pH'])
                        elif hour_data['pH'] == const.PH_BP[4]:  # neu gia tri = 9
                            data['pH'] = const.PH_QI[4]
                        else:
                            data['pH'] = const.PH_QI[5]
                    except:
                        pass

            if is_calcu_wqi:
                # Tinh WQI tong hop
                value_1 = None
                wqi = None
                try:
                    if len(is_calc_qi_group_1) > 0:
                        for indicator in is_calc_qi_group_1:
                            if value_1:
                                value_1 = value_1 * data[str(indicator)]
                            else:
                                value_1 = data[str(indicator)]

                    if value_1:
                        value_1 = value_1 ** (1. / len(is_calc_qi_group_1))
                        value_1 = value_1 / 100

                    value_2 = None
                    if len(is_calc_qi_group_2) > 0:
                        for indicator in is_calc_qi_group_2:
                            if value_2:
                                value_2 = value_2 + data[str(indicator)]
                            else:
                                value_2 = data[str(indicator)]

                    if value_2:
                        value_2 = value_2 / len(is_calc_qi_group_2)
                        value_2 = value_2 * value_2

                    value_3 = None
                    if len(is_calc_qi_group_3) > 0:
                        for indicator in is_calc_qi_group_3:
                            if value_3:
                                value_3 = value_3 + data[str(indicator)]
                            else:
                                value_3 = data[str(indicator)]

                    if value_3:
                        value_3 = value_3 / len(is_calc_qi_group_3)

                    value_4 = None
                    if len(is_calc_qi_group_4) > 0:
                        for indicator in is_calc_qi_group_4:
                            value_4 = data[str(indicator)]

                    wqi = None
                    if value_1:
                        wqi = value_1
                    else:
                        wqi = 1

                    if value_3 and value_4:
                        wqi = wqi * (value_2 * value_3 * value_4) ** (1. / 4)
                    elif value_3:
                        wqi = wqi * (value_2 * value_3) ** (1. / 3)
                    elif value_4:
                        wqi = wqi * (value_2 * value_4) ** (1. / 3)
                    else:
                        wqi = wqi * value_2 ** (1. / 2)
                except:
                    pass
                if wqi:
                    data['wqi'] = wqi
                    data['wqi'] = round(data['wqi'])

            try:
                db.wqi_data_adjust_hour.update_or_insert(
                    (db.wqi_data_adjust_hour.station_id == item.station_id) & (
                            db.wqi_data_adjust_hour.get_time == item.get_time),
                    station_id=item.station_id,
                    get_time=item.get_time,
                    data=data
                )
                db.commit()  # Luu data vao db ngay sau khi xu ly moi tram
            except:
                db.rollback()

            try:
                if data['wqi']:
                    time_old = db(db.stations.id == item.station_id).select(db.stations.qi_adjsut_time)
                    if time_old:
                        time_cal = time_old[0].qi_adjsut_time
                    if time_cal:
                        if item.get_time < time_cal:
                            logger.debug('hungdx get_time < time_cal')
                        else:
                            db(db.stations.id == item.station_id).update(qi_adjust=data['wqi'], qi_adjsut_time=item.get_time)
                            db.commit()
                    else:
                        db(db.stations.id == item.station_id).update(qi_adjust=data['wqi'], qi_adjsut_time=item.get_time)
                        db.commit()
            except:
                pass
    except Exception as ex:
        logger.info("calc_wqi_data_adjust_hour_stations eror %s", str(ex.message))
    finally:
        logger.info("calc_wqi_data_adjust_hour_stations finish")


################################################################################
def formular_1(q1, q2, bp1, bp2, c):
    res = (q1 - q2) * (bp2 - c) / (bp2 - bp1) + q2

    return res

################################################################################
def formular_2(q1, q2, bp1, bp2, c):
    res = (q2 - q1) * (c - bp1) / (bp2 - bp1) + q1

    return res


################################################################################
def do_baohoa(temp):
    res = 14.652 - 0.41022 * temp + 0.0079910 * temp * temp - 0.000077774 * temp * temp * temp
    return res

def get_list_log_after_12h_adjust(station_id, indicator, time):
    try:
        aaData = []  # Du lieu json se tra ve

        conditions = (db.data_hour_adjust.id > 0)
        conditions &= (db.data_hour_adjust.station_id == station_id)
        if time:
            time_delta = time - timedelta(hours=11)
            conditions &= (db.data_hour_adjust.get_time >= time_delta)
            conditions &= (db.data_hour_adjust.get_time <= time)

        list_data = db(conditions).select(orderby=~db.data_hour_adjust.get_time)

        # Thu tu ban ghi
        iRow = 1
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for i, item in enumerate(list_data):
            row = []
            added_item = dict()
            i_name = indicator
            i_name_decode = i_name.decode('utf-8')
            v = item.data[indicator] if item.data.has_key(indicator) else ''
            if v == '':
                added_item[i_name] = 0
            else:
                try:
                    v = float(v)
                    added_item[i_name] = float(v)
                except:
                    added_item[i_name] = 0

            if added_item.has_key(i_name):
                aaData.append(added_item[i_name])
        return aaData
    except Exception as ex:
        return 0

def getNowcastConcentration(pollutant, data):
    # if isValidNowcastData(data) :
    #     return -1;
    return truncateConcentration(pollutant, data)

def truncateConcentration(pollutant, data):
    if (isValidNowcastData(data) > 1):
        return 0
    weight = getWeightFactor(pollutant, data)
    totalConcentrationWithWeight = 0
    totalWeight = 0

    indexDataSlot = 3
    numberItem = 0
    totalConcentration = 0
    if weight > 0.5:
        for item in data:
            if item < 0:
                continue
            else:
                totalConcentrationWithWeight += item * math.pow(weight, numberItem)
                totalWeight += math.pow(weight, numberItem)
            numberItem = numberItem + 1
        totalConcentration = totalConcentrationWithWeight / totalWeight
    else:
        for item in (data):

            if item < 0:
                continue
            totalConcentrationWithWeight += item * math.pow(0.5, numberItem + 1)
            numberItem = numberItem + 1

        totalConcentration = totalConcentrationWithWeight
    return getTruncatedPollutantConcentrationBaseOnPollutant(pollutant, totalConcentration)

def isValidNowcastData(data):
    missingData = 0;
    x = range(0, 2)
    for i in x:
        try:
            if (data[i] < 0):
                missingData = missingData + 1
        except:
            missingData = missingData + 1

    return missingData

def getWeightFactor(indicator, data):
    maxConcentration = float('-inf')
    minConcentration = float('inf')

    for i in data:
        if (i < 0):
            continue
        else:
            if (i > maxConcentration):
                maxConcentration = i
            if (i < minConcentration):
                minConcentration = i

    range = maxConcentration - minConcentration
    weightFactor = 0
    try:
        weightFactor = float(minConcentration) / float(maxConcentration)
    except:
        weightFactor = 0

    if weightFactor <= float(1) / 2:
        weightFactor = float(1) / 2

    return weightFactor

def getTruncatedPollutantConcentrationBaseOnPollutant(pollutant, concentration) :
    if (pollutant == 'PM-10') :
        return float(concentration * 100 / 150)

    if (pollutant == 'PM-2-5') :
        return float(concentration * 100 / 50)

def get_max_day_aqi_adjust_pm(station_id, indicator, time):

    try:
        aaData = []  # Du lieu json se tra ve

        conditions = (db.aqi_data_adjust_hour.id > 0)
        conditions &= (db.aqi_data_adjust_hour.station_id == station_id)
        if time:
            time_delta = time + timedelta(hours=23)
            conditions &= (db.aqi_data_adjust_hour.get_time >= time)
            conditions &= (db.aqi_data_adjust_hour.get_time <= time_delta)

        list_data = db(conditions).select(orderby=~db.aqi_data_adjust_hour.get_time)

        # Thu tu ban ghi
        iRow = 1
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        if list_data:
            for i, item in enumerate(list_data):
                row = []
                added_item = dict()
                i_name = indicator
                i_name_decode = i_name.decode('utf-8')
                v = item.data[indicator] if item.data.has_key(indicator) else ''
                if v == '':
                    added_item[i_name] = 0
                else:
                    v = float(v)
                    added_item[i_name] = float(v)
                if added_item.has_key(i_name):
                    aaData.append(added_item[i_name])
        max_day_api = 0
        try:
            max_day_api = max(aaData)
        except:
            max_day_api = 0

        return max_day_api
    except Exception as ex:
        return 0


########################
@service.json
def dropdown_content(table, filter_field, get_value_field, get_dsp_field, *args, **kwargs):
    try:
        station_type = request.vars.station_type
        filter_value = request.vars.filter_value
        filter_value = filter_value.split(';')
        filter_field = filter_field.split('-')
        conditions = (db[table]['id'] > 0)
        t1 = len(filter_field)
        t2 = len(filter_value)
        if station_type:
            conditions &= (db[table].station_type == station_type)
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