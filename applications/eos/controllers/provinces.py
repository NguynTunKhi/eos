# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

@auth.requires(lambda: (auth.has_permission('view', 'provinces')))
def form():
    # If in Update mode, get equivallent record
    record = db.provinces(request.args(0)) or None
    id = request.args(0) or None
    province_default = request.vars.default
    msg = ''
    default = True
    count_default_province = db(db.provinces.default == True).count()
    default_province = db(db.provinces.id == id).select(db.provinces.default)
    for i in default_province:
        default = i.default
    frm = SQLFORM(db.provinces, record, _method = 'POST', hideerror = True, showid = False, _id = 'frmMain')


    if frm.process(onvalidation = validate, detect_record_change = True, hideerror = True).accepted:
        if province_default == 'on':
            print province_default
            if record:
                db(db.provinces.province_code != record.province_code).update(default=False)
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' %(T('provinces_' + item), frm.errors[item])
    else:
        pass
        #response.flash = message.REQUEST_INPUT

    frm.custom.widget.province_code['_maxlength'] = '8'
    frm.custom.widget.province_name['_maxlength'] = '32'


    return dict(frm = frm, default=default, count_default_province=count_default_province, msg = XML(msg))

################################################################################
def validate(frm):
    #Check condion
    #Get control value by : frm.vars.ControlName
    #If validate fail : frm.errors.ControlName = some message
    pass

def call():
    return service()

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'provinces')))
def index():
    provinces = db(db.provinces.id > 0).select()
    return dict(provinces=provinces, message='')

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'provinces')))
def get_list_provinces(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart) # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength) # So luong ban ghi se lay toi da
        # s_search = request.vars.sSearch # Chuoi tim kiem nhap tu form
        s_search = request.vars.sometext # Chuoi tim kiem nhap tu form
        province_id = request.vars.province_id
        aaData = [] # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)

        conditions = (db.provinces.id > 0)
        if province_id:
            conditions &= (db.provinces.id == province_id)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if s_search:
            conditions &= ((db.provinces.province_code.contains(s_search)) | (db.provinces.province_name.contains(s_search)))
        list_data = db(conditions).select(  db.provinces.id, 
                                            db.provinces.province_code,
                                            db.provinces.province_name,
                                            db.provinces.default,
                                            orderby = db.provinces.order_no,
                                            limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count(db.provinces.id)
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            if item.default:
                text = 'Mặc định'
            else:
                text = ''
            listA = [
                str(iRow), 
                A(item.province_code, _href = URL('form', args = [item.id])),
                item.province_name,
                LABEL(text, _class="default_province", _value=str(item.default)),
                INPUT(_group = '0', _class = 'select_item', _type = 'checkbox', _value = item.id),
            ]

            aaData.append(listA)
            iRow += 1

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
        
################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('delete', 'provinces')))
def del_provinces(table, *args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db[table].id.belongs(list_ids)).delete()
        return dict(success = True)
    except Exception as ex:
        return dict(success = False, message = str(ex))

