# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

from w2pex import const

###############################################################################
@auth.requires(auth.requires_membership('admin') | auth.requires_membership(const.GROUP_MANAGER))
def role_list():
    return dict()
    
###############################################################################
@service.json    
def get_list_role(*args, **kwargs):
    try:
        display_start = int(request.vars.iDisplayStart)
        display_length = int(request.vars.iDisplayLength)
        s_search = request.vars.sSearch
        array_object = []
        list_data = None
        total_records = 0
        limitby = (display_start, display_start + display_length + 1)
        query_search = (db.role.id > 0)
        # If there are search conditions
        if s_search:
            query_search &= ((db.role.name.contains(s_search)) |
                             (db.role.description.contains(s_search)))
        
        list_data = db(query_search).select(db.role.id,
                                            db.role.name,
                                            db.role.description,
                                            limitby = limitby)
        
        
        total_records = db(query_search).count(db.role.id)
        iRow = 1
        for item in list_data:
            listA = [
                     str(iRow),
                     A(item.name, _href = URL('role_form', args=[item.id])),
                     item.description,
                     # A(I(_class='fa fa-pencil'), _title = 'Grand function permission', _href = URL('permission_form', args=[item.id])),
                     # + ' | ' + A(I(_class='fa fa-file-text'), _title = 'Grand menu permission', _href = URL('menu_permission_form', args=[item.id])),
                     XML(INPUT(_class = 'select_item', _type = 'checkbox', _group = '0', _value = item.id)),
                     item.id
                     ]
            array_object.append(listA)
            iRow += 1
        
        return dict(iTotalRecords = total_records, iTotalDisplayRecords = total_records, aaData = array_object, success = True)
    except Exception, ex:
        logger.error(str(ex))
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@decor.requires_permission('Administration|role|role_form')
def role_form():
    id = request.args(0)
    record = db.role(db.role.id == id) or None
    update_mode = False
    
    if record:
        update_mode = True
    else:
        id = 0
    
    form = SQLFORM(db.role, record, _id = 'form_role')
    str_errors = ''
    
    form.validate(hideerror = True, detect_record_change = True)
    if form.accepted:
        if not record:
            rec = db.role.insert(**dict(form.vars))
        else:
            rec = record.update_record(**dict(form.vars))
    
        redirect(URL('role_form', args = [rec.id]))
    # if form.process(hideerror = True, detect_record_change = True).accepted:
        # # redirect(URL('role_list'))
    elif form.record_changed:
        redirect(URL('home', 'error'))
    elif form.errors:
        for item in form.errors:
            if (item == 'name'):
                str_errors += 'Name : ' + form.errors.get(item) + '<br />'
            elif (item == 'description'):
                str_errors += 'Description : ' + form.errors.get(item) + '<br />'
    else:
        pass
    
    form.custom.widget.description['_rows'] = '1'
    form.custom.widget.description['_class'] = 'form-control noresize;'
    
    return dict(form = form, id = id, errors_response = XML(str_errors))

################################################################################
@service.json
def get_list_usr_belongs_role(*args, **kwargs):
    try:
        role_id = request.vars.role_id
        display_start = int(request.vars.iDisplayStart)
        display_length = int(request.vars.iDisplayLength)
        s_search = request.vars.sSearch
        array_object = []
        list_data = None
        total_records = 0
        limitby = (display_start, display_start + display_length + 1)
        
        memberships = db(db.membership.role_id == role_id).select(db.membership.user_id)
        membership_arr = []
        for membership in memberships:
            membership_arr.append(membership.user_id)
            
        conditions = (db.usr.id.belongs(membership_arr))
                      
        # conditions = ((db.usr.id > 0) &
                      # (db.usr.id == db.membership.user_id) &
                      # (db.membership.role_id == role_id))
        
            
        if s_search:
            conditions &= ((db.usr.username.contains(s_search)) |
                           (db.usr.fullname.contains(s_search)) |
                           (db.usr.email.contains(s_search))) 
        
        list_data = db(conditions).select(db.usr.id,
                                          db.usr.fullname,
                                          db.usr.username,
                                          orderby = 'usr.id ASC', 
                                          limitby = limitby)
        
        total_records = db(conditions).count(db.usr.id)
        iRow = 1
        for item in list_data:
            listA = [
                 INPUT(_name = 'select_item',
                           _type = 'checkbox',
                           _class = 'select_item_0',
                           _value = item.id),
                 item.username,
                 item.fullname
             ]
            array_object.append(listA)
            iRow += 1
        return dict(iTotalRecords = total_records, iTotalDisplayRecords = total_records, aaData = array_object, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@service.json
def get_list_usr_not_belongs_role(*args, **kwargs):
    try:
        role_id = request.vars.role_id
        s_echo = request.vars.sEcho
        display_start = int(request.vars.iDisplayStart)
        display_length = int(request.vars.iDisplayLength)
        s_search = request.vars.sSearch
        array_object = []
        list_data = None
        total_records = 0
        limitby = (display_start, display_start + display_length + 1)
        
        memberships = db(db.membership.role_id == role_id).select(db.membership.user_id)
        membership_arr = []
        for membership in memberships:
            membership_arr.append(membership.user_id)
            
        conditions = (db.usr.id.belongs(membership_arr))
        
        users_has_role = db(conditions).select(db.usr.id)
        users = [user.id for user in users_has_role]
        
        conditions = ((db.usr.id > 0) &
                      (~db.usr.id.belongs(users)))
        
        if s_search:
            conditions &= ((db.usr.username.contains(s_search)) |
                           (db.usr.fullname.contains(s_search)) |
                           (db.usr.email.contains(s_search)))
        
        list_data = db(conditions).select(db.usr.id,
                                          db.usr.fullname,
                                          db.usr.username,
                                          orderby = 'usr.id ASC', 
                                          limitby = limitby)
        
        total_records = db(conditions).count(db.usr.id)
        iRow = 1
        for item in list_data:
            listA = [
                 INPUT(_name = 'select_item',
                       _type = 'checkbox',
                       _class = 'select_item_1',
                       _value = item.id),
                 item.username,
                 item.fullname
                 ]
            array_object.append(listA)
            iRow += 1
        return dict(iTotalRecords = total_records, iTotalDisplayRecords = total_records, aaData = array_object, success = True)
    except Exception, ex:
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)

################################################################################
@service.json
def del_membership(*args, **kwargs):
    import json
    try:
        array_data = request.vars.arrayData
        list_ids = array_data.split(',')
        length_list = len(list_ids)
        
        if (length_list == 0):
            return dict(success = True)
        role_id = int(list_ids[0])
        i = 1
        while (i < length_list):
            db((db.membership.role_id == role_id) &
               (db.membership.user_id == list_ids[i])
               ).delete() # X�a v?t l�
            i += 1
        
        return dict(success = True)
    except Exception as ex:
        return dict(success = False, message = str(ex))

################################################################################
@service.json
def insert_membership(*args, **kwargs):
    import json
    try:
        array_data = request.vars.arrayData
        list_ids = array_data.split(',')
        length_list = len(list_ids)
        
        if (length_list == 0):
            return dict(success = True)
        role_id = int(list_ids[0])
        i = 1
        while (i < length_list):
            db.membership.insert(role_id = role_id, user_id = list_ids[i])
            i += 1
        
        return dict(success = True)
    except Exception as ex:
        return dict(success = False, message = str(ex))

################################################################################
@service.json 
def del_role(*args, **kwargs):
    try:
        array_data = request.vars.ids
        list_ids = array_data.split(',')
        db(db.role.id.belongs(list_ids)).delete()
        return dict(success = True)
    except Exception as ex:
        return dict(success = False, message = str(ex))

################################################################################
def addUser(ids, role_id):
    if not ids:
        session.flash = 'message.USER_SELECTION_ADD'
    else:
        for id in ids:
            db.membership.insert(user_id = id, role_id = role_id)
        pass
    
    return ''

################################################################################
def removeUser(ids, role_id):
    if not ids:
        session.flash = 'message.USER_SELECTION_DELETE'
    else:
        for id in ids:
            db((db.membership.user_id == id) & (db.membership.role_id == role_id)).delete()
        pass
    
    return ''

################################################################################
def call():
    return service()

################################################################################
@service.json
def func_json(*args, **kwargs):
    nodes = []
    func_ids_existed = []
    
    #get all records of the permission table that has id = id of current role record
    func_records_existed = db(db.permission.role_id == request.vars['role_id']) \
                             .select(db.permission.func_id)
    
    for row in func_records_existed:
        func_ids_existed.append(row.func_id)
    
    #get all records of func table
    func_records = db(db.func.id > 0).select(orderby = db.func.id)

    for record in func_records:
        node = {'id': str(record.id),
                'parent': str(record.parent_id) if record.parent_id else '#',
                'text': record.name,
                'state' : { 'opened': True,
                            'selected': True if record.id in func_ids_existed else False }
               }
        nodes.append(node)

    return nodes

################################################################################
@decor.requires_permission('Administration|role|permission_form')
def permission_form():
    role_id = request.args(0)
    role_record = db.role(role_id)
    role_form = SQLFORM(db.role, role_record)
    
    return dict(role_form = role_form, role_id = role_id)

################################################################################
def update_permission():
    # List of function ids existed in the permission table
    func_ids_existed = []
    # List of function ids were selected
    func_ids_selected = request.vars['selected_nodes']
    # Id of current role record
    role_id = request.vars['role_id']
    
    # Get all function ids of the permission table that has id = id of current role record
    func_records_existed = db(db.permission.role_id == role_id).select(db.permission.func_id)
    for row in func_records_existed:
        func_ids_existed.append(str(row.func_id))
    
    # List of function ids selected has length > 0
    if func_ids_selected:
        func_ids_selected = func_ids_selected.split(',')
        # If in the permission table has no any record that satisfies role_id = current role id,
        # insert every function ids selected to the permission table
        if len(func_ids_existed) == 0:
            for func_id in func_ids_selected:
                db.permission.insert(role_id = role_id, func_id = func_id)
        else:
            # Insert new function ids selected
            for func_id in func_ids_selected:
                if func_id not in func_ids_existed:
                    db.permission.insert(role_id = role_id, func_id = func_id)

            # Delete function ids not selected but existed in the permission table
            for func_id in func_ids_existed:
                if func_id not in func_ids_selected:
                    db((db.permission.func_id == func_id) & (db.permission.role_id == role_id)).delete()
    # If list of function ids selected has length = 0, 
    # delete every function ids existed in the permission table
    else:
        if len(func_ids_existed) > 0:
            for func_id in func_ids_existed:
                db((db.permission.func_id == func_id) & (db.permission.role_id == role_id)).delete()
        else:
            pass

    redirect(URL('role', 'role_list'))

################################################################################
def get_func_code():
    func_id = request.vars['func_id']
    func_record = db(db.func.id == func_id).select(db.func.code).first()
    return "alert('" + func_record.code + "');"

################################################################################
@service.json
def menu_func_json(*args, **kwargs):
    nodes = []
    menu_func_ids_existed = []
    
    #get all records of the menu_permission table that has id = id of current role record
    menu_func_records_existed = db(db.menu_permission.role_id == request.vars['role_id']) \
                                  .select(db.menu_permission.menu_func_id)
    
    for row in menu_func_records_existed:
        menu_func_ids_existed.append(row.menu_func_id)
    
    #get all records of menu_func table
    menu_func_records = db(db.menu_func.id > 0) \
                            .select(orderby = db.menu_func.id)

    for record in menu_func_records:
        node = {'id': str(record.id),
                'parent': str(record.parent_id) if record.parent_id else '#',
                'text': record.name,
                'state' : { 'opened': True,
                            'selected': True if record.id in menu_func_ids_existed else False }
               }
        nodes.append(node)

    return nodes

################################################################################
@decor.requires_permission('Administration|role|menu_permission_form')
def menu_permission_form():
    role_id = request.args(0)
    role_record = db.role(role_id)
    role_form = SQLFORM(db.role, role_record)
    
    return dict(role_form = role_form, role_id = role_id)

################################################################################
def update_menu_permission():
    func_ids_existed = [] # List of function ids existed in the menu_permission table
    func_ids_selected = request.vars['selected_nodes'] # List of function ids were selected
    role_id = request.vars['role_id'] # Id of current role record
    
    # Get all function ids of the menu_permission table that has id = id of current role record
    func_records_existed = db(db.menu_permission.role_id == role_id) \
                             .select(db.menu_permission.menu_func_id)
    for row in func_records_existed:
        func_ids_existed.append(str(row.menu_func_id))
    
    # List of function ids selected has length > 0
    if func_ids_selected:
        func_ids_selected = func_ids_selected.split(',')
        # If in the menu_permission table has no any record that satisfies role_id = current role id,
        # insert every function ids selected to the menu_permission table
        if len(func_ids_existed) == 0:
            for menu_func_id in func_ids_selected:
                db.menu_permission.insert(role_id = role_id, menu_func_id = menu_func_id)
        else:
            # Insert new function ids selected
            for menu_func_id in func_ids_selected:
                if menu_func_id not in func_ids_existed:
                    db.menu_permission.insert(role_id = role_id, menu_func_id = menu_func_id)

            # Delete function ids not selected but existed in the menu_permission table
            for menu_func_id in func_ids_existed:
                if menu_func_id not in func_ids_selected:
                    db((db.menu_permission.menu_func_id == menu_func_id) & (db.menu_permission.role_id == role_id)).delete()
    # If list of function ids selected has length = 0, 
    # delete every function ids existed in the menu_permission table
    else:
        if len(func_ids_existed) > 0:
            for menu_func_id in func_ids_existed:
                db((db.menu_permission.menu_func_id == menu_func_id) & (db.menu_permission.role_id == role_id)).delete()
        else:
            pass

    redirect(URL('role', 'role_list'))

################################################################################
def get_menu_func_code():
    menu_func_id = request.vars['menu_func_id']
    menu_func_record = db(db.menu_func.id == menu_func_id).select(db.menu_func.code).first()
    return "alert('" + menu_func_record.code + "');"
