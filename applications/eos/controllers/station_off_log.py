# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
import datetime

from applications.eos.modules import common
from applications.eos.modules.w2pex import date_util

def call():
    return service()


################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def index():
    provinces = common.get_province_have_station_for_envisoft()
    areas = db(db.areas.id > 0).select()
    station_id = request.vars.station_id
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
            row = db(db.stations.id.belongs(station_ids)).select(db.stations.area_id, distinct=True)
            areas_ids = [str(it.area_id) for it in row]
            areas = db(db.areas.id.belongs(areas_ids)).select(db.areas.area_name,
                                                              db.areas.id)

    careers = db(db.manager_careers.id > 0).select(db.manager_careers.id, db.manager_careers.career_name)
    stations = db(conditions).select(orderby=db.stations.order_no)
    return dict(provinces=provinces, areas=areas, stations=stations, station_id=station_id, careers=careers)

@service.json
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def station_off_log_count_time():
    provinces = common.get_province_have_station_for_envisoft()
    areas = db(db.areas.id > 0).select()
    station_id = request.vars.station_id
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
            row = db(db.stations.id.belongs(station_ids)).select(db.stations.area_id, distinct=True)
            areas_ids = [str(it.area_id) for it in row]
            areas = db(db.areas.id.belongs(areas_ids)).select(db.areas.area_name,
                                                              db.areas.id)
    stations = db(conditions).select(orderby=db.stations.order_no)
    return dict(provinces=provinces, areas=areas, stations=stations, station_id=station_id)

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def station_off_log_by_province():
    provinces = common.get_province_have_station_for_envisoft()
    areas = db(db.areas.id > 0).select()
    station_id = request.vars.station_id
    conditions = (db.stations.id > 0)
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.stations.id.belongs(station_ids))
            row = db(db.stations.id.belongs(station_ids)).select(db.stations.area_id, distinct=True)
            areas_ids = [str(it.area_id) for it in row]
            areas = db(db.areas.id.belongs(areas_ids)).select(db.areas.area_name,
                                                              db.areas.id)
    stations = db(conditions).select(orderby=db.stations.order_no)
    return dict(provinces=provinces, areas=areas, stations=stations, station_id=station_id)

################################################################################
def roundTime(dt=None, roundTo=1):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   """
   if dt == None : return None
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0, rounding-seconds, -dt.microsecond)

#################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def get_list_station_off_log_count_time(*args, **kwargs):
    try:
        s_search = request.vars.sSearch
        a = request.vars
        station_type = request.vars.type
        sometext = request.vars.sometext
        datepicker_start = request.vars.datepicker_start
        datepicker_end = request.vars.datepicker_end
        province_id = request.vars.province_id
        area_id = request.vars.area_id
        station_id = request.vars.station_id
        connection_loss = request.vars.connection_loss
        aaData = []
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)

        # Search conditions
        conditions = (db.station_off_log.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= (db.station_off_log.station_name.contains(sometext))
        if datepicker_start:
            conditions &= (db.station_off_log.start_off >= date_util.string_to_datetime(datepicker_start))
        if datepicker_end:
            conditions &= (db.station_off_log.end_off <= date_util.string_to_datetime(datepicker_end))
        if station_type:
            conditions &= (db.station_off_log.station_type == station_type)
        if province_id:
            conditions &= (db.station_off_log.province_id == province_id)
        if area_id:
            station_ids = db(db.stations.area_id == area_id).select(db.stations.id)
            station_ids = [item.id for item in station_ids]
            conditions &= (db.station_off_log.station_id.belongs(station_ids))
        if station_id:
            conditions &= (db.station_off_log.station_id == station_id)
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.station_off_log.station_id.belongs(station_ids))

        list_data = db(conditions).select(  db.station_off_log.id, 
                                            db.station_off_log.station_id,
                                            db.station_off_log.station_name,
                                            db.station_off_log.station_type,
                                            db.station_off_log.province_id,
                                            db.station_off_log.start_off,
                                            db.station_off_log.end_off,
                                            db.station_off_log.duration,
                                            orderby = ~db.station_off_log.start_off)

        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count(db.station_off_log.id)
        # Thu tu ban ghi
        iRow = iDisplayStart + 1
        station_type = dict(db.commands.station_type.requires.options())
        areas = common.get_area_by_station_dict()
        provice_dict = common.get_province_dict()
        connection_dict = {}
        res_name, res_type, res_status, res_code , res_area = common.get_station_dict()

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            start_off = roundTime(item.start_off)
            end_off = roundTime(item.end_off)
            province_id = item.province_id
            if end_off and start_off:
                duration = (end_off - start_off).total_seconds()
            else:
                duration = 0
                
            if connection_loss:
                if duration >= int(connection_loss) * 3600:
                    if not connection_dict.has_key(item.station_id):
                        connection_dict[item.station_id] = 1
                    else:
                        connection_dict[item.station_id] += 1
                        
            else:
                if not connection_dict.has_key(item.station_id):
                    connection_dict[item.station_id] = 1
                else:
                    connection_dict[item.station_id] += 1
                    
                   

        i = 1
        total = 0 
        for key, value in connection_dict.iteritems():
            total += value
            aaData.append([str(i), res_name.get(key), value])
            i += 1
        
        data = aaData[iDisplayStart:iDisplayStart+iDisplayLength]
        
        return dict(iTotalRecords=i, iTotalDisplayRecords=i, aaData=data, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)


#################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def get_list_station_off_log_by_province(*args, **kwargs):
    try:
        s_search = request.vars.sSearch
        a = request.vars
        station_type = request.vars.type
        sometext = request.vars.sometext
        datepicker_start = request.vars.datepicker_start
        datepicker_end = request.vars.datepicker_end
        province_id = request.vars.province_id
        area_id = request.vars.area_id
        station_id = request.vars.station_id
        connection_loss = request.vars.connection_loss
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        aaData = []
        # Search conditions
        conditions = (db.station_off_log.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= (db.station_off_log.station_name.contains(sometext))
        if datepicker_start:
            conditions &= (db.station_off_log.start_off >= date_util.string_to_datetime(datepicker_start))
        if datepicker_end:
            conditions &= (db.station_off_log.end_off <= date_util.string_to_datetime(datepicker_end))
        if station_type:
            conditions &= (db.station_off_log.station_type == station_type)
        if province_id:
            conditions &= (db.station_off_log.province_id == province_id)
        if area_id:
            station_ids = db(db.stations.area_id == area_id).select(db.stations.id)
            station_ids = [item.id for item in station_ids]
            conditions &= (db.station_off_log.station_id.belongs(station_ids))
        if station_id:
            conditions &= (db.station_off_log.station_id == station_id)
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.station_off_log.station_id.belongs(station_ids))

        list_data = db(conditions).select(  db.station_off_log.id, 
                                            db.station_off_log.station_id,
                                            db.station_off_log.station_name,
                                            db.station_off_log.station_type,
                                            db.station_off_log.province_id,
                                            db.station_off_log.start_off,
                                            db.station_off_log.end_off,
                                            db.station_off_log.duration,
                                            orderby = ~db.station_off_log.start_off)

        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count(db.station_off_log.id)
        # Thu tu ban ghi
        station_type = dict(db.commands.station_type.requires.options())
        areas = common.get_area_by_station_dict()
        provice_dict = common.get_province_dict()
        connection_dict = {}

        
        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
           
            start_off = roundTime(item.start_off)
            end_off = roundTime(item.end_off)
            province_id = item.province_id
            if end_off and start_off:
                duration = (end_off - start_off).total_seconds()
            else:
                duration = 0
                
            if connection_loss:
                if duration >= int(connection_loss) * 3600:
                    if not connection_dict.has_key(province_id):
                        connection_dict[province_id] = {
                            "{}".format(item.station_id): 1
                        }
                    else:
                        if not connection_dict[province_id].has_key(item.station_id):
                            connection_dict[province_id][item.station_id] = 1
                        else:
                            connection_dict[province_id][item.station_id] += 1
                        
            else:
                if not connection_dict.has_key(province_id):
                    connection_dict[province_id] = {
                        "{}".format(item.station_id): 1
                    }
                else:
                    if not connection_dict[province_id].has_key(item.station_id):
                        connection_dict[province_id][item.station_id] = 1
                    else:
                        connection_dict[province_id][item.station_id] += 1
                    
                   

        i = 1
        total = 0 
        for key, value in connection_dict.iteritems():
            if key != "total":
                total += len(value)
                aaData.append([str(i), provice_dict.get(key), len(value)])
                i += 1
                
        aaData.insert(0, ["", "Tổng số trạm", total])
        data = aaData[iDisplayStart:iDisplayStart+iDisplayLength]
        return dict(iTotalRecords=i-1, iTotalDisplayRecords=i-1, aaData=data, success=True)
    except Exception as ex:
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], message=str(ex), success=False)

################################################
def export_station_off_log_by_province():
    import os.path, openpyxl
    s_search = request.vars.sSearch
    a = request.vars
    station_type = request.vars.type
    sometext = request.vars.sometext
    datepicker_start = request.vars.datepicker_start
    datepicker_end = request.vars.datepicker_end
    province_id = request.vars.province_id
    area_id = request.vars.area_id
    station_id = request.vars.station_id
    connection_loss = request.vars.connection_loss
    aaData = []
    
    # Search conditions
    conditions = (db.station_off_log.id > 0)
    # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
    if sometext:
        conditions &= (db.station_off_log.station_name.contains(sometext))
    if datepicker_start:
        conditions &= (db.station_off_log.start_off >= date_util.string_to_datetime(datepicker_start))
    if datepicker_end:
        conditions &= (db.station_off_log.end_off <= date_util.string_to_datetime(datepicker_end))
    if station_type:
        conditions &= (db.station_off_log.station_type == station_type)
    if province_id:
        conditions &= (db.station_off_log.province_id == province_id)
    if area_id:
        station_ids = db(db.stations.area_id == area_id).select(db.stations.id)
        station_ids = [item.id for item in station_ids]
        conditions &= (db.station_off_log.station_id.belongs(station_ids))
    if station_id:
        conditions &= (db.station_off_log.station_id == station_id)
    # hungdx phan quyen quan ly trạm theo user issue 44
    if current_user:
        if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
            list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                select(db.manager_stations.station_id)
            station_ids = [str(item.station_id) for item in list_station_manager]
            conditions &= (db.station_off_log.station_id.belongs(station_ids))

    list_data = db(conditions).select(  db.station_off_log.id, 
                                        db.station_off_log.station_id,
                                        db.station_off_log.station_name,
                                        db.station_off_log.station_type,
                                        db.station_off_log.province_id,
                                        db.station_off_log.start_off,
                                        db.station_off_log.end_off,
                                        db.station_off_log.duration,
                                        orderby = ~db.station_off_log.start_off)

    if list_data.first() is None:
        raise HTTP(400, "Không đủ dữ liệu xuất excel, vui lòng thử lại!")
    else:
        # Write header
        temp_headers = ['No.','Tỉnh/TP']
        if connection_loss == '3':
            temp_headers.append("Số lượng trạm bị gián đoạn truyền dữ liệu ≥3h")
        elif connection_loss == '12':
            temp_headers.append("Số lượng trạm bị gián đoạn truyền dữ liệu ≥12h")
        elif connection_loss == '24':
            temp_headers.append("Số lượng trạm bị gián đoạn truyền dữ liệu ≥24h")
        elif connection_loss == '48':
            temp_headers.append("Số lượng trạm bị gián đoạn truyền dữ liệu ≥48h")
        else:
            temp_headers.append("Số lượng trạm bị gián đoạn truyền dữ liệu ≥12h")
            
    # Thu tu ban ghi
    station_type = dict(db.commands.station_type.requires.options())
    areas = common.get_area_by_station_dict()
    provice_dict = common.get_province_dict()
    connection_dict = {}

    
    # Duyet tung phan tu trong mang du lieu vua truy van duoc
    for item in list_data:
        
        start_off = roundTime(item.start_off)
        end_off = roundTime(item.end_off)
        province_id = item.province_id
        if end_off and start_off:
            duration = (end_off - start_off).total_seconds()
        else:
            duration = 0
            
        if connection_loss:
            if duration >= int(connection_loss) * 3600:
                if not connection_dict.has_key(province_id):
                    connection_dict[province_id] = {
                        "{}".format(item.station_id): 1
                    }
                else:
                    if not connection_dict[province_id].has_key(item.station_id):
                        connection_dict[province_id][item.station_id] = 1
                    else:
                        connection_dict[province_id][item.station_id] += 1
                    
        else:
            if not connection_dict.has_key(province_id):
                connection_dict[province_id] = {
                    "{}".format(item.station_id): 1
                }
            else:
                if not connection_dict[province_id].has_key(item.station_id):
                    connection_dict[province_id][item.station_id] = 1
                else:
                    connection_dict[province_id][item.station_id] += 1


    i = 1
    total = 0 
    for key, value in connection_dict.iteritems():
        if key != "total":
            total += len(value)
            aaData.append([str(i), provice_dict.get(key), len(value)])
            i += 1

    aaData.insert(0, ["", "Tổng số trạm", total])
    
    wb2 = openpyxl.Workbook(write_only=True)
    file_name = request.now.strftime('Danh sách trạm mất kết nối theo tỉnh_%Y%m%d_%H%M%S.xlsx')
    file_path = os.path.join(request.folder, 'static', 'export', file_name)
    # wb.save(file_path)
    ws2 = wb2.create_sheet()
    ws2.column_dimensions['A'].width = 6
    ws2.column_dimensions['B'].width = 60
    ws2.column_dimensions['C'].width = 60
    ws2.append(temp_headers)
    for row in aaData:
        ws2.append(row)
    wb2.save(file_path)

    data = open(file_path, "rb").read()
    os.unlink(file_path)
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

    return data

#################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'alarm_log')))
def get_list_station_off_log(*args, **kwargs):
        dataItem = []
        s_search = request.vars.sSearch
        a = request.vars
        station_type = request.vars.type
        sometext = request.vars.sometext
        datepicker_start = request.vars.datepicker_start
        datepicker_end = request.vars.datepicker_end
        province_id = request.vars.province_id
        area_id = request.vars.area_id

        station_id = request.vars.station_id
        careers = request.vars.careers
        aaData = []
        connection_loss = request.vars.connection_loss
        iDisplayStart = int(request.vars.iDisplayStart)
        iDisplayLength = int(request.vars.iDisplayLength)
        limitby = (iDisplayStart, iDisplayLength + 1)  # Tuple dung de phan trang (vtri bat dau - chieu dai)
        # Search conditions
        conditions = (db.station_off_log.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if sometext:
            conditions &= (db.station_off_log.station_name.contains(sometext))
        if datepicker_start:
            conditions &= (db.station_off_log.start_off >= date_util.string_to_datetime(datepicker_start))
        if datepicker_end:
            conditions &= (db.station_off_log.end_off <= date_util.string_to_datetime(datepicker_end))
        if station_type:
            conditions &= (db.station_off_log.station_type == station_type)
        if province_id:
            conditions &= (db.station_off_log.province_id == province_id)
        if area_id:
            station_ids = db(db.stations.area_ids.belongs([area_id])).select(db.stations.id)
            station_ids = [item.id for item in station_ids]
            conditions &= (db.station_off_log.station_id.belongs(station_ids))
        if station_id:
            conditions &= (db.station_off_log.station_id == station_id)

        if careers:
            career = careers.split(",")
            station_ids = db(db.stations.career.belongs(career)).select(db.stations.id)
            station_ids = [item.id for item in station_ids]
            conditions &= (db.station_off_log.station_id.belongs(station_ids))
        # hungdx phan quyen quan ly trạm theo user issue 44
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id). \
                    select(db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db.station_off_log.station_id.belongs(station_ids))

        list_data = db(conditions).select(  db.station_off_log.id, 
                                            db.station_off_log.station_id,
                                            db.station_off_log.station_name,
                                            db.station_off_log.station_type,
                                            db.station_off_log.province_id,
                                            db.station_off_log.start_off,
                                            db.station_off_log.end_off,
                                            db.station_off_log.duration,
                                            orderby = ~db.station_off_log.start_off)

        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count(db.station_off_log.id)
        # Thu tu ban ghi
        iRow = iDisplayStart + 1
        station_type = dict(db.commands.station_type.requires.options())
        areas = common.get_area_by_station_id_dict()
        stations = common.get_station_dict()

        station_area = stations[4]

        provice_dict = common.get_province_dict()

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        data = dict()
        for item in list_data:

            area_string = []
            if station_area.get(item.station_id):
                for area_id in station_area.get(item.station_id):
                    area_idss = str(area_id).encode("utf-8")
                    area_string.append(areas.get(area_idss))

            start_off = roundTime(item.start_off)
            end_off = roundTime(item.end_off)
            if end_off and start_off:
                duration = (end_off - start_off).total_seconds()
            else:
                duration = 0
            station_type_map = []
            if str(item.station_type) in station_type:
                station_type_map = station_type[str(item.station_type)]
            if connection_loss:
                if duration >= float(connection_loss) * 3600:
                    aaData.append([
                        str(iRow),
                        item.station_name,
                        station_type_map,
                        provice_dict.get(item.province_id),
                        ",".join(area_string),
                        start_off,
                        end_off,
                        common.format_passed_time(duration),
                    ])
                    iRow += 1
            else:
                aaData.append([
                    str(iRow),
                    item.station_name,
                    station_type_map,
                    provice_dict.get(item.province_id),
                    ",".join(area_string),
                    start_off,
                    end_off,
                    common.format_passed_time(duration),
                ])
                iRow += 1
            
            dataItem = aaData[iDisplayStart:iDisplayLength+iDisplayStart]
        return dict(iTotalRecords=len(aaData), iTotalDisplayRecords=len(aaData), aaData=dataItem, success=True)

#################################################

def export_excel():
    import os.path, openpyxl
    # get search parameters
    province_id = request.vars.province_id
    datepicker_start = request.vars.datepicker_start
    datepicker_end = request.vars.datepicker_end
    area_id = request.vars.area_id
    station_type = request.vars.type
    station_id = request.vars.station_id
    sometext = request.vars.sometext
    connection_loss = request.vars.connection_loss

    conditions = (db.station_off_log.id > 0)
    if sometext:
        conditions &= (db.station_off_log.station_name.contains(sometext))
    if datepicker_start:
        conditions &= (db.station_off_log.start_off >= date_util.string_to_datetime(datepicker_start))
    if datepicker_end:
        conditions &= (db.station_off_log.end_off <= date_util.string_to_datetime(datepicker_end))
    if station_type:
        conditions &= (db.station_off_log.station_type == station_type)
    if province_id:
        conditions &= (db.station_off_log.province_id == province_id)
    if area_id:
        station_ids = db(db.stations.area_id == area_id).select(db.stations.id)
        station_ids = [item.id for item in station_ids]
        conditions &= (db.station_off_log.station_id.belongs(station_ids))
    if station_id:
        conditions &= (db.station_off_log.station_id == station_id)
    aaData = []
    table = 'station_off_log'
    list_data = db(conditions).select()


    if list_data.first() is None:
        raise HTTP(400, "Không đủ dữ liệu xuất excel, vui lòng thử lại!")
    else:
        # Write header
        temp_headers = ['No.','Tên trạm','Thành phần môi trường','Tỉnh','Nhóm','Thời gian bắt đầu','Thời gian kết thúc','Thời gian'
                  ]
        headers = []
    provice_dict = common.get_province_dict()
    ## Get station's area info
    areas = common.get_area_by_station_id_dict()
    stations = common.get_station_dict()
    station_area = stations[4]
    station_type = dict()
    start_off = dict()
    # for key, item in const.STATION_TYPE.iteritems():
    for item in common.get_station_types():
        station_type[str(item['value'])] = item['name']
    iRow = 1
    for i, item in enumerate(list_data):
        start_off = roundTime(item.start_off)
        end_off = roundTime(item.end_off)

        area_string = []
        if station_area.get(item.station_id):
            for area_id in station_area.get(item.station_id):
                area_idss = str(area_id).encode("utf-8")
                area_string.append(areas.get(area_idss))

        if end_off and start_off:
            duration = (end_off - start_off).total_seconds()
        else:
            duration = None
        if connection_loss:
            if duration >= float(connection_loss) * 3600:
                aaData.append([
                    str(iRow),
                    item.station_name,
                    station_type[str(item.station_type)],
                    provice_dict.get(item.province_id),
                    ",".join(area_string),
                    start_off,
                    end_off,
                    common.format_passed_time(duration),
                ])
                iRow += 1
        else:
            aaData.append([
                str(iRow),
                item.station_name,
                station_type[str(item.station_type)],
                provice_dict.get(item.province_id),
                ",".join(area_string),
                start_off,
                end_off,
                common.format_passed_time(duration),
            ])
            iRow += 1
            
    wb2 = openpyxl.Workbook(write_only=True)
    ws2 = wb2.create_sheet()
    ws2.column_dimensions['A'].width = 6
    ws2.column_dimensions['B'].width = 60
    ws2.column_dimensions['C'].width = 22
    ws2.column_dimensions['D'].width = 15
    ws2.column_dimensions['F'].width = 20
    ws2.column_dimensions['G'].width = 20
    ws2.append(temp_headers)
    for row in aaData:
        ws2.append(row)
    file_name = request.now.strftime('Danh sách trạm mất kết nối_%Y%m%d_%H%M%S.xlsx')
    file_path = os.path.join(request.folder, 'static', 'export', file_name)
    # wb.save(file_path)
    wb2.save(file_path)

    data = open(file_path, "rb").read()
    os.unlink(file_path)
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % file_name

    return data

@service.json
@auth.requires(lambda: (auth.has_permission('view', 'view_report')))
def get_provinces_and_staion_type(*args, **kwargs):
    try:
        html1 = "<option value='' selected>%s</option>" % T('-- Select an option --')
        html2 = "<option value='' selected>%s</option>" % T('-- Select an option --')
        area = request.vars.area_id
        conditions = db.stations.id > 0
        if current_user:
            if not (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)):
                list_station_manager = db(db.manager_stations.user_id == current_user.id).select(
                    db.manager_stations.station_id)
                station_ids = [str(item.station_id) for item in list_station_manager]
                conditions &= (db[table]['id'].belongs(station_ids))
        if area:
            conditions &= db.stations.area_id == area
        stations = db(conditions).select(db.stations.id,
                                         db.stations.station_name,
                                         db.stations.province_id)
        province_ids = [station.province_id for station in stations]

        provinces = db(db.provinces.id.belongs(province_ids)).select()

        for row in provinces:
            html1 += '<option value="%(value)s">%(name)s</option>' % dict(value=row.id, name=row.province_name)

        for item in stations:
            html2 += '<option value="%(value)s">%(name)s</option>' % dict(value=item.id, name=item.station_name)
        return dict(success=True, html1=html1, html2=html2)
    except Exception as ex:
        return dict(success=False, message=str(ex))
