# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################


@auth.requires(lambda: (auth.has_permission('view', 'manage_stations_history')))
def index():
    return locals()

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'manage_stations_history')))
def get_list_history(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart) # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength) # So luong ban ghi se lay toi da
        aaData = [] # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.manager_stations_history.id > 0)
        list_data = db(conditions).select(  db.manager_stations_history.id,
                                            db.manager_stations_history.station_id,
                                            db.manager_stations_history.station_name,
                                            db.manager_stations_history.action,
                                            db.manager_stations_history.username,
                                            db.manager_stations_history.description,
                                            db.manager_stations_history.update_time,
                                            orderby=~db.manager_stations_history.update_time,
                                            limitby=limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count(db.manager_stations_history.id)
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            data = db.stations(item.station_id) or None
            if data:
                listA = [
                str(iRow),
                A(data.station_name, _href=URL('stations','form', args=[item.station_id])),
                T(item.action),
                item.username,
                T(item.description),
                item.update_time
                ]
                aaData.append(listA)
            else:
                listA = [
                    str(iRow),
                    item.station_name,
                    T(item.action),
                    item.username,
                    T(item.description),
                    item.update_time
                ]
                aaData.append(listA)
            iRow += 1

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
        
################################################################################
def call():
    return service()