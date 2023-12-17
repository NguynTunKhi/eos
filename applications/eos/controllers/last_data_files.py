# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
def call():
    return service()

################################################################################
def index():
    return locals()

################################################################################
@service.json
def get_list_last_data_files():
    try:

        iDisplayStart = int(request.vars.iDisplayStart) # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength) # So luong ban ghi se lay toi da
        s_search = request.vars.sSearch # Chuoi tim kiem nhap tu form
        aaData = [] # Du lieu json se tra ve
        list_data = None # Du lieu truy van duoc
        iTotalRecords = 0 # Tong so ban ghi
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
    
        conditions = (db.last_data_files.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if s_search:
            conditions &= ((db.last_data_files.id.contains(s_search)) | (db.last_data_files.filename.contains(s_search)) | (db.last_data_files.station_id.contains(s_search)) | (db.last_data_files.station_name.contains(s_search)))
        list_data = db(conditions).select(  db.last_data_files.id, 
                                            db.last_data_files.filename,
                                            db.last_data_files.lasttime,
                                            db.last_data_files.station_name,
                                            limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count(db.last_data_files.id)
        # Thu tu ban ghi
        iRow = iDisplayStart + 1


        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            listA = [
                    A(str(iRow), _href = URL('form', args = [item.id])),
                    item.filename,
                    item.lasttime.strftime(eos_const.FULL_DATETIME) if item.lasttime else '',
                    item.station_name,
                    #INPUT(_name = 'select_item', _class = 'select_item_0', _type = 'checkbox', _value = item.id),
                    item.id
                ]

            aaData.append(listA)
            iRow += 1

        ''' Du lieu tra ve dang dict:
        iTotalRecords: tong so ban ghi
        iTotalDisplayRecords: tong so cot duoc hien thi
        aaData: du lieu su dung cho data table
        '''
        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
        
