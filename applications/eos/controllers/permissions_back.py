# -*- coding: utf-8 -*-
###############################################################################
# Author : 
# Date   : 
# 
# Description : 
# 
###############################################################################

import sys, pkgutil, os.path

#------------------------------------------------------------------------------
@auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
def index():
    group_id = request.vars.group_id
    group = db.auth_group(group_id)
    
    return dict(group = group)
    
#------------------------------------------------------------------------------
@service.json
@auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
def get_list_permissions(*args, **kwargs):
    try:
        aaData = []
        s_search = request.vars.sSearch
        group_id = request.vars.group_id
            
        ### Search conditions
        conditions = (db.auth_permission.group_id == group_id)
        allowed_permissions = {}

        ### Get all functions
        rows = db(db.func.id > 0).select(db.func.func_code, db.func.func_name, orderby = db.func.parent_code | db.func.func_code)
        funcs = []
        func_names = {}
        for row in rows:
            funcs.append(row.func_code)
            func_names[row.func_code] = row.func_name
        #  Chi lay nhung controller ma user hien tai co quyen
        if not auth.has_membership('admin'):
            conditions1 = (db.auth_group.manager == current_user.user_id)
            conditions1 &= (db.auth_group.created_by != current_user.user_id)
            rows1 = db(conditions1).select(db.auth_group.id)
            groups_id2 = [grp.id for grp in rows1]
            conditions2 = (db.auth_permission.group_id.belongs(groups_id2))
            rows2 = db(conditions2).select(db.auth_permission.table_name, db.auth_permission.name, distinct = True)
            funcs = []
            for row in rows2:
                if row.table_name not in funcs:
                    funcs.append(row.table_name)
                    pass
                if not allowed_permissions.has_key(row.table_name):
                    allowed_permissions[row.table_name] = []
                    pass
                allowed_permissions[row.table_name].append(row.name)
            pass
        
        # If there are search conditions
        if s_search:
            funcs = [c for c in funcs if s_search in c]
        conditions &= (db.auth_permission.table_name.belongs(funcs))
        
        list_data = db(conditions).select(  db.auth_permission.id,
                                            db.auth_permission.name,
                                            db.auth_permission.table_name,
                                            orderby = db.auth_permission.table_name)
        total_records = len(funcs)
        
        # Init return data with no permission
        aaData_dict = {}
        system_action = common.sort_dict_const_by_value(const.SYSTEM_ACTIONS)
        temp_row = {}
        sorted_actions = []
        for action in system_action:
            temp_row[action[1]['value']] = False
            sorted_actions.append(action[1]['value'])
        for item in funcs:
            if item not in aaData_dict:
                aaData_dict[item] = temp_row.copy()
        
        # Get current permissions of group
        for i, item in enumerate(list_data):
            if aaData_dict.has_key(item.table_name):
                if aaData_dict[item.table_name].has_key(item.name):
                    aaData_dict[item.table_name][item.name] = True
            
        idx = 0
        for item in aaData_dict:
            row = [
                str(idx + 1),
                T(func_names[item]) if func_names.has_key(item) else T(item),
            ]
            # Append permissions
            i = 0
            for permission in sorted_actions:
                if not aaData_dict[item].has_key(permission): continue
                i += 1
                if aaData_dict[item][permission]:
                    if auth.check_has_permission_for_manager(allowed_permissions, item, permission):
                        row.append(INPUT(_name = item, _type = 'checkbox', _column=i, _row=idx, _class = 'column_item row_item', _value = permission, _checked = 'true'))
                    else:
                        row.append('')
                else:
                    if auth.check_has_permission_for_manager(allowed_permissions, item, permission):
                        row.append(INPUT(_name = item, _type = 'checkbox', _column=i, _row=idx, _class = 'column_item row_item', _value = permission))
                    else:
                        row.append('')
            i += 1
            row.append(INPUT(_name = 'select_item_6', _type = 'checkbox', _column=i, _row=idx, _class = 'column_item row_all', _value = 'All'))
            idx += 1
            aaData.append(row)
        # return dict(iTotalRecords = total_records, iTotalDisplayRecords = total_records, aaData = aaData, success = True)
        return dict(iTotalRecords=0, iTotalDisplayRecords=0, aaData=[], success=True)
    except Exception, ex:
        logger.error(str(ex))
        return dict(iTotalRecords = 0, iTotalDisplayRecords = 0, aaData = [], message = str(ex), success = False)
        
#------------------------------------------------------------------------------
@service.json
@auth.requires(lambda: (auth.has_membership('admin') or auth.has_membership(const.GROUP_MANAGER)))
def update_permissions(*args, **kwargs):
    try:
        type = request.vars.type
        group_id = request.vars.group_id
        
        if not type or not group_id:
            return dict(success = True, message = T('Permissions updated successful!'))
            
        permissions = request.vars.permissions
        permissions = permissions.split(';')        # Cat quyen theo tung row (controller)
            
        db(db.auth_permission.group_id == group_id).delete()
        
        ### Update new permissions
        for item in permissions:
            item = item.split(',')
            for cur_per in item[1:]:
                if cur_per:
                    db.auth_permission.insert(
                        group_id = group_id,
                        table_name = item[0],
                        name = cur_per
                    )
        return dict(success = True, message = T('Permissions updated successful!'))
    except Exception, ex:
        logger.error(str(ex))
        return dict(message = str(ex), success = False)
        
################################################################################
def call():
    return service()

