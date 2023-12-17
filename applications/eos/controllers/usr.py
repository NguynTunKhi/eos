# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

from w2pex import const

def call():
    return service()

#@decor.requires_permission('Administration|usr|usr_list')
@auth.requires(lambda: (auth.has_permission('view', 'admin_user')))
def usr_list():
    return dict()

################################################################################
@service.json    
@auth.requires(lambda: (auth.has_permission('view', 'admin_user')))
def get_list_usr(*args, **kwargs):
    try:
        s_echo = request.vars.sEcho
        display_start = int(request.vars.iDisplayStart)
        display_length = int(request.vars.iDisplayLength)
        department_id = request.vars.department_id
        s_search = request.vars.sSearch
        array_object = []
        list_data = None
        total_records = 0
        limitby = (display_start, display_start + display_length + 1)
        query_search = (db.usr.id > 0)
        if department_id:
            query_search &= (db.usr.department_id == department_id)
        
        if s_search:
            query_search &= ((db.usr.username.contains(s_search)) |
                             (db.usr.fullname.contains(s_search)) |
                             (db.usr.email.contains(s_search)) |
                             (db.usr.positions.contains(s_search)))
        
        list_data = db(query_search).select(db.usr.id,
                                            db.usr.username,
                                            db.usr.fullname,
                                            db.usr.email,
                                            limitby = limitby)
        
        total_records = db(query_search).count(db.usr.id)
        iRow = 1
        for item in list_data:
            listA = [
                     str(iRow),
                     A(item.username, _href = URL('usr_form/' + str(item.id))),
                     item.fullname,
                     item.email,
                     INPUT(_group = '0', _class = 'select_item', _type = 'checkbox', _value = item.id),
                     item.id
                     ]
            array_object.append(listA)
            iRow += 1
        return dict(iTotalRecords = total_records, iTotalDisplayRecords = total_records, aaData = array_object, success = True)
    except Exception as ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
    finally:
        pass
   
################################################################################
@service.json
@auth.requires(lambda: (auth.has_permission('view', 'admin_user')))
def load_drop_down_list(*args, **kwargs):
    try:
        string_response = ''
        # Ph�ng ban
        #rows_cat = db(db.department.id > 0).select(db.department.id,
        #                       db.department.name)
        #string_response += "$('#ddl-department').find('option').remove();\n"
        #string_response += "$('#ddl-department').append(new Option('', ''));\n"
        #for row in rows_cat:
        #    string_response += "$('#ddl-department').append(new Option('%s', '%s', false, false));\n" %(row.name, row.id)
            
        return dict(success = True, data = string_response)
    except Exception, ex:
        return dict(success = False, message = str(ex))
    finally:
        pass

################################################################################
@service.json 
@auth.requires(lambda: (auth.has_permission('delete', 'admin_user')))
def del_usr(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db.usr.id.belongs(list_ids)).delete()
        return dict(success = True)
    except Exception, ex:
        return dict(success = False, message = str(ex))

################################################################################
#@decor.requires_permission('Administration|usr|usr_form')
@auth.requires(lambda: (auth.has_permission('create', 'admin_user') or auth.has_permission('edit', 'admin_user')))
def usr_form():
    usr_id = request.args(0)
    usr_record = db.usr(usr_id) or None
    
    form = SQLFORM(db.usr, usr_record, upload=URL('download'), _id = 'form_usr')
    
    form.custom.widget.lastname['_placeholder'] = T('LBL_LAST_NAME')
    form.custom.widget.firstname['_placeholder'] = T('LBL_FIRST_NAME')
    form.custom.widget.email['_placeholder'] = T('LBL_EMAIL')
    form.custom.widget.username['_placeholder'] = T('LBL_USER_NAME')
    form.custom.widget.password['_placeholder'] = T('LBL_PASSWORD') 
    form.custom.widget.note['_rows'] = 3
    form.custom.widget.note['_class'] = 'form-control noresize'
    form.custom.widget.employed_date['_class'] = 'col-sm-6 form-control date'
    form.custom.widget.salary_level['_class'] = 'col-sm-6 form-control hide'
    form.custom.widget.salary['_class'] = 'col-sm-6 form-control hide'
    form.custom.widget.insurance['_class'] = 'col-sm-6 form-control hide'
    form.custom.widget.status['_class'] = 'col-sm-6 form-control' 
    # conditions = ((db.role.id > 0) &
                  # (db.membership.role_id == db.role.id) &
                  # (db.membership.user_id == usr_id))
    memberships = db(db.membership.user_id == usr_id).select(db.membership.role_id)
    memberships_arr = []
    for membership in memberships:
        memberships_arr.append(membership.role_id)
    
    roles = db((db.role.id > 0) & (db.role.id.belongs(memberships_arr))).select(db.role.name, db.role.id)
                  
    # roles = db(conditions).select(db.role.name, db.role.id)
    errors_response = ''
    
    if form.process(detect_record_change = True).accepted:
        redirect(URL('usr_list'))
    elif form.record_changed:
        redirect(URL('home', 'error'))
    elif form.errors:
        for item in form.errors:
            errors_response += form.errors.get(item) + '<br />'
        pass
    else:
        #response.flash = message.REQUEST_INPUT
        pass
    
    return dict(form = form, roles = roles, msg = XML(errors_response))

################################################################################
def download():
    return response.download(request, db)
