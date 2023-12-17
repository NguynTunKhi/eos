# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################
@auth.requires(lambda: (auth.has_permission('create', 'admin_func') or auth.has_permission('edit', 'admin_func')))
def form():
    # If in Update mode, get equivallent record
    record = db.func(request.args(0)) or None
    msg = ''
    
    frm = SQLFORM(db.func, record, _method = 'POST', hideerror = True, showid = False, _id = 'frmMain')
    
    if frm.process(onvalidation = validate, detect_record_change = True, hideerror = True).accepted:
        session.flash = T('MSG_INFO_SAVE_SUCCESS')
        redirect(URL('index'))
    elif frm.record_changed:
        redirect(URL('home', 'error'))
    elif frm.errors:
        for item in frm.errors:
            msg += '%s: %s<br />' %(T('func_' + item), frm.errors[item])
    else:
        pass
        #response.flash = message.REQUEST_INPUT

    frm.custom.widget.func_code['_maxlength'] = '64'
    frm.custom.widget.parent_code['_maxlength'] = '64'
    frm.custom.widget.func_name['_maxlength'] = '128'

    return dict(frm = frm, msg = XML(msg))

################################################################################
def validate(frm):
    #Check condion
    #Get control value by : frm.vars.ControlName
    #If validate fail : frm.errors.ControlName = some message
    pass

def call():
    return service()

################################################################################
@auth.requires(lambda: (auth.has_permission('view', 'admin_func')))
def index():
    return locals()

################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'admin_func')))
def get_list_records(*args, **kwargs):
    try:
        iDisplayStart = int(request.vars.iDisplayStart) # Vi tri bat dau lay du lieu
        iDisplayLength = int(request.vars.iDisplayLength) # So luong ban ghi se lay toi da
        s_search = request.vars.sSearch # Chuoi tim kiem nhap tu form
        aaData = [] # Du lieu json se tra ve
        limitby = (iDisplayStart, iDisplayLength + 1) # Tuple dung de phan trang (vtri bat dau - chieu dai)
    
        conditions = (db.func.id > 0)
        # Neu chuoi tim kiem khac rong thi them dieu kien truy van voi chuoi tim kiem
        if s_search:
            conditions &= ((db.func.func_code.contains(s_search)) | (db.func.func_name.contains(s_search)))
        list_data = db(conditions).select(  db.func.id,
                                            db.func.func_code,
                                            db.func.func_name,
                                            db.func.parent_code,
                                            orderby = db.func.parent_code | db.func.func_code,
                                            limitby = limitby)
        # Tong so ban ghi khong thuc hien phan trang
        iTotalRecords = db(conditions).count(db.func.id)
        # Thu tu ban ghi
        iRow = iDisplayStart + 1

        # Duyet tung phan tu trong mang du lieu vua truy van duoc
        for item in list_data:
            row = [
                str(iRow), 
                A(item.func_code, _href = URL('form', args = [item.id])),
                item.func_name,
                item.parent_code,
                INPUT(_group = '0', _class = 'select_item', _type = 'checkbox', _value = item.id),
            ]

            aaData.append(row)
            iRow += 1

        return dict(iTotalRecords = iTotalRecords, iTotalDisplayRecords = iTotalRecords, aaData = aaData, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)